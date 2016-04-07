#coding:utf-8
__author__ = 'scott'

import os,sys,traceback,time,datetime,json

from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from rest_framework import parsers

from desert.webservice.webapi import FailCallReturn,SuccCallReturn
import desert

@api_view(['GET'])
@parser_classes( (parsers.FormParser,) )
def get_verifycode(request,format=None):
	"""
	获取验证码
	:param request:
	:param format:
	:return:
	"""
	cr = SuccCallReturn()
	try:
		image,chars = desert.image.sign_code.create_validate_code()
		code = desert.misc.getUniqueID()
		cr.assign({
			'image':image,
			'code':code
			})
		cache = desert.app.BaseAppServer.instance().getCacheServer()
		cache.set(code,chars,3600)
	except Exception,e:
		traceback.print_exc(e)
		return FailCallReturn(desert.errors.ErrorDefs.TokenInvalid).httpResponse()
	return cr.httpResponse()
