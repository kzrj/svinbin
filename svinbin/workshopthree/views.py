# -*- coding: utf-8 -*-
from django.utils import timezone

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from workshopthree import serializers
from sows import serializers as sows_serializers
from sows_events import serializers as sows_events_serializers

from sows.models import Sow
from sows_events import models as sows_events_models

from sows.views import WorkShopSowViewSet


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
                initiator=request.user,
                date=timezone.now()
                )
            
            return Response(
                {"sow": sows_serializers.SowSerializer(sow).data,
                 "message": 'Свинья успешно опоросилась.',
                 "farrow": sows_events_serializers.SowFarrowSerializer(farrow).data},
                status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=True)
    def mark_as_nurse(self, request, pk=None):
        serializer = serializers.MarkSowAsNurseSerializer(data=request.data)
        if serializer.is_valid():
            sow = self.get_object()
            sow.markasnurse_set.create_nurse_event(sow=sow, initiator=request.user, date=timezone.now())
            sow.refresh_from_db()
            
            return Response(
                {
                 "sow": sows_serializers.SowSerializer(sow).data,
                 "message": 'Свинья помечена как кормилица.',
                },
                status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)