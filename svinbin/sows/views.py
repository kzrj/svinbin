# -*- coding: utf-8 -*-
from rest_framework import viewsets

from sows.models import Sow
from sows.serializers import SowSerializer


class SowViewSet(viewsets.ModelViewSet):
    queryset = Sow.objects.all()
    serializer_class = SowSerializer