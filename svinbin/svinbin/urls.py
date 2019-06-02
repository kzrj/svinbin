# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os

from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

from rest_framework import routers

from transactions import views as transaction_views
from pigs import views as pigs_views
from events import views as events_views
from workshops.views import CreateWorkshopsView

router = routers.DefaultRouter()
router.register(r'sowtransactions/workshops', transaction_views.WorkShopOneTwoSowTransactionViewSet,
    basename='workshop-sowtransactions')
router.register(r'sowtransactions/transactions', transaction_views.SowTransactionsViewSet,
    basename='sowtransactions')
router.register(r'sows', pigs_views.SowViewSet, basename='sows')
router.register(r'events/seminations', events_views.SeminationViewSet, basename='seminations')
router.register(r'events/ultrasounds', events_views.UltrasoundViewSet, basename='ultrasounds')
router.register(r'events/spec_uboi', events_views.SlaughterSowViewSet, basename='spec_uboi')


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(router.urls)),
    url(r'^api/init_data/', CreateWorkshopsView.as_view()),
    ]
