# -*- coding: utf-8 -*-
# author: timor

from notices.serializers import *
from common.views import ModelViewSet, JsonResponse
from common import status
from collections import OrderedDict
from rest_framework.decorators import action


class MailBotViewSet(ModelViewSet):
    queryset = MailBot.objects.all()
    serializer_class = MailBotSerializer
    search_fields = ['name']
    filter_fields = ['name']
    ordering_fields = ['name']

    # send
    @action(methods=['post'], url_path='send', detail=False)
    def send(self, request, *args, **kwargs):
        self.watch_audit_log(request)
        data = {'code': 200, 'msg': None, 'content': 'action is not exist'}
        import smtplib
        from email.mime.text import MIMEText

        bot_name = request.GET['bot_name']
        bot_obj = MailBot.objects.get(name=bot_name)
        mail_user = '{}@{}'.format(bot_obj.user, bot_obj.host)

        tos = request.data['tos']
        content = request.data.get('content', 'Hello Pornhub')
        msg = content.replace('[', '|').replace(']', '|').split('|')
        text = '状态=> {}\n主机=> {}\n内容=> {}\n时间=> {}'.format(msg[3], msg[5], msg[9], msg[11])

        message = MIMEText(text, 'plain', 'utf-8')
        message['Subject'] = "{}".format(request.form['subject'])
        message['From'] = mail_user
        message['To'] = tos[0:]

        try:
            smtpObj = smtplib.SMTP_SSL(bot_obj.host)
            smtpObj.login(mail_user, bot_obj.pasword)
            smtpObj.sendmail(mail_user, tos, message.as_string())
            smtpObj.quit()
            data['msg'] = 'success'
        except smtplib.SMTPException as e:
            print(e)
            data['msg'] = 'error'

        return JsonResponse(OrderedDict([
            ('results', data)
        ], code=status.HTTP_200_OK))


class TelegramBotViewSet(ModelViewSet):
    queryset = TelegramBot.objects.all()
    serializer_class = TelegramBotSerializer
    search_fields = ['name']
    filter_fields = ['name']
    ordering_fields = ['name']

    # send
    @action(methods=['post'], url_path='send', detail=False)
    def send(self, request, *args, **kwargs):
        self.watch_audit_log(request)
        data = {'code': 200, 'msg': None, 'content': 'action is not exist'}
        import telegram
        bot_name = request.GET['bot_name']
        content = request.data.get('content', 'Hello Pornhub')
        msg = content.replace('[', '|').replace(']', '|').split('|')
        text = '状态=> {}\n主机=> {}\n内容=> {}\n时间=> {}'.format(msg[3], msg[5], msg[9], msg[11])
        bot_obj = TelegramBot.objects.get(name=bot_name)
        token = '{}:{}'.format(bot_obj.uid, bot_obj.token)
        bot = telegram.Bot(token=token)
        data['msg'] = bot.send_message(chat_id=bot_obj.chat_id, text=text)
        return JsonResponse(OrderedDict([
            ('results', data)
        ], code=status.HTTP_200_OK))
