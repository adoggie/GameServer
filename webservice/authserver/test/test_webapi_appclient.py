#--coding:utf-8--

# 测试系统各种服务资源，
#

# import imp
# imp.load_source('init','../init_script.py')

# from gevent import monkey
# monkey.patch_all()
# import psycogreen.gevent
# psycogreen.gevent.patch_psycopg()

import os,os.path,sys,struct,time,traceback,signal,threading,copy,base64,urllib,json
import datetime,base64
from datetime import datetime


# import  model.django.core.models as  core


import urllib2,urllib,time


"""
POST http://portal.m.jd.com/client.action?functionId=miaoShaAreaList&uuid=864387020833337-80717a921a98&clientVersion=4.4.3&build=23599&client=android&d_brand=HUAWEI&d_model=H60-L11&osVersion=4.4.2&screen=1184*720&partner=jingdong&area=2_2813_0_0&networkType=wifi&st=1458309566115&sign=19SsIC7iQ01_ioBwn2Tu3g&sv=2 HTTP/1.1
Charset: UTF-8
Accept-Encoding: gzip,deflate
Connection: close
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
User-Agent: Dalvik/1.6.0 (Linux; U; Android 4.4.2; H60-L11 Build/HDH60-L11)
Host: portal.m.jd.com
Content-Length: 26

body=%7B%22gid%22%3A26%7D&

"""
userToken ='AAAAATEAAAAEdGVzdAAAAAAAAAAAU7AjqgAAAAAAAAAAU7Bp+gAAAAUxMTExMQ=='
webserver = 'http://portal.m.jd.com'
url = webserver+'/client.action?functionId=miaoShaAreaList&uuid=864387020833337-80717a921a98&clientVersion=4.4.3&build=23599&client=android&d_brand=HUAWEI&d_model=H60-L11&osVersion=4.4.2&screen=1184*720&partner=jingdong&area=2_2813_0_0&networkType=wifi&st=1458309566115&sign=19SsIC7iQ01_ioBwn2Tu3g&sv=2'


test_case_list=[
    {'name':'user_login','webapi':'/auth/accessToken/','params':{'user':'wangdazhi','password':'111111','domain':'ylm'}},
    # {'name':'system_user_login','webapi':'/auth/accessToken/system/','params':{'user':'admin','password':'111111'}},
    # {'name':'domain','webapi':'/appserver/domain/ylm','params':None},
    # {'name':'app_acount_list','webapi':'/appserver/app-account','params':None},
    # {'name':'me','webapi':'/appserver/me','params':None},
    # {'name':'me','method':'PUT','webapi':'/appserver/me/','params':{'first_name':'nilo','last_name':'wang','email':'test@test.com','avatar':'no avatar','position':'cleaner'}},
    # {'name':'me-fetchall','webapi':'/appserver/me/fetchall','params':None},
    # {'name':'app-acct-bind','webapi':'/appserver/app-account/'},
    # {'name':'data-satisfaction','webapi':'/appserver/data/analyses/satisfaction/?'+urllib.urlencode(satisfaction),'params':None}, #GET
    {'name':'biz-model-list','method':'GET', 'webapi':'/appserver/bizmodels/','params':None}, #GET
    # {'name':'biz-model','method':'GET', 'webapi':'/appserver/bizmodels/satisfaction','params': {'type': 1 }}, #GET
    # {'name':'restricted_orguser_login','webapi':'/auth/restricted/orguser/login/','params':{'user':'wangdazhi','password':'111111','domain':'ylm'}},

    # {'name':'hippo_smtp_sendmail','webapi':'/hippo/sendmail/','params':{'mail_to':'24509826@qq.com','subject':'test-mail','content':'this is a test mail!'}},
    # {'name':'hippo_identify_image','webapi':'/hippo/identify_image/'},
    # {'name':'digest','method':'GET','webapi':'/auth/accessToken/digest', 'params': {'password': '111111'}}, #GET
]



#for case in test_case_list[1:]:
#    print 'do test:(',case['name'],')'

if True:
    headers = {

        'Charset': 'UTF-8',
        # 'Accept-Encoding': 'gzip,deflate',
        'Connection':'close',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'User-Agent': 'Dalvik/1.6.0 (Linux; U; Android 4.4.2; H60-L11 Build/HDH60-L11)',
        'Host': 'portal.m.jd.com',
        'Content-Length': 26,
    }

    opener = urllib2.build_opener()
    # request = urllib2.Request('http://baidu.com',headers=headers)
    # resp = urllib2.urlopen(url)
    req = urllib2.Request(url)
    for k,v in headers.items():
        req.add_header(k,v)
    req.add_data('body=%7B%22gid%22%3A26%7D&')
    resp = urllib2.urlopen(req)
    print resp.read()

    # print request.read()
    # r =  opener.open(request)
    # r.read()

    # request = urllib2.Request(webapi+case['webapi'], urllib.urlencode(case['params']),headers=headers)
    #
    # if 'method' in case:
    #     method = case.get('method').upper()
    # else:
    #     method = 'GET'
    #
    # if case.get('params'):
    #     if method == 'GET':
    #         request = urllib2.Request(webapi+case['webapi'] + '?' + urllib.urlencode(case['params']),headers=headers)
    #     else:
    #         request = urllib2.Request(webapi+case['webapi'], urllib.urlencode(case['params']),headers=headers)
    # else:
    #     request = urllib2.Request(webapi+case['webapi'],headers=headers)
    #
    # if method:
    #     request.get_method = lambda: method
    #
    # print opener.open(request).read()
