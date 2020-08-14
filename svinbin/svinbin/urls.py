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
from reports import views as reports_views

router = routers.DefaultRouter()

# transactions
# router.register(r'transactions/sowtransactions', transaction_views.SowTransactionsViewSet,
#     basename='sowtransactions')
# router.register(r'transactions/pigletstransactions', transaction_views.PigletsTransactionsViewSet,
#     basename='pigletstransactions')

# pigs
router.register(r'sows', sows_views.WorkShopSowViewSet, basename='sows')
router.register(r'boars', sows_views.BoarViewSet, basename='boars')
router.register(r'boar_breed', sows_views.BoarBreedViewSet, basename='boar_breed')

# piglets
router.register(r'piglets', piglets_views.PigletsViewSet, basename='piglets')

# events
# router.register(r'sows_events/seminations', sows_events_views.SeminationViewSet, basename='seminations')
# router.register(r'sows_events/ultrasounds', sows_events_views.UltrasoundViewSet, basename='ultrasounds')
# router.register(r'sows_events/farrows', sows_events_views.SowFarrowViewSet, basename='farrows')
# router.register(r'sows_events/spec_uboi', sows_events_views.CullingSowViewSet, basename='spec_uboi')

router.register(r'boar_events/semen', sows_events_views.SemenBoarViewSet, basename='semen_boar')

# location
router.register(r'locations', locations_views.LocationViewSet, \
 basename='locations')
router.register(r'sections', locations_views.SectionViewSet, \
 basename='sections')

# tours
router.register(r'tours', tours_views.TourViewSet, \
 basename='tours')

# users
# router.register(r'users', staff_views.UsersViewSet, \
#  basename='users')

# by workshops
# workshop one two
router.register(r'workshoponetwo/sows', workshoponetwo_views.WorkShopOneTwoSowViewSet, \
 basename='workshoponetwo-sows')

# workshop three
router.register(r'workshopthree/sows', workshopthree_views.WorkShopThreeSowsViewSet, \
 basename='workshopthree-sows')

# reports
router.register(r'reports/tours', reports_views.TourReportViewSet,
 basename='report-tours')
router.register(r'reports/director', reports_views.ReportDateViewSet,
 basename='report-director')

schema_view = get_swagger_view(title='API Docs')

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(router.urls)),
    url(r'^api/jwt/api-token-auth/', obtain_jwt_token),
    url(r'^api/jwt/api-token-refresh/', refresh_jwt_token),
    url(r'^api/jwt/api-token-verify/', verify_jwt_token),
    url(r'^api/init_data/', locations_views.CreateWorkshopsView.as_view()),
    url(r'^api/docs/$', schema_view) ,

    url(r'^api/reports/pigs_count/', reports_views.ReportCountPigsView.as_view()),
    url(r'^api/reports/operations/', reports_views.OperationsDataView.as_view()),

    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
