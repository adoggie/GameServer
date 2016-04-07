# -- coding:utf-8 --

__author__ = 'scott'


import cipher

# def encryptUserToken(auth):
# 	'''
# 		auth - AuthResult_t
#
# 	'''
# 	d = auth.marshall()
# 	token = cipher.encryptToken(d)
# 	return token
#
# def decryptUserToken(token):
# 	'''
# 		return :  AuthResult_t
# 	'''
# 	import service.lemon_impl
# 	d = utils.cipher.decryptToken(token)
# 	auth = service.lemon_impl.AuthResult_t()
# 	# d = utils.misc.hashobject2(auth)
#
# 	succ,code = auth.unmarshall(d)
# 	# auth = None
# 	if not succ:
# 		auth = None
# 	return auth

def encryptPassword(psw,salt=None):
	"""
	   加密口令 MD/SHA + SALT
	"""
	return psw

def encryptID(id):
	"""
	加密ID,防止仿冒id导致的非法数据操作
	id 可以是STRING，INTEGER类型
	"""
	id= str(id)
	return id

def decryptID(id):

	return id


def decryptToken(token):
	"""
	token - plain text (base64)
	"""
	return cipher.decryptToken(token)


def encryptToken(d):
	return cipher.encryptToken(d)