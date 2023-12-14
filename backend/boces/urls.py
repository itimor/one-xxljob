# -*- coding: utf-8 -*-
# author: timor


from django.conf.urls import url
from boces.views import *


urlpatterns = [
    url(r'^get_group/', get_group.as_view()),
    url(r'^create_group/', create_group.as_view()),
    url(r'^update_group/', update_group.as_view()),
    url(r'^delete_group/', delete_group.as_view()),
    url(r'^get_code_by_id/', get_code_by_id.as_view()),
    url(r'^get_code_history_by_id/', get_code_history_by_id.as_view()),
    url(r'^get_log_count/', get_log_count.as_view()),
]