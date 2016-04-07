#coding:utf-8

__author__ = 'scott'

import datetime,time


class WebApiCallReturn:
	def __init__(self):
		self.status = 0
		self.errcode = 0
		self.errmsg = ''
		self.result = None


class CacheFieldFormatType:
	user_app_acct_hash = "user:%s:app_acct_hash"
	user_token_format = "user_token_%s"
	system_user_token_format = "sys_user_token_%s"


class PlayerInfoChangeType:
	PASSWORD = 1
	MAINLY = 2

class DatabaseSequenceDef:
	NUMBER_ID = 'seq_player_num_id'

class PlayerLoginTokenPrefix:

	PLAYER = '01'
	TRAVELER = '02'