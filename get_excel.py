# --coding:utf-8--

import os
import sys
import openpyxl


def get_diff_author(input_dict):
    res_dict = {}

    for key in input_dict:
        value = input_dict[key]
        if len(value):
            res_dict[author] = value
    return res_dict


def get_diff_article(date_condi, input_list):
    pre_list = []
    post_list = []
    for item in input_list:
        date_str, content = item.split("_&_*_")
        if date_str > date_condi:
            post_list.extend(item)
        else:
            pre_list.extend(item)


args = sys.argv
src_dir_path = args[1]
dir_list = os.listdir(src_dir_path)
author_dict = {}
for dir_name in dir_list:
    dir_path = os.path.join(src_dir_path, dir_name)
    file_list = os.listdir(dir_path)
    for file_name in file_list:
        file_path = os.path.join(dir_path, file_name)
        data = openpyxl.load_workbook(file_path)
        table = data.get_sheet_by_name('Sheet')
        nrows = table.rows
        ncols = table.columns
        for row in nrows:
            line = [col.value for col in row]  # 取值
            author = line[2]
            date = line[3]
            content = line[9]
            type = line[10]

            if author not in author_dict:
                author_dict[author] = [date+"_&_*_"+content]
            else:
                author_dict[author] = author_dict[author].extend(date+"_"+content)









