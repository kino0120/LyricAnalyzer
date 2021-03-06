import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from time import sleep
import sys
import MeCab
import numpy as np
from PIL import Image
from sklearn.feature_extraction.text import TfidfVectorizer,CountVectorizer
import matplotlib.pyplot as plt

#二次元配列を生成する
def get_word_list(lyric):
    m = MeCab.Tagger("-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd")
    #m = MeCab.Tagger("Owackachi")
    lines = []
    keitaiso = []
    for sentence in lyric:
        keitaiso = []
        m.parse('')
        ttt = m.parseToNode(sentence)
        while ttt:
            #print(ttt.surface,ttt.feature)
            #辞書に形態素を入れていく
            tmp = {}
            tmp['surface'] = ttt.surface
            tmp['base'] = ttt.feature.split(',')[-3] #base
            tmp['pos'] = ttt.feature.split(',')[0] #pos
            tmp['pos1'] = ttt.feature.split(',')[1] #pos1
            #文頭、文末を表すBOS/EOSは省く
            if 'BOS/EOS' not in tmp['pos']:
                keitaiso.append(tmp)
            ttt = ttt.next
        lines.append(keitaiso)
    #baseが存在する場合baseを、そうでない場合surfaceをリストに格納する
    sentence_list = [] 
    for line in lines:
        #fit_transformに入れる際、単語間はスペースで連結
        word_list = ""
        for keitaiso in line:
            if (keitaiso['pos'] == '名詞') |\
                (keitaiso['pos'] == '動詞') |\
                (keitaiso['pos'] == '形容詞') :
                if not keitaiso['base'] == '*' :
                    #word_list.append(keitaiso['base'])
                    word_list += keitaiso['base'] + " "
                else: 
                    #word_list.append(keitaiso['surface'])
                    word_list += keitaiso['surface'] + " "
        #最後のスペースを削除
        word_list = word_list[:-1]
        sentence_list.append(word_list)
    return sentence_list

artist_df = pd.read_csv("music_lyric_list.csv",encoding="shift-jis")
#print(artist_df.Lyric[0].split("\u3000"))
lyrics = get_word_list(artist_df.Lyric[0].replace("\u3000","").split(","))
#lyrics = np.array(artist_df.Lyric)
#lyrics = np.array([])
#lyrics = np.append(lyrics,' '.join(get_word_list([artist_df.Lyric.tolist()])))
#print(get_word_list(artist_df.Lyric.tolist()))
#TF-IDFでベクトル化する
vectorizer = TfidfVectorizer(use_idf=True, token_pattern=u'(?u)\\b\\w+\\b',min_df=2)
vecs = vectorizer.fit_transform(lyrics)
vecs = vecs.toarray()
#numpy配列に変換
vecs = np.array(vecs)
vecs = np.mean(vecs, axis=0)
words_vectornumber = {}
for k,v in sorted(vectorizer.vocabulary_.items(), key=lambda x:x[1]):
    words_vectornumber[v] = k
#各アルバムの各単語のスコアリングをDataFrameにする
# vecs_array = vecs
# albums = []
words = vectorizer.get_feature_names()
df = pd.DataFrame({"word":words,"TF-IDF":vecs})
df = df.sort_values("TF-IDF",ascending=False)
print(df)


# 係り受け解析
from cabocha.analyzer import CaboChaAnalyzer
import CaboCha
# analyzer = CaboChaAnalyzer()
# tree = analyzer.parse("日本語の形態素解析はすごい")
# for chunk in tree:
#     for token in chunk:
#         print(token)
c = CaboCha.Parser()

for sentence in artist_df.Lyric[0].replace("\u3000","").split(","):
    # 視覚的にわかりやすいフォーマット
    print(c.parseToString(sentence))

    # プログラム的に処理しやすいフォーマット
    tree =  c.parse(sentence)
    #print(tree.toString(CaboCha.FORMAT_LATTICE))
    # 形態素を結合しつつ[{c:文節, to:係り先id}]の形に変換する
    chunks = []
    text = ""
    toChunkId = -1
    for i in range(0, tree.size()):
        token = tree.token(i)
        text = token.surface if token.chunk else (text + token.surface) 
        toChunkId = token.chunk.link if token.chunk else toChunkId
        # 文末かchunk内の最後の要素のタイミングで出力
        if i == tree.size() - 1 or tree.token(i+1).chunk:
            chunks.append({'c': text, 'to': toChunkId})

    # 係り元→係り先の形式で出力する
    for chunk in chunks:
        if chunk['to'] >= 0:
            print(chunk['c'] + " →　" + chunks[chunk['to']]['c'])
