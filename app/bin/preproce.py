# -*- coding: utf-8 -*-
"""
Created on Tue Sep 21 22:41:00 2021

@author: Alan Lin
"""
import pydicom
import cv2
import numpy as np

def usm(img):
    mgBlurred = cv2.GaussianBlur(img,(0,0),5)     
    usm = cv2.addWeighted(img,1.5,mgBlurred,-0.5,0)
    return usm
    
def Preprocessing(File,fname):
    print('flie name :',fname)
    if fname[-4:] == '.dcm':
        ds = pydicom.read_file(File)  #讀取.dcm文件
        img = ds.pixel_array  # 提取圖像信息       
        img_2d = img.astype(float)
        ## Step 2. Rescaling grey scale between 0-255
        img_2d_scaled = (np.maximum(img_2d,0) / img_2d.max()) * 255.0
        out_img = usm(255-img_2d_scaled)
        return out_img
    elif fname[-4:] == '.jpg':
        # img = Image.open(io.BytesIO(File.read()))       
        npimg = np.fromstring(File.read(), np.uint8)
        img = cv2.imdecode(npimg, cv2.IMREAD_GRAYSCALE)
        out_img = usm(img)
        return out_img
    else:
        return 'wrong format'