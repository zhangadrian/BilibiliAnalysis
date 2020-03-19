# --coding:utf-8--

is_test = False
analysis_index = 4


def cal_gini(data_dict):
    import numpy as np

    if isinstance(data_dict, dict):
        input_list = get_input_list(data_dict)
    else:
        input_list = data_dict

    input_cumsum = np.cumsum(sorted(np.append(input_list, 0)))
    input_sum = input_cumsum[-1]
    x_array = np.array(range(0, len(input_cumsum))) / np.float(len(input_cumsum) - 1)
    y_array = input_cumsum / input_sum
    b_area = np.trapz(y_array, x=x_array)
    a_area = 0.5 - b_area
    gini_index = a_area / (a_area + b_area)

    return gini_index


def get_input_list(data_dict):
    input_list = []
    if isinstance(data_dict, dict):
        for key in data_dict:
            num_str, _ = data_dict[key].split('_')
            input_list.append(int(num_str))
    else:
        for item in data_dict:
            num_str, _ = item[1].split('_')
            input_list.append(int(num_str))

    return input_list


def gen_stopword_dict(path):
    from collections import defaultdict

    stopword_dict = defaultdict(int)
    with open(path) as input_file:
        for line in input_file:
            stopword = line.strip()
            stopword_dict[stopword] = 1
    return stopword_dict


def get_median(data_dict):
    import numpy as np
    if isinstance(data_dict, list):
        input_list = data_dict
    else:
        input_list = get_input_list(data_dict)

    return np.median(np.array(input_list))


def t_test(input_1, input_2):
    import numpy as np
    from scipy import stats

    mean_1 = np.mean(input_1)
    mean_2 = np.mean(input_2)
    std_1 = np.std(input_1)
    std_2 = np.std(input_2)
    len_1 = len(input_1)
    len_2 = len(input_2)

    mod_std_1 = np.sqrt(np.float32(len_1) / np.float32(len_1 - 1) * std_1)
    mod_std_2 = np.sqrt(np.float32(len_2) / np.float32(len_2 - 1) * std_2)

    statistics, p_value = stats.ttest_ind_from_stats(mean1=mean_1, mean2=mean_2, std1=mod_std_1,
                                                     std2=mod_std_2, nobs1=len_1, nobs2=len_2)
    return statistics, p_value


def sep_data(data_dict, sep):
    group_1 = []
    group_2 = []

    for key in data_dict:
        num_str, weight_str = data_dict[key].split('_')
        if int(num_str) > sep:
            group_1.append(float(weight_str))
        else:
            group_2.append(float(weight_str))
    return group_1, group_2


def get_statis_data(options):
    import os
    from collections import defaultdict
    from random import random
    from jieba.analyse import extract_tags, textrank

    statis_data_option, statis_key_word_dict = options

    dir_path = '/Users/adhcczhang/Desktop/wechat_data_test'
    src_file_name = 'wechat_data_all_2'
    stop_word_file_name = 'stopword.txt'

    topic_word_dict = defaultdict(dict)
    if is_test:
        sample_rate = 0.01
    else:
        sample_rate = 1.00001
    stopword_dict = gen_stopword_dict(os.path.join(dir_path, stop_word_file_name))

    with open(os.path.join(dir_path, src_file_name)) as input_file:
        for index, line in enumerate(input_file):
            if random() > sample_rate:
                continue
            line_list = line.strip().split('\t')
            if len(line_list) < 9:
                continue
            try:
                if statis_data_option == "1":
                    statis_data = int(line_list[7])
                elif statis_data_option == "2":
                    statis_data = int(line_list[8])
                else:
                    statis_data = 1
                text = line_list[analysis_index]
                if text == "None":
                    continue
                temp_dict = {}
                for key_word, weight in extract_tags(text, topK=3, withWeight=True, allowPOS=()):
                    if key_word in stopword_dict:
                        continue
                    temp_dict[key_word] = str(statis_data) + '_' + str(round(weight, 2))
                for statis_key_word in statis_key_word_dict:
                    if statis_key_word not in topic_word_dict:
                        topic_word_dict[statis_key_word] = {}
                    if statis_key_word in temp_dict:
                        topic_word_dict[statis_key_word][index] = temp_dict[statis_key_word]
                    else:
                        topic_word_dict[statis_key_word][index] = str(statis_data) + '_' + str(round(0, 2))
            except Exception as e:
                # print(e)
                continue
        return topic_word_dict


def get_top_word(options):
    import os
    from collections import defaultdict
    from random import random
    from jieba.analyse import extract_tags, textrank

    statis_data_option = options

    dir_path = '/Users/adhcczhang/Desktop/wechat_data_test'
    src_file_name = 'wechat_data_all_2'
    stop_word_file_name = 'stopword.txt'

    topic_word_dict = defaultdict(int)
    if is_test:
        sample_rate = 0.01
    else:
        sample_rate = 1.00001
    stopword_dict = gen_stopword_dict(os.path.join(dir_path, stop_word_file_name))

    with open(os.path.join(dir_path, src_file_name)) as input_file:
        for index, line in enumerate(input_file):
            if random() > sample_rate:
                continue
            line_list = line.strip().split('\t')
            if len(line_list) < 9:
                continue
            try:
                if statis_data_option == '1':
                    statis_data = int(line_list[7])
                elif statis_data_option == '2':
                    statis_data = int(line_list[8])
                else:
                    statis_data = 1
                # read_num = int(line_list[8])
                text = line_list[analysis_index]
                if text == "None":
                    continue
                for key_word, weight in extract_tags(text, topK=3, withWeight=True, allowPOS=()):
                    # topic_word_dict[key_word] += read_num
                    if key_word in stopword_dict:
                        continue
                    topic_word_dict[key_word] += statis_data
            except Exception as e:
                # print(e)
                continue

    topic_word_dict = sorted(topic_word_dict.items(), key=lambda x: x[1], reverse=False)
    return topic_word_dict
    # for item in topic_word_dict:
    #     print(item)


if __name__ == '__main__':
    import sys

    top_word_set = get_top_word('2')

    word_len = len(top_word_set)
    statis_key_word_dict = {}

    for i in range(word_len-1, word_len-20, -1):
        statis_data_option, statis_key_word, statis_key_freq = '1', top_word_set[i][0], top_word_set[i][1]
        statis_key_word_dict[statis_key_word] = statis_key_freq
    data_dict_dict = get_statis_data([statis_data_option, statis_key_word_dict])
    for key in statis_key_word_dict:
        statis_key_word, statis_key_freq = key, statis_key_word_dict[key]
        print('keyword: ' + statis_key_word + ' frequency: ' + str(statis_key_freq))
        data_dict = data_dict_dict[key]
        gini_index = cal_gini(data_dict)
        median = get_median(data_dict)
        group_1, group_2 = sep_data(data_dict, median)
        statistics, p_value = t_test(group_1, group_2)
        print('gini index: ' + str(gini_index) + ' statistics value: ' + str(statistics) + ' p_value: ' + str(p_value))
