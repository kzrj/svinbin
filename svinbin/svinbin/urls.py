# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os

from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

from rest_framework import routers
from rest_framework_swagger.views import get_swagger_view

from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

from transactions import views as transaction_views
from sows import views as sows_views
from sows_events import views as sows_events_views
from locations import views as locations_views
from tours import views as tours_views
from staff import views as staff_views
from piglets import views as piglets_views
from workshoponetwo import views as workshoponetwo_views
from workshopthree import views as workshopthree_views

router = routers.DefaultRouter()

# transactions
router.register(r'sowtransactions/workshops', transaction_views.WorkShopOneTwoSowTransactionViewSet,
    basename='workshop-sowtransactions')
router.register(r'sowtransactions/transactions', transaction_views.SowTransactionsViewSet,
    basename='sowtransactions')

# pigs
router.register(r'sows', sows_views.SowViewSet, basename='sows')
router.register(r'boars', sows_views.BoarViewSet, basename='boars')

# events
router.register(r'sows_events/seminations', sows_events_views.SeminationViewSet, basename='seminations')
router.register(r'sows_events/ultrasounds', sows_events_views.UltrasoundViewSet, basename='ultrasounds')
router.register(r'sows_events/farrows', sows_events_views.SowFarrowViewSet, basename='farrows')
router.register(r'sows_events/spec_uboi', sows_events_views.CullingSowViewSet, basename='spec_uboi')

# cells
# router.register(r'pigletsgroupcells', locations_views.PigletsGroupCellViewSet, basename='pigletsgroupcell')

# by workshops
# workshop one two
router.register(r'workshoponetwo/sows', workshoponetwo_views.WorkShopOneTwoSowViewSet, \
 basename='workshoponetwo-sows')

# workshop three
# router.register(r'workshopthree/newbornpiglets', workshopthree_views.WorkShopThreeNewBornPigletsViewSet, \
 # basename='workshopthree-piglets')
router.register(r'workshopthree/sows', workshopthree_views.WorkShopThreeSowsViewSet, \
 basename='workshopthree-sows')
router.register(r'workshopthree/wsinfo', workshopthree_views.WorkshopInfo, \
 basename='workshopthree-info')

# workshop four
# router.register(r'workshopfour/piglets', workshopfour_views.WorkShopFourPigletsViewSet, \
#  basename='workshopfour-piglets')

# location
router.register(r'locations', locations_views.LocationViewSet, \
 basename='locations')
router.register(r'sections', locations_views.SectionViewSet, \
 basename='sections')

# tours
router.register(r'tours', tours_views.TourViewSet, \
 basename='tours')

# users
router.register(r'users', staff_views.UsersViewSet, \
 basename='users')

# piglets
router.register(r'piglets', piglets_views.PigletsViewSet, basename='piglets')

# inits
# router.register(r'inits', piglets_views.WorkShopNomadPigletsViewSet, \
 # basename='piglets')

schema_view = get_swagger_view(title='API Docs')

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(router.urls)),
    url(r'^api/jwt/api-token-auth/', obtain_jwt_token),
    url(r'^api/jwt/api-token-refresh/', refresh_jwt_token),
    url(r'^api/jwt/api-token-verify/', verify_jwt_token),
    url(r'^api/init_data/', locations_views.CreateWorkshopsView.as_view()),
    url(r'^api/docs/$', schema_view) 
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
