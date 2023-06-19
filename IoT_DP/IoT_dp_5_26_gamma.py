import numpy as np
import matplotlib.pyplot  as plt
import cv2
import os


dirs = ['ants','bees']
files = os.listdir('./data/ants/')
#print(files)

for i , d in enumerate(dirs):
    files= os.listdir("./data/"+d+"/") #"C:\Users\ohika\Desktop\puroguramu\data"
    print(files)
    for f in files:
        img = cv2.imread("./data/" + d + "/" + f ,1)
        print(img)
        x_img = cv2.flip(img,0)
        y_img = cv2.flip(img,1)
        xy_img = cv2.flip(img,-1)
        blur_img = cv2.blur(img, (5, 5)) # 平均化フィルタ（averaging filter）
        cv2.imwrite(f'./data/dummy_{d}/h_{f}',x_img)
        cv2.imwrite(f'./data/dummy_{d}/v_{f}',y_img)
        cv2.imwrite(f'./data/dummy_{d}/hv_{f}',xy_img)
        cv2.imwrite(f'./data/dummy_{d}/blur_{f}', blur_img)

gamma = 0.6

while gamma <= 1.2:
    lut = np.zeros((256, 1), dtype='uint8')
    for i in range(len(lut)):
        lut[i][0] = 255 * pow((float(i)/255), (1.0/gamma))

    for f in files:
        base, ext = os.path.splitext(f)
        if ext == '.jpg':
            img = cv2.imread('./data/ants/' + f)
            gamma_img = cv2.LUT(img, lut)
            f_new = './data/dummy_ants/' + str(gamma) + '_' + f
            cv2.imwrite(f_new, gamma_img)
    
    gamma += 0.6





blur_img = cv2.blur(img, (5, 5)) # 平均化フィルタ（averaging filter）
gau_img = cv2.GaussianBlur(img, (5, 5), 0) # ガウシアンフィルタ
med_img = cv2.medianBlur(img, 5) # 中央値フィルタ（メジアンフィルタ）
cv2.imwrite('./data/blur_img.jpg', blur_img)
cv2.imwrite('./data/gau_img.jpg', gau_img)
cv2.imwrite('./data/med_img.jpg', med_img)

#gamma = 0.5
#lut = np.zeros((256, 1), dtype = 'uint8') # (256, 1)のuint8行列を0で初期化
#for i in range(len(lut)):
#    lut[i][0] = 255 * pow((float(i)/255), (1.0/gamma))
#gamma_img = cv2.LUT(img, lut) # Look Up Table
#cv2.imwrite('./data/gamma_img.jpg', gamma_img)

gamma = 0.6

while gamma <= 1.2:
    lut = np.zeros((256, 1), dtype='uint8')
    for i in range(len(lut)):
        lut[i][0] = 255 * pow((float(i)/255), (1.0/gamma))

    for f in files:
        base, ext = os.path.splitext(f)
        if ext == '.jpg':
            img = cv2.imread('./data/ants/' + f)
            gamma_img = cv2.LUT(img, lut)
            f_new = './data/dummy_ants/' + str(gamma) + '_' + f
            cv2.imwrite(f_new, gamma_img)
    
    gamma += 0.6

