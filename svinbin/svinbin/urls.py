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
from workshops import views as workshops_views

router = routers.DefaultRouter()

# transactions
router.register(r'sowtransactions/workshops', transaction_views.WorkShopOneTwoSowTransactionViewSet,
    basename='workshop-sowtransactions')
router.register(r'sowtransactions/transactions', transaction_views.SowTransactionsViewSet,
    basename='sowtransactions')

# pigs
router.register(r'sows', pigs_views.SowViewSet, basename='sows')

# events
router.register(r'events/seminations', events_views.SeminationViewSet, basename='seminations')
router.register(r'events/ultrasounds', events_views.UltrasoundViewSet, basename='ultrasounds')
router.register(r'events/spec_uboi', events_views.SlaughterSowViewSet, basename='spec_uboi')

# cells
router.register(r'pigletsgroupcells', workshops_views.PigletsGroupCellViewSet, basename='pigletsgroupcell')


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(router.urls)),
    url(r'^api/init_data/', workshops_views.CreateWorkshopsView.as_view()),
    ]
