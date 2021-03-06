from __future__ import absolute_import, division, print_function, unicode_literals

import tensorflow as tf
# from model import *
from tensorflow.keras import utils
from tensorflow.keras import datasets, layers, models 
from tensorflow.keras.layers import Dropout, Dense, BatchNormalization, Conv2D, MaxPool2D, Flatten ,LSTM, TimeDistributed, Input,Activation ,AveragePooling2D 
from tensorflow.keras.callbacks import LearningRateScheduler
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.utils import plot_model
from tensorflow.keras import optimizers
from tensorflow.keras import regularizers
import matplotlib.pyplot as plt
import numpy as np
import os
from datetime import datetime
from contextlib import redirect_stdout
from tensorboard.plugins.hparams import api as hp
from contextlib import redirect_stdout
from tensorboard.plugins.hparams import api as hp


METRIC_ACCURACY = 'accuracy'
METRIC_LOSS='loss'
log_dir='../logs/train/'

HP_STRUCTURE= hp.HParam('structure_model', hp.Discrete([1,2,3,4]))
HP_DROPOUT = hp.HParam('dropout', hp.Discrete([0.30]))
HP_OPTIMIZER = hp.HParam('optimizer', hp.Discrete(['adam']))
HP_LEARNINGRATE=hp.HParam('leraning_rate', hp.Discrete([0.001]))
HP_MOMENTUM=hp.HParam('momentum', hp.Discrete([0.01]))
HP_L2=hp.HParam('l2', hp.Discrete([0.001]))
HP_ACTIVATION=hp.HParam('activation', hp.Discrete(['relu']))
HP_AUGMENTATION=hp.HParam('data_augmentation',hp.Discrete(["true"]))
hparams= None
batch_sizes=512
epoch=10

def init(hp_structure,hp_dropout,hp_optimizer,hp_learningrate,hp_l2,hp_activation,BATCH_SIZES,EPOCH):
  HP_STRUCTURE = hp_structure
  HP_DROPOUT = hp_dropout
  HP_OPTIMIZER = hp_optimizer
  HP_LEARNINGRATE = hp_learningrate
  HP_L2 = hp_l2
  HP_ACTIVATION = hp_activation
  batch_sizes=BATCH_SIZES
  epoch=EPOCH

  with tf.summary.create_file_writer(log_dir).as_default():
    hp.hparams_config(
      hparams=[hp_structure, hp_dropout, hp_optimizer,HP_MOMENTUM,hp_learningrate,hp_l2,hp_activation,HP_AUGMENTATION],
      metrics=[hp.Metric(METRIC_ACCURACY, display_name='Accuracy_test'),
              hp.Metric(METRIC_LOSS, display_name='loss_test' )
            ],
    )

  
def run(run_dir, hparams,x_train,y_train,x_test, y_test,epoch,batch_sizes):
  with tf.summary.create_file_writer(run_dir).as_default():
    hp.hparams(hparams)  # record the values used in this trial
    loss,accuracy = train_test_model(hparams,run_dir,x_train,y_train,x_test, y_test,epoch,batch_sizes)
    tf.summary.scalar(METRIC_ACCURACY, accuracy, step=1)
    tf.summary.scalar(METRIC_LOSS, loss, step=1)

def model1(hparams):
  model = tf.keras.models.Sequential([
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(4096, activation=tf.nn.relu if hparams[HP_ACTIVATION]=='relu' else tf.nn.sigmoid  , kernel_regularizer=regularizers.l2(hparams[HP_L2])),
    tf.keras.layers.Dense(2048, activation=tf.nn.relu if hparams[HP_ACTIVATION]=='relu' else tf.nn.sigmoid  , kernel_regularizer=regularizers.l2(hparams[HP_L2])),
    tf.keras.layers.Dropout(hparams[HP_DROPOUT]),
    tf.keras.layers.Dense(27, activation=tf.nn.softmax),
  ])
  return model

