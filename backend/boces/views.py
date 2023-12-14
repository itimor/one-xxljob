# -*- coding: utf-8 -*-
# author: timor


from rest_framework.views import APIView
from rest_framework import exceptions
from rest_framework.response import Response
from core.settings import xxljob_db_info
from utils.xxljob_api_by_mysql import MYSQL


class get_group(APIView):
    def get(self, request, *args, **kwargs):
        ret = {'code': 1000, 'msg': "success"}
        try:
            sql = "select * from xxl_job_group"
            db = MYSQL(xxljob_db_info, sql)
            data = db.select()
            rep_data = []
            for item in data:
                try:
                    address_list = item[5].split(',')
                except:
                    if item[5] is None:
                        address_list = ''
                    else:
                        address_list = item[5].split()
                json_data = {
                    "id": item[0],
                    "app_name": item[1],
                    "title": item[2],
                    "order": item[3],
                    "address_type": item[4],
                    "address_list": address_list,
                }
                rep_data.append(json_data)
            ret['results'] = rep_data
        except exceptions as e:
            ret['code'] = 500
            ret['msg'] = "error"
        return Response(ret)


class create_group(APIView):
    def post(self, request, *args, **kwargs):
        ret = {'code': 1000, 'msg': "success"}
        data = request.data
        id_sql = 'select * from xxl_job_group order by id desc limit 1'
        db = MYSQL(xxljob_db_info, id_sql)
        a = db.select()
        auto_increment_id = a[0][0] + 1
        try:
            sql = "INSERT INTO xxl_job_group VALUES \
                (%s, '%s', '%s', '%s', '%s', '%s' )" % \
                  (auto_increment_id, data['app_name'], data['title'], data['order'], data['address_type'],
                   data['address_list'])
            db = MYSQL(xxljob_db_info, sql)
            ret['results'] = db.insert()
        except exceptions as e:
            ret['code'] = 500
            ret['msg'] = "error"
        return Response(ret)


class update_group(APIView):
    def post(self, request, *args, **kwargs):
        ret = {'code': 1000, 'msg': "success"}
        data = request.data
        try:
            sql = "UPDATE xxl_job_group SET \
                    app_name = '%s', \
                    title = '%s', \
                    address_type = '%s', \
                    address_list = '%s' \
                    WHERE ID = %s" % \
                  (data['app_name'], data['title'], data['address_type'], data['address_list'], data['id'])
            db = MYSQL(xxljob_db_info, sql)
            ret['results'] = db.update()
        except exceptions as e:
            ret['code'] = 500
            ret['msg'] = "error"
        return Response(ret)


class delete_group(APIView):
    def post(self, request, *args, **kwargs):
        ret = {'code': 1000, 'msg': "success"}
        data = request.data
        try:
            sql = "DELETE FROM xxl_job_group WHERE ID=%d" % data['id']
            db = MYSQL(xxljob_db_info, sql)
            ret['results'] = db.update()
        except exceptions as e:
            ret['code'] = 500
            ret['msg'] = "error"
        return Response(ret)


class get_code_by_id(APIView):
    def post(self, request, *args, **kwargs):
        ret = {'code': 1000, 'msg': "success"}
        data = request.data
        try:
            sql = "SELECT * FROM xxl_job_info WHERE ID=%s" % data['task_id']
            db = MYSQL(xxljob_db_info, sql)
            ret['results'] = db.select()[0][15]
        except exceptions as e:
            ret['code'] = 500
            ret['msg'] = "error"
        return Response(ret)


class get_code_history_by_id(APIView):
    def post(self, request, *args, **kwargs):
        ret = {'code': 1000, 'msg': "success"}
        data = request.data
        try:
            sql = "SELECT * FROM xxl_job_logglue WHERE job_id=%s order by add_time desc" % data['task_id']
            db = MYSQL(xxljob_db_info, sql)
            data = db.select()
            rep_data = []
            for item in data:
                json_data = {
                    "id": item[0],
                    "glue_source": item[3],
                    "glue_remark": item[4],
                    "add_time": item[5],
                }
                rep_data.append(json_data)
            ret['results'] = rep_data
        except exceptions as e:
            ret['code'] = 500
            ret['msg'] = "error"
        return Response(ret)


class get_log_count(APIView):
    def get(self, request, *args, **kwargs):
        ret = {'code': 1000, 'msg': "success"}
        try:
            from datetime import datetime, timedelta
            end_date = datetime.now()
            start_date = end_date - timedelta(days=7)
            d = start_date.strftime("%Y-%m-%d") + " 00:00:00"
            sql = "select count(*) from xxl_job_log where handle_time>'%s'" % d
            db = MYSQL(xxljob_db_info, sql)
            data = db.select()
            ret['results'] = data[0][0]
        except exceptions as e:
            ret['code'] = 500
            ret['msg'] = "error"
        return Response(ret)
