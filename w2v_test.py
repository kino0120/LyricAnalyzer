import gensim
import gensim.models.word2vec as wv
#model = gensim.models.KeyedVectors.load_word2vec_format('word2vec_model/vector_neologd.vec', binary=True)
model = gensim.models.KeyedVectors.load_word2vec_format('word2vec_model/entity_vector.bin', binary=True)
#print(len(model.wv["愛"]))
#print(model.wv["愛"])

w1 = "美味しい"
print(model.wv.similarity(w1=w1, w2="嬉しい"))
print(model.wv.similarity(w1=w1, w2="悲しい"))
print(model.wv.similarity(w1=w1, w2="怒る"))
print(model.wv.similarity(w1=w1, w2="驚く"))
print(model.wv.similarity(w1=w1, w2="恐れる"))
print(model.wv.similarity(w1=w1, w2="嫌う"))