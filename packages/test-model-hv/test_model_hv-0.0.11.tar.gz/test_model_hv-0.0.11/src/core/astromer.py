import tensorflow as tf
import logging
import os, sys

from core.output    import RegLayer
from core.tboard    import save_scalar, draw_graph
from core.losses    import custom_rmse, custom_bce
from core.metrics   import custom_acc
from core.encoder   import Encoder
from core.utils     import load_weights
from tensorflow.keras.layers import Input, Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras import Model
from tqdm import tqdm
import time
import git
import tempfile
import shutil
import json

logging.getLogger('tensorflow').setLevel(logging.ERROR)  # suppress warnings
os.system('clear')

def get_ASTROMER(num_layers=2,
                 d_model=200,
                 num_heads=2,
                 dff=256,
                 base=10000,
                 dropout=0.1,
                 use_leak=False,
                 no_train=True,
                 maxlen=100,
                 batch_size=None,
                 pretrained_weights=False):
    if pretrained_weights:
        #model = load_weights(git_link="https://github.com/HarshVardhanGoyal/test_model.git", model_name="astromer_10022021")
        model_name="astromer_10022021"
        git_link="https://github.com/HarshVardhanGoyal/test_model.git"
        model_path = os.path.join(os.getcwd(),"weights")
    
        try: 
            test_dir = tempfile.mkdtemp()
            git.Repo.clone_from(git_link, test_dir, branch='main', depth=1)
            time.sleep(2)
            if os.path.isdir(model_path):
                if overwrite:
                    shutil.rmtree(model_path)
                else:
                    print("The saved weights already exists")
        except:
            print("Couldn't load the model")
        finally:
            sourcepath = os.path.join(test_dir, model_name)
            sourcefiles = os.listdir(sourcepath)
            destinationpath = os.path.join(model_path, model_name)
            os.makedirs(destinationpath)
            for file in sourcefiles:
                if file.endswith('.index') or file.endswith('.data-00000-of-00001') or file.endswith('.json') or file.endswith("checkpoint"):
                    print(sourcefiles)
                    print(destinationpath)
                    print(file)
                    shutil.move(os.path.join(sourcepath,file), os.path.join(destinationpath,file))

        #shutil.move(os.path.join(test_dir, model_name), model_path)
        # shutil.rmtree(test_dir)

        conf_file = os.path.join( model_path, model_name, 'conf.json')
        with open(conf_file, 'r') as handle:
            conf = json.load(handle)

        model = get_ASTROMER(num_layers=conf['layers'],
                            d_model   =conf['head_dim'],
                            num_heads =conf['heads'],
                            dff       =conf['dff'],
                            base      =conf['base'],
                            dropout   =conf['dropout'],
                            maxlen    =conf['max_obs'],
                            use_leak  =conf['use_leak'])

        # Loading the model
        if os.path.isdir(model_path):
            model = model.load_weights(destinationpath)

    else:
        serie  = Input(shape=(maxlen, 1),
                    batch_size=None,
                    name='input')
        times  = Input(shape=(maxlen, 1),
                    batch_size=None,
                    name='times')
        mask   = Input(shape=(maxlen, 1),
                    batch_size=None,
                    name='mask')
        length = Input(shape=(maxlen,),
                    batch_size=None,
                    dtype=tf.int32,
                    name='length')

        placeholder = {'input':serie,
                    'mask_in':mask,
                    'times':times,
                    'length':length}

        encoder = Encoder(num_layers,
                    d_model,
                    num_heads,
                    dff,
                    base=base,
                    rate=dropout,
                    use_leak=use_leak,
                    name='encoder')

        if no_train:
            encoder.trainable = False

        x = encoder(placeholder)

        x = RegLayer(name='regression')(x)
        model = Model(inputs=placeholder,
                    outputs=x,
                    name="ASTROMER")

    
        
    return model


@tf.function
def train_step(model, batch, opt):
    with tf.GradientTape() as tape:
        x_pred = model(batch)
        
        mse = custom_rmse(y_true=batch['output'],
                         y_pred=x_pred,
                         mask=batch['mask_out'])

       
    grads = tape.gradient(mse, model.trainable_weights)
    opt.apply_gradients(zip(grads, model.trainable_weights))
    return mse

