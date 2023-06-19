import numpy as np
import matplotlib.pyplot  as plt
import cv2

#img = cv2.imread('./data/ants/swiss-army-ant.jpg',1)

gamma = 0.6

#lut = np.zeros((256, 1), dtype = 'uint8') # (256, 1)のuint8行列を0で初期化
#for i in range(len(lut)):
#    lut[i][0] = 255 * pow((float(i)/255), (1.0/gamma))
#gamma_img = cv2.LUT(img, lut) # Look Up Table
#cv2.imwrite('./data/gamma_img.jpg', gamma_img)


import os
dirs = ['ants']
pixels = []
labels = []

#    files= os.listdir("./data/"+d+"/") #"C:\Users\ohika\Desktop\puroguramu\data"
#    print(files)
#    for f in files:
#        img = cv2.imread("./data/" + d + "/" + f ,0)
#        #print(img)
#        lut = np.zeros((256, 1), dtype = 'uint8') # (256, 1)のuint8行列を0で初期化
#        print(lut)
#        for a in range(len(lut)):
#           lut[a][0] = 255 * pow((float(a)/255), (1.0/gamma))
#       gamma_img = cv2.LUT(img, lut) # Look Up Table
#        #plt.show(gamma_img)
#       cv2.imwrite('./data/dummy_ants/g0.6_.jpg/',gamma_img)

files= os.listdir("./data/ants") 
gamma = 0.6

while gamma <= 1.2:
    lut = np.zeros((256, 1), dtype = 'uint8') # (256, 1)のuint8行列を0で初期化
    for i in range(len(lut)):
        lut[i][0] = 255 * pow((float(i)/255), (1.0/gamma))
        for f in files:
            base,ext = os.path.splitext(f)
        img = cv2.imread("./data/ants/" + f ,0)
        gamma_img = cv2.LUT(img, lut) # Look Up Table
        cv2.imwrite('./data/dummy_ants/g0.6_/'+f+'.jpg', gamma_img)