def model2(hparams):
  model = tf.keras.models.Sequential([
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(4096, activation=tf.nn.relu if hparams[HP_ACTIVATION]=='relu' else tf.nn.sigmoid  , kernel_regularizer=regularizers.l2(hparams[HP_L2])),
    tf.keras.layers.Dense(2048, activation=tf.nn.relu if hparams[HP_ACTIVATION]=='relu' else tf.nn.sigmoid  , kernel_regularizer=regularizers.l2(hparams[HP_L2])),
    tf.keras.layers.Dense(1024, activation=tf.nn.relu if hparams[HP_ACTIVATION]=='relu' else tf.nn.sigmoid  , kernel_regularizer=regularizers.l2(hparams[HP_L2])),
    tf.keras.layers.Dropout(hparams[HP_DROPOUT]),
    tf.keras.layers.Dense(27, activation=tf.nn.softmax),
  ])
  return model

def RNN_2(hparams):
    model = models.Sequential()
    
    model.add(Conv2D(16, kernel_size = [3,3], padding = 'same', activation = 'relu'))
    model.add(Conv2D(32, kernel_size = [3,3], padding = 'same', activation = 'relu'))
    model.add(MaxPool2D(pool_size = [3,3]))
    
    model.add(Conv2D(32, kernel_size = [3,3], padding = 'same', activation = 'relu'))
    model.add(Conv2D(64, kernel_size = [3,3], padding = 'same', activation = 'relu'))
    model.add(MaxPool2D(pool_size = [3,3]))
    
    model.add(Conv2D(128, kernel_size = [3,3], padding = 'same', activation = 'relu'))
    model.add(Conv2D(256, kernel_size = [3,3], padding = 'same', activation = 'relu'))
    model.add(MaxPool2D(pool_size = [3,3]))
    
    model.add(BatchNormalization())
    
    model.add(Flatten())
    model.add(Dropout(0.5))
    model.add(Dense(512, activation = 'relu', kernel_regularizer = regularizers.l2(hparams[HP_L2]) ))
    model.add(Dense(28, activation = 'softmax'))

    return model

def resnet_layer(inputs,
                 num_filters=16,
                 kernel_size=3,
                 strides=1,
                 activation='relu',
                 batch_normalization=True,
                 conv_first=True):

    conv = Conv2D(num_filters,
                  kernel_size=(kernel_size,kernel_size),
                  strides=strides,
                  padding='same',
                  kernel_initializer='he_normal',
                  kernel_regularizer=regularizers.l2(1e-4))

    x = inputs
    if conv_first:
        x = conv(x)
        if batch_normalization:
            x = BatchNormalization()(x)
        if activation is not None:
            x = Activation(activation)(x)
    else:
        if batch_normalization:
            x = BatchNormalization()(x)
        if activation is not None:
            x = Activation(activation)(x)
        x = conv(x)
    return x

def resnet_v1(input_shape=(64,64,1), depth=20, num_classes=28):

    if (depth - 2) % 6 != 0:
        raise ValueError('depth should be 6n+2 (eg 20, 32, 44 in [a])')
    # Start model definition.
    num_filters = 16
    num_res_blocks = int((depth - 2) / 6)

    inputs = Input(shape=input_shape)
    x = resnet_layer(inputs=inputs)
    # Instantiate the stack of residual units
    for stack in range(3):
        for res_block in range(num_res_blocks):
            strides = 1
            if stack > 0 and res_block == 0:  # first layer but not first stack
                strides = 2  # downsample
            y = resnet_layer(inputs=x,
                             num_filters=num_filters,
                             strides=strides)
            y = resnet_layer(inputs=y,
                             num_filters=num_filters,
                             activation=None)
            if stack > 0 and res_block == 0:  # first layer but not first stack
                # linear projection residual shortcut connection to match
                # changed dims
                x = resnet_layer(inputs=x,
                                 num_filters=num_filters,
                                 kernel_size=1,
                                 strides=strides,
                                 activation=None,
                                 batch_normalization=False)
            x = layers.add([x, y])
            x = Activation('relu')(x)
        num_filters *= 2

    # Add classifier on top.
    # v1 does not use BN after last shortcut connection-ReLU
    x = AveragePooling2D(pool_size=8)(x)
    y = Flatten()(x)
    outputs = Dense(num_classes,
                    activation='softmax',
                    kernel_initializer='he_normal')(y)

    # Instantiate model.
    model = models.Model(inputs=inputs, outputs=outputs)
    return model

