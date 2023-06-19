import cv2
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

img = cv2.imread("./data/ants/swiss-army-ant.jpg")
#img = cv2.imread("C:\Users\ohika\Desktop\puroguramu\data\ants\swiss-army-ant.jpg")
#print(img)
#print(img.shape)

plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.show()

gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
print(gray_img.shape)
plt.imshow(gray_img, cmap='gray')
plt.show()

#b, g, r = cv2.split(gray_img)
#gray_img_df = pd.DataFrame(b)
#print(gray_img_df.shape)

#print(len(img)) # 配列全体のサイズ（1次元目）
#print(len(img[0])) # 1行目の配列のサイズ（2次元目）
#print(img[0][0]) # 1行目1列目の配列の値（3次元目）
#print(img) # 配列全体の確認

#import pandas as pd
#b, g, r = cv2.split(img) # 最深次元の配列を展開する
#print(b)
#b_df = pd.DataFrame(b)
#print(b_df.shape)
#b_df.head()
