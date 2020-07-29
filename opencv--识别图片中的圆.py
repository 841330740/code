import cv2.cv2 as cv2
import numpy as np

path='a.jpg'
img = cv2.imread(path,0)
gaussimg=cv2.GaussianBlur(img,(3,3),0)   #高斯滤波，(3,3)为高斯半径
medianimg = cv2.medianBlur(gaussimg, 7)   #中值滤波
cannyimg=cv2.Canny(medianimg,0,148)       #canny边缘检测
cv2.imshow('image',cannyimg)
cv2.waitKey(1000)
circles = cv2.HoughCircles(cannyimg,cv2.HOUGH_GRADIENT,1,20,param1=50,param2=10,minRadius=0,maxRadius=300)
circles = np.uint16(np.around(circles))
img2bgr=cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
count=1     #作为信号，只取第一个霍夫圆，试着用数组取了但是没成功
for i in circles[0]:#得到的霍夫圆是按照与所给轮廓拟合度排序的，一般取第一个就是与轮廓最拟合的那个
    #如果有多个圆识别，可以试试用多次霍夫圆，试着用半径过滤到同一块的圆，再取第一个，不过这样不稳定
    cv2.circle(img2bgr,(i[0],i[1]),i[2],(0,0,255),5)   #在图像上画出这个霍夫圆
    count+=1
    if count==2:
        break    
cv2.imshow('image',img2bgr)
cv2.waitKey(1000)
