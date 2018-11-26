from __future__ import unicode_literals
from PyQt5 import QtCore,QtGui,QtWidgets  
from PyQt5.QtWidgets import *            								#部件
from PyQt5.QtCore import *
from socket import *
road = 'C:/Users/mac/Desktop/'
import sys
import time

class Ui_Down_Window(QtWidgets.QWidget):
	def setupUi(self,Down_Window):
		Down_Window.setObjectName("Down_Window")
		Down_Window.resize(820,520)
		Down_Window.setStyleSheet("background-image:url('back1.png')")
		
		self.textBrowser = QtWidgets.QTextBrowser(Down_Window)			#列表框
		self.textBrowser.setGeometry(QtCore.QRect(40,50,750,110))
		self.textBrowser.setObjectName("textBrowser")
		font = QtGui.QFont()
		font.setPointSize(16)
		font.setBold(True)
		font.setWeight(75)
		self.textBrowser.setFont(font)
		self.textBrowser1 = QtWidgets.QTextBrowser(Down_Window)
		self.textBrowser1.setGeometry(QtCore.QRect(370, 270, 420, 40))
		font.setPointSize(12)
		self.textBrowser1.setFont(font)
		self.textBrowser1.setObjectName("textBrowser1")
		self.textBrowser1.append(road)
		self.textBrowser.clear()
		ADDR = ('127.0.0.1',8000)
		s = socket()
		s.connect(ADDR)
		s.send(b'L')													#向服务器发送请求得到文件列表
		data = s.recv(1024).decode()									#收到服务器响应为OK时继续接受列表信息
		if data == 'OK':
			data = s.recv(1024).decode()
			files = data.split('#')
			for file in files:
				self.textBrowser.append(file)
		
		
		self.pushButton = QtWidgets.QPushButton(Down_Window)
		self.pushButton.setGeometry(QtCore.QRect(600,400,190,40))
		self.pushButton.setObjectName("pushButton")
		self.pushButton1 = QtWidgets.QPushButton(Down_Window)
		self.pushButton1.setGeometry(QtCore.QRect(320,400,190,40))
		self.pushButton1.setObjectName("pushButton1")
		self.pushButton2 = QtWidgets.QPushButton(Down_Window)
		self.pushButton2.setGeometry(QtCore.QRect(40,400,190,40))
		self.pushButton2.setObjectName("pushButton2")
		font = QtGui.QFont()
		font.setPointSize(16)
		font.setBold(True)
		font.setWeight(75)
		self.pushButton.setFont(font)
		self.pushButton1.setFont(font)
		self.pushButton2.setFont(font)
		self.pushButton.clicked.connect(self.loadfile)
		self.pushButton1.clicked.connect(self.save_path)
		self.pushButton2.clicked.connect(self.flush)
		
		
		self.label = QtWidgets.QLabel(Down_Window)
		self.label.setGeometry(QtCore.QRect(330,10,360,41))
		self.label.setObjectName("label")
		self.label_2 = QtWidgets.QLabel(Down_Window)
		self.label_2.setGeometry(QtCore.QRect(60,200,310,40))
		self.label_2.setObjectName("label_2")
		self.label_3 = QtWidgets.QLabel(Down_Window)
		self.label_3.setGeometry(QtCore.QRect(60,280,310,40))
		self.label_3.setObjectName("label_3")
		
		self.lineEdit = QtWidgets.QLineEdit(Down_Window)
		self.lineEdit.setGeometry(QtCore.QRect(370, 200, 421, 41))
		self.lineEdit.setObjectName("lineEdit")
		self.lineEdit.setFont(font)
		self.lineEdit.setText("")
		self.lineEdit.setPlaceholderText("请输入文件名")
		'''
		self.menubar = QtWidgets.QMenuBar(Down_Window)
		self.menubar.setGeometry(QtCore.QRect(0, 0, 821, 23))
		self.menubar.setObjectName("menubar")
		self.statusbar = QtWidgets.QStatusBar(Down_Window)
		self.statusbar.setObjectName("statusbar")
		'''
		self.retranslateUi(Down_Window)
		QtCore.QMetaObject.connectSlotsByName(Down_Window)
		
		
	def loadfile(self):
		filename = self.lineEdit.text()
		ADDR = ('127.0.0.1',8000)
		s = socket()
		s.connect(ADDR)
		s.send(('G ' + filename).encode())
		data = s.recv(1024).decode()
		if data == 'OK':
			fd = open(road + filename,'wb')
			while True:
				data = s.recv(1024)
				if data == b"##":										#服务器端发送完毕
					break
				fd.write(data)
			fd.close()
		
	def save_path(self):
		l = []
		openfile_name = QFileDialog.getExistingDirectory()
		l.append(openfile_name)
		global road
		if l[0]:
			road = l[0] + "/"
		self.textBrowser1.clear()
		self.textBrowser1.append(road)
		
	def flush(self):
		self.textBrowser.clear()
		ADDR = ('127.0.0.1',8000)
		s = socket()
		s.connect(ADDR)
		s.send(b'L')													#向服务器发送请求得到文件列表
		data = s.recv(1024).decode()									#收到服务器响应为OK时继续接受列表信息
		if data == 'OK':
			data = s.recv(1024).decode()
			files = data.split('#')
			for file in files:
				self.textBrowser.append(file)
		
	def retranslateUi(self,Down_Window):
		_translate = QtCore.QCoreApplication.translate
		Down_Window.setFixedSize(Down_Window.width(),Down_Window.height())
		Down_Window.setWindowTitle(_translate("Down_Window","ftp_download"))
		self.pushButton.setText(_translate("Down_Window","下载"))
		self.pushButton1.setText(_translate("Down_Window", "选择下载路径"))	
		self.pushButton2.setText(_translate("Down_Window", "刷新"))
		self.label.setText(_translate(
			"Down_Window","<html><head/><body><p><span style=\" font-size:18pt; font-weight:600;\">下载文件列表</span></p></body></html>"))
		self.label_2.setText(_translate(
		 "Down_Window", "<html><head/><body><p><span style=\" font-size:16pt; font-weight:600;\">请在此输入您要下载的文件名:</span></p></body></html>"))
		self.label_3.setText(_translate(
            "MainWindow", "<html><head/><body><p><span style=\" font-size:16pt; font-weight:600;\">您选择的下载路径是:</span></p></body></html>"))
		

