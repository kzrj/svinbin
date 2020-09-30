# -*- coding: utf-8 -*-
from django.db.models import Prefetch
from django.utils import timezone

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

import sows.serializers as sows_serializers
import sows_events.serializers as sows_events_serializers
import transactions.serializers as transactions_serializers
import locations.serializers as locations_serializers

import sows.models as sows_models
import sows_events.models as sows_events_models
import transactions.models as transactions_models
import locations.models as locations_models
import tours.models as tours_models

from sows.filters import SowFilter, BoarFilter

from core.permissions import ObjAndUserSameLocationPermissions, WS3Permissions, ReadOrAdminOnlyPermissions,\
  WS12Permissions


class SowViewSet(viewsets.ModelViewSet):
    queryset = sows_models.Sow.objects.get_queryset_with_not_alive()
    serializer_class = sows_serializers.SowSerializer
    filter_class = SowFilter
    permission_classes = [ObjAndUserSameLocationPermissions]

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
            self.get_queryset() \
                .select_related('location__workshop') \
                .select_related('location__sowAndPigletsCell__section', 'status', 'tour') \
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
                    "message": f'Свиноматка {sow.farm_id} переведена'
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
                sow=sow, culling_type=serializer.validated_data['culling_type'],
                reason=serializer.validated_data['reason'],
                weight=serializer.validated_data['weight'],
                initiator=request.user,
                date=timezone.now())
            return Response(
                {
                    "culling": sows_events_serializers.CullingSowSerializer(culling).data,
                    "sow": sows_serializers.SowSerializer(sow).data, 
                    "message": f'Свиноматка {sow.farm_id} выбракована'
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
                    "transaction_ids": transaction_ids,
                    "message": "Успешно переведены."
                },
                status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @action(methods=['post'], detail=True) # test +  in workshop onetwo
    def abortion(self, request, pk=None):
        sow = self.get_object()
        abortion = sows_events_models.AbortionSow.objects.create_abortion(
            sow=sow, initiator=request.user, date=timezone.now())
        return Response(
            {
                "abortion": sows_events_serializers.AbortionSowSerializer(abortion).data,
                "sow": sows_serializers.SowSerializer(sow).data,
                "message": f'Аборт у свиньи №{sow.farm_id}.'
            },
            status=status.HTTP_200_OK)


class BoarViewSet(viewsets.ModelViewSet):
    queryset = sows_models.Boar.objects.filter(active=True)
    serializer_class = sows_serializers.BoarSerializer
    filter_class = BoarFilter
    permission_classes = [WS12Permissions]

    def create(self, request):
        serializer = sows_serializers.BoarCreateSerializer(data=request.data)
        if serializer.is_valid():
            boar = sows_models.Boar.objects.create_boar(
                farm_id=serializer.validated_data['farm_id'],
                birth_id=serializer.validated_data['birth_id'],
                breed=serializer.validated_data['breed'],
                )
            return Response(
                {
                    "message": f"Хряк №{boar.farm_id} создан.",
                    "boar": sows_serializers.BoarSerializer(boar).data,
                },
                status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=True)
    def culling(self, request, pk=None):
        boar = self.get_object()        
        serializer = sows_events_serializers.CullingBoarSerializer(data=request.data)
        if serializer.is_valid():
            sows_events_models.CullingBoar.objects.create_culling_boar(
                boar=boar, culling_type=serializer.validated_data['culling_type'],
                reason=serializer.validated_data['reason'],
                weight=serializer.validated_data['weight'],
                initiator=request.user,
                date=timezone.now())
            return Response(
                {
                    "message": f"Выбраковка прошла успешно. Хряк №{boar.farm_id}.",
                    "boar": sows_serializers.BoarSerializer(boar).data
                },
                status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=True)
    def semen_boar(self, request, pk=None):
        boar = self.get_object()        
        serializer = sows_events_serializers.SemenBoarCreateSerializer(data=request.data)
        if serializer.is_valid():
            sows_events_models.SemenBoar.objects.create_semen_boar(
                boar=boar, 
                a=serializer.validated_data['a'],
                b=serializer.validated_data['b'],
                d=serializer.validated_data['d'],
                # morphology_score=serializer.validated_data['morphology_score'],
                final_motility_score=serializer.validated_data['final_motility_score'],
                date=serializer.validated_data['date'],
                initiator=request.user,
                )
            return Response(
                {
                    "message": f"Запись создана. Хряк №{boar.farm_id}.",
                    "boar": sows_serializers.BoarSerializer(boar).data
                },
                status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BoarBreedViewSet(viewsets.ModelViewSet):
    queryset = sows_models.BoarBreed.objects.all()
    serializer_class = sows_serializers.BoarBreedSerializer
    permission_classes = [ReadOrAdminOnlyPermissions]