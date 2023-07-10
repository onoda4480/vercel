import os
import re
from janome.tokenizer import Tokenizer
from janome.analyzer import Analyzer
from janome.tokenfilter import POSKeepFilter
import pandas as pd

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
    #print(files)
    test = len(files)
    print(test)