#-- coding:utf-8 --
from misc import *

class X:
	"""
	从简单数据类型转换成python对象

	p = _x({'name':'boob','body':{'color':'black'},'toys':[1,2,3,],'age':100})
	print p['toys'][1]
	print len(p.toys)
	print p.body.colors
	"""
	def __init__(self,primitive):
		self.data = primitive

	def __getattr__(self, item):
		value = self.data.get(item,None)
		if type(value) in (list,tuple,dict):
			value = X(value)
		return value

	def __len__(self):
		return len(self.data)

	def __str__(self):
		return str(self.data)

	def __getitem__(self, item):
		value = None
		if type(self.data) in (list,tuple):
			value = self.data[item]
			if type(value) in (dict,list,tuple):
				value = X(value)
		elif type(self.data) == dict:
			value = self.__getattr__(item)
		return value


def scope_lock(lock=None):
	pass
