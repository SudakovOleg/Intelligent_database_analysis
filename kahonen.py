import numpy as np
import random

class KahononNetwork(object):
    def __init__(self, input_n):
        self.input_n = input_n
        self.output_n = 2
        self.weights = np.zeros((self.input_n, self.output_n))
        self.shuffle()
        
    def shuffle(self):
        for x in range(0,self.input_n):
            for y in range(0,self.output_n):
                self.weights[x][y] = random.uniform(0., 1.0)

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
        self.weights = np.zeros((self.input_n, self.output_n))
        self.shuffle()
        return self.output_n
    
    def information(self):
        print(self.input_n)
        print(self.output_n)
    
    def train(self, input_table, epohs):
        for ep in range(0, epohs):
            for data in input_table:
                res = self.find_cluster(data)
                min_res_index = res.argsort(0)[:1]
                for x in range(0,self.input_n):
                    self.weights[x][min_res_index] = self.weights[x][min_res_index] + 0.5 * (data[x] - self.weights[x][min_res_index])
                print(data, res, min_res_index)
                
    
    def find_cluster(self, input_v):
        if len(input_v) != self.input_n:
            print("error")
        res = np.zeros(self.output_n)
        for y in range(0,self.output_n):
            for x in range(0,self.input_n):
                res[y] = res[y] + ((input_v[x] - self.weights[x][y]) ** 2.0)
            res[y] = res[y] ** 0.5
        return res
        
    def normalization(self, input_v):
        output_v = []
        for data in input_v:
            num_data = []
            for elm in data:
                if (type(elm) == str):
                    num_list = list(map(str,map(ord,elm)))
                    sum_of_num = 0.
                    for num in num_list:
                        sum_of_num = sum_of_num + float(num)
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
        