# --coding:utf-8--

import io
import os
import numpy as np
from numpy import array
from collections import defaultdict
from random import random


dir_path = '/Users/adhcczhang/Desktop/wechat_data_test'

src_file_name = 'wechat_data_abstract_readnum_fasttext_vec'
stop_word_file_name = 'stopword.txt'


def gen_stopword_dict(path):
    from collections import defaultdict
    stopword_dict = defaultdict(int)
    with open(path) as input_file:
        for line in input_file:
            stopword = line.strip()
            stopword_dict[stopword] = 1
    return stopword_dict


word_dict = defaultdict(int)
sample_num = 10000000
sample_rate = 0.1
index = 0
stopword_dict = gen_stopword_dict(os.path.join(dir_path, stop_word_file_name))

with open(os.path.join(dir_path, src_file_name)) as input_file:
    for line in input_file:
        if random() > sample_rate:
            continue
        else:
            index += 1
        if index > sample_num:
            continue

        line_list = line.strip().split('\t')
        if len(line_list) < 3:
            continue
        try:
            read_num = int(line_list[0])
            word_list = line_list[1].split()
            test_num = float(line_list[-1].split()[0])
            for word in word_list:
                if word in stopword_dict:
                    continue
                word_dict[word] += read_num
        except Exception as e:
            continue

word_dict = sorted(word_dict.items(), key=lambda x: x[1])
for item in word_dict:
    print(item)

