#!/usr/bin/env python
# coding: utf8

import requests
import json
import socket
import re

import sys
reload(sys)
sys.setdefaultencoding('utf8')

###########################配置从这里开始##########################################
args = sys.argv[1].split(',')

##拨测域名数据自动聚合脚本：动态更新数据聚合规则；
##使用方式 python xx.py {role} {srv} {step} #示例：python xx.py web checkdns 120
# step:拨测频率间隔(整数，默认单位为秒)
step = args[1]

# srv_list: 拨测标签(checknetwork|checkdns|checkcontent）
srv_list = ['checknetwork', 'checkdns', 'checkcontent']
# 获取域名列表接口
# api url
api_url = 'http://aaa/api'

# 域名品牌
brand = args[0]

brand_req = requests.get(api_url + '/domain/brand/?code={}'.format(brand)).json()["results"][0]

# 域名列表
domain_req = requests.get(api_url + '/domain/domain/?brand__code={}'.format(brand)).json()
domain_list = [item["name"] for item in domain_req["results"]]

# 域名分类,aoa|kok
role = brand_req["code"]


class CheckSum(object):
    def __init__(self, url, role, srv):
        self.url = url
        self.role = role
        self.srv = srv

    # 创建hostgroup aggregator规则,注意接口名称与获取aggid时不同:aggregator
    def createSumRule(self):
        falcon_header = conn.getFalconHeader()
        payload = {
            "tags": "role={},srv={},url={}".format(role, srv, url),
            "step": int(step),
            "numerator": "$(domain_boce/role={},srv={},url={})".format(role, srv, url),
            "metric": "kk_boce_sum",
            "hostgroup_id": 1,
            "endpoint": "kk_boce_cluster",
            "denominator": "1"
        }
        params = {
            'url': 'http://{}/api/v1/aggregator'.format(falcon_api),
            'headers': falcon_header,
            'timeout': 5,
            'json': payload
        }

        resp = s.post(**params)
        print(resp.text)
        return resp.text

    # 检查hostgroup aggregator规则是否存在
    def checkSumRule(self):
        sum_conn = CheckSum(url, role, srv)
        agg_list = conn.getAggId()
        keyword = "$(domain_boce/role={},srv={},url={})".format(role, srv, url)
        if keyword not in agg_list:
            sum_conn.createSumRule()

    def main(slef):
        try:
            sum_conn.checkSumRule()
        except Exception as e:
            print(url, e)
            pass


class OpenFalcon(object):
    def __init__(self, login_url, user, passwd):
        self.login_url = login_url
        self.user = user
        self.passwd = passwd

    # 获取open-falcon session，返回falcon headeres
    def getFalconHeader(self):
        login_res = s.post(url=login_url, data={'name': user, 'password': passwd})
        sig = json.loads(login_res.text)
        sig = sig['sig']
        api_token = '{"name":"' + user + '", "sig":"' + sig + '"}'
        falcon_header = {
            "Apitoken": api_token,
            "X-Forwarded-For": "127.0.0.1",
            "Content-Type": "application/json",
            "name": user,
            "sig": sig
        }
        return falcon_header

    # 获取hostgroup aggregator规则,注意接口名称:aggregators
    def getAggId(self):
        falcon_header = conn.getFalconHeader()
        params = {
            'url': 'http://127.0.0.1:8080/api/v1/hostgroup/1/aggregators',
            'headers': falcon_header,
            'timeout': 30
        }
        resp = s.get(**params)
        _resp = [data['numerator'] for data in json.loads(resp.text)['aggregators']]
        return _resp


if __name__ == '__main__':
    # open-falcon配置
    user = 'root'
    passwd = '123456'
    login_url = 'http://127.0.0.1:8080/api/v1/user/login'
    falcon_api = '127.0.0.1:8080'
    # 拨测节点主机名
    endpoint = socket.gethostname()

    s = requests.Session()
    conn = OpenFalcon(login_url, user, passwd)

    # 生成数据聚合规则
    for srv in srv_list:
        for item in domain_list:
            if re.match(r'^https?:/{2}\w.+$', item):
                url = '{}'.format(item)
            else:
                url = 'http://{}'.format(item)
            sum_conn = CheckSum(url, role, srv)
            sum_conn.main()

    print("执行的主机：", endpoint)
    print("脚本位置：", sys.argv[0])
    print("任务参数：", sys.argv[1])
    print("分片序号：", sys.argv[2])
    print("分片总数：", sys.argv[3])
    exit(0)