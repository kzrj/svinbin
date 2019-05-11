# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os

from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

from rest_framework import routers

from transactions.views import WorkShopOneSowTransactionViewSet

router = routers.DefaultRouter()
router.register(r'workshopone/sowtransactions', WorkShopOneSowTransactionViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(router.urls)),    
    ]