@tf.function
def valid_step(model, batch, return_pred=False, normed=False):
    with tf.GradientTape() as tape:
        x_pred = model(batch)
        # if normed:
        #     mean_x = tf.reshape(batch['mean'][:, 1], [-1, 1, 1])
        #     x_true = batch['output'] + mean_x
        #     x_pred = x_pred + mean_x
        #
        #     mse = custom_rmse(y_true=x_true,
        #                       y_pred=x_pred,
        #                       mask=batch['mask_out'])
        # else:
        x_true = batch['output']
        mse = custom_rmse(y_true=x_true,
                          y_pred=x_pred,
                          mask=batch['mask_out'])

    if return_pred:
        return mse, x_pred, x_true
    return mse

def train(model,
          train_dataset,
          valid_dataset,
          patience=20,
          exp_path='./experiments/test',
          epochs=1,
          finetuning=False,
          use_random=True,
          num_cls=2,
          lr=1e-3,
          verbose=1):

    os.makedirs(exp_path, exist_ok=True)

    # Tensorboard
    train_writter = tf.summary.create_file_writer(
                                    os.path.join(exp_path, 'logs', 'train'))
    valid_writter = tf.summary.create_file_writer(
                                    os.path.join(exp_path, 'logs', 'valid'))

    batch = [t for t in train_dataset.take(1)][0]
    draw_graph(model, batch, train_writter, exp_path)

    # Optimizer
    optimizer = tf.keras.optimizers.Adam(lr,
                                         beta_1=0.9,
                                         beta_2=0.98,
                                         epsilon=1e-9)
    # To save metrics
    train_mse  = tf.keras.metrics.Mean(name='train_mse')
    valid_mse  = tf.keras.metrics.Mean(name='valid_mse')

    # Training Loop
    best_loss = 999999.
    es_count = 0
    pbar = tqdm(range(epochs), desc='epoch')
    for epoch in pbar:
        for train_batch in train_dataset:
            mse = train_step(model, train_batch, optimizer)
            train_mse.update_state(mse)

        for valid_batch in valid_dataset:
            mse = valid_step(model, valid_batch)
            valid_mse.update_state(mse)

        msg = 'EPOCH {} - ES COUNT: {}/{} train mse: {:.4f} - val mse: {:.4f}'.format(epoch,
                                                                                      es_count,
                                                                                      patience,
                                                                                      train_mse.result(),
                                                                                      valid_mse.result())

        pbar.set_description(msg)

        save_scalar(train_writter, train_mse, epoch, name='mse')
        save_scalar(valid_writter, valid_mse, epoch, name='mse')


        if valid_mse.result() < best_loss:
            best_loss = valid_mse.result()
            es_count = 0.
            model.save_weights(exp_path+'/weights')
        else:
            es_count+=1.
        if es_count == patience:
            print('[INFO] Early Stopping Triggered')
            break

        train_mse.reset_states()
        valid_mse.reset_states()

def predict(model,
            dataset,
            conf,
            predic_proba=False):

    total_mse, inputs, reconstructions = [], [], []
    masks, times = [], []
    for step, batch in tqdm(enumerate(dataset), desc='prediction'):
        mse, x_pred, x_true = valid_step(model,
                                         batch,
                                         return_pred=True,
                                         normed=True)

        total_mse.append(mse)
        times.append(batch['times'])
        inputs.append(x_true)
        reconstructions.append(x_pred)
        masks.append(batch['mask_out'])

    res = {'mse':tf.reduce_mean(total_mse).numpy(),
           'x_pred': tf.concat(reconstructions, 0),
           'x_true': tf.concat(inputs, 0),
           'mask': tf.concat(masks, 0),
           'time': tf.concat(times, 0)}

    return res

def __init__(self, pretrained_weights):
    self.pretrained_weights = pretrained_weights
    self.git_link = 'https://github.com/HarshVardhanGoyal/test_model.git'
    self.model_name = 'Test_model.h5'
    self.model_path = os.path.join(os.getcwd(), self.model_name)

def load_model(self, overwrite=False):
    
    # Creating a temporary directory and getting the saved weights
    test_dir = tempfile.mkdtemp()
    git.Repo.clone_from(self.git_link, test_dir, branch='main', depth=1)
    if os.path.exists(self.model_path):
        if overwrite:
            print("The saved weights already exists")
        else:
            os.remove(self.model_path)
    shutil.move(os.path.join(test_dir, self.model_name), os.getcwd())
    # shutil.rmtree(test_dir)

    # Loading the model
    if os.path.exists(self.model_path):
        self.model = keras.models.load_model(self.model_path)
    return self.model