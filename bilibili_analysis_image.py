# --coding:utf-8--

import os
import pickle
import multiprocessing as mp

class Bilibili_ai:
    def __init__(self):
        self.ai_url = "https://aip.baidubce.com/rest/2.0/image-classify/v2/advanced_general"
        self.access_token = self.gen_access_token()

    @staticmethod
    def gen_access_token():
        import requests
        from urllib import parse

        token_url = 'https://aip.baidubce.com/oauth/2.0/token'
        app_key = 'oA6GoGsozSKKMy5wFpIM1LaN'
        secret_key = 'kQce6NaUoIrGx4MfDUj1ySXQMtHUunMl'

        params = {
            'grant_type': 'client_credentials',
            'client_id': app_key,
            'client_secret': secret_key,
        }
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        r = requests.post(token_url, parse.urlencode(params).encode("utf-8"), headers=headers)
        return r.json()['access_token']

    def gen_baidu_response(self, img):
        import requests
        params = {"image": img}
        request_url = self.ai_url + "?access_token=" + self.access_token
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        response = requests.post(request_url, data=params, headers=headers)
        if response:
            return response
        #爱老公啾啾

    @staticmethod
    def to_base64(image_file):
        import base64

        res_string = base64.b64encode(image_file.read())
        return res_string

    @staticmethod
    def to_base64_path(image_file_path):
        import base64

        with open(image_file_path, 'rb') as image_file:
            res_string = base64.b64encode(image_file.read())
        return res_string

    def baidu_image(self, image_file):
        import json

        img_base64 = self.to_base64(image_file)
        res_data = {}
        try:
            resp = self.gen_baidu_response(img_base64)
            res_data = json.loads(resp.text)
        except Exception as e:
            print(e)
        return res_data

    def baidu_image_path(self, image_file_path):
        import json

        img_base64 = self.to_base64_path(image_file_path)
        res_data = {}
        try:
            resp = self.gen_baidu_response(img_base64)
            res_data = json.loads(resp.text)
        except Exception as e:
            print(e)
        return res_data

    def baidu_dir(self, src_path):
        from os import listdir
        from os.path import basename, isfile, exists
        import time

        result_id = basename(src_path)
        if exists(join(dest_dir_path, result_id+'.pkl')):
            return 0

        src_files = [join(src_path, f) for f in listdir(src_path) if isfile(join(src_path, f))]
        result_dict = {}
        for file_path in src_files:
            if file_path.startswith('.'):
                continue
            time.sleep(0.1)
            with open(file_path, 'rb') as image_file:
                try_num = 2
                image_id = basename(file_path)
                for i in range(try_num):
                    # result_data = self.baidu_image(image_file)
                    result_data = self.baidu_image_path(file_path)
                    if 'error_code' not in result_data:
                        result_dict[image_id] = result_data
                        i = try_num
                        if i > 0 and False:
                            print('success ' + file_path)
                    else:
                        # print(file_path)
                        time.sleep(2)
                        # print(i)
                if 'error_code' in result_data:
                    print(2)
                    print(result_data)
                    if result_data['error_code'] == 216200 and False:
                        print(1)
                # print(result_data)
        with open(join(dest_dir_path, result_id+'.pkl'), 'wb') as output_file:
            pickle.dump(result_dict, output_file)
        return 0


if __name__ == "__main__":
    from os import listdir, makedirs
    from os.path import join, isdir, exists
    src_dir_path = "/data/adhcczhang/bilibili/get_image_test"
    dest_dir_path = "/data/adhcczhang/bilibili/get_image_ai_result"
    if not exists(dest_dir_path):
        makedirs(dest_dir_path)
    ai_test = Bilibili_ai()
    dir_list = [join(src_dir_path, f) for f in listdir(src_dir_path) if isdir(join(src_dir_path, f))]
    # pool = mp.Pool(3)

    # res = pool.map(ai_test.baidu_dir, dir_list)
    # print(result_dict)
    for dir_path in dir_list:
        ai_test.baidu_dir(dir_path)







