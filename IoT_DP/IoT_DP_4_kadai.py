import os
import cv2
import numpy as np
import pandas as pd

dirs = ['ants','bees']
pixels = []
labels = []

for i , d in enumerate(dirs):
    files= os.listdir("./data/"+d+"/") #"C:\Users\ohika\Desktop\puroguramu\data"
    #print(files)

    for f in files:
        img = cv2.imread("./data/" + d + "/" + f ,0)
        #print(img)
        img = cv2.resize(img,(128, 128))
        img = np.array(img).flatten().tolist()
        pixels.append(img)

        labels.append(i)

pixels_df = pd.DataFrame(pixels)
pixles_df = pixels_df / 255
labels_df = pd.DataFrame(labels)
labels_df = labels_df.rename(columns={0: 'label'})
img_set = pd.concat([pixles_df, labels_df], axis=1)
print(img_set.head())
print(img_set.tail(10))

img_set.to_csv('img_set.csv', index=False)