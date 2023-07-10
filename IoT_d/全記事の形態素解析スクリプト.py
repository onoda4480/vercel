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
df = pd.DataFrame(docterm)
print(df.head())
print(df.tail())


#                                                   0
#0  旧式 禁断 パワーアップ 最新 ソフト 一挙 チェック フラッシュ バック テレビ 連携 パ...
#1  アップル デベロッパプレビュー リリース 次期 明らか アップル 年月日 米国 カリフォルニ...
#2  サービス 終了 後 電子 書籍 永遠 の デジ 通 ソニー コンピュータ エンターテイメント...
#3  ウェブページ イメージ ワザ 虎の巻 会社 概要 自社 ウェブページ イメージ ブログページ...
#4  レノボ プロ ゴルファー 斉藤 愛 璃選手 オフィシャル・スポンサーシップ 契約 締結 レノ...

#                                                     0
#395  インタビュー 斉藤 和義 音楽 バカ カッコ さ がれ 年月日 虹 向こう 出立 バンド マ...
#396  インタビュー ヒュー ジャック マン 本当 さ 自分 こと ロボット 格闘技 世界 舞台  人...
#397  柴 咲 コウ 話題 プロジェクト デビュー 前夜 シークレットライブ 開催 日本 屈指 女優...
#398  編集 部 的 映画 批評 フランス 人種 差別 国 ツアー 旅行 日本人 友人 送迎 車 乗...
#399  インタビュー マシュー・グレイ・ギュブラー シェマー・ムーア お互い 今 一番 状態 常識 ...
