import cv2
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from mainWindow import Ui_MainWindow
import base64
import time
import requests
from urllib import request
import ssl
import json


def Image_Recognition(image, API_Key, Secret_Key):
    try:
        gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)

        # client_id 为官网获取的AK， client_secret 为官网获取的SK
        host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id='+API_Key+'&client_secret='+Secret_Key
        req = request.Request(host)
        response = request.urlopen(req, context=gcontext).read().decode('UTF-8')
        # print(response)

        # 获取调用鉴权接口获取的access_token的字典
        result = json.loads(response)
        access_token = result['access_token']
        # print(access_token)

        # 处理图片 base64编码，
        """要求base64编码后大小不超过4M，最短边至少15px，最长边最大4096px,
        支持jpg/png/bmp格式，注意：图片需要base64编码、去掉编码头。"""
        f = open(image, 'rb')
        img = base64.b64encode(f.read())

        # 开始访问 API
        # 请求头
        headers = {
           'Content-Type':'application/x-www-form-urlencoded'
        }
        # 请求 URL
        # host = 'https://aip.baidubce.com/rest/2.0/image-classify/v2/advanced_general'
        host = "https://aip.baidubce.com/rest/2.0/image-process/v1/selfie_anime"
        host = host+'?access_token='+access_token
        # 请求体
        data = {}
        data['access_token'] = access_token
        data['image'] =img
        # post请求
        res = requests.post(url=host, headers=headers, data=data)
        req = res.json()

        # print(req)
        if 'image' in req:
            req = req['image']
            image_new = './images/'+str(int(time.time())) + ".jpg"
            f = open(image_new, "wb")
            f.write(base64.b64decode(req))
            req = image_new
            f.close()
        else:
            req ='未识别' #API接口调用异常

        return req

    except Exception as e:
        print(e)

