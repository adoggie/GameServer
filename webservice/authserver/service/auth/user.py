#coding:utf-8

__author__ = 'scott'

import os,sys,traceback,time,datetime,json

from django.db import connection
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from rest_framework import parsers

from desert.webservice.webapi import FailCallReturn,SuccCallReturn
import desert.webservice.webapi  as webapi
from desert import misc
import desert
from desert.app import BaseAppServer

import serializer
import model.django.core.models as core
import service.base
import service.error
from decorators import player_auth_token_check

def encryptUserPassword(passwd):
	return desert.misc.getdigest(passwd)

def createPlayerToken(player):
	prefix = service.base.PlayerLoginTokenPrefix.PLAYER
	token = ''
	if player.is_temp:
		prefix = service.base.PlayerLoginTokenPrefix.TRAVELER

	token = prefix + desert.misc.getUniqueID()+ str(player.num_id)
	token = desert.misc.getdigest(token)
	return desert.security.encrypt.encryptToken(token)

def nextSequenceIdFromFile(filename='./player_numid.seq'):
	num_id = 0
	try:
		f = open(filename)
		num_id = int(f.read())
	except:
		num_id =0
		traceback.print_exc()
	num_id+=1
	try:
		f = open(filename,'w')
		f.write(str(num_id))
	except:
		traceback.print_exc()
	return num_id


def assignPlayerUniqueNumberID():
	"""
	分配全局玩家账号ID
	"""
	if True:
		num_id = nextSequenceIdFromFile()
	else:
		num_id = desert.misc.getdbsequence_pg( connection, service.base.DatabaseSequenceDef.NUMBER_ID )
	return num_id


@api_view(['POST'])
@parser_classes( (parsers.FormParser,) )
def player_create(request, format=None):
	"""
	create new player .
	account&password&device_id
	:param request:
	:param format:
	:return:
	"""
	cr = SuccCallReturn()
	serial = serializer.PlayerCreateForm(data = request.data)
	try:
		if not serial.is_valid():
			return FailCallReturn(desert.errors.ErrorDefs.ParameterIllegal).httpResponse()
		if core.Player.objects.filter(account = request.data['account']).count():
			return FailCallReturn(desert.errors.ErrorDefs.ObjectDuplicated).httpResponse()
		num_id = assignPlayerUniqueNumberID()
		if num_id == desert.base.ValueType.NULL:
			return FailCallReturn(service.error.ErrorDefs.AssignPlayerNumberIDFailed).httpResponse()
		player = serial.save(num_id = num_id)
		player.password = encryptUserPassword(player.password)
		player.save()
		cr.assign({
			'account':player.account,
			'num_id': player.num_id,
			# 'token': token
		})
	except Exception,e:
		traceback.print_exc(e)
		return FailCallReturn(desert.errors.ErrorDefs.UserNameOrPasswordError).httpResponse()
	return cr.httpResponse()


@api_view(['POST'])
@parser_classes( (parsers.FormParser,) )
def player_login(request, format=None):
	"""

	account=fire&password=111111&device_id=4442323&sku=101&platform=1
	:param request:
	:param format:
	:return:
	"""
	cr = SuccCallReturn()
	serial = serializer.PlayerLoginForm(data = request.data)
	try:
		if not serial.is_valid():
			return FailCallReturn(desert.errors.ErrorDefs.ParameterIllegal).httpResponse()
		passwd = encryptUserPassword(request.data['password'])
		rs = core.Player.objects.filter(account=request.data['account'],password = passwd,is_temp=False)
		if not rs:
			return FailCallReturn(desert.errors.ErrorDefs.ObjectNotExisted).httpResponse()
		player = rs[0]
		device_id = request.data['device_id']
		sku = request.data['sku']
		platform = request.data['platform']

		token = createPlayerToken(player)
		log = core.PlayerLogin()
		log.player = player
		log.create_time = datetime.datetime.now()
		log.sku = sku
		log.platform = platform
		log.device_id = device_id
		log.ip_addr = request.META['REMOTE_ADDR']
		log.token = token
		log.save()

		if not core.PlayerDevice.objects.filter(player=player,device_id=device_id,sku=sku).count():
			device = core.PlayerDevice(player=player,device_id=device_id,sku = sku ,create_time = datetime.datetime.now())
			device.save()

		cr.assign(token)
		redis = BaseAppServer.instance().getCacheServer()
		key = 'token_%s'%token
		value = log.toJson()
		redis.set( key,value)
		# 通知游戏服务器用户登录

	except Exception,e:
		traceback.print_exc(e)
		return FailCallReturn(desert.errors.ErrorDefs.UserNameOrPasswordError).httpResponse()
	return cr.httpResponse()


