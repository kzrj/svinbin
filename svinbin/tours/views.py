# -*- coding: utf-8 -*-
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from tours.models import Tour
from tours.serializers import TourSerializer
from tours.filters import TourFilter
from core.permissions import ReadOrAdminOnlyPermissions


class TourViewSet(viewsets.ModelViewSet):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer
    filter_class = TourFilter
    permission_classes = [ReadOrAdminOnlyPermissions]