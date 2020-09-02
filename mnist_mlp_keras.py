#!/usr/bin/env python

"""Intro to Python

SRP 2020 Donkeycar teams
intro to python
+ what is python
+ python as a calculator (interactive)
+ variables
+ int, float, str, bool
+ lists
+ scripts
+ if ... else, for
+ functions, main

intro to keras
+ what is keras
+ MLP in keras
+ keras documentation

HW:
+ go understand the keras models in the parts/keras.py

Python Version: 2.7

Example:
  $ python intro.py

"""

# builtin 
# for python2 and python3 compatibility
from __future__ import absolute_import, division, print_function 
from tensorflow import keras
from tensorflow.keras.datasets import mnist
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.layers import Input, Dense
from tensorflow.keras.models import Model
import matplotlib.pyplot as plt
# third-party

# own mods

__author__ = "Chong Yue Linn"
__copyright__=""
__credits__=""

__license__ = ""
__version__ = "1.0.0"
__maintainer__ = "anyone but me"
__email__ = "mpechon@nus.edu.sg"
__status__ = ""


if __name__ == '__main__':
  # load MNIST dataset
  (X_train, Y_train), (X_test, Y_test) = mnist.load_data()

  # visualisize MNIST pictures to check it is ok
  # print (Y_train[0])
  # imgplot = plt.imshow(X_train[0])
  # plt.show()

  # make images into lists
  X_train = X_train.reshape(X_train.shape[0], 28*28)
  X_test = X_test.reshape(X_test.shape[0], 28*28)
  # print(X_train.shape)

  # normalize
  X_train = X_train.astype('float32')
  X_test = X_test.astype('float32')
  X_train /= 255
  X_test /= 255

  # one-hot encoding
  Y_train = to_categorical(Y_train, 10)
  Y_test = to_categorical(Y_test, 10)
  # print(Y_train[0])

  # build the model
  input_shape=(28*28,)
  img_in=Input(shape=input_shape, name="img_in")
  x=Dense(350, input_shape=input_shape, activation='relu')(img_in)
  x=Dense(50, activation='relu')(x)
  output=Dense(10, activation='softmax')(x)
  model=Model(inputs=[img_in], outputs=[output])
  model.summary()

  # train
  model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
  model.fit(X_train, Y_train, epochs=10, batch_size=256, verbose=1, validation_split=0.2)

  test_results = model.evaluate(X_test, Y_test, verbose=1)
  print('Loss:', test_results[0], "Accuracy:", test_results[1])
  # loss: the error value 
  # accuracy: ratio of times the prediction is correct

  # viz results
  imgplot = plt.imshow(X_test[0].reshape(28,28))
  plt.show()
  print("Label:", Y_test[0])
  print("Model prediction:", model.predict(X_test[0:256])[0])

  
