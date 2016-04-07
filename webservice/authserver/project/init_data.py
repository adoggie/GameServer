# -- coding:utf-8 --
import os
import sys,datetime

PATH = os.path.dirname(os.path.abspath(__file__))

LIBS=(
	PATH+'/../../common/',
)
for lib in LIBS:
	sys.path.insert(0,lib)



os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

from model.django.core import models as core
from desert.misc import X,genUUID,getdigest,genRandomString

USER_TYPE_ADMIN = SYS_USER_TYPE_ADMIN = 1
USER_TYPE_NORMAL = 2

sf_auth_uri = 'https://login.salesforce.com/services/oauth2/authorize?response_type=code&client_id=3MVG9ZL0ppGP5UrBaWfLJxKHPpqFQHGY1G4ViJZxYd.GypuWOEfF_.BiAGwhHNUk1mB_KuJGdyWLT5kJvOHuh&redirect_uri=http%3a%2f%2flocalhost%3a8001%2foauth&state=first'

def_sys_users = [
	{
		'user_name': 'admin',
		'user_type': SYS_USER_TYPE_ADMIN,
		'password': '111111'
	}
]

def_apps = {
	1:{'name':u'salesforce','type':1,'is_active':True, u'auth_uri': '/desk/ap/sflogin.do', u'auth_param': ''} ,
	2:{'name':u'desk','type':2,'is_active':True, u'auth_uri': '/desk/ap/desklogin.do', u'auth_param': 'site=%s'} ,
	# 3:{'name':u'twitter','type':3,'is_active':True, } ,
}

def_models = [
	{'name':'satisfaction','type':1,'comment':u'满意度调查','apps':[1,2]}
]

def_clients=[
	{'domain':'ylm','name':u'尤丽美','address':u'上海徐汇区虹桥路200号','zipcode':u'2001234','country':u'china','create_date':datetime.datetime.now(),
		'models':[1,],
		'users':[
			{'user_name':u'wangdazhi','user_type':USER_TYPE_ADMIN,'password':111111,'first_name':u'dazhi','last_name':u'wang',
			'email':u'wangdazhi@ylm.com',
				'apps':[
					{'type':1,'app_user_name':u'wangdazhi@ylm.com'},
					{'type':2,'app_user_name':u'wangdazhi@qq.com'}
				]
			},
			{'user_name':u'xiaoxin','user_type':USER_TYPE_NORMAL,'password':111111,'first_name':u'xin','last_name':u'xiao',
			'email':u'xiaoxin@ylm.com',
				'apps':[
					{'type':1,'app_user_name':u'xiaoxin@ylm.com'},
					{'type':2,'app_user_name':u'xiaoxin@qq.com'}
				]
			},

		]
	}
]


def clearup():
	core.SystemUser.objects.all().delete()
	core.OrgUserAppConfig.objects.all().delete()
	core.OrgUser.objects.all().delete()
	core.Orgnization.objects.all().delete()
	core.Application.objects.all().delete()
	core.AnalysisDataModel.objects.all().delete()

def init_database():
	clearup()

	for user in def_sys_users:
		sys_user = X(user)
		print sys_user.user_name
		salt = 	genRandomString()
		password = getdigest(salt + sys_user.password)

		curTime = datetime.datetime.now()
		userObj = core.SystemUser(user_name = sys_user.user_name,
		                          user_type = sys_user.user_type,
		                          password = password,
		                          salt = salt,
		                          create_date = curTime,
		                          login_time = curTime,
		                          is_active = True
		                          )
		userObj.save()

	for key,app  in def_apps.items():
		app = X(app)
		core.Application(name=app.name,
		                 type=app.type,
		                 is_active=app.is_active,
		                 auth_uri=app.auth_uri,
		                 auth_param=app.auth_param).save()

	biz_models = []
	for model in def_models:
		model = X(model)
		apps = []
		dbo = core.AnalysisDataModel(name = model.name,type = model.type,comment=model.comment)
		dbo.save()
		for app_id in model.apps:
			app = core.Application.objects.get(type = app_id)
			dbo.apps.add(app)
		# print dbo.apps.all()
		biz_models.append(dbo)

	for client in def_clients:
		c = X(client)
		org = core.Orgnization(domain=c.domain,name=c.name,create_date=datetime.datetime.now(),
					employee = 1,phone='13916624477')
		org.save()

		# print client
		for user in c.users:
			print user.user_name
			salt = genRandomString()
			password = '111111'
			password = getdigest( salt + password)
			user_obj = core.OrgUser(org= org,user_type=user.user_type,user_name=user.user_name,password=password,
				first_name= user.first_name,last_name=user.last_name,alias=u'',
				middle_name='mairo',position='sales manager',
				email=user.email,create_date = datetime.datetime.now(),
				is_active = True,login_time= datetime.datetime.now(),salt=salt
			)
			user_obj.save()
			for app in user.apps:
				app_type = core.Application.objects.get(type = app.type)
				app_obj = core.OrgUserAppConfig(app = app_type,user = user_obj,is_active = True,
					app_access_token=genUUID(),
					app_instance_url=u'http://sf.com/instance_url',
					app_user_id = u'2313123123124214',
					app_user_name = app.app_user_name,
					app_auth_time = datetime.datetime.now()
				)
				app_obj.save()

		for m in biz_models:
			org.data_models.add(m)



if __name__ == "__main__":
	try:
		init_database()
	except Exception as e:
		print e