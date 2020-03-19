# --coding:utf-8--

import io
import os
import numpy as np
from numpy import array
from numpy.random import normal, randint
from scipy.stats import mode
from matplotlib import pyplot
import matplotlib.font_manager as fm
from collections import defaultdict

dir_path = '/Users/adhcczhang/Desktop/wechat_data_test'

src_file_name = 'wechat_data_all_2'

src_file_path = os.path.join(dir_path, src_file_name)
read_num_list = []

myfont = fm.FontProperties(fname='./SimHei.ttf')

def draw_bar(data_array):
    xticks = ['0', '10', '50', '100', '1000', '2000',]
    # xticks = []
    # for i in range(0, 10001, 10):
    #     xticks.append(i)

    bar_num = defaultdict(int)
    for data in data_array:
        for i in range(1, len(xticks)):
            if int(xticks[i]) > data >= int(xticks[i-1]):
                bar_num[xticks[i]] += 1
    xticks = xticks[1:]
    pyplot.bar(xticks, [bar_num[xtick] for xtick in xticks], align='center')

    pyplot.xlabel(u'点赞数量数量级', fontproperties=myfont)
    pyplot.ylabel(u'文章数量', fontproperties=myfont)
    pyplot.title(u'文章点赞量分布直方图', fontproperties=myfont)
    pyplot.show()


def draw_hist(data_array):
    pyplot.hist(data_array, 10)
    pyplot.show()


with open(src_file_path) as src_file:
    for index, line in enumerate(src_file):
        line_list = line.strip().split('\t')
        # print(len(line_list))
        try:
            read_num_list.append(int(line_list[8]))
        except Exception as e:
            # print(line_list[7])
            continue
        if index % 10000 == 0:
            print(index)
        if index > 10000000000:
            break


read_num_array = array(read_num_list)
print(len(read_num_list))
print(np.mean(read_num_array))
print(np.median(read_num_array))
# mode(read_num_array)
draw_bar(read_num_array)
# draw_hist(read_num_array)
