# 域名拨测系统

## 检测uswgi工作
```bash
uwsgi --http :8000 --module core.wsgi
```
这个能看到详细日志

## win mysql错误
使用pymysql
```bash
 mysqlclient 1.3.13 or newer is required; you have 0.9.3
```
解决 django降级
```
pip install django==2.1.4
```# one-xxljob
