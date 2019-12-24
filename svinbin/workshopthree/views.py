# -*- coding: utf-8 -*-
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from workshopthree import serializers
from sows import serializers as sows_serializers
from sows_events import serializers as sows_events_serializers

from sows.models import Sow, Gilt
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
                initiator=request.user
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
            sow.mark_as_nurse
            
            return Response(
                {
                 "sow": sows_serializers.SowSerializer(sow).data,
                 "message": 'Свинья помечена как кормилица.',
                },
                status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=True)
    def create_gilt(self, request, pk=None):
        serializer = serializers.NewGiltBirthIdSerializer(data=request.data)
        if serializer.is_valid():
            sow = self.get_object()
            Gilt.objects.create_gilt(serializer.validated_data['birth_id'], sow)

            return Response(
                {
                 "message": f'Ремонтная свинка с номером {serializer.validated_data["birth_id"]} \
                        успешно создана.',
                },
                status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WorkshopInfo(viewsets.ViewSet):
    # @action(methods=['get'], detail=False)
    # def info(self, request, format=None):
    #     # to move to models
    #     data = dict()
    #     data['Цех'] = dict()
    #     for section in locations_models.Section.objects.filter(workshop__number=3):
    #         data[str(section.number)] = locations_models.Location.objects \
    #             .get_sowandpiglets_cells_by_section(section) \
    #             .get_cells_data()
    #         data[str(section.number)]['sow_count'] = Sow.objects.filter( \
    #             location__sowAndPigletsCell__section=section).count()
    #         piglets_count = NewBornPigletsGroup.objects.filter( \
    #             location__sowAndPigletsCell__section=section).aggregate(Sum('quantity'))['quantity__sum']
    #         data[str(section.number)]['piglets_count'] = piglets_count if piglets_count else 0

    #         for key in data[str(section.number)].keys():
    #             if data['Цех'].get(key):
    #                 data['Цех'][key] = data['Цех'][key] + data[str(section.number)][key]
    #             else:
    #                 data['Цех'][key] = data[str(section.number)][key]

        # return Response(data)

    @action(methods=['get'], detail=False)
    def balances_by_tours(self, request, format=None):
        tours = Tour.objects.get_tours_in_workshop_by_sows_and_piglets( \
            locations_models.WorkShop.objects.filter(number=3).first())
        return Response(tours.get_recounts_balance_data())