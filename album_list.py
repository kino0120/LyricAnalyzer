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
    sleep(1)
    html = requests.get(url)
    soup = BeautifulSoup(html.content, 'html.parser')
    return soup

artist_df = pd.read_csv("music_list.csv",index_col=False)

#各曲のページをスクレイピングする
contents_list = []
for i, url in artist_df.URL.iteritems():
    contents_list.append(scraping_web_page(url))
#歌詞、発売日、商品番号をdataframeに格納する
lyrics = []
sales_dates = []
cd_nums = []
for contents in contents_list:
    #lyrics.append(contents.find(id='kashi_area').text)
    lyrics.append(contents.find(id='kashi_area').get_text(','))
    #sales_dates.append(contents.find(id='view_amazon').text)
    #album_data = contents.find(id='view_amazon').text
    #print(album_data)
    #sales_dates.append(re.search(r'発売日：..........', album_data).group().replace("発売日：",""))
    #cd_nums.append(re.search(r'商品番号：.........', album_data).group().replace("商品番号：",""))
    #cd_nums.append(contents.find(id='view_amazon').text[19:28])
    #print(re.search(r'発売日：..........', album_data).group().replace("発売日：",""),re.search(r'商品番号：.........', album_data).group().replace("商品番号：",""))
artist_df["Lyric"] = ""
print(len(artist_df["Lyric"]))
print(len(lyrics))
artist_df["Lyric"] = lyrics
#artist_df['Sales_Date'] = sales_dates
#artist_df['CD_Number'] = cd_nums 

print(artist_df)
artist_df.to_csv("music_lyric_list.csv",encoding="shift-jis")