# -*- coding: utf-8 -*-
from rest_framework import viewsets

from pigs.models import Sow
from pigs.serializers import SowSerializer


class SowViewSet(viewsets.ModelViewSet):
    queryset = Sow.objects.all()
    serializer_class = SowSerializer