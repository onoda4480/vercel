"""
このコードは色々な検証を一つに詰め込んでいます。
読み込みやプロットに時間がかかる,イテレーションを長く取っている箇所など使いにくい状態です。
適切な部分にまとめたり、加工して使いやすいように改良して利用してください。
"""
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn import linear_model
df = pd.read_csv('housing.data.txt',
                 header=None,sep='\s+')

df.columns = ['CRIM', 'ZN', 'INDUS', 'CHAS', 
              'NOX', 'RM', 'AGE', 'DIS', 'RAD', 
              'TAX', 'PTRATIO', 'B', 'LSTAT', 'MEDV']
df.head()

import matplotlib.pyplot as plt
from mlxtend.plotting import scatterplotmatrix
cols = ['LSTAT', 'INDUS', 'NOX', 'RM', 'MEDV']

scatterplotmatrix(df[cols].values, figsize=(10, 8), 
                  names=cols, alpha=0.5)

plt.tight_layout()

plt.show()

#データの数、行数（サンプル数）と列数（特徴量）を表示
print("df.shape",df.shape)

import numpy as np
from mlxtend.plotting import heatmap


cm = np.corrcoef(df[cols].values.T)
hm = heatmap(cm, row_names=cols, column_names=cols)


plt.show()

class LinearRegressionGD(object):

    def __init__(self, eta=0.001, n_iter=1000):
        self.eta = eta
        self.n_iter = n_iter

    def fit(self, X, y):
        self.w_ = np.zeros(1 + X.shape[1])
        self.cost_ = []

        for i in range(self.n_iter):
            output = self.net_input(X)
            errors = (y - output)
            self.w_[1:] += self.eta * X.T.dot(errors)
            self.w_[0] += self.eta * errors.sum()
            cost = (errors**2).sum() / 2.0
            self.cost_.append(cost)
        return self

    def net_input(self, X):
        return np.dot(X, self.w_[1:]) + self.w_[0]

    def predict(self, X):
        return self.net_input(X)

#始めに１つの説明変数だけ指定してモデル作りをしてみる。    
    
X = df[['RM']].values
y = df['MEDV'].values

#sklearnのスケーラーを使って標準化
from sklearn.preprocessing import StandardScaler
sc_x = StandardScaler()
sc_y = StandardScaler()
X_std = sc_x.fit_transform(X)
y_std = sc_y.fit_transform(y[:, np.newaxis]).flatten()

# 平均と標準偏差の記憶
X_mean = sc_x.mean_
X_std_dev = np.sqrt(sc_x.var_)

y_mean = sc_y.mean_
y_std_dev = np.sqrt(sc_y.var_)

#作成した勾配降下法を使ってパラメータを求め、予測値を計算
lr = LinearRegressionGD()
lr.fit(X_std, y_std)
y_predict=lr.w_[1]*X_std+lr.w_[0] #勾配降下法によって得られたパラメータを使ったyの予測値


plt.plot(range(1, lr.n_iter+1), lr.cost_)
plt.ylabel('SSE')
plt.xlabel('Epoch')
plt.tight_layout()

plt.show()

def lin_regplot(X, y, model):
    plt.scatter(X, y, c='steelblue', edgecolor='white', s=70)
    plt.plot(X, model.predict(X), color='black', lw=2)    
    return 

lin_regplot(X_std, y_std, lr)
plt.xlabel('Average number of rooms [RM] (standardized)')
plt.ylabel('Price in $1000s [MEDV] (standardized)')

plt.show()

print('Slope: %.3f' % lr.w_[1])
print('Intercept: %.3f' % lr.w_[0])

# 標準化されたデータを元に戻す関数
def revert_standardization(result_data, mean, std_dev):
    original_data = (result_data * std_dev) + mean
    return original_data

#標準化された予測値を標準化前に戻す
y_org_pred=revert_standardization(y_predict, y_mean, y_std_dev)
y_org_pred = np.squeeze(y_org_pred)

from distutils.version import LooseVersion
import sklearn

#sklearnに実装されている関数を使った線形回帰モデルの実行
from sklearn.linear_model import LinearRegression
slr = LinearRegression()
slr.fit(X, y)
y_pred = slr.predict(X)
print('Slope: %.3f' % slr.coef_[0])#回帰モデルの傾き
print('Intercept: %.3f' % slr.intercept_)#回帰モデルの切片

