# -*- coding: utf-8 -*-
# author: itimor


from django.conf.urls import url
from rest_framework import routers
from domains.views import CDNViewSet, IPPoolViewSet, BrandViewSet, DomainTypeViewSet, DomainViewSet, xxljobViewSet

router = routers.DefaultRouter()

router.register(r'cdn', CDNViewSet)
router.register(r'ipool', IPPoolViewSet)
router.register(r'brand', BrandViewSet)
router.register(r'domaintype', DomainTypeViewSet)
router.register(r'domain', DomainViewSet)
router.register(r'xxljob', xxljobViewSet)

urlpatterns = [
]

urlpatterns += router.urls
