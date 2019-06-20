# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os

from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

from rest_framework import routers
from rest_framework_swagger.views import get_swagger_view

from transactions import views as transaction_views
from sows import views as sows_views
from sows_events import views as sows_events_views
from workshops import views as workshops_views
from workshopthree import views as workshopthree_views
from workshopfour import views as workshopfour_views

router = routers.DefaultRouter()

# transactions
router.register(r'sowtransactions/workshops', transaction_views.WorkShopOneTwoSowTransactionViewSet,
    basename='workshop-sowtransactions')
router.register(r'sowtransactions/transactions', transaction_views.SowTransactionsViewSet,
    basename='sowtransactions')

# pigs
router.register(r'sows', sows_views.SowViewSet, basename='sows')

# events
router.register(r'sows_events/seminations', sows_events_views.SeminationViewSet, basename='seminations')
router.register(r'sows_events/ultrasounds', sows_events_views.UltrasoundViewSet, basename='ultrasounds')
router.register(r'sows_events/spec_uboi', sows_events_views.CullingSowViewSet, basename='spec_uboi')

# cells
router.register(r'pigletsgroupcells', workshops_views.PigletsGroupCellViewSet, basename='pigletsgroupcell')

# by workshops
# workshop three
router.register(r'workshopthree/piglets', workshopthree_views.WorkShopThreePigletsViewSet, \
 basename='workshopthree-piglets')
router.register(r'workshopthree/sows', workshopthree_views.WorkShopThreeSowsViewSet, \
 basename='workshopthree-sows')

# workshop four
router.register(r'workshopfour/piglets', workshopfour_views.WorkShopFourPigletsViewSet, \
 basename='workshopfour-piglets')


schema_view = get_swagger_view(title='API Docs')

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(router.urls)),
    url(r'^api/init_data/', workshops_views.CreateWorkshopsView.as_view()),
    url(r'^api/docs/$', schema_view)
    ]
