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
    
    def output_calc(self, input_table, prev_mid = 0.):
        sum_of_res = 0.
        count_of_res = np.zeros((self.output_n,1))
        for data in input_table:
            res = self.find_cluster(data)
            min_res_index = res.argsort(0)[:1]
            max_res_index = res.argsort(0)[-1]
            sum_of_res = sum_of_res + (res[max_res_index])
            mid = sum_of_res / len(input_table)
            print("Mid -", mid, " ", mid, " prev_mid = ", prev_mid)
            if mid > prev_mid:
                self.output_set(self.output_n + 1)
                return self.output_calc(input_table, mid)
            else:
                return self.output_set(self.output_n - 1)
    
    def output_set(self, output_n):
        self.output_n = output_n
        self.weight = np.random.rand(self.input_n,self.output_n)
        return self.output_n
    
    def information(self):
        print(self.input_n)
        print(self.output_n)
    
    def train(self, input_table, epohs):
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
             alpha = alpha * (1 - it/epohs)
        print("\nThe final self.weight: \n",np.round(self.weight,4))
        print("\nThe data with cluster number: \n", input_table)
        return input_table
    
    def find_cluster(self, input_v):
        distMin = float("inf") # Инициализируем минимальную дистанцию
        input_v = np.append(input_v, 0, axis=1)
        for j in range(self.output_n): # Для каждого выхода
            # Считаем дистанцию (квадрат из евкидовой суммы всех весов выхода и всех данных входа
            dist = np.square(distance.euclidean(self.weight[:,j], input_v[0:self.input_n]))
            # Если дистанция меньше минимальной - переопределяем
            if distMin>dist:
                distMin = dist
                jMin = j
                input_v[self.input_n] = j
        return input_v
        
    def normalization(self, input_v):
        output_v = []
        for data in input_v:
            num_data = []
            for elm in data:
                if (type(elm) == str):
                    num_list = list(map(str,map(ord,elm)))
                    sum_of_num = 0.
                    for num in num_list:
                        sum_of_num = sum_of_num + (float(num) ** 2)
                    num_data.append(sum_of_num)
                else:
                    num_data.append(elm)
            output_v.append(num_data)
        
        for i in range(0, self.input_n):
            maximum = 0
            for data in output_v:
                if data[i] > maximum:
                    maximum = data[i]
                    
            for data in output_v:
                data[i] = data[i] / maximum
        print(output_v)
        return output_v
        