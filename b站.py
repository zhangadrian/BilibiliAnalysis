import requests
import json
import csv
import time

# 构建请求头
headers = {
    # 'Buvid': 'XZ512D1509193D98B13705F88F4266CFF9B32',
    'User-Agent': 'Mozilla/5.0 BiliDroid/5.40.0 (bbcallen@gmail.com)',
    # 'Device-ID': 'Lk16QnVEfRt_TnxEOEQ4DDgNPQw9Dzo',
    'Host': 'app.biliapi.net',
    'Connection': 'Keep-Alive',
    # 'Accept-Encoding': 'gzip',

}

# 声明一个列表存储字典
data_list = []


def start_spider():

    page = 1
    while True:
        time.sleep(1)
        url = 'https://app.biliapi.net/x/v2/region/show/child/list?appkey=1d8b6e7d45233436&build=5400000&channel=360' \
              '&mobi_app=android&order=view&platform=android&pn={}&ps=20&rid=33&tag_id=0'.format(page)
        page += 1
        resp = requests.get(url, headers=headers, verify=False)
        json_data = resp.json()

        # 先取出所需信息的键值对，下面是一个列表，列表存储的是我们所需要的信息
        datas = json_data.get('data')
        # 如果数据存在就抓取，否则就退出
        if datas:
            # 遍历
            for data in datas:
                # 标题
                title = data.get('title')
                # up主名字
                name = data.get('name')
                # 播放数
                play = data.get('play')
                # 评论数
                duration = data.get('duration')

                # 声明一个字典存储数据
                data_json = {}
                data_json['title'] = title
                data_json['name'] = name
                data_json['play'] = play
                data_json['duration'] = duration
                data_list.append(data_json)

                print(data_json)
        else:
            break


def main():

    start_spider()

    # 将数据写json文件
    with open('data_json.json', 'a+', encoding='utf-8-sig') as f:
        json.dump(data_list, f, ensure_ascii=False, indent=4)
    print('json文件写入完成')

    # 将数据写入csv文件
    with open('data_csv.csv', 'w', encoding='utf-8-sig', newline='') as f:
        # 表头
        title = data_list[0].keys()
        # 声明writer对象
        writer = csv.DictWriter(f, title)
        # 写入表头
        writer.writeheader()
        # 批量写入数据
        writer.writerows(data_list)
    print('csv文件写入完成')


if __name__ == '__main__':

    main()