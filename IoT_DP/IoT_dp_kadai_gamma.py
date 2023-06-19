import numpy as np
import matplotlib.pyplot as plt
import cv2
import os
import time

dirs = ['ants', 'bees']
start_time = time.time() 
total_execution_time = 0

for d in dirs:
    files = os.listdir("./data/" + d + "/")
    dir_start_time = time.time()
    
    for f in files:
        img = cv2.imread("./data/" + d + "/" + f, 1)
        x_img = cv2.flip(img, 0)
        y_img = cv2.flip(img, 1)
        xy_img = cv2.flip(img, -1)
        blur_img = cv2.blur(img, (5, 5))
        cv2.imwrite(f'./data/dummy_{d}/h_{f}', x_img)
        cv2.imwrite(f'./data/dummy_{d}/v_{f}', y_img)
        cv2.imwrite(f'./data/dummy_{d}/hv_{f}', xy_img)
        cv2.imwrite(f'./data/dummy_{d}/blur_{f}', blur_img)

    gamma = 0.6

    while gamma <= 1.2:
        lut = np.zeros((256, 1), dtype='uint8')
        for i in range(len(lut)):
            lut[i][0] = 255 * pow((float(i) / 255), (1.0 / gamma))

        files = os.listdir("./data/" + d + "/")

        for f in files:
            base, ext = os.path.splitext(f)
            if ext == '.jpg':
                img = cv2.imread('./data/' + d + '/' + f, 1)
                gamma_img = cv2.LUT(img, lut)
                f_new = f'./data/dummy_{d}/' + str(gamma) + '_' + f
                cv2.imwrite(f_new, gamma_img)

        gamma += 0.6

    dir_end_time = time.time()
    dir_execution_time = dir_end_time - dir_start_time
    total_execution_time += dir_execution_time
    print(f"処理時間（{d}）: {dir_execution_time}秒")

    #処理時間（ants）: 3.0705726146698秒
    #処理時間（bees）: 2.0279972553253174秒

end_time = time.time()
execution_time = end_time - start_time
print(f"全体の処理時間: {total_execution_time}秒")
#全体の処理時間: 5.098569869995117秒
