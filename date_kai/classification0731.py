# ライブラリのインポート
import matplotlib.pyplot as plt
import pydotplus
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import export_graphviz
from IPython.display import Image
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from mlxtend.plotting import plot_decision_regions
from sklearn.ensemble import RandomForestClassifier

# 小数点以下の表示桁数を3桁にする 
np.set_printoptions(precision=3, suppress=True)
plt.rcParams['font.size'] = 14        
      
# ワインデータセットの読み込み
df = pd.read_csv('wine.data', header=None)

df.columns = ['Class label', 'Alcohol', 'Malic acid', 'Ash',
                   'Alcalinity of ash', 'Magnesium', 'Total phenols',
                   'Flavanoids', 'Nonflavanoid phenols', 'Proanthocyanins',
                   'Color intensity', 'Hue', 'OD280/OD315 of diluted wines',
                   'Proline']

#すべてのデータを使用
#X = df.iloc[:, 1:].values

# 特徴量に色（10列）とプロリンの量(13列)を選択
X =df.iloc[:, [10,13]].values 

# 正解ラベルの設定(ラベルはゼロから開始するようマイナス1する)
y = df.iloc[:, 0].values -1

# 特徴量と正解ラベルを訓練データとテストデータに分割 8割の訓練、2割のテスト
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)


# 特徴量の標準化
sc = StandardScaler()
# 訓練データを変換器で標準化
X_train_std = sc.fit_transform(X_train)
# テストデータを作成した変換器で標準化
X_test_std = sc.transform(X_test)

#ロジスティック回帰モデルを作成
model1=LogisticRegression(max_iter=100,multi_class='ovr',solver='liblinear',C=1.0,penalty='l2',l1_ratio=None,random_state=0)

# モデルの訓練
model1.fit(X_train_std, y_train)

# テストデータで正解率を計算
y_test_pred = model1.predict(X_test_std)
ac_score = accuracy_score(y_test, y_test_pred)
print("ロジスティック回帰")
print('全体の正解率 = %.2f' % (ac_score))

#未知データ１つの検証
add_data1=[[0.1,-0.1]]
print("未知データの分類予測",model1.predict(add_data1))
print("スコア",model1.decision_function(add_data1))
print("未知データの確率",model1.predict_proba(add_data1))

# ロジスティック回帰モデルによる訓練データのプロット
plt.figure(figsize=(8,4)) #プロットのサイズ指定
plot_decision_regions(X_train_std, y_train, model1)

#ソフトマックス回帰モデルを作成
model2=LogisticRegression(max_iter=100,multi_class='multinomial',solver='lbfgs',C=1.0,penalty='l2',l1_ratio=None,random_state=0)

# モデルの訓練
model2.fit(X_train_std, y_train)

# テストデータで正解率を計算
y_test_pred = model2.predict(X_test_std)
ac_score = accuracy_score(y_test, y_test_pred)
print("ソフトマックス回帰")
print('全体の正解率 = %.2f' % (ac_score))

# ロジスティック回帰モデルによる訓練データのプロット
plt.figure(figsize=(8,4)) #プロットのサイズ指定
plot_decision_regions(X_train_std, y_train, model2)

#未知データ１つの検証
add_data1=[[0.1,-0.1]]
print("未知データの分類予測",model2.predict(add_data1))
print("スコア",model2.decision_function(add_data1))
print("未知データの確率",model2.predict_proba(add_data1))

#カーネルPCAを使った場合

#すべてのデータを使用
X = df.iloc[:, 1:].values

# 特徴量と正解ラベルを訓練データとテストデータに分割
X_train, X_test, y_train, y_test=train_test_split(X, y, test_size=0.2, random_state=0)

# 特徴量の標準化
sc = StandardScaler()
X_train_std = sc.fit_transform(X_train)
X_test_std =sc.transform(X_test)

# 特徴量は13個
print("特徴量全て使用の確認：(サンプル数,特徴量)")
print("X_train_stdとX_test_std.shape")
print(X_train_std.shape,  X_test_std.shape)

from sklearn.decomposition import KernelPCA

# 次元削減後の次元を2に指定し、主成分分析を実行（使用カーネルはガウス：rbf）gammaは精度パラメータ：ガウス分布の広がり：小：緩やかで訓練データの感度が下がる、大：過学習しやすい
KPCA = KernelPCA(n_components=2, kernel='rbf', gamma=0.3, random_state=0)

# 訓練データで主成分分析のモデル作成
X_train_kpca = KPCA.fit_transform(X_train_std)
# 訓練データで作成したモデルでテストデータを主成分分析
X_test_kpca = KPCA.transform(X_test_std)

# 特徴量は2個に削減されている
print("カーネルPCA後の特徴量数の確認：(サンプル数,特徴量)")
print("X_train_kpcaとX_test_kpca")
print(X_train_kpca.shape, X_test_kpca.shape)

# ロジスティック回帰モデルに適用
model3 = LogisticRegression( multi_class='ovr', max_iter=100, solver='liblinear', penalty='l2', random_state=0)

# モデルの訓練　
model3.fit(X_train_kpca, y_train)

# テストデータで正解率を計算
y_test_pred = model3.predict(X_test_kpca)
ac_score = accuracy_score(y_test, y_test_pred)
print("カーネルPCAによるロジスティック回帰")
print('正解率 = %.2f' % (ac_score))

# カーネルPCA後のロジスティック回帰モデルによる訓練データのプロット
plt.figure(figsize=(8,4)) #プロットのサイズ指定
plot_decision_regions(X_train_kpca, y_train, model3)
# カーネルPCA後のテストデータのプロット
plt.figure(figsize=(8,4)) #プロットのサイズ指定
plot_decision_regions(X_test_kpca, y_test, model3)


#基準違いの未知データ（値は同じ）を１つの検証
add_data1=[[0.1,-0.1]]
print("未知データの分類予測",model3.predict(add_data1))
print("スコア",model3.decision_function(add_data1))
print("未知データの確率",model3.predict_proba(add_data1))

print("このデータは縦横の評価軸（特徴量)がモデル１や２とは全く違うので比較できない")


from sklearn.pipeline import make_pipeline

pipe_lr = make_pipeline(StandardScaler(),
                        #PCA(n_components=2),
                        KernelPCA(n_components=2, kernel='rbf', gamma=0.3, random_state=0),
                        LogisticRegression(random_state=1, solver='lbfgs'))
                        #LogisticRegression(random_state=1, solver='liblinear'))

pipe_lr.fit(X_train, y_train)
y_pred = pipe_lr.predict(X_test)
print('Test Accuracy: %.3f' % pipe_lr.score(X_test, y_test))