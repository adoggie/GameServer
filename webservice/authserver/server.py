#--coding:utf-8--


import imp,os,sys,traceback

PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append('%s/../common'%PATH)
import init_script

import django
if hasattr(django,'setup'):
	django.setup()

from gevent import monkey

# monkey.patch_all()



from project import settings
if settings.datebase_is_pgsql():
	import psycogreen.gevent
	psycogreen.gevent.patch_psycopg()


import desert
from desert import app
from gevent.pywsgi import WSGIServer
from django.core.handlers.wsgi import WSGIHandler
import service.config
import getopt




class ServerApp( app.BaseAppServer ):
	app.BaseAppServer.init_script = init_script

	def __init__(self,name):
		app.BaseAppServer.__init__(self,name)

	def initRpc(self):
		return

	def initNosql(self):
		return
		# app.BaseAppServer.initNosql(self)
		desert.nosql.database = self.mongo.db
		pass

	def initCache(self):
		app.BaseAppServer.initCache(self)
		pass

	def initDatabase(self):
		if not settings.datebase_is_pgsql():
			return
		cfg = self.yamlcfg[self.conf.get('postgresql')]
		if cfg:
			dbname = cfg['dbname']
			host = cfg['host']
			port = cfg['port']
			user = cfg['user']
			passwd = cfg['passwd']
			settings.DATABASES['default']['NAME'] = dbname
			settings.DATABASES['default']['USER'] = user
			settings.DATABASES['default']['PASSWORD'] = passwd
			settings.DATABASES['default']['HOST'] = host
			settings.DATABASES['default']['PORT'] = port

	def initLogs(self):
		cfg = self.conf.get('log')
		if cfg:
			value = cfg.get('stdout')
			if value :
				self.getLogger().addHandler( app.BaseAppServer.LOGCLS.StdoutHandler(sys.stdout))
			value = cfg.get('file')
			if value:
				self.getLogger().addHandler(app.BaseAppServer.LOGCLS.FileHandler(value))
			value = cfg.get('dgram')
			if value:
				self.getLogger().addHandler(app.BaseAppServer.LOGCLS.DatagramHandler(value))
		if self.getLogger().handlers:
			sys.stdout = self.getLogger()

	def run(self):

		service.config.initialize(self)
		self.init(init_script.GLOBAL_SETTINGS_FILE,init_script.GLOBAL_SERVICE_FILE)

		self.initLogs()
		# self.initDatabase()

		#- init http service
		cfg = self.conf['http']
		host= cfg['host']
		if not host:
			host = ''
		address = (host,cfg['port'])
		ssl = cfg['ssl']
		app.BaseAppServer.run(self)
		if ssl:
			print 'Webservice Serving [SSL] on %s...'%str(address)
			WSGIServer(address, WSGIHandler(),keyfile=cfg['keyfile'],certfile=cfg['certfile']).serve_forever()
		print 'WebService serving on %s...'%str(address)
		WSGIServer(address, WSGIHandler()).serve_forever()


def usage():
	pass

if __name__ == '__main__':
	"""
	server.py
		-h help
		-n xxx
		--name=xxx
	"""

	servername = 'auth_server'
	try:
		options,args = getopt.getopt(sys.argv[1:],'hn:',['help','name='])
		for name,value in options:
			if name in ['-h',"--help"]:
				usage()
				sys.exit()
			if name in ('-n','--name'):
				servername = value
		print 'server name:',servername
		ServerApp(servername).run()
	except:
		traceback.print_exc()
		sys.exit()
