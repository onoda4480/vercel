import os
import re
from janome.tokenizer import Tokenizer
from janome.analyzer import Analyzer
from janome.tokenfilter import POSKeepFilter
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer

dirs = ['it-life-hack', 'movie-enter']
docterm = []
label = []
tmp1 = []
tmp2 = ''

# 名詞のみの配列を作る
t = Tokenizer()
token_filters = [POSKeepFilter(['名詞'])]
a = Analyzer(token_filters=token_filters)

# IT，Movieの各ディレクトリに対し，処理を行う
for i, d in enumerate(dirs):
    files = os.listdir("./data/" + d + "/")
    
    for file in files:
        f = open("./data/" + d + "/" + file, 'r', encoding='utf-8')
        text = f.read()
        #print(text)
        reg_text = re.sub(r'[0-9a-zA-Z]+', '', text)  # 英数字を除去
        reg_text = re.sub(r'[:;/+\.-]+', '', reg_text)  # ：；などを除去（講義中に実施したもの）
        reg_text = re.sub(r'[\n\s]+', '', reg_text)  # 改行、空白文字を除去

        for token in a.analyze(reg_text):
            tmp1.append(token.surface)
            tmp2 = ' '.join(tmp1)
        docterm.append(tmp2)  # doctermにtmp2を追加
        tmp1 = []

        label.append(i)
        f.close()

# 結果の表示
#df = pd.DataFrame(docterm)
#print(df.head())
#print(df.tail())


cv = CountVectorizer()
docterm_cv = cv.fit_transform(np.array(docterm)) # 単語出現回数カウント
docterm_cnt = docterm_cv.toarray() # 行列に変換
df = pd.DataFrame(docterm_cnt)
print(pd.DataFrame(docterm_cnt).shape)
print(cv.get_feature_names_out()[0:50])

cv = CountVectorizer(min_df=0.01, max_df=0.5)
docterm_cv = cv.fit_transform(np.array(docterm))
docterm_cnt = docterm_cv.toarray()
df = pd.DataFrame(docterm_cnt)
print(docterm_cnt.shape) # (400, 2834) → 7,613単語カット
print(df)

tv = TfidfVectorizer(min_df=0.01,max_df=0.5,sublinear_tf=True)
docterm_tv = tv.fit


t = Tokenizer(wakati=True)

print(len(wakati))
print(wakati[0])
print(label[0])