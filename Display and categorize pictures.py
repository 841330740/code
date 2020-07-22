import os
from PyQt5 import QtCore,QtGui,QtWidgets,Qt
import sys
import requests
import numpy as np
import cv2.cv2 as cv2
from PIL import Image,ImageDraw,ImageFont
from shutil import copyfile

#界面
class Ui(object):    
    def setupUi(self,Form): 
        Form.setObjectName("Form")            
        Form.setWindowTitle("图片分类工具")        
        Form.resize(1350,700)        
        Form.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)        
        Form.setWindowIcon(QtGui.QIcon('C:/Users/sj/Desktop/加边框/detect.png'))
        #抬头        
        self.groupBox1=QtWidgets.QGroupBox(Form)          
        self.groupBox1.setGeometry(QtCore.QRect(0,0,1350,70))        
        self.groupBox1.setObjectName("groupBox1")                    
        self.groupBox1.setStyleSheet('#groupBox1{background-color:#6677ff}')
        #背景group
        self.groupBox2=QtWidgets.QGroupBox(Form)                         
        self.groupBox2.setGeometry(QtCore.QRect(0,70,1350,630))        
        self.groupBox2.setObjectName("groupBox2")                    
        self.groupBox2.setStyleSheet('#groupBox2{background-color:#5555ff}')                
        #图窗1        
        self.lab1=QtWidgets.QLabel(Form)                        
        self.lab1.setGeometry(QtCore.QRect(0,70,600,300))        
        self.lab1.setObjectName("lab1")           
        self.lab1.raise_()        
        self.lab1.setStyleSheet('#lab1{background-color:#ffffff}')
        #小图窗1        
        self.lab11=QtWidgets.QLabel(self.lab1)                  
        self.lab11.setGeometry(QtCore.QRect(400,0,200,150))        
        self.lab11.setObjectName("lab11")           # 设置阴影 只有加了这步才能设置边框颜色         
        self.lab11.setFrameShape(QtWidgets.QFrame.Box)        # 可选样式有Raised、Sunken、Plain（这个无法设置颜色）等        
        self.lab11.setFrameShadow(QtWidgets.QFrame.Raised)        #线条宽度        
        self.lab11.setLineWidth(1)        
        self.lab11.hide()         
        self.lab11.setStyleSheet('#lab11{background-color:#ffffff}')
        #图窗2        
        self.lab2=QtWidgets.QLabel(Form)                        
        self.lab2.setGeometry(QtCore.QRect(750,70,600,300))        
        self.lab2.setObjectName("lab2")           
        self.lab2.raise_()        
        self.lab2.setStyleSheet('#lab2{background-color:#ffffff}')
        #小图窗2        
        self.lab22=QtWidgets.QLabel(self.lab2)                  
        self.lab22.setGeometry(QtCore.QRect(400,0,200,150))        
        self.lab22.setObjectName("lab22")           
        self.lab22.setFrameShape(QtWidgets.QFrame.Box)        
        self.lab22.setFrameShadow(QtWidgets.QFrame.Raised)        
        self.lab22.setLineWidth(1)        
        self.lab22.hide()         
        self.lab22.setStyleSheet('#lab22{background-color:#ffffff}')
        #图窗3        
        self.lab3=QtWidgets.QLabel(Form)                        
        self.lab3.setGeometry(QtCore.QRect(0,400,600,300))        
        self.lab3.setObjectName("lab3")           
        self.lab3.raise_()        
        self.lab3.setStyleSheet('#lab3{background-color:#ffffff}')
        #小图窗3        
        self.lab33=QtWidgets.QLabel(self.lab3)                  
        self.lab33.setGeometry(QtCore.QRect(400,0,200,150))        
        self.lab33.setFrameShape(QtWidgets.QFrame.Box)        
        self.lab33.setFrameShadow(QtWidgets.QFrame.Raised)        
        self.lab33.setLineWidth(1)        
        self.lab33.setObjectName("lab33")           
        self.lab33.hide()         
        self.lab33.setStyleSheet('#lab33{background-color:#ffffff}')
        #图窗4        
        self.lab4=QtWidgets.QLabel(Form)                        
        self.lab4.setGeometry(QtCore.QRect(750,400,600,300))        
        self.lab4.setObjectName("lab4")        
        self.lab4.raise_()        
        self.lab4.setStyleSheet('#lab4{background-color:#ffffff}')
        #小图窗4        
        self.lab44=QtWidgets.QLabel(self.lab4)                  
        self.lab44.setGeometry(QtCore.QRect(400,0,200,150))        
        self.lab44.setObjectName("lab44")           
        self.lab44.setFrameShape(QtWidgets.QFrame.Box)        
        self.lab44.setFrameShadow(QtWidgets.QFrame.Raised)        
        self.lab44.setLineWidth(1)        
        self.lab44.hide()         
        self.lab44.setStyleSheet('#lab44{background-color:#ffffff}')                 
        #按钮1：选择图片文件        
        #多选图片文件，至多选择四个        
        self.btn1=QtWidgets.QPushButton(Form)                   
        self.btn1.setGeometry(QtCore.QRect(625,80,100,30))        
        self.btn1.setObjectName("btn1")        
        self.btn1.setText('选择图像')        
        self.btn1.clicked.connect(Form.wichBtn)
        #按钮2：插入文字        
        self.btn3=QtWidgets.QPushButton(Form)                   
        self.btn3.setGeometry(QtCore.QRect(625,120,100,30))        
        self.btn3.setText('载入文字')        
        self.btn3.setObjectName("btn3")        
        self.btn3.clicked.connect(Form.TextInsert)
        #按钮3：清空窗口        
        self.btn4=QtWidgets.QPushButton(Form)                   
        self.btn4.setGeometry(QtCore.QRect(625,160,100,30))        
        self.btn4.setText('清空窗口')        
        self.btn4.setObjectName("btn4")        
        self.btn4.clicked.connect(Form.ImageClear)
        #按钮4：缺陷显示        
        self.btn5=QtWidgets.QPushButton(Form)                   
        self.btn5.setGeometry(QtCore.QRect(625,200,100,30))        
        self.btn5.setText('缺陷显示')        
        self.btn5.setObjectName("btn5")        
        self.btn5.clicked.connect(Form.MatShow)
        #文本输入框        
        self.text1=QtWidgets.QTextEdit(Form)                   
        self.text1.setGeometry(QtCore.QRect(625,240,100,250))        
        self.text1.setPlaceholderText('在此处输入文字'+'\n'+'格式:'+'\n'+'文字+#窗口'+'\n'+'（如：冲太阳咧嘴微笑#1234）')        
        self.text1.setObjectName("text1")
        #复选框1        
        self.checkb1 = QtWidgets.QCheckBox(Form)               
        self.checkb1.setGeometry(QtCore.QRect(625,500,70,30))        
        self.checkb1.setText('1')        
        self.checkb1.setObjectName("checkb1")        
        self.checkb1.toggle()
        #复选框2        
        self.checkb2 = QtWidgets.QCheckBox(Form)                
        self.checkb2.setGeometry(QtCore.QRect(700,500,70,30))        
        self.checkb2.setText('2')        
        self.checkb2.setObjectName("checkb2")        
        self.checkb2.toggle()
        #复选框3        
        self.checkb3 = QtWidgets.QCheckBox(Form)                
        self.checkb3.setGeometry(QtCore.QRect(625,540,70,30))        
        self.checkb3.setText('3')        
        self.checkb3.setObjectName("checkb3")        
        self.checkb3.toggle()
        #复选框3        
        self.checkb4 = QtWidgets.QCheckBox(Form)                 
        self.checkb4.setGeometry(QtCore.QRect(700,540,70,30))        
        self.checkb4.setText('4')        
        self.checkb4.setObjectName("checkb4")        
        self.checkb4.toggle()
        #按钮5：分类OK        
        self.btn5=QtWidgets.QPushButton(Form)                   
        self.btn5.setGeometry(QtCore.QRect(620,580,50,30))        
        self.btn5.setText('判为ok')        
        self.btn5.setObjectName("btn5")        
        self.btn5.clicked.connect(Form.SaveAsOK)
        #按钮6：分类NG        
        self.btn6=QtWidgets.QPushButton(Form)                   
        self.btn6.setGeometry(QtCore.QRect(680,580,50,30))        
        self.btn6.setText('判为NG')        
        self.btn6.setObjectName("btn6")        
        self.btn6.clicked.connect(Form.SaveAsNG)
