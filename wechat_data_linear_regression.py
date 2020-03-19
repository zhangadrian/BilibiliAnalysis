# --coding:utf-8--

import io
import os
import numpy as np
from sklearn.linear_model import LinearRegression, Lasso
from sklearn.svm import SVR
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import explained_variance_score, mean_squared_error
from sklearn.model_selection import train_test_split
from sknn.mlp import Regressor,Layer
import matplotlib.pyplot as plt
from theano.tensor.signal import downsample

dir_path = '/Users/adhcczhang/Desktop/wechat_data_test'

src_file_name = 'wechat_data_abstract_readnum_fasttext_vec'

data_X = []
data_Y = []
count = 0
with open(os.path.join(dir_path, src_file_name)) as input_file:
    for index, line in enumerate(input_file):
        line_list = line.strip().split('\t')
        if index > 1000000:
            break
        try:
            Y = int(line_list[0])
            X = [float(eles) for eles in line_list[-1].split()]
            data_Y.append(Y)
            data_X.append(X)
            if index % 10000 == 0:
                print(index)
        except Exception as e:
            count += 1
            print(count)
            # print(e)
            continue

data_X = np.array(data_X)
data_Y = np.array(data_Y)
x_train,x_test,y_train,y_test = train_test_split(data_X,data_Y,random_state=33,test_size=0.25)
# print(len(data_Y))
# model = LinearRegression()
# model = Lasso(alpha=0.01)
# model = SVR(kernel="poly")
model = GradientBoostingRegressor()
model = Regressor(
        layers=[Layer("Sigmoid", units=6), Layer("Sigmoid", units=14), Layer("Linear")],
        learning_rate=0.02,
        random_state=2018,
        n_iter=100)

model.fit(x_train, y_train)

y_predict = model.predict(x_test[:, :])
# print(explained_variance_score(data_Y,predict_X))
# 0.05905022487859224
# print(model.score(x_test,y_test))
print(mean_squared_error(y_predict, y_test))