def train_test_model(hparams,log_dir,x_train,y_train,x_test, y_test,epoch,batch_sizes):
  epochs = epoch
  batch_size = batch_sizes

  if hparams[HP_STRUCTURE]==3:
    print("---------------------------RNN----------------------------------------------")
    model=RNN_2(hparams)
    batch_size=128


  elif hparams[HP_STRUCTURE]==1:
    print("---------------------------dense1----------------------------------------------")
    model=model1(hparams)

  elif hparams[HP_STRUCTURE]==2:
    print("---------------------------dense2----------------------------------------------")
    model=model2(hparams)

  else :
    print("---------------------------resnet----------------------------------------------")
    model=resnet_v1()
    batch_size=256

  if hparams[HP_OPTIMIZER]=='adam':
    optimizer=optimizers.Adam(lr= hparams[HP_LEARNINGRATE], decay=1e-6)
  else:
    optimizer= optimizers.SGD(lr= hparams[HP_LEARNINGRATE], decay=1e-6, momentum=hparams[HP_MOMENTUM])


  model.compile(optimizer=optimizer,
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])
  

  tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir)

  reduce_lr = tf.keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.02, patience=5,verbose=1 )

  model.fit(x = x_train, y = y_train,batch_size=batch_size, validation_data=(x_test, y_test), epochs = epochs,callbacks=[tensorboard_callback,reduce_lr])
   
  loss,accuracy = model.evaluate(x_test, y_test)

  model.save(log_dir+'/my_model_acc_'+str(accuracy)+'.h5')

  model.save_weights(log_dir+'/my_model_weights.h5')

  plot_model(model,log_dir+'/my_model.png')

  with open(log_dir+'/my_model_summary.txt', 'w') as f:
     with redirect_stdout(f):
         model.summary()

  return loss,accuracy

def lancer():
  path_data = "../resources/data_set/np_array/"
  (x_train, y_train), (x_test, y_test) = (np.load(path_data+"x_train_64_64.npy"),np.load(path_data+"y_train_64_64.npy")) , (np.load(path_data+"x_test_64_64.npy"),np.load(path_data+"y_test_64_64.npy"))
  x_train = np.reshape(x_train,(-1,64,64,1))
  x_test = np.reshape(x_test,(-1,64,64,1))

  # with tf.summary.create_file_writer(log_dir).as_default():
  #   hp.hparams_config(
  #     hparams=[HP_STRUCTURE, HP_DROPOUT, HP_OPTIMIZER,HP_MOMENTUM,HP_LEARNINGRATE,HP_L2,HP_ACTIVATION,HP_AUGMENTATION],
  #     metrics=[hp.Metric(METRIC_ACCURACY, display_name='Accuracy_test'),
  #             hp.Metric(METRIC_LOSS, display_name='loss_test' )
  #           ],
  #   )


  for aug in HP_AUGMENTATION.domain.values:
    for activate in HP_ACTIVATION.domain.values:
      for structure in HP_STRUCTURE.domain.values:
        for dropout_rate in HP_DROPOUT.domain.values:
          for optimizer in HP_OPTIMIZER.domain.values:
            for learning_rate in HP_LEARNINGRATE.domain.values:
              for momentum in HP_MOMENTUM.domain.values:
                for l2 in HP_L2.domain.values:
                  print(optimizer)
                  hparams = {
                        HP_AUGMENTATION: aug,
                        HP_STRUCTURE: structure,
                        HP_DROPOUT: dropout_rate,
                        HP_OPTIMIZER: optimizer,
                        HP_L2: l2,
                        HP_MOMENTUM: momentum,
                        HP_LEARNINGRATE: learning_rate,
                        HP_ACTIVATION :activate
                        }
                  print(type(structure))

                  if structure==1 :
                    modelstrcture="model1"
                  elif structure==2 :
                    modelstrcture="model2"
                  elif structure==3 :
                    modelstrcture="rnn"
                  else :
                    modelstrcture="resnet"

                  now = datetime.now()
                  dt_string = now.strftime("%d-%m-%Y_%H:%M:%S")

                  run_name = "/mo_"+modelstrcture+"_aug_"+str(True)+"_act_"+str(activate)+"_do_"+str(dropout_rate)+"_l2_"+str(l2)+"_op_"+str(optimizer)+"_lr_"+str(learning_rate)+"_mome_"+str(momentum)+"_"+dt_string
                  
                  print('--- Starting trial: %s' % run_name)
                  print({h.name: hparams[h] for h in hparams})
                  run(log_dir+run_name, hparams,x_train,y_train,x_test, y_test,epoch,batch_sizes)

if __name__ == "__main__":
    
  lancer()