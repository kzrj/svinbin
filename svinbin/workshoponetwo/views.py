# -*- coding: utf-8 -*-
from django.db import models

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
import tours.serializers as tours_serializers

import sows.models as sows_models
import sows_events.models as sows_events_models
import piglets.models as piglets_models
import piglets_events.models as piglets_events_models
import transactions.models as transactions_models
import locations.models as locations_models
import tours.models as tours_models


from sows.views import WorkShopSowViewSet
    

class WorkShopOneTwoSowViewSet(WorkShopSowViewSet):
    @action(methods=['post'], detail=False)
    def create_new(self, request):
        serializer = serializers.CreateFarmIdSerializer(data=request.data)
        if serializer.is_valid():
            sow = sows_models.Sow.objects.create_new_and_put_in_workshop_one(
                serializer.validated_data['farm_id'])
            return Response(
                {
                    "sow": sows_serializers.SowSerializer(sow).data,
                    "message": 'ok',
                },
                status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
            # semination employee is request user. TODO: need to choose semination employee
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
                 sow,
                 request.user,
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

    @action(methods=['get'], detail=False)
    def sows_by_tours(self, request):
        data = list()
        workshop = locations_models.WorkShop.objects.get(number=1)
        tours = tours_models.Tour.objects.get_tours_in_workshop_by_sows(workshop)
        for tour in tours:
            qs = tour.sows.get_suporos_in_workshop(workshop)
            if qs.count() > 0:
                data.append(
                    {   
                        'tour': tours_serializers.TourSerializer(tour).data,
                        'sows': sows_serializers.SowSerializer(qs, many=True).data,
                        'count': qs.count()
                    }
                )

        return Response(data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False)
    def sows_by_tours_ws2(self, request):
        data = list()
        workshop = locations_models.WorkShop.objects.get(number=2)
        tours = tours_models.Tour.objects.get_tours_in_workshop_by_sows(workshop)
        for tour in tours:
            qs = tour.sows.get_suporos_in_workshop(workshop)
            if qs.count() > 0:
                data.append(
                    {   
                        'tour': tours_serializers.TourSerializer(tour).data,
                        'sows': sows_serializers.SowSerializer(qs, many=True).data,
                        'count': qs.count()
                    }
                )
        qs = sows_models.Sow.objects.get_not_suporos_in_workshop(workshop)
        if qs.count() > 0:
            data.append({
                    'tour': {'id': 'Не супорос'},
                    'sows': sows_serializers.SowSerializer(qs, many=True).data,
                    'count': qs.count()
                    })

        return Response(data, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True)
    def ultrasoundv2(self, request, pk=None):
        sow = self.get_object() 
        serializer = sows_events_serializers.CreateUltrasoundSerializer(data=request.data)
        if serializer.is_valid():
            ultrasound = sows_events_models.UltrasoundV2.objects.create_ultrasoundV2(
                 sow,
                 request.user,
                 serializer.validated_data['result'])
            return Response(
                {
                    "ultrasoundv2": sows_events_serializers.UltrasoundV2Serializer(ultrasound).data,
                    "sow": sows_serializers.SowSerializer(sow).data, 
                    "message": "ok"
                },
                status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)