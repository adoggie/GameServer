#--coding:utf-8--


import os,os.path,sys,struct,time,traceback,signal,threading,datetime


class ErrorDefs:
	class InnerError:
		def __init__(self,errcode,errmsg=''):
			self.code = errcode
			self.msg = errmsg

	SUCC = InnerError(0,'SUCC')
	SessionExpired		= 	InnerError(1001, u'Not signed in or the session has expired.')
	InternalException 	= 	InnerError(1002, u'Internal error occurred.')
	PasswdIncorret 		=	InnerError(1003, u'Incorret password.')
	ObjectDuplicated  =	InnerError(1004, u'The Object has been taken.')
	UserNameOrPasswordError  =	InnerError(1005, u'Username / password combination is incorrect.')
	PermissionDenied	=	InnerError(1006, u'Permission denied.')
	ParameterIllegal	= 	InnerError(1007, u'Invalid parameter(s).')
	ObjectNotExisted	= 	InnerError(1008, u'Object does not exists.')
	TokenInvalid = InnerError(1009, u'TokenInvalid')



def generateErrorTypesToJavascript():
	"""
	为javascript开发 转换错误类型
	"""
	jsfile = 'ErrorDefs.js'
	f = open(jsfile,'w')

	pass


