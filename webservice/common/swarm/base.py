#coding:utf-8

__author__ = 'scott'

import datetime,time

class AppPlatformType:
	"""
	应用类型
	"""
	Salesforce = 1
	Desk = 2


class OrgUserType:
	Admin = 1
	User = 2

class AnalysisDataModeSubtypeDef:
	SEC_OP = 0x01
	SALES_REV = 0x02
	SERV_COUNT = 0x04
	SERV_SCORE = 0x08
	SERV_DURA = 0x10

class AnalysisDataModeDef:
	"""
	分析数据模型
	"""

	class ResultType:
		DESCRIPTIVE = 1    # Report from facts
		REGRESSION = 2     # Prediction from facts with regression


	class DataMode:
		def __init__(self,name,type_,subtypes_={}, res_types_=[]):
			self.name = name
			self.type = type_
			self.subtypes = subtypes_
			self.res_types = res_types_


	satisfaction = DataMode('satisfaction',1,subtypes_={
			'sec_op': 		0x01, 		#'Second opportunity of sales'
			'sales_rev': 	0x02,   # Sales revenue
			'serv_count': 	0x04,        # Count of services
			'serv_score':	0x08,       # Service score
			'serv_dura': 	0x10         # Service duration
		},
		res_types_ = [
			{
				'type': ResultType.DESCRIPTIVE,
				'title': 'Second sales performance situation',
				'desc': 'Analysis the service data like service times and service satisfaction those can influence the '
				        'second sales opportunities and performance.',
				'created_at': time.mktime(datetime.date(2015, 9, 1).timetuple()),
				'created_by': 'system',
				'updated_at': time.mktime(datetime.date(2015, 9, 1).timetuple()),
				'labels': ['sales']
			},
			{
				'type': ResultType.REGRESSION,
				'title': 'Second sales performance correlation',
				'desc': 'Analysis of correlation between sales performance and service data like service times and '
				        'service satisfaction. You can make some prediction if the correlation exists.',
				'created_at': time.mktime(datetime.date(2015, 9, 1).timetuple()),
				'created_by': 'system',
				'updated_at': time.mktime(datetime.date(2015, 9, 1).timetuple()),
				'labels': ['sales']
			},
		])


class AnalysisTimeGranuleType:
	DAY = 1
	WEEK = 2
	MONTH = 3
	QUARTER = 4




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

