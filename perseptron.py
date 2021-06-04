import numpy as np
import os.path
import sys
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

class Perception(object):
    def __init__(self, input_n, output_n, layout_n=0, layout_c=0):
        self.model = tf.keras.Sequential()
        if not layout_c:
            self.model.add(layers.Dense(units=output_n, activation='sigmoid', input_dim=input_n))
        else:
            self.model.add(layers.Dense(units=layout_n, activation='sigmoid', input_dim=input_n))
            self.model.add(layers.Dropout(0.3))
            for lay in range(layout_c - 1):
                self.model.add(layers.Dense(units=layout_n, activation='sigmoid'))
                #self.model.add(layers.Dropout(0.3))
            self.model.add(layers.Dense(output_n, activation='sigmoid'))
        self.model.compile(loss='categorical_crossentropy',
                            optimizer='sgd',
                            metrics=['accuracy'])

    def train(self, train_x, train_y, epohs, batch_size, validation_split=0.15):
        print("Data for deep learning:\n", train_x)
        print("Labels for deep learning:\n",train_y)
        history = self.model.fit(train_x, train_y,
        epochs=epohs,
        batch_size=batch_size,
        validation_split=validation_split,
        verbose=1)
        plt.plot(history.history['val_accuracy'])
        plt.plot(history.history['accuracy'])
        plt.grid(True)
        plt.show()

    def predict(self, data, lables, true_answers):
        for elm_indx in range(len(data)):
            print("Element:\n", np.array([data[elm_indx]]), lables[elm_indx], "Right Answer:\n", true_answers[elm_indx])
            test_x = np.array([data[elm_indx]])
            predict = self.model.predict(test_x)
            print("Answer:\n", predict)