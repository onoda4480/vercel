import os
import re
from janome.tokenizer import Tokenizer
from janome.analyzer import Analyzer
from janome.tokenfilter import POSKeepFilter
import pandas as pd
import numpy as np
from keras.preprocessing import sequence
import itertools
from collections import Counter

dirs = ['it-life-hack', 'movie-enter']
wakati = []
label = []    # ITライフハック or 映画エンターテイメントのラベル
t = Tokenizer(wakati=True)

# ITライフハックと映画エンターテイメントのディレクトリを処理する
for i, d in enumerate(dirs):
    files = os.listdir('./data/' + d)

    for file in files:
        f = open('./data/' + d + '/' + file, 'r', encoding='utf-8')
        text = f.read()

        reg_text = re.sub(r'[0-9a-zA-Z]+', '', text)    # 英数字の除去
        reg_text = re.sub(r'[:;/+\.-]', '', reg_text)   # 特殊文字の除去
        reg_text = re.sub(r'[\s\n]', '', reg_text)      # 空白文字の除去

        wakati.append(t.tokenize(reg_text))
        label.append(i)
        f.close()

# 処理結果の出力
print(len(wakati))
print(list(wakati[0]))
print(label[0])

word_freq = Counter(itertools.chain(*wakati))

dic = []
for word_uniq in word_freq.most_common():
    dic.append(word_uniq[0])

print(len(dic))
print(dic)

# =======================================================
# 辞書の作成および単語のID割り当て
# =======================================================
dic_inv = {}
for i, word_uniq in enumerate(dic, start=1):
    dic_inv.update({word_uniq: i})

print(len(dic_inv))
print(dic_inv)

# ==============================================
# wakatiをIDに変換
# ==============================================
wakati_id = [[dic_inv[word] for word in waka] for waka in wakati]
print(len(wakati_id))
print(list(wakati_id[0]))

# 不足していたコードを追加
wakati_id = sequence.pad_sequences(wakati_id, maxlen=3382)
print(list(wakati_id[0]))
