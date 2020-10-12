# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone

from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

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
from core.permissions import ObjAndUserSameLocationPermissions, ReadOrAdminOnlyPermissions, WS12Permissions
    

class WorkShopOneTwoSowViewSet(WorkShopSowViewSet):
    permission_classes = [IsAuthenticated, WS12Permissions]

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
                    "message": f'Свиноматка {sow.farm_id} помечена.',
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
                    "message": "Осеменение проведено."
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

    @action(methods=['post'], detail=False, serializer_class=sows_events_serializers.SowsMassCullingSerializer)
    def mass_culling(self, request):
        serializer = sows_events_serializers.SowsMassCullingSerializer(data=request.data)
        if serializer.is_valid():
            sows_qs = sows_models.Sow.objects.filter(pk__in=serializer.validated_data['sows'])
            sows_events_models.CullingSow.objects.mass_culling(
                sows_qs=sows_qs,
                culling_type=serializer.validated_data['culling_type'],
                reason=serializer.validated_data['reason'],
                weight=serializer.validated_data['weight'],
                initiator=request.user
                )

            return Response(
                {
                    "message": f"Свиноматки выбыли."
                },
                status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False, serializer_class=sows_events_serializers.CreateDoubleSeminationSerializer)
    def double_semination(self, request):
        serializer = sows_events_serializers.CreateDoubleSeminationSerializer(data=request.data)
        if serializer.is_valid():
            sow = sows_models.Sow.objects.get_queryset_with_not_alive() \
                .filter(farm_id=serializer.validated_data['farm_id']).first()
            sow.prepare_for_double_semenation()

            semination1 = sows_events_models.Semination.objects.create_semination(
                sow=sow, week=serializer.validated_data['week'],
                initiator=request.user, 
                semination_employee=serializer.validated_data['seminator1'],
                boar=serializer.validated_data['boar1'])

            semination2 = sows_events_models.Semination.objects.create_semination(
                sow=sow, week=serializer.validated_data['week'],
                initiator=request.user, 
                semination_employee=serializer.validated_data['seminator2'],
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

    