#回帰モデルで得られた回帰式の確認
lin_regplot(X, y, slr)
plt.xlabel('Average number of rooms [RM]')
plt.ylabel('Price in $1000s [MEDV]')

plt.show()


#データを訓練データとテストデータに分けて汎化性能を持たせる
from sklearn.model_selection import train_test_split

X = df.iloc[:, :-1].values
#df.iloc[:, :-1]は、dfのすべての行（:）と最後の列を除いたすべての列（:-1）を選択する
y = df['MEDV'].values

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=0)

#14個のうち、13個の説明変数を使って重回帰モデルを選択　訓練データとテストデータの予測値を求める。
slr = LinearRegression()

slr.fit(X_train, y_train)
y_train_pred = slr.predict(X_train)
y_test_pred = slr.predict(X_test)

from sklearn.model_selection import KFold, cross_val_score

kfold = KFold(n_splits=10)
print("cross_val_score:", cross_val_score(slr, X_train, y_train, cv=kfold))

# 残差プロット
plt.figure(figsize=(8,4))#プロットのサイズ指定
plt.scatter(y_train_pred,  y_train_pred - y_train,
            c='red', marker='o', edgecolor='white',
            label='Training data')
plt.scatter(y_test_pred,  y_test_pred - y_test,
            c='blue', marker='s', edgecolor='white',
            label='Test data')
plt.xlabel('Predicted values')
plt.ylabel('Residuals')
plt.legend(loc='upper left')
plt.hlines(y=0, xmin=-10, xmax=50, color='black', lw=2)
plt.xlim([-10, 50])
plt.tight_layout()

plt.show()


#作成したモデルの評価　MSEの値は小さいほど良く、R2は1に近いほど良い
#trainデータ（訓練データ）のスコアがtestデータのスコアよりも良すぎると訓練のし過ぎで過学習となる。
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error

print('MSE train: %.3f, test: %.3f' % (
        mean_squared_error(y_train, y_train_pred),
        mean_squared_error(y_test, y_test_pred)))
print('R^2 train: %.3f, test: %.3f' % (
        r2_score(y_train, y_train_pred),
        r2_score(y_test, y_test_pred)))


#ラッソモデルを使って13個ある説明変数（特徴量）のうちパラメータcoefを0にして過学習を防ぐ
from sklearn.linear_model import Lasso

lasso = Lasso(alpha=0.1)
lasso.fit(X_train, y_train)
y_train_pred = lasso.predict(X_train)
y_test_pred = lasso.predict(X_test)
print("ラッソ回帰のパラメータ：",lasso.coef_)
print('LAssoMSE train: %.3f, test: %.3f' % (
        mean_squared_error(y_train, y_train_pred),
        mean_squared_error(y_test, y_test_pred)))
print('LassoR^2 train: %.3f, test: %.3f' % (
        r2_score(y_train, y_train_pred),
        r2_score(y_test, y_test_pred)))

#リッジ回帰で最適なαを求める
# αを変化させる
n_alphas = 50
ridge_alphas = np.logspace(-2, 0.7, n_alphas)

# αを変えて何度もRidge回帰を実行
# 推定された回帰係数を格納するリスト
ridge_coefs = []
sc_x = StandardScaler()
sc_y = StandardScaler()
X_std = sc_x.fit_transform(X)
y_std = sc_y.fit_transform(y[:, np.newaxis]).flatten()

# 平均と標準偏差の記憶
X_mean = sc_x.mean_
X_std_dev = np.sqrt(sc_x.var_)

y_mean = sc_y.mean_
y_std_dev = np.sqrt(sc_y.var_)

# forループで何度もRidge回帰を推定する
for a in ridge_alphas:
    ridge = linear_model.Ridge(alpha=a, fit_intercept=False)
    ridge.fit(X, y)
    ridge_coefs.append(ridge.coef_)

# X軸に-log10(α)、Y軸に係数を置いた折れ線グラフ
# アレイに変換
ridge_coefs = np.array(ridge_coefs)
ridge_coefs.shape
# αを変換
log_alphas = -np.log10(ridge_alphas)
# X軸に-log10(α)、Y軸に係数を置いた折れ線グラフ
plt.plot(ridge_alphas, ridge_coefs)
# X軸の範囲
plt.xlim([min(ridge_alphas) - 0.1, max(ridge_alphas) + 0.3])

