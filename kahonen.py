import numpy as np
from scipy.spatial import distance
import random

class KahononNetwork(object):
    def __init__(self, input_n):
        self.input_n = input_n
        self.output_n = 10
        self.weight = np.random.rand(self.input_n,self.output_n)
        

    def print_weights(self):
        print(self.weights)
    
    def train_auto_output(self, input_table):
        #Начальное число кластеров половина данных
        self.output_set(int(len(input_table)/2))
        #Добавляем индексы в словарь
        clusters_in_use = {i: False for i in range(self.output_n)}
        #Тренируем в количестве эпох (входных параметров * 50)
        new_table = self.train(input_table, len(input_table) * 50)
        #Запоминаем какие кластера были использованы
        for data in new_table:
            clusters_in_use[int(data[-1])] = True
        
        #Переменная текущего кластера
        index_in_use = 0
        for key in clusters_in_use:
            #Для каждего кластера в котором есть значения
            if clusters_in_use[key] == True:
                #Во всех данных с этим кластером обновляем кластер на значение текущего кластера
                for data in new_table:
                    if key == int(data[-1]):
                        data[-1] = index_in_use
                #Перед проверкой следующего не пустого кластера, инкрементируем значение текущего кластера
                index_in_use = index_in_use + 1
        #Ставим количество кластеров в сети равным по факту используемым
        self.output_set(index_in_use)
        return new_table

    def output_set(self, output_n):
        self.output_n = output_n
        self.weight = np.random.rand(self.input_n,self.output_n)
        return self.output_n
    
    def information(self):
        print(self.input_n)
        print(self.output_n)
    
    def train(self, input_table , epohs):
        n = len(input_table)
        alpha = 1 # Коэфициент обучения
        #Нулевой вектор длиной в количество даннх
        addZeros = np.zeros((n, 1))
        #Добавляем по 0 в конец каждого вектора в данных
        input_table = np.append(input_table, addZeros, axis=1)
        print("The SOM algorithm: \n")
        print("The training data: \n", input_table)
        print("\nTotal number of data: ",n)
        print("Total number of features: ",self.input_n)
        print("Total number of Clusters: ",self.output_n)
        print("\nThe initial self.weight: \n", np.round(self.weight,2))
        for it in range(epohs): # Количество итераций
             list_of_index = list(range(n))
             random.shuffle(list_of_index)
             for i in list_of_index: # Для каждого вектора из перемешанных данных
                distMin = float("inf") # Инициализируем минимальную дистанцию
                for j in range(self.output_n): # Для каждого выхода
                    # Считаем дистанцию (квадрат из евкидовой суммы всех весов выхода и всех данных входа
                    dist = np.square(distance.euclidean(self.weight[:,j], input_table[i,0:self.input_n]))
                    # Если дистанция меньше минимальной - переопределяем
                    if distMin>dist:
                        distMin = dist
                        jMin = j
                        input_table[i,self.input_n] = j
                self.weight[:,jMin] = self.weight[:,jMin]*(1-alpha) + alpha*input_table[i,0:self.input_n]   
             # Уменьшаем альфа
             alpha = alpha * (1 - it/n)
        print("\nThe final self.weight: \n",np.round(self.weight,4))
        print("\nThe data with cluster number: \n", input_table)
        return input_table
    
    def find_cluster(self, input_v):
        distMin = float("inf") # Инициализируем минимальную дистанцию
        input_v = np.append(input_v, 0)
        for j in range(self.output_n): # Для каждого выхода
            # Считаем дистанцию (квадрат из евкидовой суммы всех весов выхода и всех данных входа
            dist = np.square(distance.euclidean(self.weight[:,j], input_v[0:self.input_n]))
            # Если дистанция меньше минимальной - переопределяем
            if distMin>dist:
                distMin = dist
                jMin = j
                input_v[self.input_n] = j
        return input_v

