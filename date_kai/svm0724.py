# ライブラリのインポート
#%matplotlib inline
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.svm import LinearSVC
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from mlxtend.plotting import plot_decision_regions
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# ワインデータセットの読み込み
df = pd.read_csv('wine.data', header=None)

df.columns = ['Class label', 'Alcohol', 'Malic acid', 'Ash',
                   'Alcalinity of ash', 'Magnesium', 'Total phenols',
                   'Flavanoids', 'Nonflavanoid phenols', 'Proanthocyanins',
                   'Color intensity', 'Hue', 'OD280/OD315 of diluted wines',
                   'Proline']
dfful=df

df = df[44:71]

# 特徴量に色（10列）とプロリンの量(13列)を選択
X = df.iloc[:,[10,13]].values
# 正解ラベルの設定(ラベルはゼロから開始するようマイナス1する)
y = df.iloc[:, 0].values -1

# 特徴量の標準化
sc = StandardScaler()
X_std = sc.fit_transform(X)

# ハードマージン（ハードマージン）のモデルを作成
model = LinearSVC(loss='hinge', C=10000.0, multi_class='ovr', penalty='l2', random_state=0)

# モデルの訓練
model.fit(X_std, y)

print("model.coef_[0]:",model.coef_[0]) #パラメータw
print("model.intercept_[0]:",model.intercept_[0]) #パラメータw0

# 決定境界用の変数X_pltを作成
X_plt = np.linspace(-3, 3, 200)[:, np.newaxis]

# 決定境界の作成
w = model.coef_[0]
w0 = model.intercept_[0]
decision_boundary = -w[0]/w[1] * X_plt - w0/w[1]

# 決定境界の上下にマージン作成
margin = 1/w[1]
margin_up = decision_boundary + margin
margin_down = decision_boundary - margin

plt.figure(figsize=(8,4)) #プロットのサイズ指定

# 決定境界、マージンのプロット
plt.plot(X_plt, decision_boundary, linestyle = "-",  color='black', label='LinearSVC')
plt.plot(X_plt, margin_up, linestyle = ":", color='red', label='margin')
plt.plot(X_plt, margin_down, linestyle = ":",color='blue', label='margin')

# 訓練データの散布図
plt.scatter(X_std[:, 0][y==1], X_std[:, 1][y==1], c='r', marker='x', label='1')
plt.scatter(X_std[:, 0][y==0], X_std[:, 1][y==0], c='b', marker='s', label='0')
plt.legend(loc='best')
plt.title(label='Hard-Margin')

plt.show

# LinearSVC（ソフトマージン）のモデル
#C(float)：正則化パラメータ 規定値=1.0
#正則化の強さはCに反比例し、正でなければならない。

model2 = LinearSVC(loss='hinge', C=1.0, multi_class='ovr', penalty='l2', random_state=0)

# モデルの訓練
model2.fit(X_std, y)

# 決定境界の作成
w = model2.coef_[0]
w0 = model2.intercept_[0]
decision_boundary2 = -w[0]/w[1] * X_plt - w0/w[1]

# 決定境界の上下にマージン作成
margin2 = 1/w[1]
margin_up2 = decision_boundary2 + margin2
margin_down2 = decision_boundary2 - margin2

plt.figure(figsize=(8,4)) #プロットのサイズ指定

# 決定境界、マージンのプロット
plt.plot(X_plt, decision_boundary2, linestyle = "-",  color='black', label='LinearSVC')
plt.plot(X_plt, margin_up2, linestyle = ":", color='red', label='margin')
plt.plot(X_plt, margin_down2, linestyle = ":",color='blue', label='margin')

# 訓練データの散布図
plt.scatter(X_std[:, 0][y==1], X_std[:, 1][y==1], c='r', marker='x', label='1')
plt.scatter(X_std[:, 0][y==0], X_std[:, 1][y==0], c='b', marker='s', label='0')
plt.legend(loc='best')
plt.title(label='Soft-Margin')
plt.show

#すべてのデータを使用
# 特徴量に色（9列）とプロリンの量(12列)を選択
X = dfful.iloc[:,[9,12]].values
# 正解ラベルの設定(ラベルはゼロから開始するようマイナス1する)
y = dfful.iloc[:, 0].values -1

# 特徴量と正解ラベルを訓練データとテストデータに分割
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

# 特徴量の標準化
sc = StandardScaler()
# 訓練データを変換器で標準化
X_train_std = sc.fit_transform(X_train)
# テストデータを作成した変換器で標準化
X_test_std = sc.transform(X_test)

print('X_train_stdの形状:',X_train_std.shape,' y_trainの形状:', y_train.shape,' X_test_stdの形状：', X_test_std.shape,' y_testの形状：', y_test.shape)

# SVCのモデルを作成
model = SVC(kernel='rbf', gamma=2.5 , C=100.0, decision_function_shape='ovr' ,random_state=0) 
#model = SVC(kernel='rbf', gamma=1.5 , C=100.0, decision_function_shape='ovr' ,random_state=0) 
#model = SVC(kernel='rbf', gamma=0.01 , C=100.0, decision_function_shape='ovr' ,random_state=0) 

# モデルの訓練
model.fit(X_train_std, y_train)

# 正解率を計算する
y_test_pred = model.predict(X_test_std)
ac_score = accuracy_score(y_test, y_test_pred)
print('正解率 = %.2f' % (ac_score))

# 訓練データのプロット
plt.figure(figsize=(8,4)) #プロットのサイズ指定
plot_decision_regions(X_train_std, y_train, model)
plt.title(label='Train_data')
plt.show

# テストデータのプロット
plt.figure(figsize=(8,4)) #プロットのサイズ指定
plot_decision_regions(X_test_std, y_test, model) 
plt.title(label='Test_data')
plt.show