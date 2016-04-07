#coding:utf-8

from django.conf.urls import patterns, include, url

from rest_framework.routers import  DefaultRouter

import service
# router = DefaultRouter()
# router.register(r'WEBAPI/appserver/app-account',UserAppViewSet,'account')	#第三方账号绑定
# router.register(r'WEBAPI/appserver/data/analyses', service.swarm.data.DataAnalysesViewSet,'data')	#第三方账号绑定
# router.register(r'WEBAPI/appserver/bizmodels', service.swarm.bizmodel.BizModelViewSet,'bizmodel')	#模型视图

domain_pattern = '[a-zA-Z0-9][-a-zA-Z0-9]{0,62}'
urlpatterns = patterns('',

	url(r'^api/auth/user/create/$',service.auth.user.player_create,name='player_create'),
	url(r'^api/auth/user/login/$',service.auth.user.player_login),
	url(r'^api/auth/user/quicklogin/$',service.auth.user.player_quicklogin),
	url(r'^api/auth/user/logout/$',service.auth.user.player_logout),
	url(r'^api/auth/user/change_password/$',service.auth.user.player_change_password),
	url(r'^api/auth/verifycode/$',service.auth.verifycode.get_verifycode),

	url(r'^api/auth/user/type/$',service.auth.user.userTypeByDeviceID),

	# url(r'^api/auth/token/detail/$',service.auth.token.decode_user_token,name='token_detail'),


)

# urlpatterns += router.urls
# print urlpatterns