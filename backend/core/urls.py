# -*- coding: utf-8 -*-
# author: timor

from django.conf.urls import url, include
from django.conf.urls.static import static
from django.views.generic.base import TemplateView
from core import settings
from rest_framework_jwt.views import obtain_jwt_token as jwt_token
from rest_framework.documentation import include_docs_urls

urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + \
              [
                  # api文档
                  url(r'^docs/', include_docs_urls(title='X Document')),

                  # 工具管理
                  url(r'api/tool/', include(('tools.urls', 'tools'), namespace="tools")),
                  # 系统管理
                  url(r'api/sys/', include(('systems.urls', 'systems'), namespace="systems")),
                  # 域名管理
                  url(r'api/domain/', include(('domains.urls', 'domains'), namespace="domains")),
                  # 拨测管理
                  url(r'api/boce/', include(('boces.urls', 'boces'), namespace="boces")),
                  # 通知管理
                  url(r'api/notice/', include(('notices.urls', 'notices'), namespace="notices")),
              ]

if settings.APP_ENV == 'prod':
    from django.contrib.staticfiles.views import serve
    urlpatterns += [
        # 静态模板
        url(r'', TemplateView.as_view(template_name="index.html")),
        url('favicon.ico', serve, {'path': '/favicon.ico'}),
    ]
