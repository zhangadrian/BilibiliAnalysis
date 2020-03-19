# --coding:utf-8--

from bs4 import BeautifulSoup
from urllib.request import urlopen, urlretrieve
import pickle
import multiprocessing as mp
import time


class Bilibili:
    def __init__(self):
        self.headers = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cookie': 'finger=edc6ecda; LIVE_BUVID=AUTO1415378023816310; stardustvideo=1; CURRENT_FNVAL=8; buvid3=0D8F3D74-987D-442D-99CF-42BC9A967709149017infoc; rpdid=olwimklsiidoskmqwipww; fts=1537803390'

        }
        self.danmu_url = 'https://api.bilibili.com/x/v1/dm/list.so?oid='
        self.comment_url = 'https://api.bilibili.com/x/v2/reply?type=1&oid='
        self.info_url = 'http://api.bilibili.com/archive_stat/stat?aid='
        self.data_url = "http://api.bilibili.com/x/web-interface/view?aid="
        self.video_url = 'https://www.bilibili.com/video/av'

    def download_data(self, oid):
        import json
        from time import sleep
        url = self.data_url + str(oid)
        try:
            sleep(10)
            html = urlopen(url)
            data = html.read()
            soup = BeautifulSoup(data, features="html.parser")
            text = soup.text
            json_dict = json.loads(text)
            if json_dict['code'] == 0:
                print(json_dict['data'])
        except Exception as e:
            print(e)

    def download_comment(self, oid):
        import requests
        import json
        import time

        url = self.comment_url + str(oid)
        # video_url = self.video_url + str(oid)
        # video_url = 'https://www.bilibili.com/video/av84955633?spm_id_from=333.5.b_646f7567615f6d6164.21'
        comment_res = []
        try:
            res = requests.get(url, headers=self.headers)
            res.raise_for_status()
            soup = BeautifulSoup(res.text, features='html.parser')
            # page_num = soup.find('div', attrs={'class', 'page-jump'})
            # print(page_num)
            text = soup.text
            text_dict = json.loads(text)
            if 'data' not in text_dict:
                return comment_res
            if 'page' not in text_dict['data']:
                return comment_res
            if 'count' not in text_dict['data']['page']:
                return comment_res
            total_comment_num = text_dict['data']['page']['count']
            comment_page_num = int(total_comment_num/20) + 1

            for i in range(1, comment_page_num+1):
                time.sleep(0.1)
                url = self.comment_url + str(oid) + '&pn=' + str(i)
                res = requests.get(url, headers=self.headers)
                res.raise_for_status()
                soup = BeautifulSoup(res.text, features='html.parser')
                text = soup.text
                text_dict = json.loads(text)

                if 'data' not in text_dict:
                    continue
                if 'replies' not in text_dict['data']:
                    continue
                replies = text_dict['data']['replies']
                if not replies:
                    continue
                for reply in replies:
                    reply_dict = {
                        'user_name': reply['member']['uname'],
                        'user_sex': reply['member']['sex'],
                        'reply_ctime': reply['ctime'],
                        'reply_content': reply['content']['message'],
                        'reply_like': reply['like'],
                    }

                    comment_res.append(reply_dict)

                    if reply['rcount'] > 0:
                        for rreply in reply['replies']:
                            reply_dict = {
                                'user_name': rreply['member']['uname'],
                                'user_sex': rreply['member']['sex'],
                                'reply_ctime': rreply['ctime'],
                                'reply_content': rreply['content']['message'],
                                'reply_like': rreply['like'],
                            }
                            comment_res.append(reply_dict)
            # print(comment_res)
            return comment_res
            # print(comment_res)
            # print(comment_page_num)
            # print(res.text)
        except requests.HTTPError as e:
            print(e)
            print('http error')
        except requests.RequestException as e:
            print(e)
            print('request error')
        except Exception as e:
            print(replies)
            print(e)
            print(oid + 'download_comment Unknown error')

    def download_danmu(self, oid):
        import requests
        import re

        # url = self.danmu_url + str(oid)
        page_url = self.video_url + str(oid) + '/'
        res_list = []
        try:
            time.sleep(0.1)
            page_res = requests.get(page_url, headers=self.headers)
            soup = BeautifulSoup(page_res.text, features='html.parser')
            text = soup.text
            cid = re.findall(r"\"pages\"\:\[\{\"cid\":(.*?)\,", text, re.S)[0]
            url = self.danmu_url + str(cid)
            res = requests.get(url, headers=self.headers)
            res.encoding = 'utf8'
            bs = BeautifulSoup(res.text, features='html.parser')
            # with open('text.txt', 'w') as input_file:
            #     input_file.write(res.text)
            # print(res.text.encode('gb18030'))
            for tag in bs.find_all(name='d'):
                res_list.append(tag.attrs['p'] + '\t&&&\t' + tag.text)
            # print(res_list)
            return res_list
        except requests.HTTPError as e:
            print(e)
            print('http error')
        except requests.RequestException as e:
            print(e)
            print('request error')
        except Exception as e:
            print(e)
            print('download_danmu Unknown error')

    def download_info(self, oid):
        import requests
        import json
        import time

        url = self.info_url + str(oid)
        try:
            time.sleep(0.1)
            res = requests.get(url, headers=self.headers)
            res.raise_for_status()
            soup = BeautifulSoup(res.text, features='html.parser')
            # page_num = soup.find('div', attrs={'class', 'page-jump'})
            # print(page_num)
            text = soup.text
            text_dict = json.loads(text)
            # print(text_dict)
            return text_dict

        except requests.HTTPError as e:
            print(e)
            print('http error')
        except requests.RequestException as e:
            print(e)
            print('request error')
        except Exception as e:
            print(e)
            print('download_info Unknown error')

    def download_video(self, oid, quality, oid_dir_path):
        import requests, hashlib, urllib.request, re
        import os
        import sys

        def get_playlist(video_url, cid, quality):
            time.sleep(0.1)
            entropy = 'rbMCKn@KuamXWlPMoJGsKcbiJKUfkPF_8dABscJntvqhRSETg'
            appkey, sec = ''.join([chr(ord(i)+2) for i in entropy[::-1]]).split(':')
            params = 'appkey=%s&cid=%s&otype=json&qn=%s&quality=%s&type=' % (appkey, cid, quality, quality)
            chksum = hashlib.md5(bytes(params + sec, 'utf8')).hexdigest()
            url_api = 'https://interface.bilibili.com/v2/playurl?%s&sign=%s' % (params, chksum)
            headers = {
                'Referer': video_url,  # 注意加上referer
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
            }

            html = requests.get(url_api, headers=headers).json()
            video_list = [html['durl'][0]['url']]
            # print(video_list)
            return video_list

        def get_video(video_list, title, start_url, page):
            time.sleep(0.1)
            num = 1
            print('[正在下载P{}段视频,请稍等...]:'.format(page) + title)
            # currentVideoPath = os.path.join(sys.path[0], 'bilibili_video', title)  # 当前目录作为下载目录
            currentVideoPath = os.path.join(oid_dir_path, 'bilibili_video', title)
            for i in video_list:
                opener = urllib.request.build_opener()
                # 请求头
                opener.addheaders = [
                    # ('Host', 'upos-hz-mirrorks3.acgvideo.com'),  #注意修改host,不用也行
                    (
                    'User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:56.0) Gecko/20100101 Firefox/56.0'),
                    ('Accept', '*/*'),
                    ('Accept-Language', 'en-US,en;q=0.5'),
                    ('Accept-Encoding', 'gzip, deflate, br'),
                    ('Range', 'bytes=0-'),  # Range 的值要为 bytes=0- 才能下载完整视频
                    ('Referer', start_url),  # 注意修改referer,必须要加的!
                    ('Origin', 'https://www.bilibili.com'),
                    ('Connection', 'keep-alive'),
                ]
                urllib.request.install_opener(opener)
                # 创建文件夹存放下载的视频
                if not os.path.exists(currentVideoPath):
                    os.makedirs(currentVideoPath)
                # 开始下载
                if len(video_list) > 1:
                    urllib.request.urlretrieve(url=i,
                                               filename=os.path.join(currentVideoPath, r'{}-{}.flv'.format(title, num)))  # 写成mp4也行  title + '-' + num + '.flv'
                else:
                    urllib.request.urlretrieve(url=i, filename=os.path.join(currentVideoPath, r'{}_1.flv'.format(title)))  # 写成mp4也行  title + '-' + num + '.flv'
                num += 1


        video_url = 'https://api.bilibili.com/x/web-interface/view?aid='+oid
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/55.0.2883.87 Safari/537.36'
        }
        # print(video_url)
        html = requests.get(video_url, headers=headers).json()
        data = html['data']
        mid = data['owner']['mid']
        cid_list = data['pages']
        for item in cid_list:
            print(item)
            cid = str(item['cid'])
            title = item['part']
            title = re.sub(r'[\/\\:*?"<>|]', '', title)

            page = str(item['page'])
            video_url = video_url + "/?p=" + page

            video_list = get_playlist(video_url, cid, quality)
            get_video(video_list, title, video_url, page)
        return data

    def download_search_list(self, search_word):
        import requests
        import re
        import time

        init_url = 'https://search.bilibili.com/all?keyword={}&from_source=nav_search&page='.format(search_word)
        order_list = ['&order=totalrank', '&order=click', '&order=pubdate', '&order=dm', '&order=stow']
        page_num = 50
        oid_list = []
        try:
            for i in range(1, page_num+1):
                for j in range(0, len(order_list)):
                    time.sleep(0.1)
                    url = init_url + str(i) + order_list[j]
                    res = requests.get(url, headers=self.headers)
                    res.raise_for_status()
                    soup = BeautifulSoup(res.text, features='html.parser')
                    search_list = soup.find(name="ul", attrs={"class": "video-list clearfix"})
                    if not search_list:
                        continue
                    # video_item_list = search_list.fina_all(name='li', attrs={"class": "video-item matrix"})
                    for video_item in search_list:
                        video_url = video_item.find(name='a').attrs['href']
                        video_oid = re.findall(r"av(.*?)\?", video_url)
                        oid_list.extend(video_oid)
            oid_list = list(set(oid_list))
            # print(oid_list)
            return oid_list

        except requests.HTTPError as e:
            print(e)
            print('http error')
        except requests.RequestException as e:
            print(e)
            print('request error')
        except Exception as e:
            print(e)
            print(' Unknown error')

    def download_user_info(self, mid):
        import requests
        import json
        import time

        user_stat = 'https://api.bilibili.com/x/space/upstat?mid={}'.format(mid)
        user_info = 'https://api.bilibili.com/x/space/acc/info?mid={}'.format(mid)
        user_power = 'https://elec.bilibili.com/api/query.rank.do?mid={}'.format(mid)
        user_relation = 'https://api.bilibili.com/x/relation/stat?vmid={}'.format(mid)
        user_video = 'https://api.bilibili.com/x/space/navnum?mid={}'.format(mid)
        info_dict = {}
        try:
            time.sleep(0.1)
            url = user_stat
            res = requests.get(url, headers=self.headers)
            res.raise_for_status()
            soup = BeautifulSoup(res.text, features='html.parser')
            text = soup.text
            text_dict = json.loads(text)
            info_dict['total_view'] = text_dict['data']['archive']['view']
            info_dict['total_like'] = text_dict['data']['likes']

            url = user_info
            res = requests.get(url, headers=self.headers)
            res.raise_for_status()
            soup = BeautifulSoup(res.text, features='html.parser')
            text = soup.text
            text_dict = json.loads(text)
            info_dict['name'] = text_dict['data']['name']
            info_dict['sex'] = text_dict['data']['sex']
            info_dict['face'] = text_dict['data']['face']
            info_dict['sign'] = text_dict['data']['sign']
            info_dict['rank'] = text_dict['data']['rank']
            info_dict['level'] = text_dict['data']['level']
            if 'official' in text_dict['data']:
                info_dict['official'] = text_dict['data']['official']

            url = user_relation
            res = requests.get(url, headers=self.headers)
            res.raise_for_status()
            soup = BeautifulSoup(res.text, features='html.parser')
            text = soup.text
            text_dict = json.loads(text)
            info_dict['following'] = text_dict['data']['following']
            info_dict['follower'] = text_dict['data']['follower']

            url = user_power
            res = requests.get(url, headers=self.headers)
            res.raise_for_status()
            soup = BeautifulSoup(res.text, features='html.parser')
            text = soup.text
            text_dict = json.loads(text)
            if 'data' in text_dict:
                info_dict['power_number'] = text_dict['data']['count']
                info_dict['power_count'] = text_dict['data']['total_count']

            url = user_video
            res = requests.get(url, headers=self.headers)
            res.raise_for_status()
            soup = BeautifulSoup(res.text, features='html.parser')
            text = soup.text
            text_dict = json.loads(text)
            info_dict['video_num'] = text_dict['data']['video']
            return info_dict

        except requests.HTTPError as e:
            print(e)
            print('http error')
        except requests.RequestException as e:
            print(e)
            print('request error')
        except Exception as e:
            print(e)
            print('Unknown error')


