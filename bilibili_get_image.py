# --coding:utf-8--

import os
import pickle
import multiprocessing as mp


def ffmpeg_get_frame(src_file_path, dest_file_path):
    cmd = './ffmpeg -i {} -r 0.1 -f image2 {}-%05d.jpg'.format(src_file_path, dest_file_path)
    os.system(cmd)
    return 0


def download_image(src_url, dest_file_path):
    from urllib.request import urlretrieve
    urlretrieve(src_url, dest_file_path)
    return 0


def extract_file(src_dir_path, dest_dir_path):
    import os
    print(src_dir_path)
    if os.path.exists(os.path.join(dest_dir_path, 'top.jpg')):
        return 0
    if len(os.listdir(src_dir_path)) == 0:
        return 0
    try:
        src_video_dir = os.path.join(src_dir_path, [dir_path for dir_path in os.listdir(src_dir_path) if
                                                    os.path.isdir(os.path.join(src_dir_path, dir_path))][0])
        new_src_video_dir = src_video_dir.replace(' ', '')
        os.rename(src_video_dir, new_src_video_dir)
        src_video_dir = os.path.join(new_src_video_dir, [dir_path for dir_path in os.listdir(new_src_video_dir) if
                                                         os.path.isdir(os.path.join(new_src_video_dir, dir_path))][0])
        new_src_video_dir = src_video_dir.replace(' ', '')
        os.rename(src_video_dir, new_src_video_dir)
        src_video_dir = new_src_video_dir
        for index, video_file_path in enumerate(os.listdir(src_video_dir)):
            src_video_file_path = os.path.join(src_video_dir, video_file_path)
            new_src_video_file_path = src_video_file_path.replace(' ', '')
            os.rename(src_video_file_path, new_src_video_file_path)
            src_video_file_path = new_src_video_file_path
            dest_video_file_path = os.path.join(dest_dir_path, str(index))
            ffmpeg_get_frame(src_video_file_path, dest_video_file_path)
        src_info_file_path = os.path.join(src_dir_path, [file_path for file_path in os.listdir(src_dir_path) if
                                                os.path.isfile(os.path.join(src_dir_path, file_path.replace(' ', '')))][-1])
        with open(src_info_file_path, 'rb') as src_info_file:
            info_list = pickle.load(src_info_file)
            top_image_url = info_list[-1]['pic']
            download_image(top_image_url, os.path.join(dest_dir_path, 'top.jpg'))
    except Exception as e:
        print(src_video_file_path)
        print(e)
        return 0



def get_file_list(dir_item):
    if dir_item.startswith('.'):
        return 0
    dest_extract_dir_path = os.path.join(dest_dir_path, dir_item)
    if not os.path.exists(dest_extract_dir_path):
        os.makedirs(dest_extract_dir_path)
    src_extract_dir_path = os.path.join(dir_path, dir_item)
    extract_file(src_extract_dir_path, dest_extract_dir_path)


if __name__ == "__main__":
    dir_path = '/data/adhcczhang/bilibili/抗击肺炎大作战'
    dest_dir_path = '/data/adhcczhang/bilibili/get_image_test'
    pool = mp.Pool(8)
    if not os.path.exists(dest_dir_path):
        os.makedirs(dest_dir_path)
    dir_item_list = os.listdir(dir_path)
    # for dir_item in dir_item_list:
    #     get_file_list(dir_item)
    res = pool.map(get_file_list, dir_item_list)
