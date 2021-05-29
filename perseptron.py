import numpy as np
import os.path
import sys
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

class Perception(object):
    def __init__(self, input_n, output_n, layout_n=0, layout_c=0):
        self.model = tf.keras.Sequential()
        if not layout_c:
            self.model.add(layers.Dense(units=output_n, activation='relu', input_dim=input_n))
        else:
            self.model.add(layers.Dense(units=layout_n, activation='relu', input_dim=input_n))
            for lay in range(layout_c):
                self.model.add(layers.Dense(units=layout_n, activation='relu'))
                self.model.add(layers.Dropout(0.5))
            self.model.add(layers.Dense(output_n, activation='softmax'))
        self.model.compile(loss='categorical_crossentropy',
                            optimizer='adam',
                            metrics=['accuracy'])

    def train(self, train_x, train_y, epohs, batch_size, validation_split=0.1):
        print("Data for deep learning:\n", train_x)
        print("Labels for deep learning:\n",train_y)
        self.model.fit(train_x, train_y,
        epochs=epohs,
        batch_size=batch_size,
        validation_split=validation_split,
        verbose=1)

    def predict(self, data):
        for elm in data:
            print("Element:\n", np.array([elm]))
            test_x = np.array([elm])
            predict = self.model.predict(test_x)
            print("Answer:\n", predict)