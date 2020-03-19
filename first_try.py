from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
import os
import io
print("start...")

url_list = ["http://data.gdeltproject.org/events/index.html", "http://data.gdeltproject.org/gkg/index.html"]
data_url_list = ['http://data.gdeltproject.org/events/', 'http://data.gdeltproject.org/gkg/']
for index, url_str in enumerate(url_list):
    if index == 0:
         continue
    dest_dir_path = 'event_dir_' + str(index)

    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)

    html = urlopen(url_str).read().decode('utf-8')
    soup = BeautifulSoup(html, features='lxml')
    all_href = soup.find_all('a')
    href_list = [l['href'] for l in all_href]
    base_url = data_url_list[index]

    for i in range(0, len(href_list)):
    # for i in range(3, 10):
        href_str = href_list[i]
        get_url = base_url + href_str
        print(get_url)
        if os.path.exists(os.path.join(dest_dir_path, href_str)):
            continue
        r = requests.get(get_url)
        with open(os.path.join(dest_dir_path, href_str), 'wb') as f:
            f.write(r.content)
