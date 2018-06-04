#!/usr/bin/python
# -*- coding: utf-8 -*-
from PIL import Image
import numpy as np
import re
import math
import operator
from functools import reduce
import matplotlib.pyplot as plt
import os
import cv2

def join(start_num, end_num, width, height):
    img = cv2.cvtColor(cv2.imread('./temp/' + str(start_num).zfill(6) + '.jpg'), cv2.COLOR_BGR2GRAY)
    image = img[0:height, 0:width]
    for i in range(start_num, end_num + 1, 5):
        img = cv2.cvtColor(cv2.imread('./temp/' + str(i).zfill(6) + '.jpg'), cv2.COLOR_BGR2GRAY)
        x = int(image.shape[1]) - 50
        local_template = image[0:height, x:(x + 30)]
        res=cv2.matchTemplate(img,local_template,cv2.TM_CCOEFF_NORMED)
        min_val,max_val,min_loc,max_loc = cv2.minMaxLoc(res)
        cut_1 = image[0:height, 0:(x + 15)]
        cut_2 = img[0:height, (max_loc[0] + 15):width]
        image = np.concatenate([cut_1, cut_2], axis=1)
    cv2.imwrite("result.jpg", image)

def pic_diff(s1,s2):
    diff = np.long(0)
    for x in range(s1.shape[0]):
        for y in range(s1.shape[1]):
            if(s2[x,y].any() > s1[x,y].any()):
                diff += np.long((s2[x,y] - s1[x,y]) / 100)
            else:
                diff += np.long((s1[x,y] - s2[x,y]) / 100)
    #diff = diff / (s1.shape[0] * s1.shape[1])
    return diff

start,end,x,y,width,height = input().split(' ')
x = int(x) ;
y = int(y)
width = int(width)
height = int(height)

start_list = re.split('[.\\\\]' , start)
folder = start_list[2]
start_num = int(start_list[3])

end_list = re.split('[.\\\\]' , end)
end_num = int(end_list[3])

box = (x, y, x + width, y + height)

img = []
for i in range(start_num, end_num + 1):
    img.append(Image.open('./' + folder + '/' + str(i).zfill(6) + '.jpg'))


for i in range(start_num, end_num + 1):
    temp_img = img[i - start_num].crop(box)
    if os.path.exists('./temp/' + str(i).zfill(6) + '.jpg'):
        os.remove('./temp/' + str(i).zfill(6) + '.jpg')
    temp_img.save('./temp/' + str(i).zfill(6) + '.jpg')


local_img = []
for i in range(start_num, end_num + 1):
    local_img.append(cv2.cvtColor(cv2.imread('./temp/' + str(i).zfill(6) + '.jpg'), cv2.COLOR_BGR2GRAY))

diff = []
for i in range(start_num, end_num):
    diff.append(pic_diff(local_img[i - start_num], local_img[i - start_num + 1]))

result = sum(diff) / len(diff)
if result > 7000:
    print("是滚动字幕")
    #image = np.concatenate([cv2.imread('./temp/' + str(start_num).zfill(6) + '.jpg'), cv2.imread('./temp/' + str(end_num).zfill(6) + '.jpg')], axis=1)
    if os.path.exists("result.jpg"):
        os.remove("result.jpg")
    join(start_num, end_num, width, height)
else:
    print("不是滚动字幕")
    if os.path.exists("result.jpg"):
        os.remove("result.jpg")
    image = cv2.imread('./temp/' + str(start_num).zfill(6) + '.jpg')
    cv2.imwrite("result.jpg", image)



