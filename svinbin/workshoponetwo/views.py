# -*- coding: utf-8 -*-
from django.db import models

from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from core import import_farm

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
import staff.models as staff_models

from sows.views import WorkShopSowViewSet
    

class WorkShopOneTwoSowViewSet(WorkShopSowViewSet):
    @action(methods=['post'], detail=False)
    def create_new(self, request):
        workshop = locations_models.WorkShop.objects.get(number=1)
        serializer = serializers.CreateFarmIdSerializer(data=request.data)
        if serializer.is_valid():
            sow = sows_models.Sow.objects.create_new_from_noname(
                serializer.validated_data['farm_id'],
                workshop
                )
            if sow:
                return Response(
                    {
                        "sow": sows_serializers.SowSerializer(sow).data,
                        "message": 'Создана свиноматка с номером {}.' \
                            .format(serializer.validated_data['farm_id']),
                    },
                    status=status.HTTP_200_OK)
            else:
                return Response(
                    {
                        "sow": None,
                        "message": 'Нет ремонтных свиноматок. Создайте свиноматку без номера.',
                    },
                    status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False)
    def create_new_without_farm_id(self, request):
        workshop = locations_models.WorkShop.objects.get(number=1)    
        sow = sows_models.Sow.objects.create_new_from_gilt_without_farm_id()
        noname_sows = sows_models.Sow.objects.get_without_farm_id_in_workshop(workshop)
        return Response(
            {
                "sow": sows_serializers.SowSerializer(sow).data,
                "noname_sows_count": noname_sows.count(), 
                "message": 'Создана ремонтная свиноматка.',
            },
            status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True)
    def assing_farm_id(self, request, pk=None):
        sow = self.get_object()
        serializer = serializers.CreateFarmIdSerializer(data=request.data)
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
    def semination(self, request, pk=None):
        sow = self.get_object() 
        serializer = sows_events_serializers.CreateSeminationSerializer(data=request.data)
        if serializer.is_valid():
            # semination employee is request user. TODO: need to choose semination employee
            semination = sows_events_models.Semination.objects.create_semination(
                sow, serializer.validated_data['week'], request.user, request.user,
                serializer.validated_data['boar'] )
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
                 serializer.validated_data['result'],
                 serializer.validated_data['days'],)
            return Response(
                {
                    "ultrasound": sows_events_serializers.UltrasoundSerializer(ultrasound).data,
                    "sow": sows_serializers.SowSerializer(sow).data, 
                    "message": "ok"
                },
                status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False)
    def mass_semination(self, request):
        serializer = sows_serializers.SowsMassSeminationSerializer(data=request.data)
        if serializer.is_valid():
            sows_qs = sows_models.Sow.objects.filter(pk__in=serializer.validated_data['sows'])
            sows_events_models.Semination.objects.mass_semination(
                sows_qs=sows_qs,
                week=serializer.validated_data['week'],
                semination_employee=serializer.validated_data['semination_employee'],
                boar=serializer.validated_data['boar'],
                initiator=request.user
                )

            return Response(
                {
                    "message": "ok"
                },
                status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False)
    def mass_ultrasound(self, request):
        serializer = sows_serializers.SowsMassUltrasoundSerializer(data=request.data)
        if serializer.is_valid():
            sows_qs = sows_models.Sow.objects.filter(pk__in=serializer.validated_data['sows'])
            sows_events_models.Ultrasound.objects.mass_ultrasound(
                sows_qs=sows_qs,
                days=serializer.validated_data['days'],
                result=serializer.validated_data['result'],
                initiator=request.user
                )

            return Response(
                {
                    "message": "Узи проведено."
                },
                status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=True)
    def double_semination(self, request, pk=None):
        sow = self.get_object() 
        serializer = serializers.DoubleSeminationSerializer(data=request.data)
        if serializer.is_valid():
            semination1 = sows_events_models.Semination.objects.create_semination(
                sow=sow, week=serializer.validated_data['week'],
                initiator=request.user, 
                semination_employee=serializer.validated_data['semination_employee'],
                boar=serializer.validated_data['boar1'])

            semination2 = sows_events_models.Semination.objects.create_semination(
                sow=sow, week=serializer.validated_data['week'],
                initiator=request.user, 
                semination_employee=serializer.validated_data['semination_employee'],
                boar=serializer.validated_data['boar2'])
            return Response(
                {
                    "semination1": sows_events_serializers.SeminationSerializer(semination1).data,
                    "semination2": sows_events_serializers.SeminationSerializer(semination2).data,
                    "sow": sows_serializers.SowSerializer(sow).data, 
                    "message": "Свиноматка {} осеменена 2 раза".format(sow.farm_id)
                },
                status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @action(methods=['post'], detail=False)
    def import_seminations_from_farm(self, request):
        serializer = serializers.ImportSeminationsFile(data=request.data)
        if serializer.is_valid():
            wb = import_farm.init_wb(serializer.validated_data['file'])
            rows = import_farm.get_semenation_rows(wb)
            import_farm.is_there_single_tour_in_file(rows=rows)
            seminated_list, already_seminated_in_tour, sows_in_another_tour, proholost_list = \
                import_farm.create_semination_lists(rows, request.user)

            return Response(
            {
                "seminated_list_count": len(seminated_list),
                "seminated_list_farm_ids": [sow.farm_id for sow in seminated_list],
                "already_seminated_in_tour_count": len(already_seminated_in_tour),
                "already_seminated_in_tour_farm_ids": [sow.farm_id for sow in already_seminated_in_tour],
                "proholost_list": len(proholost_list),
                # "sows_in_another_tour_farm_ids": [sow.farm_id for sow in sows_in_another_tour], 
                "sows_in_another_tour": sows_serializers.SowSerializer(sows_in_another_tour, \
                	 many=True).data,
                "sows_in_another_tour_count": len(sows_in_another_tour),  
                "message": "Файл загружен и обработан."
            },
            status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)