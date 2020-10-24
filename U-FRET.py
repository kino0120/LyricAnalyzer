import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from time import sleep
import sys
import matplotlib.pyplot as plt
from selenium import webdriver
import chromedriver_binary
import os

#アーティスト入力
artist = "andymori"
# アクセスするURL
TARGET_URL ='https://www.ufret.jp/search.php?key=' + artist

# 各動作間の待ち時間（秒）
INTERVAL = 3

# ブラウザ起動
driver = webdriver.Chrome()
driver.maximize_window()
sleep(INTERVAL)
driver.get(TARGET_URL)
url_list= []
sleep(INTERVAL)
#music_list = driver.find_elements_by_tag_name("a")
urls = driver.find_elements_by_css_selector(".list-group-item.list-group-item-action")
#music_list = driver.find_elements_by_class_name("group-item-action")
#music_list = driver.find_elements_by_partial_link_text('/song')
for url in urls:
    url = url.get_attribute("href")
    if type(url) is str:
        if "song." in url:
            url_list.append(url)
            print(url)

for url in url_list[:2]:
    driver.get(url)
    sleep(10)
    chord_list = driver.find_elements_by_tag_name("rt")
    for chord in chord_list:
        chord = chord.text
        print(chord)





#曲一覧ページをスクレイピングする
#artist = "andymori"
#soup = scraping_web_page('https://www.ufret.jp/search.php?key=' + artist)

url_list= []
for elem in soup.find_all(href=re.compile('/song.+')):
    url = elem.get('href')
    url_list.append(url)
    print(url)

for url in url_list:
    print('aaa')
    print(url)
    print('https://www.ufret.jp' + url)
    soup = scraping_web_page('https://www.ufret.jp' + url)
    #n1 = soup.find(class_=re.compile('row'))
    #n1 = soup.find_all('div',class_="row")[8]#.find_all('div',class_="row")[-1]#.find_all('div',class_= "col-lg-9")
    #n1 = soup.find('div',class_="col-lg-9",id="mt-3 musical-sheet")#.find('div',id="my-chord-data")
    #my-chord-data > div:nth-child(1) > p:nth-child(1) > span.krijcheug > ruby > rt
    n1 = soup.select('#my-chord-data')
    #print(len(n1))
    #my-chord-data > div:nth-child(2) > p:nth-child(1)
    print(n1)
    #for n2 in n1:
    #    print('b')ß
        #print(n2)
    #for n2 in n1:
    #    print(n2)
    #n1 = soup.find_all(class_=re.compile('chord'))
    #.find(class_=re.compile('col-lg-9'))
    #.find(class_=re.compile('my-chord-data'))
    #print(n1)
    # for n2 in n1:
    #     print(n2)
    #     #chord_list = soup.find(id=re.compile('krijcheug'))
    #     n3 = n2.find_all(class_=re.compile('col-lg-9'))
    #     print(n3)