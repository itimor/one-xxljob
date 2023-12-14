# -*- coding: utf-8 -*-
# author: timor

from domains.serializers import *
from common.views import ModelViewSet, FKModelViewSet, JsonResponse, BulkModelMixin
from rest_framework.decorators import action
from common import status
from collections import OrderedDict
from core.settings import jobapi
from datetime import datetime, timedelta
from statistics import median


class CDNViewSet(BulkModelMixin):
    queryset = CDN.objects.all()
    serializer_class = CDNSerializer
    search_fields = ['name', 'code']
    filter_fields = ['name', 'code']
    ordering_fields = ['code']


class IPPoolViewSet(BulkModelMixin):
    queryset = IPPool.objects.all()
    serializer_class = IPPoolSerializer
    search_fields = ['ip']
    filter_fields = ['ip']
    ordering_fields = ['ip']

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve'] or self.resultData:
            return IPPoolReadSerializer
        return IPPoolSerializer


class BrandViewSet(BulkModelMixin):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    search_fields = ['name']
    filter_fields = ['name', 'status', 'code']
    ordering_fields = ['status']


class DomainTypeViewSet(BulkModelMixin):
    queryset = DomainType.objects.all()
    serializer_class = DomainTypeSerializer
    search_fields = ['name']
    filter_fields = ['name', 'code']
    ordering_fields = ['name']


class DomainViewSet(BulkModelMixin):
    queryset = Domain.objects.all()
    serializer_class = DomainSerializer
    search_fields = ['name']
    filter_fields = ['brand__code', 'brand', 'type', 'status']
    ordering_fields = ['type']

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve'] or self.resultData:
            return DomainReadSerializer
        return DomainSerializer


class xxljobViewSet(BulkModelMixin):
    queryset = xxljob.objects.all()
    serializer_class = xxljobSerializer
    search_fields = ['name']
    filter_fields = ['group']
    ordering_fields = ['name']

    def create(self, request, *args, **kwargs):
        instance = request.data
        payload = {
            'jobGroup': instance["group"],
            'jobDesc': instance["name"],
            'executorRouteStrategy': instance["router"],
            'jobCron': instance["jobCron"],
            'glueType': instance["type"],
            'executorHandler': None,
            'executorBlockStrategy': instance["block"],
            'childJobId': None,
            'executorTimeout': 0,
            'executorFailRetryCount': 0,
            'author': instance["author"],
            'alarmEmail': None,
            'executorParam': instance["param"],
        }
        job = jobapi.add(payload)
        instance.update({"task_id": job['content']})
        serializer = self.get_serializer(data=instance)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return JsonResponse(OrderedDict([
            ('results', instance)
        ], code=status.HTTP_200_OK))

    def perform_update(self, serializer):
        super(xxljobViewSet, self).perform_update(serializer)
        instance = serializer.data
        print(instance["group"])
        try:
            payload = {
                'id': instance["task_id"],
                'jobGroup': instance["group"],
                'jobDesc': instance["name"],
                'executorRouteStrategy': instance["router"],
                'jobCron': instance["jobCron"],
                'glueType': instance["type"],
                'executorHandler': None,
                'executorBlockStrategy': instance["block"],
                'childJobId': None,
                'executorTimeout': 0,
                'executorFailRetryCount': 0,
                'author': instance["author"],
                'alarmEmail': None,
                'executorParam': instance["param"],
            }
            jobapi.update(payload)
        except Exception as e:
            print(e)

    # 删除、启动、停止job
    @action(methods=['post'], url_path='action_task', detail=False)
    def action_task(self, request, *args, **kwargs):
        self.watch_audit_log(request)
        action = request.data['action']
        data = {'code': 200, 'msg': None, 'content': 'action is not exist'}
        try:
            task_id = request.data['task_id']
            payload = {
                'id': task_id
            }

            if action == 'remove':
                data = jobapi.remove(payload)
            elif action == 'start':
                data = jobapi.start(payload)
            elif action == 'stop':
                data = jobapi.stop(payload)
            else:
                pass
        except Exception as e:
            print(e)
        return JsonResponse(OrderedDict([
            ('results', data)
        ], code=status.HTTP_200_OK))

    # 保存job code
    @action(methods=['post'], url_path='save_code', detail=False)
    def save_code(self, request, *args, **kwargs):
        self.watch_audit_log(request)
        data = {'code': 200, 'msg': None, 'content': 'action is not exist'}
        try:
            payload = {
                'id': request.data['task_id'],
                'glueSource': request.data['code'],
                'glueRemark': 'update{}'.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            }
            data = jobapi.save(payload)
        except Exception as e:
            print(e)
            pass
        return JsonResponse(OrderedDict([
            ('results', data)
        ], code=status.HTTP_200_OK))

    # job 报表
    @action(methods=['post'], url_path='chatinfo', detail=False)
    def chatinfo(self, request, *args, **kwargs):
        self.watch_audit_log(request)
        d1 = datetime.now()
        d2 = d1 - timedelta(days=7)
        startDate = request.data.get('startDate', d2.strftime("%Y-%m-%d %H:%M:%S"))
        endDate = request.data.get('endDate', d2.strftime("%Y-%m-%d %H:%M:%S"))
        payload = {
            'startDate': startDate,
            'endDate': endDate
        }
        data = {'code': 200, 'msg': None, 'content': 'action is not exist'}
        try:
            data = jobapi.chatinfo(payload)
        except Exception as e:
            print(e)
        return JsonResponse(OrderedDict([
            ('results', data)
        ], code=status.HTTP_200_OK))

    # domain delay
    @action(methods=['post'], url_path='domain_delay', detail=False)
    def domain_delay(self, request, *args, **kwargs):
        from utils.falcon_api import FalconApi
        from utils.time import string2timestamp
        falcon = FalconApi(endpoint="http://47.56.11.71:8080", user='root', password='v5benzro-gf*TY1k')
        nodes = BoceNode.objects.all()
        hostnames = [i.name for i in nodes]
        self.watch_audit_log(request)
        domain = request.data['domain']
        start_time = string2timestamp(request.data['startDate'])
        end_time = string2timestamp(request.data['endDate'])
        counters = ["domain_boce/role=bw,srv=checkdelay,url=%s" % domain]
        query = {
            "step": 240,
            "start_time": start_time,
            "end_time": end_time,
            "hostnames": hostnames,
            "consol_fun": "AVERAGE",
            "counters": counters
        }
        r = falcon.graph.history.post(data=query)
        response = dict()
        max_value = []
        min_value = []
        median_value = []
        for i in r:
            values = []
            for v in i["Values"]:
                if v['value']:
                    values.append(v['value'] * 1000)
            max_value.append(max(values))
            min_value.append(min(values))
            median_value.append(median(values))

        response["endpoint"] = hostnames
        response["max_value"] = max_value
        response["min_value"] = min_value
        response["median_value"] = median_value
        return JsonResponse(OrderedDict([
            ('results', response)
        ], code=status.HTTP_200_OK))
