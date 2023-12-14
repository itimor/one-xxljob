# -*- coding: utf-8 -*-
# author: timor

from django.db import models
from common.models import BaseModel


class MailBot(BaseModel):
    name = models.CharField(max_length=112, unique=True, verbose_name='名称')
    host = models.CharField(max_length=112, verbose_name='主机')
    user = models.CharField(max_length=112, verbose_name='账号')
    password = models.CharField(max_length=112, verbose_name='密码')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-create_time']
        verbose_name = "邮件机器人"
        verbose_name_plural = verbose_name


class TelegramBot(BaseModel):
    name = models.CharField(max_length=112, unique=True, verbose_name='名称')
    uid = models.CharField(max_length=112, verbose_name='账号id')
    token = models.CharField(max_length=112, verbose_name='token')
    chat_id = models.CharField(max_length=112, verbose_name='chat_id')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-create_time']
        verbose_name = "tg机器人"
        verbose_name_plural = verbose_name
