import numpy as np
from kahonen import KahononNetwork
from perseptron import Perception
from sklearn import preprocessing

class Ai(object):
    def __init__(self, rows):
        input_size = len(rows[0])
        #Тренируем сеть Кохонена
        self.kahonen = KahononNetwork(input_size)
        data = normalization(rows, input_size)
        data = self.kahonen.train_auto_output(data)
        
        #Выводим итог классификации
        for out in range(self.kahonen.output_n):
            print("\n____CLUSTER  ", out, "____")
            for i in range(len(rows)):
                if int(data[i][-1]) == out:
                    print(rows[i])
            print("____________________")
        
        self.perseptron = Perception(input_size, self.kahonen.output_n,  self.kahonen.output_n * 2, 1)
        
        #Готовим ответы для обучающей выборки
        train = []
        for vector in data:
            v = [0 for x in range(self.kahonen.output_n)]
            v[int(vector[-1])] = 1
            print(v)
            train.append(v)
        while len(data) != len(train):
            v = [0 for x in range(self.kahonen.output_n)]
            train.append(v)
        train_y = np.array([np.array(x) for x in train[:]])
        
        #Выводим подготовленные данные и обучаем персептрон
        print(data, "x: ", data[:,0:-1], "y: ", train_y)
        self.perseptron.train(data[:,0:-1],train_y, 1000, 1)

    def predict(self, rows):
        data = normalization(rows, self.kahonen.input_n)
        print(data)
        self.perseptron.predict(data, rows)

def normalization(input_data , input_n):
    output_v = []
    for data in input_data:
        num_data = []
        for elm in data:
            if (type(elm) == str):
                num_list = list(map(str,map(ord,elm)))
                sum_of_num = 0.
                for num in num_list:
                    sum_of_num = sum_of_num - (float(num))
                num_data.append(-1/sum_of_num)
            else:
                num_data.append(elm)
        output_v.append(num_data)
    output_v = preprocessing.normalize(np.reshape(output_v, (1,-1)))
    for i in range(len(output_v[0])):
        print(output_v[0][i])
        while output_v[0][i] < 0.1:
            output_v[0][i] *= 10
    return np.reshape(output_v, (-1,input_n))
    for i in range(0, input_n):
        maximum = 0
        for data in output_v:
            if data[i] > maximum:
                maximum = data[i]
                
        for data in output_v:
            data[i] = data[i] / maximum
    return output_v