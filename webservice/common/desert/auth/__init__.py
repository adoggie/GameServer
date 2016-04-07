__author__ = 'zhangbin'

from auth import AuthUserInfo_t
from desert.security import encrypt

def decodeUserToken( token):
	data = encrypt.decryptToken(token)
	# user_info = AuthUserInfo_t()
	# succ, = user_info.unmarshall( d )
	# if not succ:
	# 	return None
	return data

def encodeUserToken( userinfo):
	# d = user_info.marshall()
	token = encrypt.encryptToken(userinfo)
	return token