# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 22:09:47 2016

@author: gal
"""

import cv2
import glob

imglib = "D:\\ImagesGT\\"
outlib = "D:\\ImagesGT\\edge\\"   #must exsist

#import numpy as np
#from matplotlib import pyplot as plt

for file in glob.glob(imglib + "*.png"):
    print(file)
    img = cv2.imread(file,0)
    edges = cv2.Canny(img,100,200)
    cv2.imwrite(outlib + file[len(imglib):],edges)
    
    
#
#img = cv2.imread("D:\\ImagesGT\\1.png",0)
#edges = cv2.Canny(img,100,200)
#cv2.imwrite("D:\\ImagesGT\\1_edge.png",edges)
 
#plt.subplot(121),plt.imshow(img,cmap = 'gray')
#plt.title('Original Image'), plt.xticks([]), plt.yticks([])
#plt.subplot(122),plt.imshow(edges,cmap = 'gray')
#plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
# 
#plt.show()