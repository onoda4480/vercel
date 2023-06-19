import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from sklearn.linear_model import LinearRegression
from statsmodels.stats.outliers_influence import variance_inflation_factor
import numpy as np
# データの準備
data = pd.read_csv('housing.data.txt', header=None, sep='\s+')
data.columns = ['CRIM', 'ZN', 'INDUS', 'CHAS', 'NOX', 'RM', 'AGE', 'DIS', 'RAD', 'TAX', 'PTRATIO', 'B', 'LSTAT', 'MEDV']
from mlxtend.plotting import scatterplotmatrix
cols = ['LSTAT', 'INDUS', 'NOX', 'RM', 'MEDV']


# 'LSTAT', 'INDUS', 'NOX', 'RM' の列のみを持つデータフレームを作成
selected_cols = ['LSTAT', 'INDUS', 'NOX', 'RM']
X_selected = data[selected_cols].copy()
print("データフレームにしたXのチェック\n",X_selected.head())

X = data[['LSTAT', 'INDUS', 'NOX', 'RM']].values
y = data['MEDV'].values

## モデルの構築 ols関数
lm_model = smf.ols(formula='y ~ RM +NOX+INDUS+LSTAT',
                   data=data).fit()
lm_model2 = smf.ols(formula='y ~ RM +INDUS+LSTAT',
                   data=data).fit()
lm_model3 = smf.ols(formula='y ~ RM +LSTAT',
                   data=data).fit()

# モデルの構築 glm関数でガウシアン 結果はols関数と同じ
model_formula = 'y ~ RM +NOX+INDUS+LSTAT'  # モデル式
glm_model = smf.glm(formula=model_formula, data=data, family=sm.families.Gaussian())

model_formula2 = 'y ~ RM +INDUS+LSTAT'  # モデル式
glm_model2 = smf.glm(formula=model_formula2, data=data, family=sm.families.Gaussian())

model_formula3 = 'y ~ RM +LSTAT'  # モデル式
glm_model3 = smf.glm(formula=model_formula3, data=data, family=sm.families.Gaussian())

# モデルの学習結果
glm_result = glm_model.fit()
glm_result2 = glm_model2.fit()
glm_result3 = glm_model3.fit()


# AIC
aic_calc=round(-2 * (glm_result.llf - (glm_result.df_model + 1)), 3)
print("aic_calc:", aic_calc)

AIC = glm_result.aic
print("AIC:", AIC)
AIC2 = glm_result2.aic
print("AIC2:",AIC2)
AIC3 = glm_result3.aic
print("AIC3:",AIC3)
# モデルの評価
print(glm_result.summary())
print(glm_result2.summary())
print(glm_result3.summary())
print(lm_model.summary())
print(lm_model2.summary())
print(lm_model3.summary())

#多重共線性のチェック
from statsmodels.stats.outliers_influence import variance_inflation_factor

def calculate_vif(X):   #Xはデータフレーム型
    vif = pd.DataFrame()
    vif["Variables"] = X.columns
    vif["VIF"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
    return vif

#選択した説明変数のVIFチェック
vif_result = calculate_vif(X_selected)
print("全体のVIF結果：\n",vif_result)

# 着目した説明変数のみで再度VIFチェック
RM_vif = data[['RM', 'LSTAT']]
# 説明変数間の相関行列を計算
correlation_matrix = RM_vif.corr()
# 相関行列から相関係数を取得
correlation_coefficients = correlation_matrix.values
print("R_RM_LSTAT(相関行列）:\n",correlation_coefficients)
print("RM_vif:\n",calculate_vif(RM_vif))

# 残差の取得
Se = lm_model.resid
Se.head(3)
lm_model.fittedvalues.head(3)

# 決定係数と調整済み決定係数の計算
y_bar = np.mean(y)         # yの平均値
y_hat = glm_result.predict() # yの当てはめ値
R2=round(np.sum((y_hat - y_bar)**2) / np.sum((y - y_bar)**2), 3)
print("R2:",R2)
print("glm_result.fittedvalues.head(3):",glm_result.fittedvalues.head(3))
print("Se:",Se)
n = len(y) # サンプルサイズ
d = 4              # 説明変数の数
r2_adj = 1 - ((np.sum(Se**2) / (n - d - 1)) / 
    (np.sum((y - y_bar)**2) / (n - 1)))
print("r2_adj:",round(r2_adj, 3))