def bilibili_data_downloader(oid):
    b_class = Bilibili()
    oid_dir_path = os.path.join(dir_path, oid)
    if not os.path.exists(oid_dir_path):
        os.makedirs(oid_dir_path)
    data_file_path = oid_dir_path + '/' + oid + '.pkl'
    if os.path.exists(data_file_path):
        return 0
    comment_dict = b_class.download_comment(oid)
    danmu_list = b_class.download_danmu(oid)
    info_dict = b_class.download_info(oid)
    video_info = b_class.download_video(oid, '15', oid_dir_path)
    user_info = b_class.download_user_info(video_info['owner']['mid'])
    data_file = open(data_file_path, 'wb')
    pickle.dump([comment_dict, danmu_list, info_dict, user_info, video_info], data_file)


if __name__ == "__main__":
    import os
    # av_list = list(range(1000000, 1500000))
    # # print(url_path_list)
    # # for i in range(3, 1000):
    # #     download_data(i)
    # pool = mp.Pool(10)
    # res = pool.map(download_data, av_list)
    b_test = Bilibili()
    # oid = '84941209'
    oid = '84442591'
    mid_test = '51896064'

    search_word_love = '小盐的甜罐'
    search_word = '抗击肺炎大作战'

    # oid_list_love = b_test.download_search_list(search_word_love)

    oid_list = b_test.download_search_list(search_word)

    dir_path = './' + search_word

    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    pool = mp.Pool(8)
    res = pool.map(bilibili_data_downloader, oid_list)


    # for index, oid in enumerate(oid_list):
    #
    #     oid_dir_path = os.path.join(dir_path, oid)
    #     if not os.path.exists(oid_dir_path):
    #         os.makedirs(oid_dir_path)
    #     data_file_path = oid_dir_path + '/' + oid + '.pkl'
    #     if os.path.exists(data_file_path):
    #         continue
    #     comment_dict = b_test.download_comment(oid)
    #     danmu_list = b_test.download_danmu(oid)
    #     info_dict = b_test.download_info(oid)
    #     mid = b_test.download_video(oid, '15')
    #     user_info = b_test.download_user_info(mid)
    #     data_file = open(data_file_path, 'wb')
    #     pickle.dump([comment_dict, danmu_list, info_dict, user_info], data_file)
    #     print('number of video:' + str(index + 1))
