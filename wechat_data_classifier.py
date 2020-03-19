# --coding:utf-8--

import io
import os
import numpy as np
from random import random
from sklearn.linear_model import Perceptron
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

dir_path = '/Users/adhcczhang/Desktop/wechat_data_test'

src_file_name = 'wechat_data_abstract_readnum_fasttext_vec'

data_X = []
data_Y = []
sample_rate = 0.01

threshold = 100
count = 0
with open(os.path.join(dir_path, src_file_name)) as input_file:
    for index, line in enumerate(input_file):
        if random() > sample_rate:
            continue
        line_list = line.strip().split('\t')
        try:
            Y = int(line_list[0])
            X = [float(eles) for eles in line_list[-1].split()]
            label = 0
            if Y > 500:
                label = 1
                count += 1
            data_Y.append(label)
            data_X.append(X)
            # if index % 10000 == 0:
            #     print(index)
        except Exception as e:
            # count += 1
            # print(count)
            # print(e)
            continue

print('正例个数: %d' % count)
data_X = np.array(data_X)
data_Y = np.array(data_Y)
x_train, x_test, y_train, y_test = train_test_split(data_X, data_Y, random_state=33, test_size=0.25)

model_list = [
    Perceptron(max_iter=100),
    SVC(kernel='rbf', gamma=0.10, C=10.0)
]

model_index = 1
model = model_list[model_index]


model.fit(x_train, y_train)
y_predict = model.predict(x_test)
print(len(y_test))
print('error number: %d' % (y_predict != y_test).sum())
print('精确度: %.2f' % accuracy_score(y_test, y_predict))


