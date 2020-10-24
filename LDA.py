from gensim import corpora,models
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

df = pd.read_csv("neologd.csv",encoding="shift-jis")
df = df.set_index(df.columns[0])
text_list = df.iloc[:,0].tolist()
dictionary =corpora.Dictionary([text_list])

corpus=[dictionary.doc2bow(tokens) for tokens in [text_list]]

#トピック数の設定
zk=10
#モデルの学習
model = models.LdaModel(corpus,num_topics=zk,id2word=dictionary,random_state=2020)
model.save('lda_bz.model')

#各曲の各トピックへの所属確率の算出。(曲数×トピック数)のnumpy
Prob_songs=np.array(model.get_document_topics(corpus,minimum_probability=0))[:,:,1]

#DataFrameに収納
L=[ z for z in range(1,zk+1)]
col_name=list(map(lambda x: "Prob_"+str(x),L))
df_prob=pd.DataFrame(Prob_songs)
df_prob.columns=col_name

#所属確率最大のトピック番号も算出
df_prob["Max"]=df_prob.idxmax(axis=1)
def del_Prob(x):
    return int(x.split("_")[1])
df_prob["Max"]=df_prob["Max"].apply(lambda x : del_Prob(x))

#各トピックの出現確率の算出。曲のトピックへの所属確率を全曲で足して、全トピックで1になるように正規化
df_topic=pd.DataFrame(df_prob.drop("Max",axis=1).sum()/df_prob.drop("Max",axis=1).sum().sum())
df_topic.columns=["Prob"]
df_topic["Topic"]=[ z for z in range(1,zk+1)]

#可視化
plt.figure(figsize = (30,20))
ax= sns.barplot(x="Topic",y="Prob",data=df_topic,color="darkblue")
ax.set_xlabel("Topic",fontsize=50)
ax.set_ylabel("Prob",fontsize=50)
ax.tick_params(axis='x', labelsize=40)
ax.tick_params(axis='y', labelsize=40)
plt.savefig("LDA.jpg")


topic_word_prob=[]

for z in range(zk):
    word=[]
    prob=[]
    topic = model.show_topic(z,1000) #適当な単語数分

    for t in topic:
        word.append(t[0])
        prob.append(t[1])
        
    df_lda=pd.DataFrame({"word":word,"prob":prob})
    topic_word_prob.append(df_lda)

print(topic_word_prob)
