# -*- coding: utf-8 -*-
# author: timor

from domains.models import *
from rest_framework import serializers
from utils.verifys import is_domain, is_ip


class CDNSerializer(serializers.ModelSerializer):
    class Meta:
        model = CDN
        fields = '__all__'


class IPPoolReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = IPPool
        fields = '__all__'
        depth = 1


class IPPoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = IPPool
        fields = '__all__'

    def create(self, validated_data):
        ip = validated_data.get('ip')
        if is_ip(ip):
            obj = IPPool.objects.create(**validated_data)
        else:
            raise Exception('%s 非有效ip' % ip)
        return obj

    def update(self, instance, validated_data):
        ip = validated_data.get('ip')
        if is_ip(ip):
            instance = validated_data
        else:
            raise Exception("非有效ip")
        instance.save()
        return instance


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class DomainTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DomainType
        fields = '__all__'


class DomainReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domain
        fields = '__all__'
        depth = 1


class DomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domain
        fields = '__all__'


class xxljobSerializer(serializers.ModelSerializer):
    class Meta:
        model = xxljob
        fields = '__all__'
