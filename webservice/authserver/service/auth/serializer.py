#coding:utf-8

__author__ = 'scott'

from django.db import  connection

from rest_framework import  serializers
from model.django.core import models as core
import datetime
import desert
import service





class PlayerCreateForm(serializers.Serializer):
	account = serializers.CharField(max_length=40,min_length=4)
	password = serializers.CharField(min_length=4,max_length=20)
	device_id = serializers.CharField(max_length=100,required=True)
	name = serializers.CharField(max_length=30,required=False)
	sex = serializers.IntegerField(required=False)
	email = serializers.EmailField(required=False)


	def create(self, validated_data):
		player = core.Player(**validated_data)
		player.last_login = datetime.datetime.now()
		player.create_time = datetime.datetime.now()
		player.num_id = validated_data['num_id']
		return player


	def update(self, instance, validated_data):
		pass



class PlayerLoginForm(serializers.Serializer):
	account = serializers.CharField(max_length=40,min_length=4)
	password = serializers.CharField(min_length=4,max_length=20)
	device_id = serializers.CharField(max_length=100)
	sku = serializers.CharField(max_length=30)
	platform = serializers.IntegerField()

class PlayerQuickLoginForm(serializers.Serializer):
	device_id = serializers.CharField(max_length=100)
	sku = serializers.CharField(max_length=30)
	platform = serializers.IntegerField()


class PlayerChangePasswordForm(serializers.Serializer):
	token = serializers.CharField(max_length=200)
	old = serializers.CharField(min_length=4,max_length=30)
	new = serializers.CharField(min_length=4,max_length=30)