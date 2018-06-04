#!/usr/bin/python
# -*- coding: utf-8 -*-

import cv2
import numpy as np
'''
img1 = cv2.cvtColor(cv2.imread("./temp/016660.jpg"), cv2.COLOR_BGR2GRAY)
img2 = cv2.cvtColor(cv2.imread("./temp/016665.jpg"), cv2.COLOR_BGR2GRAY)
local_template = img1[0:50, 264:274]
res=cv2.matchTemplate(img2,local_template,cv2.TM_CCOEFF_NORMED)
min_val,max_val,min_loc,max_loc = cv2.minMaxLoc(res)
cut_1 = img1[0:50, 0:269]
cut_2 = img2[0:50, max_loc[0] + 5:528]
image = np.concatenate([cut_1, cut_2], axis=1)
cv2.imwrite("temp.jpg", image)
'''

def join(start_num, end_num, width, height):
    img = cv2.cvtColor(cv2.imread('./temp/' + str(start_num).zfill(6) + '.jpg'), cv2.COLOR_BGR2GRAY)
    image = img[0:height, 0:width]
    for i in range(start_num, end_num + 1, 5):
        img = cv2.cvtColor(cv2.imread('./temp/' + str(i).zfill(6) + '.jpg'), cv2.COLOR_BGR2GRAY)
        x = int(image.shape[1]) - 50
        local_template = image[0:height, x:(x + 20)]
        res=cv2.matchTemplate(img,local_template,cv2.TM_CCOEFF_NORMED)
        min_val,max_val,min_loc,max_loc = cv2.minMaxLoc(res)
        cut_1 = image[0:height, 0:(x + 10)]
        cut_2 = img[0:height, (max_loc[0] + 10):width]
        image = np.concatenate([cut_1, cut_2], axis=1)
    cv2.imwrite("result.jpg", image)

join(16660, 16908, 528, 50)
