#--coding:utf-8--


import os,os.path,sys,struct,time,traceback,signal,threading,datetime

class ValueType:
	NULL = 0


class TypeValue:
	def __init__(self,value,msg=''):
		self.name = ''
		self.value = value
		self.msg = msg


