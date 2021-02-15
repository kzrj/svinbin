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
from piglets_events import views as piglets_events_views
from rollbacks.views import RollbackViewSet
from veterinary import views as veterinary_views

router = routers.DefaultRouter()

# pigs
router.register(r'sows', sows_views.WorkShopSowViewSet, basename='sows')
router.register(r'boars', sows_views.BoarViewSet, basename='boars')
router.register(r'boar_breed', sows_views.BoarBreedViewSet, basename='boar_breed')

# piglets
router.register(r'piglets', piglets_views.PigletsViewSet, basename='piglets')

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
router.register(r'users', staff_views.UsersViewSet, \
 basename='users')

# by workshops
# workshop one two
router.register(r'workshoponetwo/sows', workshoponetwo_views.WorkShopOneTwoSowViewSet, \
 basename='workshoponetwo-sows')

# workshop three
router.register(r'workshopthree/sows', workshopthree_views.WorkShopThreeSowsViewSet, \
 basename='workshopthree-sows')
router.register(r'workshopthree/reports/mark_as_gilts_journal', workshopthree_views.MarksAsGiltListView,)

# reports
router.register(r'reports/tours', reports_views.TourReportViewSet,
 basename='report-tours')
router.register(r'reports/tours_v2', reports_views.TourReportV2ViewSet,
 basename='report-tours-v2')
router.register(r'reports/director', reports_views.ReportDateViewSet,
 basename='report-director')
router.register(r'reports/recounts', piglets_events_views.RecountViewSet,
 basename='report-director')

# rollbacks
router.register(r'rollbacks', RollbackViewSet, basename='rollbacks')

# veterinary
router.register(r'veterinary/recipes', veterinary_views.RecipeViewSet, basename='veterinary-recipes')
router.register(r'veterinary/drugs', veterinary_views.DrugViewSet, basename='veterinary-drugs')
router.register(r'veterinary/piglets_events', veterinary_views.PigletsVetEventViewSet, 
	basename='veterinary-piglets-events')

schema_view = get_swagger_view(title='API Docs')

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(router.urls)),
    url(r'^api/jwt/api-token-auth/', obtain_jwt_token),
    url(r'^api/jwt/api-token-refresh/', refresh_jwt_token),
    url(r'^api/jwt/api-token-verify/', verify_jwt_token),
    
    url(r'^api/reports/pigs_count/', reports_views.ReportCountPigsView.as_view()),
    url(r'^api/reports/operations/', reports_views.OperationsDataView.as_view()),

    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
