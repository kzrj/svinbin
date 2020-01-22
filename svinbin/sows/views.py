# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import connection
from django.db.models import F, Prefetch

from rest_framework.views import APIView
from rest_framework import viewsets, status, generics, mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination

import sows.serializers as sows_serializers
import sows_events.serializers as sows_events_serializers
import transactions.serializers as transactions_serializers
import locations.serializers as locations_serializers

import sows.models as sows_models
import sows_events.models as sows_events_models
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

    def list(self, request):
        queryset = self.filter_queryset(
            self.get_queryset().select_related('location__sowAndPigletsCell__section', 'status', 'tour') \
                .prefetch_related('semination_set__tour') \
                .prefetch_related(
                    Prefetch(
                        'ultrasound_set',
                        queryset=sows_events_models.Ultrasound.objects.all().select_related('u_type', 'tour'),
                    )
                )
        )

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = sows_serializers.SowManySerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = sows_serializers.SowManySerializer(queryset, many=True)
        return Response(serializer.data)


    @action(methods=['post'], detail=False)
    def add_new_seminated_to_ws1(self, request):
        # for init
        location = locations_models.Location.objects.get(workshop__number=1)
        serializer = sows_serializers.InitOnlyCreateSeminatedSow(data=request.data)
        if serializer.is_valid():
            sow = sows_models.Sow.objects.init_only_create_new(
                farm_id=serializer.validated_data['farm_id'],
                location=location
                )
            boar, created = sows_models.Boar.objects.get_create_boar(serializer.validated_data['boar'])
            semination = sows_events_models.Semination.objects.create_semination(
                sow=sow, 
                week=serializer.validated_data['week'],
                semination_employee=request.user,
                boar=boar,
                initiator=request.user
                )

            return Response(
                {
                    "sow": sows_serializers.SowSerializer(sow).data,
                    "semination": sows_events_serializers.SimpleSeminationSerializer(semination).data
                },
                status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False)
    def add_new_ultrasounded_to_ws12(self, request):
        # for init
        serializer = sows_serializers.InitOnlyCreateUltrasoundedSow(data=request.data)
        if serializer.is_valid():
            location = locations_models.Location.objects.get(
                workshop__number=serializer.validated_data['workshop_number'])
            sow = sows_models.Sow.objects.init_only_create_new(
                farm_id=serializer.validated_data['farm_id'],
                location=location
                )
            boar, created = sows_models.Boar.objects.get_create_boar(serializer.validated_data['boar'])
            semination = sows_events_models.Semination.objects.create_semination(
                sow=sow, 
                week=serializer.validated_data['week'],
                semination_employee=request.user,
                boar=boar,
                initiator=request.user
                )
            
            ultrasound = sows_events_models.Ultrasound.objects.create_ultrasound(
                sow=sow,
                days=serializer.validated_data['days'],
                initiator=request.user,
                result=True,
                )

            return Response(
                {
                    "sow": sows_serializers.SowSerializer(sow).data,
                    "semination": sows_events_serializers.SimpleSeminationSerializer(semination).data,
                    "ultrasound": sows_events_serializers.SimpleUltrasoundSerializer(ultrasound).data
                },
                status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False)
    def add_new_suporos_to_ws3(self, request):
        serializer = sows_serializers.InitOnlyCreateSuporosWs3Sow(data=request.data)
        if serializer.is_valid():
            cell = locations_models.SowAndPigletsCell.objects.get(
                section__number=serializer.validated_data['section'],
                number=serializer.validated_data['cell'],
                )
            location = locations_models.Location.objects.get(sowAndPigletsCell=cell)
            sow = sows_models.Sow.objects.init_only_create_new(
                farm_id=serializer.validated_data['farm_id'],
                location=location
                )
            boar, created = sows_models.Boar.objects.get_create_boar(serializer.validated_data['boar'])
            semination = sows_events_models.Semination.objects.create_semination(
                sow=sow, 
                week=serializer.validated_data['week'],
                semination_employee=request.user,
                boar=boar,
                initiator=request.user
                )

            u_type = sows_events_models.UltrasoundType.objects.get(days=60)
            ultrasound = sows_events_models.Ultrasound.objects.create_ultrasound(
                sow=sow,
                result=True,
                days=60,
                initiator=request.user
                )

            return Response(
                {
                    "sow": sows_serializers.SowSerializer(sow).data,
                    "semination": sows_events_serializers.SimpleSeminationSerializer(semination).data,
                    "ultrasound": sows_events_serializers.SimpleUltrasoundSerializer(ultrasound).data
                },
                status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False)
    def add_new_oporos_to_ws3(self, request):
        serializer = sows_serializers.InitOnlyCreateFarrowSow(data=request.data)
        if serializer.is_valid():
            cell = locations_models.SowAndPigletsCell.objects.get(
                section__number=serializer.validated_data['section'],
                number=serializer.validated_data['cell'],
                )
            location = locations_models.Location.objects.get(sowAndPigletsCell=cell)
            sow = sows_models.Sow.objects.init_only_create_new(
                farm_id=serializer.validated_data['farm_id'],
                location=location
                )
            boar, created = sows_models.Boar.objects.get_create_boar(serializer.validated_data['boar'])
            semination = sows_events_models.Semination.objects.create_semination(
                sow=sow, 
                week=serializer.validated_data['week'],
                semination_employee=request.user,
                boar=boar,
                initiator=request.user
                )

            u_type = sows_events_models.UltrasoundType.objects.get(days=60)
            ultrasound = sows_events_models.Ultrasound.objects.create_ultrasound(
                sow=sow,
                result=True,
                days=60,
                initiator=request.user
                )

            farrow = sows_events_models.SowFarrow.objects.create_sow_farrow(
                sow=sow,
                initiator=request.user,
                alive_quantity=serializer.validated_data['alive_quantity'],
                dead_quantity=serializer.validated_data['dead_quantity'],
                mummy_quantity=serializer.validated_data['mummy_quantity'],
                )

            return Response(
                {
                    "sow": sows_serializers.SowSerializer(sow).data,
                    "semination": sows_events_serializers.SimpleSeminationSerializer(semination).data,
                    "ultrasound": sows_events_serializers.SimpleUltrasoundSerializer(ultrasound).data,
                    "farrow": sows_events_serializers.SimpleSowFarrowSerializer(farrow).data
                },
                status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BoarViewSet(viewsets.ModelViewSet):
    queryset = sows_models.Boar.objects.all()
    serializer_class = sows_serializers.BoarSerializer


class WorkShopSowViewSet(SowViewSet):
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


    @action(methods=['post'], detail=True) # test +  in workshop onetwo
    def abortion(self, request, pk=None):
        sow = self.get_object()
        abortion = sows_events_models.AbortionSow.objects.create_abortion(
            sow=sow, initiator=request.user)
        return Response(
            {
                "abortion": sows_events_serializers.AbortionSowSerializer(abortion).data,
                "sow": sows_serializers.SowSerializer(sow).data, 
            },
            status=status.HTTP_200_OK)