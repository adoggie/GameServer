# coding=utf-8

"""
auth: sam
date: 2015/07/13
"""
import json,time
from django.db import models


class Player(models.Model):
	"""
	游戏玩家用户
	"""
	num_id = models.BigIntegerField(unique=True,db_index=True,verbose_name=u'游戏玩家唯一标识')
	account = models.CharField(max_length=40,db_index=True,unique=True,verbose_name=u'游戏玩家账号名称')
	password = models.CharField(max_length=40,db_index=True,verbose_name=u'玩家账号密码')
	create_time = models.DateTimeField(db_index=True,verbose_name=u'创建时间')
	device_id = models.CharField(max_length=200,db_index=True,verbose_name=u'注册时设备编号')
	last_login = models.DateTimeField(db_index=True,verbose_name=u'最近一次登陆时间')

	# privacy
	name = models.CharField(max_length=30,null=True,verbose_name=u'玩家姓名')
	certificate = models.CharField(max_length=30,null=True,db_index=True,verbose_name=u'身份证号')
	sex = models.SmallIntegerField(default=0,db_index=True,verbose_name=u'性别')
	phone = models.CharField(max_length=30,null=True,db_index=True,verbose_name=u'手机号')
	email = models.CharField(max_length=40,null=True,db_index=True,verbose_name=u'邮件')

	# exp and money ----
	exp = models.BigIntegerField(default=0,verbose_name=u'经验值')
	next_exp = models.BigIntegerField(default=0,verbose_name=u'升级需要的经验值')
	level = models.IntegerField(db_index=True,default=1,verbose_name=u'用户等级')
	money = models.BigIntegerField(default=0,verbose_name=u'玩家金钱数')

	is_temp = models.BooleanField(default=False,verbose_name=u'是否游客')

class PlayerDevice(models.Model):
	"""
	记录玩家玩过游戏的设备记录，一款sku可以是多个设备
	快速登录时，判别是否在此列表中，存在表示已被用户绑定，需要切换到正常用户登录，否则直接登录进游戏
	"""
	player = models.ForeignKey('Player',db_index=True)
	device_id = models.CharField(max_length=200,db_index=True,verbose_name=u'设备编号')
	sku = models.CharField(max_length=20,db_index=True,verbose_name=u'游戏类型')
	create_time = models.DateTimeField(db_index=True,verbose_name=u'登陆时间')

class PlayerProgressState(models.Model):
	"""
	记录游戏进度，便于再次启动游戏恢复之前的场景
	"""
	num_id = models.BigIntegerField(unique=True,db_index=True,verbose_name=u'游戏玩家唯一标识')
	sku = models.CharField(max_length=20,db_index=True,verbose_name=u'游戏类型')
	state = models.CharField(max_length=400,verbose_name=u'游戏进度状态json')

class PlayerLogin(models.Model):
	"""
	玩家登陆日志
	"""
	player = models.ForeignKey('Player',db_index=True)
	create_time = models.DateTimeField(db_index=True,verbose_name=u'登陆时间')
	sku = models.CharField(max_length=20,db_index=True,verbose_name=u'游戏类型')
	platform = models.SmallIntegerField(db_index=True,verbose_name=u'登陆客户端平台')
	detail = models.CharField(max_length=400,null=True)
	ip_addr = models.CharField(max_length=20,null=True)
	device_id = models.CharField(max_length=200,db_index=True,verbose_name=u'设备编号')
	token = models.CharField(max_length=500,verbose_name=u'登陆令牌')

	class Meta:
		db_table = 'log_player_login'

	def toJson(self):
		return json.dumps(
				{'num_id':self.player.num_id,
				'login_time':time.time(),
				'expire_time':time.time()+3600*24,
				'sku':self.sku,
				'platform':self.platform,
				'device_id':self.device_id
				})



class PlayerRecharge(models.Model):
	"""
	玩家充值记录
	"""
	player = models.ForeignKey('Player',db_index=True)
	create_time = models.DateTimeField(db_index=True,verbose_name=u'充值时间')
	before_value = models.BigIntegerField(db_index=True,verbose_name=u'充值前金币数量')
	confirm_value = models.BigIntegerField(db_index=True,verbose_name=u'充值之后金币数量')

	pay_money = models.IntegerField(db_index=True,verbose_name=u'实际支付金额')
	pay_type = models.SmallIntegerField(db_index=True,verbose_name=u'支付类型') # 1 - 支付宝 , 2 - 微信 , 3 - 其他
	pay_evidence = models.CharField(max_length=400,null=True,verbose_name=u'充值凭证')
	pay_time = models.DateTimeField(db_index=True,null=True,verbose_name=u'支付完成时间')
	order_num = models.CharField(max_length=60,db_index=True,verbose_name=u'订单编号')
	detail = models.CharField(max_length=300,verbose_name=u'订单描述')
	status = models.SmallIntegerField(db_index=True,verbose_name=u'订单状态') # 1 - 待支付 ， 2 - 已支付成功 , 3 - 错误
	error_code = models.SmallIntegerField(db_index=True,verbose_name=u'支付错误码')
	error_msg = models.CharField(max_length=400,null=True,verbose_name=u'支付错误描述')
	class Meta:
		db_table = 'log_player_recharge'


class PlayerInfoChange(models.Model):
	"""
	玩家信息修改记录
	"""
	player = models.ForeignKey('Player',db_index=True)
	create_time = models.DateTimeField(db_index=True,verbose_name=u'修改时间')
	original = models.TextField(null=True,verbose_name=u'未修改前用户信息')
	content = models.TextField(verbose_name=u'修改之后用户信息') # json encode
	type = models.SmallIntegerField(verbose_name=u'修改信息类型') # 1 - password, 2 - mainly

	class Meta:
		db_table = 'log_player_info_change'




class PlayerExp(models.Model):
	"""
	玩家经验值变更记录
	"""
	player = models.ForeignKey('Player',db_index=True)
	create_time = models.DateTimeField(db_index=True,verbose_name=u'充值时间')
	before_value = models.BigIntegerField(db_index=True,verbose_name=u'更改之前经验')
	confirm_value = models.BigIntegerField(db_index=True,verbose_name=u'更改之后经验')
	exp = models.IntegerField(db_index=True,verbose_name=u'获得的经验')
	detail = models.CharField(max_length=200,verbose_name=u'描述')

	class Meta:
		db_table = 'log_player_exp'
