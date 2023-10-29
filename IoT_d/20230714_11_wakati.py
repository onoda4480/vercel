import os
import re
from janome.tokenizer import Tokenizer
from janome.analyzer import Analyzer
from janome.tokenfilter import POSKeepFilter
import pandas as pd
import numpy as np
import itertools
from collections import Counter
from tensorflow.keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers import Embedding, LSTM, Dense
import matplotlib.pyplot as plt

dirs = ['it-life-hack', 'movie-enter']
tmp = []
wakati = []
label = []    # IT記事 or 映画記事のラベル
t = Tokenizer()
token_filters = [POSKeepFilter(['名詞'])]
a = Analyzer(char_filters=[], tokenizer=t, token_filters=token_filters)
# IT，Movieの各ディレクトリに対し，処理を行う
for i, d in enumerate(dirs):
  files = os.listdir('./data/' + d)

  for file in files:
    f = open('./data/' + d + '/' + file, 'r', encoding='utf-8')
    text = f.read()

    reg_text = re.sub(r'[0-9a-zA-Z]+', '', text)    # 英数字の除去
    reg_text = re.sub(r'[:;/+\.-]', '', reg_text)   # 記号の除去
    reg_text = re.sub(r'[\s\n]', '', reg_text)      # 空白文字，改行の除去

    wakati_test = []
    for token in a.analyze(reg_text):
        wakati.append(token.surface)
    wakati.append(tmp)

    
    #for token in a.analyze(reg_text):
    #    tmp.append(token.surface)
    #wakati.append(tmp)
    #tmp = []
    
    #label.append(i)
    f.close()

word_freq = Counter(itertools.chain(* wakati))
dic = []
for word_uniq in word_freq.most_common():
  dic.append(word_uniq[0])
dic_inv = {}
for i, word_uniq in enumerate(dic, start=1):
  dic_inv.update({word_uniq: i})
wakati_id = [[dic_inv[word] for word in waka] for waka in wakati]

wakati_test_id = []
for word in wakati_test:
  if word in dic_inv:
    wakati_test_id.append(dic_inv[word])

wakati_id = sequence.pad_sequences(np.array(wakati_id), dtype=np.int32, maxlen=399)

label = np.array(label)
wakati_id
#ここまでが前処理,ここからがLSTM

model = Sequential()
model.add(Embedding(11540, 512, input_length=399)) # 埋め込み層（入力単語数 11540ノード，出力512ノード）
model.add(LSTM(128, dropout=0.5))                  # LSTMブロック
model.add(Dense(1, activation='sigmoid')) # 出力はIT or 映画の1ノード

model.summary()
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
hist = model.fit(np.array(wakati_id, dtype=np.int32), label, batch_size=32, verbose=1, 
                 epochs=30, validation_split=0.2)

f = open('./data/test_movie.txt','r', encoding='utf-8')
text = f.read()

reg_text = re.sub(r'[0-9a-zA-Z]+', '', text)    # 英数字の除去
reg_text = re.sub(r'[:;/+\.-]', '', reg_text)   # 記号の除去
reg_text = re.sub(r'[\s\n]', '', reg_text)      # 空白文字，改行の除去

wakati_test = []
for token in a.analyze(reg_text):
    wakati_test.append(token.surface)
    #wakati.append(tmp)
f.close()


plt.plot(hist.history['loss'])
plt.plot(hist.history['val_loss'])
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'val'], loc='upper right')
plt.show()

plt.plot(hist.history['accuracy'])
plt.plot(hist.history['val_accuracy'])
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'val'], loc='upper left')
plt.show()
predictions = model.predict(np.array(wakati_id, dtype=np.int32))
print(predictions)