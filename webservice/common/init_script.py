__author__ = 'scott'

import os,sys

# PYTHONPATH+= $common/python
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
pwd =''
PRJ_PATH = os.path.dirname(os.path.abspath(__file__))
# TCE_PATH = os.environ['TCE_PYTHON']

ETC_PATH = PRJ_PATH  +'/etc'

LIBS=(
	PRJ_PATH,
	PRJ_PATH+'../common/python',
	# TCE_PATH
)
for lib in LIBS:
	sys.path.insert(0,lib)


GLOBAL_SETTINGS_FILE = ETC_PATH + '/settings.yaml'
GLOBAL_SERVICE_FILE = ETC_PATH + '/services.xml'
GLOBAL_SERVER_EPS_FILE = ETC_PATH + '/server_eps.conf'


if __name__ == '__main__':
	print globals()