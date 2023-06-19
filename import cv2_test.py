import cv2
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
img = cv2.imread("./data/ants/swiss-army-ant.jpg")

b, g, r = cv2.split(img) # 最深次元の配列を展開する
print(b)
b_df = pd.DataFrame(b)
print(b_df.shape)
b_df.head()
print(b_df.describe())
b_df_max =  b_df.max()
print(b_df_max.sort_values())
b_df_min = b_df.min()
print(b_df_min.sort_values())
