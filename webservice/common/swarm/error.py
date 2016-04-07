#coding:utf-8
__author__ = 'scott'

import desert

class ErrorDefs:
	InnerError = desert.errors.ErrorDefs.InnerError
	# class InnerError:
	# 	def __init__(self,errcode,errmsg=''):
	# 		self.code = errcode
	# 		self.msg = errmsg

	SUCC = InnerError(0,'')
	AppUnAuthorized	= 	InnerError(5001,u'app未授权')
	DataInProcessing	= 	InnerError(5002,u'请求处理中')
