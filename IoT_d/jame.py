from janome.tokenizer import Tokenizer
from janome.analyzer import Analyzer
from janome.tokenfilter import POSKeepFilter
import re
import collections
import os

f = open('data/it-life-hack/it-life-hack-6292880.txt', encoding='utf-8')
text = f.read()
print(text)
f.close()

t = Tokenizer()
for token in t.tokenize(text):
    print(token)

reg_text = re.sub(r'[0-9a-zA-Z]+','',text)
reg_text = re.sub(r'[:;/+\.-]+','',reg_text)
reg_text = re.sub(r'[\n\s]+','',reg_text)
print(reg_text)

token_filters = [POSKeepFilter(['名詞'])]
a = Analyzer(char_filters=[], tokenizer=t, token_filters=token_filters)

for token in a.analyze(reg_text):
    print(token)

text = []
for token in a.analyze(reg_text):
    text.append(token.surface) #表層型＝元の文章（単語）そのもの
#カスタマイズされた形態素解析器
c = collections.Counter(text)
print(c)

