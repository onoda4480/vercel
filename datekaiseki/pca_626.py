import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# データの読み込みと前処理
df_pca = pd.read_csv('pcadatautf.csv', header=None, encoding='utf-8')
df_pca.columns = ['国語x1', '英語x2', '数学x3', '理科x4']
X = np.array(df_pca)

# Xが入力の行列（NumPy配列）であるとします
# 各列ごとに平均と不偏標準偏差を計算 defaultはddof=1の不偏標準偏差を計算、ddof=0で母標準偏差
means = np.mean(X, axis=0)
std_devs = np.std(X, axis=0, ddof=1)
# 各列の値から平均を引き、不偏標準偏差で割る
Xu_std = (X - means) / std_devs
# 結果の表示
print("不偏標準偏差を使った標準化：",Xu_std)

sc = StandardScaler()
X_std = sc.fit_transform(X)

# 主成分分析の実行
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_std)
Xu_pca = pca.fit_transform(Xu_std)
# 主成分得点の計算
z1 = -X_pca[:, 0]  # 第1主成分
z2 = X_pca[:, 1]   # 第2主成分
# 主成分得点の計算
zu1 = -Xu_pca[:, 0]  # 第1主成分
zu2 = Xu_pca[:, 1]   # 第2主成分
print("主成分得点zu1")
print(zu1)
print("主成分得点zu2")
print(zu2)
"""
数式で計算
print("主成分得点z1")
z1=-PCA.components_[0,:]@X_std.T
print(z1)
print("主成分得点z2")
z2=PCA.components_[1,:]@X_std.T
print(z2)
"""

# 主成分分析の結果の表示
print("固有値")
print(pca.explained_variance_)
print("因子寄与率")
print(pca.explained_variance_ratio_)
print("固有ベクトルの形状")
print(pca.components_.shape)
print('')
print("固有ベクトル")
print(pca.components_)

# 因子負荷量の計算
loadings = pca.components_.T * np.sqrt(pca.explained_variance_)


#plt.xlabel('PC1')
#plt.ylabel('PC2')
#plt.title('Principal Component Analysis')
#plt.legend()
#plt.show()
