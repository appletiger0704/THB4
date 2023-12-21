# -*- coding: utf-8 -*-
"""
Created on Sun Dec 17 14:34:34 2023

@author: User
"""

from PIL import Image
from datetime import datetime
import os

# East_auto
now = datetime.now()
today = now.strftime("%Y%m%d")
path = rf"C:\Users\User\Desktop\East_auto\{today}"
img = ["6_06QPF.png", "6_12QPF.png", "6_18QPF.png", "6_24QPF.png"]
os.chdir(path)

# 設定要裁剪的區域 (左, 上, 右, 下)
crop_area = (625, 300, 1080, 1050)

def cropped(img):
    
    image = Image.open(os.path.join(path, img))
    cropped_image = image.crop(crop_area)
    cropped_image.save("cropped_" + img)

for i in img:
    
    cropped(i)