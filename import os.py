import os
import cv2
import numpy as np

dirs = ['ants','bees']
pixels = []
labels = []

for i , d in enumerate(dirs):
    files= os.listdir("./data/"+d+"/") #"C:\Users\ohika\Desktop\puroguramu\data"
    print(i)

    for f in files:
        img = cv2.imread("./date/"+d+"/"+f+"/" ,0)
        print(f) 
        img = cv2.resize(img,(128, 128))
        img = np.array(img).flatten().tolist()
        pixels.append(img)

        labels.append(i)

