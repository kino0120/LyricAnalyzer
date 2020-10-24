import torch
from transformers.modeling_bert import BertModel
from transformers.tokenization_bert_japanese import BertJapaneseTokenizer

# 分かち書きをするtokenizerです
tokenizer = BertJapaneseTokenizer.from_pretrained('bert-base-japanese-whole-word-masking')

# BERTの日本語学習済みパラメータのモデルです
model = BertModel.from_pretrained('bert-base-japanese-whole-word-masking')
print(model)