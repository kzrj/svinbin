# -*- coding: utf-8 -*-
from rest_framework import viewsets

import piglets.serializers as piglets_serializers
import piglets.models as piglets_models


class WorkShopNomadPigletsViewSet(viewsets.GenericViewSet):
    queryset = piglets_models.NomadPigletsGroup.objects.all()
    serializer_class = piglets_serializers.NomadPigletsGroupSerializer

    # def get_queryset(self):
    #     return piglets_models.NomadPigletsGroup.objects.all()