# 軸ラベル
plt.title('Ridge')
plt.legend(df.columns,loc='upper left',fontsize=7)
plt.xlabel('alpha')
plt.ylabel('Coefficients')

ridge_best = linear_model.RidgeCV(
    cv=10, alphas=ridge_alphas, fit_intercept=False)
ridge_best.fit(X_train, y_train) 

y_train_pred = ridge_best.predict(X_train)
y_test_pred = ridge_best.predict(X_test)

# 最適な-log10(α)
round(-np.log10(ridge_best.alpha_), 3)
# 最適なα
print("最適なα：",round(ridge_best.alpha_, 3))
# 最適なαの時の、回帰係数
print("リッジ回帰による最適なαの時の、回帰係数（13個でフィッティング）\n:",ridge_best.coef_.round(2))

print('RidgeCV_MSE train: %.3f, test: %.3f' % (
        mean_squared_error(y_train, y_train_pred),
        mean_squared_error(y_test, y_test_pred)))
print('RidgeCV_R^2 train: %.3f, test: %.3f' % (
        r2_score(y_train, y_train_pred),
        r2_score(y_test, y_test_pred)))


#多項式回帰
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import ElasticNet
# 特徴量を2次多項式に変換
POLY = PolynomialFeatures(degree=2, include_bias = False)

# 線形回帰モデルを作成
model = LinearRegression()
model2 = Lasso(alpha=0.3,max_iter=100000)
# L1+L2正則化のモデルを作成
model3 = ElasticNet(alpha=0.3,l1_ratio=0.6,max_iter=100000)

X_train_pol = POLY.fit_transform(X_train)
X_test_pol = POLY.transform(X_test)
X_train_pol.shape, X_test_pol.shape

# モデルの訓練
model.fit(X_train_pol, y_train)
model2.fit(X_train_pol, y_train)
model3.fit(X_train_pol, y_train)
# MSEの計算
y_train_pred = model.predict(X_train_pol)
y_test_pred = model.predict(X_test_pol)
y_train_pred2 = model2.predict(X_train_pol)
y_test_pred2 = model2.predict(X_test_pol)
y_train_pred3 = model3.predict(X_train_pol)
y_test_pred3 = model3.predict(X_test_pol)

print(' PolynomialMSE train: %.2f, test: %.2f' % (
        mean_squared_error(y_train, y_train_pred),
        mean_squared_error(y_test, y_test_pred)))
print('PolynomialR^2 train:%.3f, test: %.3f' % (
        r2_score(y_train, y_train_pred),
        r2_score(y_test, y_test_pred)))

print(' PolynomialLassoMSE train: %.2f, test: %.2f' % (
        mean_squared_error(y_train, y_train_pred2),
        mean_squared_error(y_test, y_test_pred2)))
print('PolynomialLassoR^2 train:%.3f, test: %.3f' % (
        r2_score(y_train, y_train_pred2),
        r2_score(y_test, y_test_pred2)))

print(' PolynomialElasticNetMSE train: %.2f, test: %.2f' % (
        mean_squared_error(y_train, y_train_pred3),
        mean_squared_error(y_test, y_test_pred3)))
print('PolynomialElasticNetR^2 train:%.3f, test: %.3f' % (
        r2_score(y_train, y_train_pred3),
        r2_score(y_test, y_test_pred3)))


# 正則化無しの傾きと切片
print("正則化無しの切片",model.intercept_) 
print("説明変数の数：",model.coef_.shape) 
#print(model.coef_)

# L1正則化の傾きと切片
#print(model2.intercept_) 
#print(model2.coef_.shape)
#print(model2.coef_)

# L1+L2正則化の傾きと切片
#print(model3.intercept_) 
#print(model3.coef_.shape)
#print(model3.coef_)

# 残差プロット
plt.figure(figsize=(8,4))#プロットのサイズ指定

plt.scatter(y_train_pred,  y_train_pred - y_train,
            c='red', marker='o', edgecolor='white',
            label='Training data')
plt.scatter(y_test_pred,  y_test_pred - y_test,
            c='blue', marker='s', edgecolor='white',
            label='Test data')
plt.xlabel('Predicted values')
plt.ylabel('Residuals')
plt.legend(loc='upper left')
plt.hlines(y=0, xmin=-10, xmax=50, color='black', lw=2)
plt.xlim([-10, 50])
plt.tight_layout()

plt.show()
