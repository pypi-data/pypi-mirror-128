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

class ASTROMER:
    def __init__(self, num_layers=2,
                 d_model=200,
                 num_heads=2,
                 dff=256,
                 base=10000,
                 dropout=0.1,
                 use_leak=False,
                 no_train=True,
                 maxlen=100,
                 batch_size=None,
                 pretrained_weights=False,
                 finetuning = None,
                 overwrite=False):
        self.num_layers=num_layers
        self.d_model=d_model
        self.num_heads=num_heads
        self.dff=dff
        self.base=base
        self.dropout=dropout
        self.use_leak=use_leak
        self.no_train=no_train
        self.maxlen=maxlen
        self.batch_size=batch_size
        self.pretrained_weights=pretrained_weights
        self.overwrite_weights=overwrite
        self.git_link="https://github.com/HarshVardhanGoyal/test_model.git"
        self.model_path = os.path.join(os.getcwd(),"weights")
        self.model_name = "astromer_10022021"

        # Getting the desired model_name
        if finetuning in [None, "ogle", "alcock"]:
            self.finetuning = finetuning
        else:
            raise ValueError("Specified fine-tuned model does not exist")
        
    # Function to get the model
    def get_ASTROMER(self):
        if self.pretrained_weights:
            self.load_configuration()

        serie  = Input(shape=(self.maxlen, 1),
                    batch_size=None,
                    name='input')
        times  = Input(shape=(self.maxlen, 1),
                    batch_size=None,
                    name='times')
        mask   = Input(shape=(self.maxlen, 1),
                    batch_size=None,
                    name='mask')
        length = Input(shape=(self.maxlen,),
                    batch_size=None,
                    dtype=tf.int32,
                    name='length')

        placeholder = {'input':serie,
                    'mask_in':mask,
                    'times':times,
                    'length':length}

        encoder = Encoder(self.num_layers,
                    self.d_model,
                    self.num_heads,
                    self.dff,
                    base=self.base,
                    rate=self.dropout,
                    use_leak=self.use_leak,
                    name='encoder')

        if self.no_train:
            encoder.trainable = False

        x = encoder(placeholder)

        x = RegLayer(name='regression')(x)
        model = Model(inputs=placeholder,
                    outputs=x,
                    name="ASTROMER")

        if self.pretrained_weights:
            # Loading the model weights
            try:
                if self.finetuning is not None:
                    print(f"Loading {self.finetuning} finetuned Model...")
                    model.load_weights(os.path.join(self.model_path, self.model_name, "finetuning", self.finetuning, "weights"))
                else:
                    print("Loading Base Model...")
                    model.load_weights(os.path.join(self.model_path, self.model_name, "weights"))
                print("Weights loaded successfully!")
            except:
                print("Couldn't load model weights!") 
        return model

    def load_configuration(self):

        # model_name="astromer_10022021"
        # git_link="https://github.com/HarshVardhanGoyal/test_model.git"
        # model_path = os.path.join(os.getcwd(),"weights")

        # Creating a temporary directory and cloning the desired repo
        test_dir = tempfile.mkdtemp()
        git.Repo.clone_from(self.git_link, test_dir, branch='main', depth=1)
        # time.sleep(2)

        # Defining the source path of the weights (i.e temporary directory)
        sourcepath = os.path.join(test_dir, self.model_name)

        # Checking the directories
        if not os.path.exists(self.model_path):
            os.makedirs(self.model_path)
        
        if os.path.exists(os.path.join(self.model_path, self.model_name)):
            if self.overwrite_weights:
                shutil.rmtree(os.path.join(self.model_path, self.model_name))
                shutil.move(sourcepath,self.model_path)
            else:
                print("The saved weights already exists")
        else:
            # Moving the weights to the code directory
            shutil.move(sourcepath,self.model_path)
     
        # Removing the temporary directory
        os.system('rmdir /S /Q "{}"'.format(test_dir))

        # Loading the conf file from the downloaded weights folder
        conf_file = os.path.join( self.model_path, self.model_name, 'conf.json')
        with open(conf_file, 'r') as handle:
            conf = json.load(handle)

        # Getting the astromer model as per the desired configuration
        self.num_layers=conf['layers']
        self.d_model   =conf['head_dim']
        self.num_heads =conf['heads']
        self.dff       =conf['dff']
        self.base      =conf['base']
        self.dropout   =conf['dropout']
        self.maxlen    =conf['max_obs']
        self.use_leak  =conf['use_leak']
        


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