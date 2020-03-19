# --coding:utf-8--

import requests
import os
import json
from bs4 import BeautifulSoup
from urllib.request import urlopen, urlretrieve
import multiprocessing as mp
from random import random


def download_pic(line):
    line_list = line.split('\t')
    index = line_list[-1]
    try:
        read_num = int(line_list[7])
        like_num = int(line_list[8])
        url = line_list[6]
        html = urlopen(url)
        data = html.read()
        soup = BeautifulSoup(data, features="html.parser")
        imgs = soup.find_all('img')
        sub_index = 0
        for img in imgs:
            if img.get('data-src'):
                file_name = index + '_' + str(read_num) + '_' + str(like_num) + "_" + str(
                    sub_index) + '.png'
                file_path = os.path.join(dest_dir_path, file_name)
                if not os.path.exists(file_path):
                    urlretrieve(img.get('data-src'), file_path)
                    sub_index += 1
                    break
    except Exception as e:
        print(1)


if __name__ == "__main__":
    dir_path = '/Users/adhcczhang/Desktop/wechat_data_test'
    src_file_name = 'wechat_data_all'
    dest_dir_path = './img'
    sample_date = 1.0001
    index_threshold = 10
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)
    url_path_list = []
    with open(os.path.join(dir_path, src_file_name)) as input_file:
        for index, line in enumerate(input_file):
            line_list = line.strip().split('\t')
            if index > index_threshold:
                continue
            if random() > sample_date:
                continue
            if index % 10 == 0:
                print(index)
            url_path_list.append(line.strip() + '\t' + str(index))

    # print(url_path_list)
    pool = mp.Pool(10)
    res = pool.map(download_pic, url_path_list)
