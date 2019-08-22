# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import connection

from rest_framework.views import APIView
from rest_framework import viewsets, status, generics, mixins
from rest_framework.response import Response
from rest_framework.decorators import action

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
import tours.models as tours_models

from sows.filters import SowFilter


class SowViewSet(viewsets.ModelViewSet):
    queryset = sows_models.Sow.objects.all()
    serializer_class = sows_serializers.SowSerializer
    filter_class = SowFilter

    def retrieve(self, request, pk=None):
        sow = self.get_object()
        tours_info = list()
        for tour in tours_models.Tour.objects.filter(pk__in=sow.get_tours_pk()):
            tours_info.append(
                {
                    'tour_title': str(tour),
                    'seminations': sows_events_serializers.SimpleSeminationSerializer(
                        sow.get_seminations_by_tour(tour), many=True).data,
                    'ultrasounds': sows_events_serializers.SimpleUltrasoundSerializer(
                        sow.get_ultrasounds1_by_tour(tour), many=True).data,
                    'ultrasoundsV2': sows_events_serializers.SimpleUltrasoundV2Serializer(
                        sow.get_ultrasoundsv2_by_tour(tour), many=True).data,
                    'farrows': sows_events_serializers.SimpleSowFarrowSerializer(
                        sow.get_farrows_by_tour(tour), many=True).data,
                }
            )

        return Response(
            { 
                'sow': sows_serializers.SowSerializer(sow).data,
                'tours_info': tours_info
            },
            status=status.HTTP_200_OK
        )


class WorkShopSowViewSet(SowViewSet):
    # queryset = sows_models.Sow.objects.all()
    # serializer_class = sows_serializers.SowSerializer
    # filter_class = SowFilter

    @action(methods=['post'], detail=False)
    def move_many_by_queryset(self, request):
        # sows = here need to get queryset by filter

        serializer = locations_serializers.LocationPKSerializer(data=request.data)
        if serializer.is_valid():

            # here create transaction for each in queryset

            return Response(
                {
                    # "transaction": transactions_serializers.SowTransactionSerializer(transaction).data,
                    # "sows": sows_serializers.SowSerializer(sows, many=True).data, 
                },
                status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        pass

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

    @action(methods=['post'], detail=True) # test +  in workshop onetwo
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

    @action(methods=['post'], detail=False)
    def move_many(self, request):
        serializer = sows_serializers.SowsToMoveSerializer(data=request.data)
        if serializer.is_valid():

            transaction_ids = transactions_models.SowTransaction.objects.create_many_transactions(
                serializer.validated_data['sows'],
                serializer.validated_data['to_location'],
                request.user
                )

            return Response(
                {
                    # "transaction_ids": transactions_serializers.SowTransactionSerializer(transaction).data,
                    # "sows": sows_serializers.SowSerializer(sows, many=True).data, 
                    "transaction_ids": transaction_ids,
                    "message": "ok"
                },
                status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        