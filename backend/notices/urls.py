# -*- coding: utf-8 -*-
# author: itimor


from django.conf.urls import url
from rest_framework import routers
from notices.views import MailBotViewSet, TelegramBotViewSet

router = routers.DefaultRouter()

router.register(r'mailbot', MailBotViewSet)
router.register(r'tgbot', TelegramBotViewSet)

urlpatterns = [
]

urlpatterns += router.urls