#功能
class MainWindow(QtWidgets.QMainWindow):    
    def __init__(self,parent=None):        
        super(MainWindow,self).__init__(parent)        
        self.ui=Ui()        
        self.ui.setupUi(self)        
      #查找#符号位置    
    def IndexSharp(self,p):        
        for i in range(0,len(p)):            
            if p[i]=='#':                
                break        
        return i
    #opencv图像转array,使用ImageDraw添加文字   
    def cv2ImgAddText(self,img, text, left, top, textColor=(0, 255, 0), textSize=20):       
        if (isinstance(img, np.ndarray)):            
            img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))        
        draw = ImageDraw.Draw(img)        
        fontStyle = ImageFont.truetype("font/simsun.ttc", textSize, encoding="utf-8")        
        draw.text((left, top), text, textColor, font=fontStyle)        
        return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)        
    #确认str中是否包含某字符    
    def checknum(self,s,stri):        
        for i in range(0,len(stri)):            
            if s==stri[i]:               
                j=1               
                break            
            else:               
                j=0
        return j
    #文本插入    
    def TextInsert(self):        
        try:            
            x=self.ui.text1.toPlainText()            
            if self.checknum('1',x[self.IndexSharp(x)+1:])==1:                
                img1 = self.cv2ImgAddText(lab1img,x[:self.IndexSharp(x)], 0, 0, (255, 0 , 0), 40)                
                sp=img1.shape                
                img11 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)                
                _image = QtGui.QImage(img11[:], img11.shape[1], img11.shape[0], img11.shape[1] * 3, QtGui.QImage.Format_RGB888) 
                outimg = QtGui.QPixmap(_image).scaled(sp[1]*(self.ui.lab1.height()/sp[0]), sp[0]*(self.ui.lab1.height()/sp[0])) #设置图片大小                
                self.ui.lab1.setPixmap(outimg)            
            if self.checknum('2',x[self.IndexSharp(x)+1:])==1:                
                img1 = self.cv2ImgAddText(lab2img,x[:self.IndexSharp(x)], 0, 0, (255, 0 , 0), 40)                
                sp=img1.shape                
                img11 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)                
                _image = QtGui.QImage(img11[:], img11.shape[1], img11.shape[0], img11.shape[1] * 3, QtGui.QImage.Format_RGB888)               
                outimg = QtGui.QPixmap(_image).scaled(sp[1]*(self.ui.lab1.height()/sp[0]), sp[0]*(self.ui.lab1.height()/sp[0])) #设置图片大小                
                self.ui.lab2.setPixmap(outimg)            
            if self.checknum('3',x[self.IndexSharp(x)+1:])==1:                
                img1 = self.cv2ImgAddText(lab3img,x[:self.IndexSharp(x)], 0, 0, (255, 0 , 0), 40)                
                sp=img1.shape                
                img11 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)                
                _image = QtGui.QImage(img11[:], img11.shape[1], img11.shape[0], img11.shape[1] * 3, QtGui.QImage.Format_RGB888)                 
                outimg = QtGui.QPixmap(_image).scaled(sp[1]*(self.ui.lab1.height()/sp[0]), sp[0]*(self.ui.lab1.height()/sp[0])) #设置图片大小                
                self.ui.lab3.setPixmap(outimg)            
            if self.checknum('4',x[self.IndexSharp(x)+1:])==1:                
                img1 = self.cv2ImgAddText(lab4img,x[:self.IndexSharp(x)], 0, 0, (255, 0 , 0), 40)                
                sp=img1.shape                
                img11 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)                
                _image = QtGui.QImage(img11[:], img11.shape[1], img11.shape[0], img11.shape[1] * 3, QtGui.QImage.Format_RGB888)                 
                outimg = QtGui.QPixmap(_image).scaled(sp[1]*(self.ui.lab1.height()/sp[0]), sp[0]*(self.ui.lab1.height()/sp[0])) #设置图片大小                
                self.ui.lab4.setPixmap(outimg)        
        except Exception:            
            pass
    #保存为OK    
    def SaveAsOK(self):        
        try:            
            if self.ui.checkb1.isChecked():                
                path2=os.path.dirname(path[0][0])+'/OK'                
                if not os.path.exists(path2):                   
                    os.makedirs(path2)                
                    copyfile(path[0][0],path2+'/'+os.path.basename(path[0][0]))                
                    #os.unlink(path[0][0])        
        except Exception:            
            pass        
        try:            
            if self.ui.checkb2.isChecked():                
                path2=os.path.dirname(path[0][1])+'/OK'                
                if not os.path.exists(path2):                   
                    os.makedirs(path2)                
                    copyfile(path[0][1],path2+'/'+os.path.basename(path[0][1]))                
                    #os.unlink(path[0][1])        
        except Exception:            
            pass        
        try:            
            if self.ui.checkb3.isChecked():                
                path2=os.path.dirname(path[0][2])+'/OK'                
                if not os.path.exists(path2):                   
                    os.makedirs(path2)                
                    copyfile(path[0][2],path2+'/'+os.path.basename(path[0][2]))                
                    #os.unlink(path[0][2])        
        except Exception:            
            pass        
        try:            
            if self.ui.checkb4.isChecked():                
                path2=os.path.dirname(path[0][3])+'/OK'                
                if not os.path.exists(path2):                   
                    os.makedirs(path2)                
                    copyfile(path[0][3],path2+'/'+os.path.basename(path[0][3]))                
                    #os.unlink(path[0][3])        
        except Exception:            
            pass        
    #保存为NG    
    def SaveAsNG(self):        
        try:            
            if self.ui.checkb1.isChecked():                
                path2=os.path.dirname(path[0][0])+'/NG'                
                if not os.path.exists(path2):                   
                    os.makedirs(path2)                
                    copyfile(path[0][0],path2+'/'+os.path.basename(path[0][0]))                
                    #os.unlink(path[0][0])        
        except Exception:            
            pass        
        try:            
            if self.ui.checkb2.isChecked():                
                path2=os.path.dirname(path[0][1])+'/NG'                
                if not os.path.exists(path2):                   
                    os.makedirs(path2)                
                    copyfile(path[0][1],path2+'/'+os.path.basename(path[0][1]))                
                    #os.unlink(path[0][1])        
        except Exception:            
            pass        
        try:            
            if self.ui.checkb3.isChecked():                
                path2=os.path.dirname(path[0][2])+'/NG'                
                if not os.path.exists(path2):                   
                    os.makedirs(path2)                
                    copyfile(path[0][2],path2+'/'+os.path.basename(path[0][2]))                
                    #os.unlink(path[0][2])        
        except Exception:            
            pass        
        try:            
            if self.ui.checkb4.isChecked():                
                path2=os.path.dirname(path[0][3])+'/NG'                
                if not os.path.exists(path2):                   
                    os.makedirs(path2)                
                    copyfile(path[0][3],path2+'/'+os.path.basename(path[0][3]))                
                    #os.unlink(path[0][3])        
        except Exception:            
            pass
    #显示Mat    
    def MatShow(self):        
        if len(path[0])>0:            
            MatPath=os.path.dirname(path[0][0])+'/Mat'            
        try:                
            pathmat1=MatPath+'/'+os.path.basename(path[0][0])                
            #imdecode从内存中读取图片，如果内存中的数据太短或者不是合法的数据就返回一个空的矩阵                
            #将mat对象转换为RGB                
            #np.fromfile(pathmat1,dtype=np.uint8) 将pathmat1以uint8读出                
            Mat1=cv2.imdecode(np.fromfile(pathmat1,dtype=np.uint8),-1)                
            sp=Mat1.shape                
            Mat11 = cv2.cvtColor(Mat1, cv2.COLOR_BGR2RGB)                
            _image1 = QtGui.QImage(Mat11[:], Mat11.shape[1], Mat11.shape[0], Mat11.shape[1] * 3, QtGui.QImage.Format_RGB888)                 
            outimg1 = QtGui.QPixmap(_image1).scaled(sp[1]*(self.ui.lab11.height()/sp[0]), sp[0]*(self.ui.lab11.height()/sp[0])) #设置图片大小                
            self.ui.lab11.setPixmap(outimg1)            
        except Exception:                
            pass            
        try:                
            pathmat2=MatPath+'/'+os.path.basename(path[0][1])                
            Mat2=cv2.imdecode(np.fromfile(pathmat2,dtype=np.uint8),-1)                
            sp=Mat2.shape                
            Mat22 = cv2.cvtColor(Mat2, cv2.COLOR_BGR2RGB)                
            _image2 = QtGui.QImage(Mat22[:], Mat22.shape[1], Mat22.shape[0], Mat22.shape[1] * 3, QtGui.QImage.Format_RGB888)                 
            outimg2 = QtGui.QPixmap(_image2).scaled(sp[1]*(self.ui.lab11.height()/sp[0]), sp[0]*(self.ui.lab11.height()/sp[0])) #设置图片大小                
            self.ui.lab22.setPixmap(outimg2)            
        except Exception:                
            pass            
        try:                
            pathmat3=MatPath+'/'+os.path.basename(path[0][2])                
            Mat3=cv2.imdecode(np.fromfile(pathmat3,dtype=np.uint8),-1)                
            sp=Mat3.shape                
            Mat33 = cv2.cvtColor(Mat3, cv2.COLOR_BGR2RGB)                
            _image3 = QtGui.QImage(Mat33[:], Mat33.shape[1], Mat33.shape[0], Mat33.shape[1] * 3, QtGui.QImage.Format_RGB888)                 
            outimg3 = QtGui.QPixmap(_image3).scaled(sp[1]*(self.ui.lab11.height()/sp[0]), sp[0]*(self.ui.lab11.height()/sp[0])) #设置图片大小                
            self.ui.lab33.setPixmap(outimg3)            
        except Exception:                
            pass            
        try:                
            pathmat4=MatPath+'/'+os.path.basename(path[0][3])                
            Mat4=cv2.imdecode(np.fromfile(pathmat4,dtype=np.uint8),-1)                
            sp=Mat4.shape                
            Mat44 = cv2.cvtColor(Mat4, cv2.COLOR_BGR2RGB)                
            _image4 = QtGui.QImage(Mat44[:], Mat44.shape[1], Mat44.shape[0], Mat44.shape[1] * 3, QtGui.QImage.Format_RGB888)                 
            outimg4 = QtGui.QPixmap(_image4).scaled(sp[1]*(self.ui.lab11.height()/sp[0]), sp[0]*(self.ui.lab11.height()/sp[0])) #设置图片大小                
            self.ui.lab44.setPixmap(outimg4)            
        except Exception:                
            pass            
        if len(path[0])==1:                
            if self.ui.lab11.isHidden():                    
                self.ui.lab11.show()            
        if len(path[0])==2:                
            if self.ui.lab11.isHidden():                    
                self.ui.lab11.show()                
            if self.ui.lab22.isHidden():                    
                self.ui.lab22.show()            
        if len(path[0])==3:                
            if self.ui.lab11.isHidden():                    
                self.ui.lab11.show()                
            if self.ui.lab22.isHidden():                    
                self.ui.lab22.show()                
            if self.ui.lab33.isHidden():                    
                self.ui.lab33.show()            
        if len(path[0])==4:                
            if self.ui.lab11.isHidden():                    
                self.ui.lab11.show()                
            if self.ui.lab22.isHidden():                    
                self.ui.lab22.show()                
            if self.ui.lab33.isHidden():                    
                self.ui.lab33.show()                
            if self.ui.lab44.isHidden():                    
                self.ui.lab44.show()            
    #选择文件功能按钮    
    def wichBtn(self):        
        global path        
        global lab1img,lab2img,lab3img,lab4img        
        path=Qt.QFileDialog.getOpenFileNames()        
        if len(path[0])==1:            
            if self.ui.lab11.isVisible():                
                self.ui.lab11.clear()                
                self.ui.lab11.hide()        
        elif len(path[0])==2:            
            if self.ui.lab11.isVisible():                
                self.ui.lab11.clear()                
                self.ui.lab11.hide()            
            if self.ui.lab22.isVisible():                
                self.ui.lab22.clear()                
                self.ui.lab22.hide()        
        elif len(path[0])==3:            
            if self.ui.lab11.isVisible():                
                self.ui.lab11.clear()                
                self.ui.lab11.hide()            
            if self.ui.lab22.isVisible():                
                self.ui.lab22.clear()                
                self.ui.lab22.hide()            
            if self.ui.lab33.isVisible():                
                self.ui.lab33.clear()                
                self.ui.lab33.hide()        
        elif len(path[0])==4:            
            if self.ui.lab11.isVisible():                
                self.ui.lab11.clear()                
                self.ui.lab11.hide()            
            if self.ui.lab22.isVisible():                
                self.ui.lab22.clear()                
                self.ui.lab22.hide()            
            if self.ui.lab33.isVisible():                
                self.ui.lab33.clear()                
                self.ui.lab33.hide()            
            if self.ui.lab44.isVisible():                
                self.ui.lab44.clear()                
                self.ui.lab44.hide()        
        for i in range(0,len(path[0])):            
            img1=cv2.imdecode(np.fromfile(path[0][i],dtype=np.uint8),-1)            
            sp=img1.shape            
            img11 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)            
            _image = QtGui.QImage(img11[:], img11.shape[1], img11.shape[0], img11.shape[1] * 3, QtGui.QImage.Format_RGB888)             
            outimg = QtGui.QPixmap(_image).scaled(sp[1]*(self.ui.lab1.height()/sp[0]), sp[0]*(self.ui.lab1.height()/sp[0])) #设置图片大小            
            if i==0:                
                self.ui.lab1.setPixmap(outimg)                
                lab1img=img1            
            elif i==1:                
                self.ui.lab2.setPixmap(outimg)                 
                lab2img=img1            
            elif i==2:                
                self.ui.lab3.setPixmap(outimg)                 
                lab3img=img1            
            else:                
                self.ui.lab4.setPixmap(outimg)                 
                lab4img=img1
    #窗口清空    
    def ImageClear(self):        
        self.ui.lab1.clear()        
        self.ui.lab11.clear()        
        self.ui.lab11.hide()        
        self.ui.lab2.clear()        
        self.ui.lab22.clear()        
        self.ui.lab22.hide()        
        self.ui.lab3.clear()        
        self.ui.lab33.clear()        
        self.ui.lab33.hide()        
        self.ui.lab4.clear()        
        self.ui.lab44.clear()        
        self.ui.lab44.hide()    
if __name__=="__main__":    
    app=QtWidgets.QApplication(sys.argv)    
    win=MainWindow()    
    win.show()    
    sys.exit(app.exec_())

