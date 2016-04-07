# -*- coding: UTF-8 -*-

import traceback,os,sys,time,os.path
import copy


from desert import config
from desert import  logging
class BaseAppServer:

	LOGCLS = logging.Logger

	def __init__(self,name):
		self.name = name
		self.yamlcfg = None
		self.servicefile = None
		self.conf = None
		self.communicator = None
		self.cache = None
		self.mongo = None
		self.fs = None
		BaseAppServer._handle = self

		self.NOSQL_ENABLE = 1
		self.CACHE_ENABLE = 1
		self.RPC_ENABLE = 1
		self.logger = logging.Logger()

	def getLogger(self):
		return self.logger

	def getName(self):
		return self.name

	def getConfig(self):
		return self.conf

	def getYamlConfig(self):
		return self.yamlcfg

	def getModuleConfig(self,name):
		conf = self.yamlcfg.get(name)
		return conf

	def preInitialize(self):
		'''
		拾取参数 - name

		'''
		argv = copy.deepcopy(sys.argv)
		try:
			while argv:
				p = argv.pop(0).strip().lower()
				if p =='-name':
					name = argv.pop(0)
					self.name = name
		except:
			traceback.print_exc()

	def init(self,yamfile,servicefile=''):
		self.preInitialize()
		self.yamlcfg = config.YamlConfigReader(yamfile).props
		self.servicefile = servicefile
		self.conf = self.yamlcfg.get(self.name)
		if self.RPC_ENABLE:
			self.initRpc()
		if self.NOSQL_ENABLE:
			self.initNosql()
		if self.CACHE_ENABLE:
			self.initCache()

	def initNosql(self):
		from desert.nosql import mongo

		cfg = self.yamlcfg[self.conf.get('mongodb')]
		if cfg:
			self.mongo = mongo.Connection(cfg['database'],host=cfg['host'],port=cfg.get('port',27017))
			self.fs = mongo.Connection('fs',host=cfg['host'],port=cfg.get('port',27017))

	def initCache(self):
		from desert.nosql import rediscache

		cfg = self.yamlcfg[self.conf.get('redis')]
		if cfg:
			self.cache = rediscache.RedisServer(host=cfg['host'])


	def initRpc(self):
		import tcelib as tce
		self.communicator = tce.RpcCommunicator().instance()
		if self.servicefile:
			self.communicator.init(self.name).initMessageRoute(self.servicefile)


	def run(self):
		print 'Service [%s] started..'%self.name

	def getEndPoint(self,name):
		return self.communicator.currentServer().findEndPointByName(name)

	def getEndPointConnection(self,name):
		return self.getEndPoint(name).impl

	def setRpcMQCircuit(self,conn_call,conn_back):
		if isinstance(conn_call,str):
			conn_call = self.getEndPointConnection(conn_call)
		if isinstance(conn_back,str):
			conn_back = self.getEndPointConnection(conn_back)
		conn_call.setLoopbackMQ(conn_back)

	def getFS(self):
		return self.fs

	def getNoSQLDB(self):
		return  self.mongo

	def getCacheServer(self):
		return self.cache

	getRedis = getCacheServer

	_handle = None
	@classmethod
	def instance(cls):
		if not cls._handle :
			cls._handle = cls()
		return cls._handle


if __name__ == '__main__':
	pass #send_sms("13916624477","老张,新年快乐诶!!!")