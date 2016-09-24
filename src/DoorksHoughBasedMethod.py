import cv2
import numpy as np
from skimage import data, color

img = cv2.imread('HoughInput.png',0)
edges = cv2.Canny(img,20,30)


minLineLength = 10
maxLineGap = 20
lines = cv2.HoughLinesP(edges,1,np.pi/180,20,minLineLength,maxLineGap)

for Nline in range(0,lines.shape[0]):
    for x1,y1,x2,y2 in lines[Nline]:
        cv2.line(edges,(x1,y1),(x2,y2),0,4)


circles = cv2.HoughCircles(edges,cv2.HOUGH_GRADIENT,1,50,
                            param1=100,param2=30,minRadius=0,maxRadius=0)

circles = np.uint16(np.around(circles))
img2= color.gray2rgb(img)
for i in circles[0,:]:
    # draw the outer circle
    cv2.circle(img2,(i[0],i[1]),i[2],(0,0,200),2)
    # draw the center of the circle
    cv2.circle(img2,(i[0],i[1]),2,(0,0,200),3)

cv2.imwrite('Try.png',img2)
cv2.imshow('show',img2)
cv2.waitKey(0)
