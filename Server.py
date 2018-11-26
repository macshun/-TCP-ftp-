# -*- coding: cp936 -*-
from __future__ import unicode_literals
from socket import *
import multiprocessing as mp
import os
import signal
import sys
import time

FILE_PATH = "E:/tftp_serve/"

class FtpServer(object):
	def __init__(self,connfd):
		self.connfd = connfd
	def handler(self):
		while True:
			data = self.connfd.recv(1024).decode()				#���տͻ�������
			if not data:
				print(self.connfd.getpeername, '�ͻ����˳�')
				self.connfd.close()
				sys.exit(0)
			elif data[0] == 'L':
				self.do_list()
			elif data[0] == 'G':
				filename = data[2:]
				self.do_get(filename)
			elif data[0] == 'P':
				filename = data[2:]
				self.do_put(filename)
	def do_list(self):
		file_list = os.listdir(FILE_PATH)	
		if not file_list:
			self.connfd.send("�ļ���Ϊ��".encode())
			return
		else:
			self.connfd.send(b'OK')
			time.sleep(0.1)
		files = ""
		for file in file_list:
			if file[0] != '.' and \
				os.path.isfile(FILE_PATH + file):
				files = files + file + '#'
		self.connfd.send(files.encode())
	def do_get(self,filename):
		try:
			fd = open(FILE_PATH + filename,'rb')
		except:
			self.connfd.send("�ļ�������".encode())
			return
		self.connfd.send(b'OK')
		while True:
			data = fd.read(1024)
			if not data:
				self.connfd.send(b'##')
				break
			self.connfd.send(data)
		print("�ļ��������")
	def do_put(self,filename):
		try:
			fd = open(FILE_PATH + filename,'wb')
		except:
			self.connfd.send("�޷��ϴ�".encode())
			return
		self.connfd.send(b'OK')
		while True:
			data = self.connfd.recv(1024)
			if data == b"##":
				break
			fd.write(data)
		fd.close()
		print("�ϴ����")


def main():
	HOST = '127.0.0.1'
	PORT = 8000
	ADDR = (HOST,PORT)
	s = socket()
	s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
	s.bind(ADDR)
	s.listen(5)															#������������
	print("Listen to port 8000......")									#���տͻ��˵Ľ����󣬷���connfd���൱��һ���ض����ӣ���addr�ǿͻ���ip+port
	
	while True:
		try:
			connfd, addr = s.accept()
		except KeyboardInterrupt:
			s.close()
			sys.exit("�˳�������")
		except Exception as e:
			print(e)
			continue
		print("�ͻ��˵�¼�� ",addr)
		tftp = FtpServer(connfd)
		p = mp.Process(target = tftp.handler)
		p.start()
		time.sleep(0.1)
		p.join()

if __name__ == "__main__":
	main()