@api_view(['POST'])
@parser_classes( (parsers.FormParser,) )
def player_quicklogin(request, format=None):
	"""
	快速登录游戏，无需提供用户账号，直接传递设备号进行游玩
	如果玩家快速登录，发现设备编号已经被注册用户使用了，则返回错误，提示用户用账号登录
	:param request:
		device_id
		sku
		platform
	:param format:
	:return:
	"""
	def createTraveler(device_id,sku):
		"""
		创建临时玩家
		"""

		player = core.Player()
		player.is_temp = True
		player.create_time = datetime.datetime.now()
		player.last_login = datetime.datetime.now()
		player.num_id = assignPlayerUniqueNumberID()
		player.account = '_' + desert.misc.getdigest( device_id + sku )
		player.password = '_' + desert.misc.getdigest( device_id + sku )
		player.device_id = device_id

		return player

	cr = SuccCallReturn()
	serial = serializer.PlayerQuickLoginForm(data = request.data)
	try:
		if not serial.is_valid():
			return FailCallReturn(desert.errors.ErrorDefs.ParameterIllegal).httpResponse()
		device_id = request.data['device_id']
		sku = request.data['sku']
		platform = request.data['platform']
		if core.PlayerDevice.objects.filter(device_id=device_id,sku = sku).count():
			return FailCallReturn(service.error.ErrorDefs.TravelerReject_DeviceHasBoundAnother).httpResponse()
		# create traveler


		rs = core.Player.objects.filter(device_id=device_id,is_temp = True)
		if rs:
			player = rs[0]
		else:
			player = createTraveler(device_id,sku)
			if player.num_id == desert.base.ValueType.NULL:
				return FailCallReturn(service.error.ErrorDefs.AssignPlayerNumberIDFailed).httpResponse()
			player.save()

		token = createPlayerToken(player)
		log = core.PlayerLogin()
		log.player = player
		log.create_time = datetime.datetime.now()
		log.sku = request.data['sku']
		log.platform = request.data['platform']
		log.device_id = request.data['device_id']
		log.ip_addr = request.META['REMOTE_ADDR']
		log.token = token
		log.save()
		cr.assign(token)
		redis = BaseAppServer.instance().getCacheServer()
		key = 'token_%s'%token
		value = log.toJson()
		redis.set( key,value)


	except Exception,e:
		traceback.print_exc(e)
		return FailCallReturn(desert.errors.ErrorDefs.UserNameOrPasswordError).httpResponse()
	return cr.httpResponse()


@api_view(['POST'])
@parser_classes( (parsers.FormParser,) )
@player_auth_token_check
def player_change_password(request,format=None):
	"""
	修改玩家登录口令
	:param request:
	:param format:
	:return:
	"""
	cr = SuccCallReturn()
	serial = serializer.PlayerChangePasswordForm(data = request.data)
	try:
		if not serial.is_valid() :
			return FailCallReturn(desert.errors.ErrorDefs.ParameterIllegal).httpResponse()
		token = request.data['token']
		old = request.data['old']
		new = request.data['new']


		old = encryptUserPassword(old)
		new = encryptUserPassword(new)
		if request.player.password != old :
			return FailCallReturn(desert.errors.ErrorDefs.PasswdIncorret).httpResponse()
		request.player.password = new
		request.player.save()

		change = core.PlayerInfoChange()
		change.player = request.player
		change.create_time = datetime.datetime.now()
		change.original = old
		change.content = new
		change.type = service.base.PlayerInfoChangeType.PASSWORD
		change.save()
	except Exception,e:
		traceback.print_exc(e)
		return FailCallReturn(desert.errors.ErrorDefs.TokenInvalid).httpResponse()
	return cr.httpResponse()



@api_view(['POST'])
@parser_classes( (parsers.FormParser,) )
@player_auth_token_check
def player_logout(request,format=None):
	"""
	修改玩家登录口令
	:param request:
	:param format:
	:return:
	"""
	cr = SuccCallReturn()
	try:
		pass
		# request.player
	except Exception,e:
		traceback.print_exc(e)
		return FailCallReturn(desert.errors.ErrorDefs.TokenInvalid).httpResponse()
	return cr.httpResponse()


@api_view(['GET'])
@parser_classes( (parsers.FormParser,) )
def digest(request,format=None):
	"""
	Md5 Encoding for the password and retrieve the salt
	:param request:
		password: Password
		salt: Not required
	:param format:
	:return:
		digest:{
			res: XXXXXXXXXXXXXX,
			salt: XXXX
		}
	"""
	cr = SuccCallReturn()
	try:
		password = request.query_params.get('password')
		salt = request.query_params.get('salt')
		if salt is None:
			salt = misc.genRandomString()

		str = misc.getdigest(salt + password)

		cr.assign({
			'digest': str,
			'salt': salt
		})
	except Exception,e:
		traceback.print_exc(e)
		return FailCallReturn(desert.errors.ErrorDefs.TokenInvalid).httpResponse()
	return cr.httpResponse()



@api_view(['GET'])
@parser_classes( (parsers.FormParser,) )
def userTypeByDeviceID(request, format=None):
	"""
	根据设备ID查询用户类型
	device_id
	:param request:
	:param format:
	:return:

	"""
	# user type return: 0 - not existed, 1 - unbound , 2 - bound
	result = 0
	cr = SuccCallReturn()
	device_id = request.query_params.get('device_id')
	try:
		if not device_id:
			return FailCallReturn(desert.errors.ErrorDefs.ParameterIllegal).httpResponse()
		rs = core.PlayerDevice.objects.filter(device_id = device_id)
		if  rs:
			device = rs[0]
			if device.player.is_temp:
				result = 1
			else:
				result = 2
		cr.assign(result)
	except Exception,e:
		traceback.print_exc(e)
		return FailCallReturn(desert.errors.ErrorDefs.UserNameOrPasswordError).httpResponse()
	return cr.httpResponse()
