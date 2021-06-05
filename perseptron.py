import numpy as np
import os.path
import sys
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras import metrics

class Perception(object):
    def __init__(self, input_n, output_n, layout_n=0, layout_c=0):
        self.model = tf.keras.Sequential()
        #Однослойная сеть (без скрытых слоев)
        if not layout_c:
            self.model.add(layers.Dense(units=output_n, activation='relu', input_dim=input_n))
        #Многослойная сеть
        else:
            self.model.add(layers.Dense(units=layout_n, activation='relu', input_dim=input_n))
            #self.model.add(layers.Dropout(0.3))
            for lay in range(layout_c - 1):
                self.model.add(layers.Dense(units=layout_n, activation='sigmoid'))
                #self.model.add(layers.Dropout(0.3))
            self.model.add(layers.Dense(output_n, activation='softmax'))
        self.model.compile(loss='categorical_crossentropy',
                            optimizer='sgd',
                            metrics=metrics.categorical_accuracy)

    def train(self, train_x, train_y, epohs, batch_size, validation_split=0):
        #Тренировка сети и построение графиков
        print("Data for deep learning:\n", train_x)
        print("Labels for deep learning:\n",train_y)
        # Set callback functions to early stop training and save the best model so far
        callbacks = [ModelCheckpoint(filepath='best_model.h5', monitor='loss', save_best_only=True)]
        history = self.model.fit(train_x, train_y,
        epochs=epohs,
        batch_size=batch_size,
        validation_split=validation_split,
        verbose=1,
        callbacks=callbacks)
        plt.plot(history.history['loss'])
        plt.plot(history.history['categorical_accuracy'])
        plt.grid(True)
        plt.show()

    def predict(self, data, lables):
        #Предсказание для каждого элемента отдельно с выводом его нечислового значения
        for elm_indx in range(len(data)):
            print("Element:\n", np.array([data[elm_indx]]), "\n", lables[elm_indx])
            test_x = np.array([data[elm_indx]])
            predict = self.model.predict(test_x)
            print("Answer:\n", predict)