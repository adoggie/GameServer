#-- coding:utf-8 --
__author__ = 'root'

import os,traceback
from desert import misc

class Logger:
	def __init__(self):
		self.handlers=[]
		self.dumpEnabled = True    #默认不启动日志输出
		if os.path.exists('logdump.no'):
			self.dumpEnabled = False

	__handle = None
	@staticmethod
	def instance():
		if not Logger.__handle:
			Logger.__handle = Logger()

		return Logger.__handle
	
	@property
	def handlers(self):
	    return self.handlers


	def addHandler(self,h):
		self.handlers.append(h)
		return h

	def info(self,s):
		self.write(s,'INFO')

	def error(self,s):
		self.write(s,'ERROR')

	def debug(self,s):
		self.write(s)

	def write(self,s,level='DEBUG'):
		if not self.dumpEnabled:
			return

		import time
		if not s.strip():
			return
		stime = misc.formatTimestamp(int(time.time()))
		s = stime + ' %s '%level + s
		for h in self.handlers:
			try:
				h.write(s)
			except:
				traceback.print_exc()

	def writelines(self,text,level='DEBUG'):
		#text = text.strip()
		self.write(text+'\n',level)


	class StdoutHandler:
		def __init__(self,stdout=None):
			self.stdout = stdout

		def write(self,s):
			if self.stdout:
				try:
					self.stdout.write(s+'\n')
				except:
					self.stdout.write(s.encode('gbk')+'\n')


	class FileHandler:
		def __init__(self,file,mode='a+'):
			self.file = file
			self.mode = mode
			self.hfile = None

		def write(self,s):
			if not self.hfile:
				self.hfile = open(self.file,self.mode)
			if self.hfile:
				try:
					self.hfile.write(s+'\n')
				except:
					self.hfile.write(s.encode('gbk')+'\n')
				self.hfile.flush()

	class DatagramHandler:
		def __init__(self,dest=('127.0.0.1',17948)):
			self.dest = dest
			if type(dest)==str:
				host,port = dest.split(':')
				self.dest = (host,int(port))
			self.sock = None

		def write(self,s):
			import socket
			if not self.sock:
				self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
			try:
				self.sock.sendto(s,0,self.dest)
			except:
				self.sock.sendto(s.encode('gbk'),0,self.dest)