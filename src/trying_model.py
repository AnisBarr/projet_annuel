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
from contextlib import redirect_stdout
from tensorboard.plugins.hparams import api as hp
from contextlib import redirect_stdout
from tensorboard.plugins.hparams import api as hp


# Preparing the dataset
# Setup train and test splits

path_data = "../resources/np_array/"


(x_train, y_train), (x_test, y_test) = (np.load(path_data+"x_train_float32_2.npy"),np.load(path_data+"y_train_float32_2.npy")) , (np.load(path_data+"x_test_float32_2.npy"),np.load(path_data+"y_test_float32_2.npy"))

#y_train = utils.to_categorical(y_train, 10)
#y_test = utils.to_categorical(y_test, 10)
x_train = np.reshape(x_train,(-1,64,64,1))
x_test = np.reshape(x_test,(-1,64,64,1))
x_train /= 255
x_test /= 255





HP_STRUCTURE= hp.HParam('structure_model', hp.Discrete([10]))
HP_DROPOUT = hp.HParam('dropout', hp.Discrete([0.20]))
HP_OPTIMIZER = hp.HParam('optimizer', hp.Discrete(['adam']))
HP_LEARNINGRATE=hp.HParam('leraning_rate', hp.Discrete([0.001]))
HP_MOMENTUM=hp.HParam('momentum', hp.Discrete([0.01]))
HP_L2=hp.HParam('l2', hp.Discrete([0.0]))
HP_ACTIVATION=hp.HParam('activation', hp.Discrete(['relu']))
HP_AUGMENTATION=hp.HParam('data_augmentation',hp.Discrete(["false"]))
batch_size=1024
epochs=50
METRIC_ACCURACY = 'accuracy'
METRIC_LOSS='loss'

log_dir='../logs'


with tf.summary.create_file_writer(log_dir).as_default():
  hp.hparams_config(
    hparams=[HP_STRUCTURE, HP_DROPOUT, HP_OPTIMIZER,HP_MOMENTUM,HP_LEARNINGRATE,HP_L2,HP_ACTIVATION,HP_AUGMENTATION],
    metrics=[hp.Metric(METRIC_ACCURACY, display_name='Accuracy_test'),
             hp.Metric(METRIC_LOSS, display_name='loss_test' )
           ],
  )




def aument_model(x_train,y_train,batch_size,model,log_dir):
  train_datagen = ImageDataGenerator(
          rotation_range=45,
          width_shift_range=.15,
          height_shift_range=.15,
          horizontal_flip=True,
          )
  train_datagen.fit(x_train)
  train_datagen_ = train_datagen.flow(x_train, y_train, batch_size=batch_size)
  val_datagen = ImageDataGenerator(
          rotation_range=45,
          width_shift_range=.15,
          height_shift_range=.15,
          horizontal_flip=True,
          )
  val_datagen.fit(x_test)
  val_datagen = val_datagen.flow(x_test, y_test, batch_size=batch_size)
      
  tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)
  history= model.fit_generator(train_datagen_,
                      validation_data=val_datagen,
                      epochs=30,
                      callbacks=[tensorboard_callback]
                                )
  return history
                







def run(run_dir, hparams):
  with tf.summary.create_file_writer(run_dir).as_default():
    hp.hparams(hparams)  # record the values used in this trial
    loss,accuracy = train_test_model(hparams,run_dir,x_train,y_train)
    tf.summary.scalar(METRIC_ACCURACY, accuracy, step=1)
    tf.summary.scalar(METRIC_LOSS, loss, step=1)

  
def RNN(hparams):
  ConvNN_model = models.Sequential()

  ConvNN_model.add(layers.Conv2D(32, (3, 3), activation='relu'))
  ConvNN_model.add(layers.MaxPooling2D((2, 2)))

  ConvNN_model.add(layers.Conv2D(64, (3, 3), activation='relu'))

  # encode rows of matrix
  ConvNN_model.add(TimeDistributed(LSTM(128, activation='relu')))
  ConvNN_model.add(Dropout(0.2))

  # encode columns
  ConvNN_model.add(LSTM(128, activation='relu'))

  ConvNN_model.add(layers.Dense(64, activation='relu'))
  ConvNN_model.add(layers.Dropout(hparams[HP_DROPOUT]))
  ConvNN_model.add(layers.Dense(27, activation='softmax'))
  return ConvNN_model


