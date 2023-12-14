#!/usr/bin/env python
# coding: utf8
import requests
import socket
import time

import sys
reload(sys)
sys.setdefaultencoding('utf8')

##域名拨测任务自动更新脚本;

##################################################################################
###########################配置从这里开始##########################################
args = sys.argv[1].split(',')
# xxl-job jobid,在UI上查看(web)
jobid = args[0]
# 拨测频率
step = args[2]

# api url
api_url = 'http://boce.bjshxg.com/api'

# 域名品牌
brand = args[1]

brand_req = requests.get(api_url + '/domain/brand/?code={}'.format(brand)).json()["results"][0]

# 内容劫持关键字
keywords = brand_req["keyword"].split('|')
keywords = brand_req["keyword"].split('|')

# 域名分类,官网:web,h5:h5,app下载:appdown,代理:agent
role = brand_req["code"]

# 域名列表
domain_req = requests.get(api_url + '/domain/domain/?brand__code={}&status=true'.format(brand_req["code"])).json()
domain_list = [item["name"] for item in domain_req["results"]]

# cdn ip池
cdn_req = requests.get(api_url + '/domain/ipool/').json()
cdn_list = [item["ip"] for item in cdn_req["results"]]

task_source = """#!/usr/bin/env python
#coding: utf8
#version: 0.1
##依赖python3.6+
##代理域名健康检测，代理域名先过云盾，再过创宇，云盾未作防护，要在创宇加白，所有拨测节点IP要在创宇域名分组加白
##代理域名内容劫持关键字：keyword='亚博' 按需修改

import requests
import threading
import time
import Queue
import random
import json
import socket
import IPy
from datetime import datetime

import sys
reload(sys)
sys.setdefaultencoding('utf8')

#域名品牌分类， huohu|kok
domain_type = "%s"
#内容劫持关键字
keywords = %s
# 拨测频率
step = %s
#域名列表
domain_list = %s
#cdn ip池
cdn_list = %s

'''ua'''
user_agent_list = [
    "NetworkBench/5.1.5.63"
    ]
user_agent = random.choice(user_agent_list)
headers = {'user-agent': user_agent}

class myThread(threading.Thread):
    def __init__(self,name,q):
        threading.Thread.__init__(self)
        self.name = name
        self.q = q
    def run(self):
        print("Starting " + self.name)
        while True:
            try:
                checkDomain(self.name,self.q)
            except:
                break
        print("Exiting " + self.name)


def checkDomain(threadName,q):
    url = q.get(timeout=2)
    try:
        r = requests.get(url,headers=headers,stream=True,timeout = 4)
        print(q.qsize(),threadName,url)
        network_value = 0
        try:
            srv_ip = r.raw._connection.sock.getpeername()[0]
            for ipaddr in cdn_list:
                if srv_ip in IPy.IP('{}'.format(ipaddr)):
                    dns_value = 0
                    break
                else:
                    dns_value = 1
        except:
            dns_value = 1
        try:
            for keyword in keywords:
                if keyword in r.text:
                    content_value = 0
                    break
                else:
                    content_value = 1
        except:
            content_value = 1

    except Exception as e:
        print(url,e)
        usedTime = None
        network_value = 1
        dns_value = None
        content_value = None



    '''网络检测数据'''
    falcon_network_format = {
    'Metric': 'domain_boce',
    'Endpoint': endpoint,
    'Timestamp': timestamp,
    'Step': step,
    'Value': network_value,
    'CounterType': falcontype,
    'TAGS': 'url={},role={},srv=checknetwork'.format(url,domain_type)
    }
    push_data.append(falcon_network_format)

    '''dns劫持检测数据'''
    falcon_dns_format = {
    'Metric': 'domain_boce',
    'Endpoint': endpoint,
    'Timestamp': timestamp,
    'Step': step,
    'Value': dns_value,
    'CounterType': falcontype,
    'TAGS': 'url={},role={},srv=checkdns'.format(url,domain_type)
    }
    push_data.append(falcon_dns_format)

    '''内容劫持检测数据'''
    falcon_content_format = {
    'Metric': 'domain_boce',
    'Endpoint': endpoint,
    'Timestamp': timestamp,
    'Step': step,
    'Value': content_value,
    'CounterType': falcontype,
    'TAGS': 'url={},role={},srv=checkcontent'.format(url,domain_type)
    }
    push_data.append(falcon_content_format)



def pushData():
    threadList = []
    for i in range(0,20):
        listname = 'Thread-' + str(i)
        threadList.append(listname)
    workQueue = Queue.Queue(100) 
    threads = []
    for tName in threadList:
        thread = myThread(tName,workQueue)
        thread.start()
        threads.append(thread)
    for url in domain_list:
        workQueue.put(url)
    for t in threads:
        t.join()

    try:
        #print(json.dumps(push_data, sort_keys=True, indent=4))
        r = requests.post(open_falcon_api, data=json.dumps(push_data))
        print(r.text)        
    except Exception as e:
        pass   

if __name__ == '__main__':
    '''open-falcon'''
    endpoint = socket.gethostname()
    timestamp = int(time.time())
    open_falcon_api = 'http://127.0.0.1:1988/v1/push'
    falcontype = 'GAUGE'
    push_data =[]

    pushData()
    exit(0)
"""


class XXLJOB:
    def __init__(self, xxljob_info):
        self.api_url = xxljob_info["api_url"]
        self.username = xxljob_info["username"]
        self.password = xxljob_info["password"]
        # 定义请求header
        self.headers = {'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'}
        # 获取cookies
        self.cookies = self.login()

    def request(self, uri, payload=None, method="POST"):
        url = self.api_url + uri
        if method == "POST":
            req = requests.post(url=url, data=payload, headers=self.headers, cookies=self.cookies)
        else:
            req = requests.get(url=url, cookies=self.cookies)
        return req.json()

    def login(self):
        uri = '/login'
        payload = {
            "userName": self.username,
            "password": self.password,
            "ifRemember": "on"
        }
        req = requests.post(self.api_url + uri, data=payload, headers=self.headers)
        return req.cookies

    def save(self, payload):
        uri = '/jobcode/save'
        req = self.request(uri, payload)
        return req


if __name__ == '__main__':
    # 拨测节点主机名
    endpoint = socket.gethostname()
    s = requests.Session()
    print(role, keywords, step, domain_list, cdn_list)
    task_source = task_source % (role, keywords, step, domain_list, cdn_list)

    xxljob_info = {
        "api_url": "http://bbb:9090/xxl-job-admin",
        "username": "admin",
        "password": "123456",
    }
    jobapi = XXLJOB(xxljob_info)
    payload = {
        'id': jobid,
        'glueSource': task_source,
        'glueRemark': 'update{}'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    }
    jobapi.save(payload)