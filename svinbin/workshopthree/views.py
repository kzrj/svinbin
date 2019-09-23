# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.decorators import action

from workshopthree import serializers
from sows import serializers as sows_serializers
from sows_events import serializers as sows_events_serializers
from piglets import serializers as piglets_serializers
from piglets_events import serializers as piglets_events_serializers
from transactions import serializers as transactions_serializers
from locations import serializers as locations_serializers

from sows.models import Sow
from sows_events import models as sows_events_models
from piglets.models import NomadPigletsGroup, NewBornPigletsGroup
from piglets_events import models as piglets_events_models
from transactions import models as transactions_models
from locations import models as locations_models

from sows.views import WorkShopSowViewSet
from piglets.views import NewBornPigletsViewSet, WorkShopNomadPigletsViewSet


class WorkShopThreeNewBornPigletsViewSet(NewBornPigletsViewSet):
    pass


class WorkShopThreeSowsViewSet(WorkShopSowViewSet):
    @action(methods=['post'], detail=True)
    def sow_farrow(self, request, pk=None):
        serializer = sows_events_serializers.CreateSowFarrowSerializer(data=request.data)
        if serializer.is_valid():
            sow = self.get_object()
            farrow = sows_events_models.SowFarrow.objects.create_sow_farrow(
                sow=sow,
                alive_quantity=serializer.validated_data['alive_quantity'],
                dead_quantity=serializer.validated_data['dead_quantity'],
                mummy_quantity=serializer.validated_data['mummy_quantity'],
                initiator=request.user
                )
            
            return Response(
                {"sow": sows_serializers.SowSerializer(sow).data,
                 "message": 'Свинья успешно опоросилась.',
                 "farrow": sows_events_serializers.SowFarrowSerializer(farrow).data},
                status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
