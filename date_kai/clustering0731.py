# ライブラリのインポート
import matplotlib.pyplot as plt
import pydotplus
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from mlxtend.plotting import plot_decision_regions
from sklearn.cluster import KMeans

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

# K-Meansのモデルを作成
model2 = KMeans(n_clusters=2, random_state=103)
model3 = KMeans(n_clusters=3, random_state=103)
model4 = KMeans(n_clusters=4, random_state=103)

#モデルの訓練
model2.fit(X_train_std )
model3.fit(X_train_std)
model4.fit(X_train_std )
plt.figure(figsize=(8,12)) #プロットのサイズ指定

# クラスタ数2のK-Meansの散布図
plt.subplot(3, 1, 1)
plt.scatter(X_train_std[:,0], X_train_std[:,1], c=model2.labels_)
plt.scatter(model2.cluster_centers_[:,0], model2.cluster_centers_[:,1],s=250, marker='*',c='red')
plt.title('K-means(n_clusters=2)')

# クラスタ数3のK-Meansの散布図
plt.subplot(3, 1, 2)
plt.scatter(X_train_std[:,0],X_train_std[:,1], c=model3.labels_)
plt.scatter(model3.cluster_centers_[:,0], model3.cluster_centers_[:,1],s=250, marker='*',c='red')
plt.title('K-means(n_clusters=3)')

# クラスタ数4のK-Meansの散布図
plt.subplot(3, 1, 3)
plt.scatter(X_train_std[:,0], X_train_std[:,1], c=model4.labels_)
plt.scatter(model4.cluster_centers_[:,0], model4.cluster_centers_[:,1],s=250, marker='*',c='red')
plt.title('K-means(n_clusters=4)')

plt.show

plt.figure(figsize=(8,8)) #プロットのサイズ指定

# 色とプロリンの散布図
plt.subplot(2, 1, 1)
plt.scatter(X_train_std[:,0],X_train_std[:,1], c=model3.labels_)
plt.title('training data y')

# K-Meansの散布図
plt.subplot(2, 1, 2)
plt.scatter(X_train_std[:,0], X_train_std[:,1], c=model3.labels_)
plt.scatter(model3.cluster_centers_[:,0], model3.cluster_centers_[:,1],s=250, marker='*',c='red')
plt.title('K-means(n_clusters=3)')

plt.show

print("モデル3クラスタリング結果",model3.labels_)
print("モデル3クラスタリング重心",model3.cluster_centers_)

distortions = []
for i in range(1, 11):
    km = KMeans(n_clusters=i, 
                init='k-means++', 
                n_init=10, 
                max_iter=300, 
                random_state=0)
    km.fit(X_train_std)
    distortions.append(km.inertia_)
plt.plot(range(1, 11), distortions, marker='o')
plt.xlabel('Number of clusters')
plt.ylabel('Distortion')
plt.tight_layout()

plt.show()


import numpy as np
from matplotlib import cm
from sklearn.metrics import silhouette_samples

km = KMeans(n_clusters=3, 
            init='k-means++', 
            n_init=10, 
            max_iter=300,
            tol=1e-04,
            random_state=0)
y_km = km.fit_predict(X_train_std)

cluster_labels = np.unique(y_km)
n_clusters = cluster_labels.shape[0]
silhouette_vals = silhouette_samples(X_train_std, y_km, metric='euclidean')
y_ax_lower, y_ax_upper = 0, 0
yticks = []
for i, c in enumerate(cluster_labels):
    c_silhouette_vals = silhouette_vals[y_km == c]
    c_silhouette_vals.sort()
    y_ax_upper += len(c_silhouette_vals)
    color = cm.jet(float(i) / n_clusters)
    plt.barh(range(y_ax_lower, y_ax_upper), c_silhouette_vals, height=1.0, 
             edgecolor='none', color=color)

    yticks.append((y_ax_lower + y_ax_upper) / 2.)
    y_ax_lower += len(c_silhouette_vals)
    
silhouette_avg = np.mean(silhouette_vals)
plt.axvline(silhouette_avg, color="red", linestyle="--") 

plt.yticks(yticks, cluster_labels + 1)
plt.ylabel('Cluster')
plt.xlabel('Silhouette coefficient')
plt.tight_layout()