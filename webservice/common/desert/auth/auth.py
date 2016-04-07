
# -- coding:utf-8 --

#---------------------------------
#  TCE
#  Tiny Communication Engine
#
#  sw2us.com copyright @2012
#  bin.zhang@sw2us.com / qq:24509826
#---------------------------------

import os,os.path,sys,struct,time,traceback,time
# import tcelib as tce

	
class AuthUserInfo_t:
# -- STRUCT -- 
	def __init__(self,user_id='',user_name='',user_realname='',login_time=0,login_type=0,expire_time=0,device_id=''):
		self.user_id = user_id
		self.user_name = user_name
		self.user_realname = user_realname
		self.login_time = login_time
		self.login_type = login_type
		self.expire_time = expire_time
		self.device_id = device_id
		
	def __str__(self):
		return 'OBJECT<AuthUserInfo_t :%s> { user_id:%s,user_name:%s,user_realname:%s,login_time:%s,login_type:%s,expire_time:%s,device_id:%s}'%(hex(id(self)),str(self.user_id),str(self.user_name),str(self.user_realname),str(self.login_time),str(self.login_type),str(self.expire_time),str(self.device_id) ) 
		
	def marshall(self):
		d =''
		if type(self.user_id)==type(0) or type(self.user_id) == type(0.1): self.user_id=str(self.user_id)
		if not self.user_id: self.user_id=''
		try:
			self.user_id = self.user_id.encode('utf-8')
		except:pass
		d += struct.pack('!I', len(str(self.user_id)))
		d += str(self.user_id)
		if type(self.user_name)==type(0) or type(self.user_name) == type(0.1): self.user_name=str(self.user_name)
		if not self.user_name: self.user_name=''
		try:
			self.user_name = self.user_name.encode('utf-8')
		except:pass
		d += struct.pack('!I', len(str(self.user_name)))
		d += str(self.user_name)
		if type(self.user_realname)==type(0) or type(self.user_realname) == type(0.1): self.user_realname=str(self.user_realname)
		if not self.user_realname: self.user_realname=''
		try:
			self.user_realname = self.user_realname.encode('utf-8')
		except:pass
		d += struct.pack('!I', len(str(self.user_realname)))
		d += str(self.user_realname)
		d += struct.pack('!q',self.login_time)
		d += struct.pack('!i',self.login_type)
		d += struct.pack('!q',self.expire_time)
		if type(self.device_id)==type(0) or type(self.device_id) == type(0.1): self.device_id=str(self.device_id)
		if not self.device_id: self.device_id=''
		try:
			self.device_id = self.device_id.encode('utf-8')
		except:pass
		d += struct.pack('!I', len(str(self.device_id)))
		d += str(self.device_id)
		return d
		
	def unmarshall(self,d,idx_=0):
		idx = idx_
		try:
			__size, = struct.unpack('!I',d[idx:idx+4])
			idx+=4
			self.user_id = d[idx:idx+__size]
			idx+=__size
			__size, = struct.unpack('!I',d[idx:idx+4])
			idx+=4
			self.user_name = d[idx:idx+__size]
			idx+=__size
			__size, = struct.unpack('!I',d[idx:idx+4])
			idx+=4
			self.user_realname = d[idx:idx+__size]
			idx+=__size
			self.login_time, = struct.unpack('!q',d[idx:idx+8])
			idx+=8
			self.login_type, = struct.unpack('!i',d[idx:idx+4])
			idx+=4
			self.expire_time, = struct.unpack('!q',d[idx:idx+8])
			idx+=8
			__size, = struct.unpack('!I',d[idx:idx+4])
			idx+=4
			self.device_id = d[idx:idx+__size]
			idx+=__size
		except:
			traceback.print_exc()
			return False,idx
		return True,idx
		

