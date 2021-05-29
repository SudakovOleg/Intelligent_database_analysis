import numpy as np
import os.path
import sys
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

class Perception(object):
    def __init__(self, input_n, output_n, layout_n=0, layout_c=0)
        self.model = tf.keras.Sequential()
        if not layout_c:
            model.add(layers.Dense(units=output_n, activation='relu', input_dim=input_n))
        elif:
            model.add(layers.Dense(units=layout_n, activation='relu', input_dim=input_n))
            for lay in range(layout_c - 1):
                model.add(layers.Dense(units=layout_n, activation='relu'))
                model.add(layers.Dense(output_n, activation='sigmoid'))
         model.compile(optimizer='rmsprop',  loss='binary_crossentropy', metrics=['accuracy'])

    def train(self, train_x, train_y, epohs, batch_size, validation_split=0.15):
        model.fit(train_x, train_y,
        epochs,
        batch_size,
        validation_split)

    def predict(self, data):
        predict = model.predict(data)
        print(predict)