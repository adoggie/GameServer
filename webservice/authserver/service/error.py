#coding:utf-8
__author__ = 'scott'

import desert

class ErrorDefs(desert.errors.ErrorDefs):
	InnerError = desert.errors.ErrorDefs.InnerError

	TravelerReject_DeviceHasBoundAnother = InnerError(5001,u" TravelerReject_DeviceHasBoundAnother ,游客登录拒绝:设备已绑定玩家")
	AssignPlayerNumberIDFailed = InnerError(5002,u"AssignPlayerNumberIDFailed 分配用户标识号失败")

