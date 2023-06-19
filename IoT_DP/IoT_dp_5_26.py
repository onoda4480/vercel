import numpy as np
import matplotlib.pyplot  as plt
import cv2


img = cv2.imread('./data/ants/swiss-army-ant.jpg',1)
print(img.shape) # 画素数（Y,X），カラーチャネル数
#plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
#plt.show()
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
print(gray_img.shape)
#plt.imshow(gray_img, cmap='gray')
#plt.show()


ret, bin_img = cv2.threshold(gray_img, 100, 255, cv2.THRESH_BINARY) 
#plt.imshow(bin_img, cmap='gray')
#plt.show()

kernel = np.ones((3,3),np.uint8)

#img_cl = cv2.morphologyEx(bin_img, cv2.MORPH_CLOSE, kernel)
#plt.imshow(img_cl, cmap='gray')
#plt.show()


#hist_gr_1,bins =np.histogram(img.ravel(),256,[0,256])
#hist_gr_2,bins =np.histogram(img.ravel(),256,[0,256])
#hist_gr_3,bins =np.histogram(img.ravel(),256,[0,256])


hist_b = cv2.calcHist([img], [0], None, [256], [0, 256])
hist_g = cv2.calcHist([img], [1], None, [256], [0, 256])
hist_r = cv2.calcHist([img], [2], None, [256], [0, 256])

plt.xlim(0, 255)
#plt.plot(hist_gr ,'-r')
plt.plot(hist_b, '-b', label='Blue')
plt.plot(hist_g, '-g', label='Green')
plt.plot(hist_r, '-r', label='Red')

#plt.plot(hist_gr_1,'-b')
#plt.plot(hist_gr_2,'-g')
#plt.plot(hist_gr_3,'-r')

plt.xlabel('pixsel value')
plt.ylabel('number of pixsel')
#plt.show()

x_img = cv2.flip(img,0)
y_img = cv2.flip(img,1)
xy_img = cv2.flip(img,-1)

cv2.imwrite('./data/x_img.jpg' ,x_img)
cv2.imwrite('./data/y_img.jpg',y_img)
cv2.imwrite('./data/xy_img.jpg',xy_img)

blur_img = cv2.blur(img, (5, 5)) # 平均化フィルタ（averaging filter）
gau_img = cv2.GaussianBlur(img, (5, 5), 0) # ガウシアンフィルタ
med_img = cv2.medianBlur(img, 5) # 中央値フィルタ（メジアンフィルタ）
cv2.imwrite('./data/blur_img.jpg', blur_img)
cv2.imwrite('./data/gau_img.jpg', gau_img)
cv2.imwrite('./data/med_img.jpg', med_img)

gamma = 0.5
lut = np.zeros((256, 1), dtype = 'uint8') # (256, 1)のuint8行列を0で初期化
for i in range(len(lut)):
    lut[i][0] = 255 * pow((float(i)/255), (1.0/gamma))
gamma_img = cv2.LUT(img, lut) # Look Up Table
cv2.imwrite('./data/gamma_img.jpg', gamma_img)