def model2(hparams):
  model = tf.keras.models.Sequential([
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(4096, activation=tf.nn.relu if hparams[HP_ACTIVATION]=='relu' else tf.nn.sigmoid  , kernel_regularizer=regularizers.l2(hparams[HP_L2])),
    tf.keras.layers.Dense(2048, activation=tf.nn.relu if hparams[HP_ACTIVATION]=='relu' else tf.nn.sigmoid  , kernel_regularizer=regularizers.l2(hparams[HP_L2])),
    tf.keras.layers.Dense(1024, activation=tf.nn.relu if hparams[HP_ACTIVATION]=='relu' else tf.nn.sigmoid  , kernel_regularizer=regularizers.l2(hparams[HP_L2])),
    tf.keras.layers.Dense(512, activation=tf.nn.relu if hparams[HP_ACTIVATION]=='relu' else tf.nn.sigmoid  , kernel_regularizer=regularizers.l2(hparams[HP_L2])),
    tf.keras.layers.Dropout(hparams[HP_DROPOUT]),
    tf.keras.layers.Dense(27, activation=tf.nn.softmax),
  ])
  return model





def resnet_layer(inputs,
                 num_filters=16,
                 kernel_size=3,
                 strides=1,
                 activation='relu',
                 batch_normalization=True,
                 conv_first=True):
    """2D Convolution-Batch Normalization-Activation stack builder

    # Arguments
        inputs (tensor): input tensor from input image or previous layer
        num_filters (int): Conv2D number of filters
        kernel_size (int): Conv2D square kernel dimensions
        strides (int): Conv2D square stride dimensions
        activation (string): activation name
        batch_normalization (bool): whether to include batch normalization
        conv_first (bool): conv-bn-activation (True) or
            bn-activation-conv (False)

    # Returns
        x (tensor): tensor as input to the next layer
    """
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


def resnet_v1(input_shape=(64,64,1), depth=20, num_classes=27):
    """ResNet Version 1 Model builder [a]

    Stacks of 2 x (3 x 3) Conv2D-BN-ReLU
    Last ReLU is after the shortcut connection.
    At the beginning of each stage, the feature map size is halved (downsampled)
    by a convolutional layer with strides=2, while the number of filters is
    doubled. Within each stage, the layers have the same number filters and the
    same number of filters.
    Features maps sizes:
    stage 0: 32x32, 16
    stage 1: 16x16, 32
    stage 2:  8x8,  64
    The Number of parameters is approx the same as Table 6 of [a]:
    ResNet20 0.27M
    ResNet32 0.46M
    ResNet44 0.66M
    ResNet56 0.85M
    ResNet110 1.7M

    # Arguments
        input_shape (tensor): shape of input image tensor
        depth (int): number of core convolutional layers
        num_classes (int): number of classes (CIFAR10 has 10)

    # Returns
        model (Model): Keras model instance
    """
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


def train_test_model(hparams,log_dir,x_train,y_train):
  if hparams[HP_STRUCTURE]==1:
    model=RNN(hparams)
  if hparams[HP_STRUCTURE]==2:
    model=model2(hparams)
  else :
    print("---------------------------resnet----------------------------------------------")
    model=resnet_v1()

  if hparams[HP_OPTIMIZER]=='adam':
    optimizer=optimizers.Adam(lr= hparams[HP_LEARNINGRATE], decay=1e-6)
  else:
    optimizer= optimizers.SGD(lr= hparams[HP_LEARNINGRATE], decay=1e-6, momentum=hparams[HP_MOMENTUM])


  model.compile(optimizer=optimizer,
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])
  

  if  hparams[HP_AUGMENTATION]=="true":
    history=aument_model(x_train,y_train,batch_size,model,log_dir)

  tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir)

  reduce_lr = tf.keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.01, patience=5,verbose=1 )

  model.fit(x = x_train, y = y_train,validation_split=.1, epochs = epochs,callbacks=[tensorboard_callback,reduce_lr])
  
  loss,accuracy = model.evaluate(x_test, y_test)

  model.save(log_dir+'/my_model.h5')

  model.save_weights(log_dir+'/my_model_weights.h5')

  plot_model(model,log_dir+'/my_model.png')

  with open(log_dir+'/my_model_summary.txt', 'w') as f:
     with redirect_stdout(f):
         model.summary()

  return loss,accuracy




def lancer(): 
  session_num = 0

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
                  if structure==1 :
                    modelstrcture="layer_512*10"
                  else :
                    if structure==2 :
                      modelstrcture="layer_1024*512*256*10"
                    else :
                      modelstrcture="8_layers_1024*...*10"
                  run_name = "/mo_"+modelstrcture+"_aug_"+str(aug)+"_act_"+str(activate)+"_do_"+str(dropout_rate)+"_l2_"+str(l2)+"_op_"+str(optimizer)+"_lr_"+str(learning_rate)+"_mome_"+str(momentum)+"04/04/2020"
                  print('--- Starting trial: %s' % run_name)
                  print({h.name: hparams[h] for h in hparams})
                  run(log_dir+run_name, hparams)
                  session_num += 1
                  print("-----------session_num :"+str(session_num)+"---------------")