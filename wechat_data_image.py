# --coding:utf-8--

import io
import time
import random
import string
import requests
import json
from urllib.parse import quote_plus
from urllib.parse import urlencode
from collections import defaultdict


def curlmd5(input):
    from hashlib import md5
    m = md5(input.encode('UTF-8'))
    return m.hexdigest().upper()


def get_reg_sign(image):
    from hashlib import md5
    APPID = "2126903099"
    APPKey = "MJLlwhPmkSKbVbtY"
    unix_time = str(int(time.time()))
    # nonce_str = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    param_dict = {
        'app_id': APPID,
        'image': image,
        'time_stamp': unix_time,
        'nonce_str': unix_time,
        'topk': "1",
    }
    temp_str = ""
    for key in sorted(param_dict.keys()):
        temp_str += '{}={}&'.format(key, quote_plus(str(param_dict[key]), safe=''))
    temp_str += 'app_key=' + APPKey
    # sorted_dict = sorted(param_dict.items(), key=lambda item: item[0], reverse=False)
    # sorted_dict.append(('app_key', APPKey))
    # sha = md5()
    # rawtext = urlencode(sorted_dict).encode()
    # sha.update(rawtext)
    # md5text = sha.hexdigest().upper()

    sign = curlmd5(temp_str)
    param_dict['sign'] = sign
    return param_dict


def do_http_post(url, param_dict):
    from urllib import parse
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    r = requests.post(url, parse.urlencode(param_dict).encode("utf-8"), headers=headers)
    return r


def to_base64(image_path):
    import base64
    from PIL import Image
    from os.path import exists

    jpg_path = image_path.split('.')[0] + '.jpg'
    if not exists(jpg_path):
        im = Image.open(image_path)
        im.save(jpg_path)

    with open(jpg_path, 'rb') as img_file:
        # res_string = base64.urlsafe_b64encode(img_file.read())
        res_string = base64.b64encode(img_file.read())
    return res_string


def is_png(path):
    from os.path import isfile
    if 'png' in path and isfile(path):
        return True
    else:
        return False


def gen_access_token():
    from urllib import parse
    app_key = 'oA6GoGsozSKKMy5wFpIM1LaN'
    secret_key = 'kQce6NaUoIrGx4MfDUj1ySXQMtHUunMl'

    url = 'https://aip.baidubce.com/oauth/2.0/token'
    params = {
        'grant_type': 'client_credentials',
        'client_id': app_key,
        'client_secret': secret_key,
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    r = requests.post(url, parse.urlencode(params).encode("utf-8"), headers=headers)
    return r


def qq_iamge():
    from os import listdir
    from os.path import join
    url = "https://api.ai.qq.com/fcgi-bin/vision/vision_scener"
    # url = "https://api.ai.qq.com/fcgi-bin/vision/vision_objectr"
    src_dir_path = '/Users/adhcczhang/Desktop/codes/webscrap/img'
    src_files = [join(src_dir_path, f) for f in listdir(src_dir_path) if is_png(join(src_dir_path, f))]

    for file_path in src_files:
        time.sleep(1)
        img_base64 = to_base64(file_path)
        param_dict = get_reg_sign(img_base64)
        print(param_dict['sign'])
        try:
            resp = do_http_post(url, param_dict)
            res_data = json.loads(resp.text)
        except Exception as e:
            print(e)
            continue
        print(res_data)


def gen_baidu_response(request_url, access_token, img):
    params = {"image": img}
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        return response


def baidu_image(access_token, url, src_dir_path):
    from os import listdir
    from os.path import join

    src_files = [join(src_dir_path, f) for f in listdir(src_dir_path) if is_png(join(src_dir_path, f))]

    for file_path in src_files:
        time.sleep(1)
        img_base64 = to_base64(file_path)
        try:
            resp = gen_baidu_response(url, access_token, img_base64)
            res_data = json.loads(resp.text)
        except Exception as e:
            print(e)
            continue
        print(res_data)


def get_result(input):
    import json
    result_dict = json.loads(input)
    return result_dict


if __name__ == '__main__':
    # main()
    r = gen_access_token()
    access_token = r.json()['access_token']
    # print(access_token)
    src_dir_path = '/Users/adhcczhang/Desktop/codes/webscrap/img'
    request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v2/advanced_general"
    # request_url = 'https://aip.baidubce.com/rest/2.0/image-classify/v1/object_detect'
    baidu_image(access_token, request_url, src_dir_path)
