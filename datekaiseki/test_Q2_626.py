from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
import numpy as np

q2=np.array([[0.2,0],[0.3,1],[0.4,1],[0.5,1],[0.1,1]])
test_label=q2[:,1]
y_pred=1/(1+np.exp(-(-7+20*q2[:,0])))
print("y_pred:",y_pred)

y_pred_binary = (y_pred >= 0.5).astype(int)  # 0.5を閾値として二値化

print("y_pred_binary:", y_pred_binary)

print(classification_report(test_label, y_pred_binary))
print(confusion_matrix(test_label, y_pred_binary))

import matplotlib.pyplot as plt
from sklearn import metrics

ac_score = metrics.accuracy_score(test_label, y_pred_binary)
print('正解率{0:.1f}%'.format(ac_score * 100)) # :.1f 小数点桁数1桁

# FPR, TPR, 閾値 を算出
fpr, tpr, thresholds = metrics.roc_curve(test_label, y_pred)

# AUCスコア
auc = metrics.auc(fpr, tpr)

# ROC曲線をプロット
plt.plot(fpr, tpr,label='ROC curve (area = %.2f)'%auc)
plt.legend()
plt.title('ROC curve')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.grid(True)
plt.show()