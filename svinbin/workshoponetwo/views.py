# -*- coding: utf-8 -*-
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from workshoponetwo import serializers
import sows.serializers as sows_serializers
import sows_events.serializers as sows_events_serializers
import piglets.serializers as piglets_serializers
import piglets_events.serializers as piglets_events_serializers
import transactions.serializers as transactions_serializers
import locations.serializers as locations_serializers

import sows.models as sows_models
import sows_events.models as sows_events_models
import piglets.models as piglets_models
import piglets_events.models as piglets_events_models
import transactions.models as transactions_models
import locations.models as locations_models


class WorkShopSowViewSet(viewsets.GenericViewSet):
    queryset = sows_models.Sow.objects.all()
    serializer_class = sows_serializers.SowSerializer

    @action(methods=['post'], detail=True)
    def move_to(self, request, pk=None):
        sow = self.get_object()        
        serializer = locations_serializers.LocationPKSerializer(data=request.data)
        if serializer.is_valid():
            transaction = transactions_models.SowTransaction.objects.create_transaction(
                sow, serializer.validated_data['location'], request.user)
            return Response(
                {
                    "transaction": transactions_serializers.SowTransactionSerializer(transaction).data,
                    "sow": sows_serializers.SowSerializer(sow).data, 
                },
                status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=True)
    def culling(self, request, pk=None):
        sow = self.get_object()        
        serializer = sows_events_serializers.CreateCullingSowPkSerializer(data=request.data)
        if serializer.is_valid():
            culling = sows_events_models.CullingSow.objects.create_culling(
                sow, serializer.validated_data['culling_type'],
                serializer.validated_data['reason'], request.user)
            return Response(
                {
                    "culling": sows_events_serializers.CullingSowSerializer(culling).data,
                    "sow": sows_serializers.SowSerializer(sow).data, 
                },
                status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class WorkShopOneTwoSowViewSet(WorkShopSowViewSet):
    @action(methods=['post'], detail=True)
    def assing_farm_id(self, request, pk=None):
        sow = self.get_object()
        serializer = serializers.FarmIdSerializer(data=request.data)
        # initiator = request.user.workshopemployee
        if serializer.is_valid():
            sow.assing_farm_id(serializer.validated_data['farm_id'])
            return Response(
                {
                    "sow": sows_serializers.SowSerializer(sow).data,
                    "message": 'ok',
                },
                status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=True)
    def put_in_semination_row(self, request, pk=None):
        sow = self.get_object()        
        transaction = transactions_models.SowTransaction.objects.create_transaction(
            sow, locations_models.Location.objects.get(section__name="Ряд осеменения"),
            request.user)
        return Response(
            {
                "transaction": transactions_serializers.SowTransactionSerializer(transaction).data,
                "sow": sows_serializers.SowSerializer(sow).data, 
            },
            status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True)
    def semination(self, request, pk=None):
        sow = self.get_object() 
        serializer = sows_events_serializers.CreateSeminationSerializer(data=request.data)
        if serializer.is_valid():
            semination = sows_events_models.Semination.objects.create_semination(
                sow, serializer.validated_data['week'], request.user, request.user)
            return Response(
                {
                    "semination": sows_events_serializers.SeminationSerializer(semination).data,
                    "sow": sows_serializers.SowSerializer(sow).data, 
                    "message": "ok"
                },
                status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=True)
    def ultrasound(self, request, pk=None):
        sow = self.get_object() 
        serializer = sows_events_serializers.CreateUltrasoundSerializer(data=request.data)
        if serializer.is_valid():
            ultrasound = sows_events_models.Ultrasound.objects.create_ultrasound(
                sow, serializer.validated_data['week'], request.user,
                 serializer.validated_data['result'])
            return Response(
                {
                    "ultrasound": sows_events_serializers.UltrasoundSerializer(ultrasound).data,
                    "sow": sows_serializers.SowSerializer(sow).data, 
                    "message": "ok"
                },
                status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)