# -*- coding: utf-8 -*-
# author: timor

from django.db import models
from common.models import BaseModel


class CDN(BaseModel):
    name = models.CharField(max_length=112, unique=True, verbose_name='CDN厂商')
    code = models.CharField(max_length=112, unique=True, verbose_name='CDN英文')
    status = models.BooleanField(default=True, verbose_name=u'状态')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-create_time']
        verbose_name = "CDN厂商"
        verbose_name_plural = verbose_name


class IPPool(BaseModel):
    cdn = models.ForeignKey(CDN, on_delete=models.CASCADE, verbose_name='CDN厂商')
    ip = models.CharField(max_length=112, unique=True, verbose_name='ip地址')

    def __str__(self):
        return self.ipaddr

    class Meta:
        ordering = ['-create_time']
        verbose_name = "边缘节点IP"
        verbose_name_plural = verbose_name


class Brand(BaseModel):
    name = models.CharField(max_length=255, unique=True, verbose_name='名称')
    code = models.CharField(max_length=112, unique=True, verbose_name='code')
    status = models.BooleanField(default=True, verbose_name=u'状态')
    keyword = models.CharField(max_length=255, verbose_name='关键字')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-create_time']
        verbose_name = "域名品牌"
        verbose_name_plural = verbose_name


class DomainType(BaseModel):
    name = models.CharField(max_length=255, unique=True, verbose_name='名称')
    code = models.CharField(max_length=112, unique=True, verbose_name='code')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-create_time']
        verbose_name = "域名类型"
        verbose_name_plural = verbose_name


class Domain(BaseModel):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, blank=True, null=True, verbose_name=u'品牌')
    type = models.ForeignKey(DomainType, on_delete=models.CASCADE, blank=True, null=True, verbose_name=u'类型')
    name = models.CharField(max_length=255, verbose_name='域名')
    status = models.BooleanField(default=True, verbose_name=u'状态')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-create_time']
        verbose_name = "域名管理"
        verbose_name_plural = verbose_name

    def save(self, *args, **kwargs):
        import re
        if re.match(r'^https?:/{2}\w.+$', self.name):
            pass
        else:
            self.name = 'http://{}'.format(self.name)
        super(Domain, self).save(*args, **kwargs)


route_type = {
    'FIRST': '第一个',
    'LAST': '最后一个',
    'ROUND': '轮询',
    'RANDOM': '随机',
    'SHARDING_BROADCAST': '分片广播',
}

glue_type = {
    'GLUE_GROOVY': 'java',
    'GLUE_SHELL': 'shell',
    'GLUE_PYTHON': 'python',
    'GLUE_PHP': 'php',
    'GLUE_NODEJS': 'nodejs',
}

block_type = {
    'SERIAL_EXECUTION': '单机串行',
    'DISCARD_LATER': '丢弃后续调度',
    'COVER_EARLY': '覆盖之前调度',
}


class xxljob(BaseModel):
    task_id = models.CharField(max_length=3, blank=True, verbose_name='task_id')
    status = models.BooleanField(default=False, verbose_name=u'启动状态')
    group = models.CharField(max_length=3, blank=True, verbose_name='执行器')
    name = models.CharField(max_length=112, unique=True, verbose_name='名称')
    router = models.CharField(max_length=20, choices=tuple(route_type.items()), default='frist', verbose_name=u'路由策略')
    jobCron = models.CharField(max_length=20, verbose_name='cron表达式')
    type = models.CharField(max_length=20, choices=tuple(glue_type.items()), default='python', verbose_name=u'GLUE类型')
    block = models.CharField(max_length=20, choices=tuple(block_type.items()), default='signle', verbose_name=u'阻塞策略')
    author = models.CharField(max_length=12, verbose_name='负责人')
    param = models.CharField(max_length=30, blank=True, verbose_name='任务参数')
    code = models.TextField(blank=True, verbose_name=u'GLUE源代码')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-create_time']
        verbose_name = "拨测任务"
        verbose_name_plural = verbose_name
