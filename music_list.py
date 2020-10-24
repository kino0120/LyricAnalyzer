import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from time import sleep
import sys
import MeCab
import numpy as np
from PIL import Image
from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib.pyplot as plt

def scraping_web_page(url):
    sleep(5)
    html = requests.get(url)
    soup = BeautifulSoup(html.content, 'html.parser')
    return soup
#曲一覧ページをスクレイピングする
artist = "andymori"
soup = scraping_web_page('https://www.uta-net.com/search/?Aselect=1&Keyword=' + artist)
#htmlをパースして曲名、各曲URL、アーティスト名、作詞、作曲者名を取得する
contents = []
contents.append(soup.find_all(href=re.compile('/song/\d+/$')))
contents.append(soup.find_all(href=re.compile('/song/\d+/$')))
contents.append(soup.find_all(class_=re.compile('td2')))
contents.append(soup.find_all(class_=re.compile('td3')))
contents.append(soup.find_all(class_=re.compile('td4')))
infomations = []
for i, content in enumerate(contents):
    tmp_list = []
    for element in content:
        if i == 0:
            tmp_list.append(element.get('href'))
        else:
            tmp_list.append(element.string)
    infomations.append(tmp_list)
#DataFrameにする
artist_df = pd.DataFrame({
    'URL' : infomations[0],
    'SongName' : infomations[1],
    'Artist' : infomations[2],
    'Lyricist' : infomations[3],
    'Composer' : infomations[4]})
#URLにホストネームを付加
artist_df.URL = artist_df.URL.apply(lambda x : 'https://www.uta-net.com' + x)
#作曲者の名前の中で、uniqu数が最大の人のみのデータにする
main_lyricist = artist_df.Lyricist.value_counts().index[0]
artist_df = artist_df[artist_df.Lyricist==main_lyricist].reset_index(drop=True)
artist_df.to_csv("music_list.csv")

