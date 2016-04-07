#coding:utf-8
__author__ = 'scott'

import os,datetime,json,traceback

import desert
from desert.webservice import webapi
from desert.webservice.webapi import FailCallReturn,SuccCallReturn
from desert.app import BaseAppServer
import model.django.core.models as core

def player_auth_token_check(func):
	def _wrapper(request,*args,**kwargs):
		token = request.data.get('token')
		if not  token:
			return FailCallReturn(desert.errors.ErrorDefs.TokenInvalid).httpResponse()


		redis = BaseAppServer.instance().getCacheServer()
		key = 'token_%s'%token
		value = redis.get( key)
		if not value:
			return FailCallReturn(desert.errors.ErrorDefs.TokenInvalid).httpResponse()

		data = json.loads( value)

		rs = core.Player.objects.filter(num_id = data['num_id'])
		if not rs:
			return FailCallReturn(desert.errors.ErrorDefs.ObjectNotExisted).httpResponse()
		request.player = rs[0]

		return func(request,*args,**kwargs)
	return _wrapper