class Ui_MainWindow(QtWidgets.QWidget):									#创建窗口类，继承QtWidgets.QWidget
	def setupUi(self,MainWindow):										#ui界面设计
		MainWindow.setObjectName("MainWindow")							#窗口名称	
		MainWindow.resize(540,440)										#窗口大小	
		MainWindow.setStyleSheet("background-image:url('upload.png')")	#背景图		
		
		
		#上传按钮
		self.pushButton = QtWidgets.QPushButton(MainWindow)				#在MainWindow里添加按钮
		self.pushButton.setGeometry(QtCore.QRect(30,320,220,40))		#设置位置和大小
		self.pushButton.setObjectName("pushButton")						#给按钮命名
		font = QtGui.QFont()
		font.setPointSize(16)											#文本大小
		font.setBold(True)
		font.setWeight(75)
		self.pushButton.setFont(font)
		self.pushButton.clicked.connect(self.upfile)
		
		#下载按钮
		self.pushButton1 = QtWidgets.QPushButton(MainWindow)
		self.pushButton1.setGeometry(QtCore.QRect(250,320,220,40))
		self.pushButton1.setObjectName("pushButton1")
		font = QtGui.QFont()
		font.setPointSize(16)											#文本大小
		font.setBold(True)
		font.setWeight(75)
		self.pushButton1.setFont(font)
		self.pushButton1.clicked.connect(self.jump_to_download)
#####################################################
		self.retranslateUi(MainWindow)
		QtCore.QMetaObject.connectSlotsByName(MainWindow) 				#关联信号槽,将名称与按钮对应
#####################################################
		#上传
	def upfile(self):
		l = []
		openfile_name = QFileDialog.getOpenFileName(self)
		l.append(openfile_name)											#上传文件在本地的路径和类型
		if l[0][0]:														
			ADDR = ('127.0.0.1',8000)									
			s = socket()
			s.connect(ADDR)
			road = l[0][0]
			fd = open(road,'rb')
			filename = road.split('/')[-1]								#取最后的文件名	
			s.send(("P " + filename).encode())							#向服务器发送请求，encode编码						
			data = s.recv(1024).decode()								#解码
			if data == 'OK':
				while True:
					data = fd.read(1024)
					if not data:
						s.send(b'##')									#当为空时发送##，服务器停止等待接受
						break
					s.send(data)
	#子界面
	def jump_to_download(self):
		MainWindow.hide()
		Down_Window = QtWidgets.QDialog()
		ui = Ui_Down_Window()
		ui.setupUi(Down_Window)
		Down_Window.show()
		Down_Window.exec_()												#启动事件循环
		MainWindow.show()												#退出子窗口后显示主界面
		
		
	def retranslateUi(self,MainWindow):
		_translate = QtCore.QCoreApplication.translate
		MainWindow.setFixedSize(MainWindow.width(), MainWindow.height())#禁止窗口最大化
		MainWindow.setWindowTitle(_translate("MainWindow","ftp"))
		self.pushButton.setText(_translate("MainWindow","上传"))
		self.pushButton1.setText(_translate("MainWindow","下载"))
if __name__ == "__main__":
	import sys
	app = QtWidgets.QApplication(sys.argv)
	MainWindow = QtWidgets.QMainWindow()								#重载窗口设计
	ui = Ui_MainWindow()												#实例化
	ui.setupUi(MainWindow)
	MainWindow.show()													#调用方法
#	MainWindow.exec_()
#	time.sleep(5)														
	sys.exit(app.exec_())												#启动事件循环