class ui_MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(ui_MainWindow, self).__init__(parent)
        # 创建一个定时器对象
        self.timer_camera = QTimer(self)
        self.timer_camera.timeout.connect(self.show_camera)

    def init_setting(self):
        self.cap = cv2.VideoCapture()  # 初始化摄像头
        self.CAM_NUM = 0
        self.__flag_work = 0
        self.isMoveState = True
        self.isMove = False
        self.scan = ScanThread()
        self.scan._siginal.connect(self.updateMove)
        self.scan.start()
        self.scan_cursor.setVisible(False)

    # def init_camera_page(self):
    #     self.Camera_label.clear()
    #     self.Open_Camera_Btn.setText(u'开启摄像机')

    # 返回主页面
    def return_main_page(self):
        print(self.stackedWidget.currentIndex())
        if self.stackedWidget.currentIndex() == 2:
            self.stackedWidget.setCurrentIndex(0)
            self.picture_label.clear()
            self.label.clear()
            self.showImageName = None
            self.png = None
            self.imgName = None
        # elif self.stackedWidget.currentIndex() == 2:
        #     self.stackedWidget.setCurrentIndex(0)
        #     self.Uplode_Picture_label.clear()
        #     self.picture_label.clear()
        #     self.png = None
        #     self.imgName = None
        #     self.scan_cursor.setVisible(False)
        elif self.stackedWidget.currentIndex() == 1:
            self.stackedWidget.setCurrentIndex(0)
            self.Camera_label.clear()
            self.picture_label.clear()
            # self.border_label_3.setVisible(False)
            self.showImageName = None
            self.timer_camera.stop()
            self.cap.release()
            self.Camera_label.clear()
            self.scan_cursor.setVisible(False)

    # 显示警告框
    def show_warning_box(self, text):
        self.dialog = DialogWindow()
        # self.dialog.setStyleSheet('background-color:blue;color:black')
        self.dialog.text_label.setText(text)
        self.dialog.show()


    def closeEvent(self, event):
        if self.cap.isOpened():
            self.cap.release()
        if self.timer_camera.isActive():
            self.timer_camera.stop()
        event.accept()

    # 点击确定按钮，返回主页面显示要识别图片
    def get_current_image(self):
        self.imgName = self.showImageName + ".jpg"
        self.showImage.save(self.imgName, "JPG", 100)
        self.png = QtGui.QPixmap(self.showImage).scaled(self.picture_label.width(),
                                                        self.picture_label.height())
        return self.png

    def close_camera(self):
        self.timer_camera.stop()
        self.cap.release()
        self.Camera_label.clear()

    def show_camera(self):
        self.showImageName = './images/' + str(int(time.time()))
        self.Take_Picture_Btn.setVisible(True)
        flag, self.image = self.cap.read()
        # show = cv2.resize(self.image, (400, 290))
        show = cv2.resize(self.image, None, fx=1, fy=1, interpolation=cv2.INTER_CUBIC)
        # cv2.copyMakeBorder(self.image,0,0,50,0,cv2.BORDER_CONSTANT,value=[0,255,0])
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
        self.showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)
        self.Camera_label.setPixmap(QtGui.QPixmap.fromImage(self.showImage))

    def load_picture(self):
        self.imgName, self.imgType = QFileDialog.getOpenFileName(None,
                                                       "上传图片",
                                                       "",
                                                       " *.jpg;;*.png;;*.jpeg;;*.bmp;;All Files (*)")
        print(self.imgName, self.imgType)
        return self.imgName, self.imgType
    # def load_picture(self):
    #     self.imgName, self.imgType = QFileDialog.getOpenFileName(None,
    #                                                    "上传图片",
    #                                                    "",
    #                                                    " *.jpg;;*.png;;*.jpeg;;*.bmp;;All Files (*)")
    def updateMove(self):
        # self.scan_cursor.setVisible(True)
        self.cursor = QtCore.QPropertyAnimation(self.scan_cursor, b'geometry')  # 设置动画的对象及其属性
        self.cursor.setDuration(2000)  # 设置动画间隔时间
        if self.isMoveState:
            self.isMoveState =False
            self.cursor.setStartValue(QtCore.QRect(240, 130, 520, 16))  # 设置动画对象的起始属性
            self.cursor.setEndValue(QtCore.QRect(240, 430, 520, 16))  # 设置动画对象的结束属性
        else:
            self.isMoveState =True
            self.cursor.setStartValue(QtCore.QRect(240, 130, 520, 16))  # 设置动画对象的起始属性
            self.cursor.setEndValue(QtCore.QRect(240, 430, 520, 16))  # 设置动画对象的结束属性
        self.cursor.start()  # 启动动画

    #展示结果
    def show_result(self):
        self.Image_recognition._imgeSinginal.connect(self.showResult)
        self.Image_recognition.start()

    # 展示识别结果
    def showResult(self, req):
        self.scan_cursor.setVisible(False)
        self.stackedWidget.setCurrentIndex(2)
        # 左侧label显示识别的图片
        self.png = QtGui.QPixmap(req).scaled(self.label.width(), self.label.height())
        self.label.setPixmap(self.png)

        # f = open(self.showImageName + "1.jpg", "wb")
        # self.img = f.write(base64.b64decode(req))
        # self.png = QtGui.QPixmap(self.img).scaled(self.label.width(),
        #                                               self.label.height())
        # self.border_label_4.setPixmap(self.png)
        # 右侧label显示识别结果
        # self.category_1.setText(req[0]['keyword'] + ":")
        # self.score_1.setText(str(round(req[0]['score'] * 100, 2)) + "%")
        # self.category_2.setText(req[1]['keyword'] + ":")
        # self.score_2.setText(str(round(req[1]['score'] * 100, 2)) + "%")
        # self.category_3.setText(req[2]['keyword'] + ":")
        # self.score_3.setText(str(round(req[2]['score'] * 100, 2)) + "%")
        # f = open(self.imgName+"1.jpg", "wb")
        # self.png1 = f.write(base64.b64decode(req))

        # f.close()


# 图像识别线程
class Rec(QThread):
    _imgeSinginal = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

    def setImage(self, API_Key, Secret_Key, imgName=None,):
        self.imgName=imgName
        self.API_Key = API_Key
        self.Secret_Key = Secret_Key

    def run(self):
        req = Image_Recognition(self.imgName, self.API_Key, self.Secret_Key)
        self._imgeSinginal.emit(req)


class ScanThread(QThread):
    _siginal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

    def run(self):
        while 1 > 0:
            time.sleep(2)
            self._siginal.emit()

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(350, 115)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(0, 0, 350, 115))
        self.label.setStyleSheet("border-image: url(images/14.png);")
        self.label.setText("")
        self.label.setObjectName("label")
        self.text_label = QtWidgets.QLabel(Dialog)
        self.text_label.setGeometry(QtCore.QRect(20, 25, 311, 71))
        font = QtGui.QFont()
        font.setFamily("优设标题黑")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.text_label.setFont(font)
        self.text_label.setStyleSheet("font: 11pt \"优设标题黑\";\n"
"color: rgb(255, 255, 255);")
        self.text_label.setAlignment(QtCore.Qt.AlignCenter)
        self.text_label.setWordWrap(True)
        self.text_label.setObjectName("text_label")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "提示"))
        self.text_label.setText(_translate("Dialog", "请输入"))

# 子窗口
class DialogWindow(QMainWindow, Ui_Dialog):
    def __init__(self):
        super(DialogWindow, self).__init__()
        self.setupUi(self)


