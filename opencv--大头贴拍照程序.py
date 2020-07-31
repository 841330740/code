import cv2.cv2 as cv2
import numpy as np
import time

save_path='C:/Users/sj/Desktop/addframe/1231/' #保存图片的文件夹路径
capture = cv2.VideoCapture(0)                        # 创建一个VideoCapture对象
cv2.namedWindow("frame", cv2.WINDOW_NORMAL)          #创建一个frame窗口
capture.set(3,960) #设置分辨率
capture.set(4,540)
cv2.resizeWindow("frame", 960, 540)
while(True):
    ret, frame = capture.read()                     # 一帧一帧读取视频
    path='C:/Users/sj/Desktop/json-png/ni1'         #背景图片的文件夹路径
    fileimg=path+'/timg2.png'                       #背景图片的路径
    img=cv2.imread(fileimg)
    imghsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)      #BGR转HSV色彩空间
    Maskbg=cv2.inRange(imghsv,(0,0,0),(180,255,20))     #将懒羊羊的脸部ROI提取出来(涂黑的部分，其他图片只需要把拍照的区域涂黑，再改一下尺寸或者拍照的像素等，就可以代码复用了)
    gaussimg=cv2.GaussianBlur(Maskbg,(3,3),0)      #高斯滤波
    medianimg = cv2.medianBlur(gaussimg, 7)
    timg1 = cv2.bitwise_and(frame, frame, mask=Maskbg)     #相同尺寸才可以进行bt与
    dst=cv2.add(timg1,img)         #图片叠加
    cv2.imshow('frame',dst)
    try:
        key=cv2.waitKey(1) &0xFF     #cv2.waitKey()有输入时返回输入值的ASCll,&0xFF表示取低八位
        #必须先把收到的值先存储下来，否则如果输入q第一次判断不是t以后，第二次判断就变成无值的判断，null当然也不等于q了，不将输入的值保存下来，就导致输入q无法退出，除非在他进行第二次判断之前飞速按下q，才能成功退出。多个指令时建议使用队列来做。
        if key == ord('t'):       #拍照，这里表示输入的是t
            cv2.imencode('.png',dst)[1].tofile(save_path+str(time.strftime('%Y%m%d%H%M%S',time.localtime(time.time())))+'.png') #保存图片,日期+时间.png
            cv2.waitKey(500) #截图后显示0.5秒
        elif key == ord('q'):   #这里表示输入的是q，即是退出
            break
    except Exception:
        pass
    
capture.release()                                   # 释放cap,销毁窗口
cv2.destroyAllWindows()
