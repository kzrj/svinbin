# -*- coding: utf-8 -*-

from rest_framework import viewsets

from tours.models import Tour
from tours.serializers import TourSerializer
from tours.filters import TourFilter


class TourViewSet(viewsets.ModelViewSet):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer
    filter_class = TourFilter