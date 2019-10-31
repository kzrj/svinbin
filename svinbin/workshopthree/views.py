# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Sum

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

from sows.models import Sow, Gilt
from sows_events import models as sows_events_models
from piglets.models import NomadPigletsGroup, NewBornPigletsGroup
from piglets_events import models as piglets_events_models
from transactions import models as transactions_models
from locations import models as locations_models

from sows.views import WorkShopSowViewSet
from piglets.views import NewBornPigletsViewSet, WorkShopNomadPigletsViewSet


class WorkShopThreeNewBornPigletsViewSet(NewBornPigletsViewSet):
    @action(methods=['post'], detail=True)
    def culling_piglets(self, request, pk=None):        
        serializer = piglets_events_serializers.CullingPigletsTypesSerializer(data=request.data)
        if serializer.is_valid():
            piglets_group = self.get_object()
            culling = piglets_events_models.CullingNewBornPiglets.objects.create_culling_piglets(
                piglets_group=piglets_group,
                culling_type=serializer.validated_data['culling_type'],
                quantity=1,
                reason=serializer.validated_data['reason'],
                initiator=request.user
                )

            return Response(
                {"new_born_piglet_group": piglets_serializers.NewBornPigletsGroupSerializer(piglets_group).data,
                 "message": '%s piglet from piglet group' % serializer.validated_data['culling_type'],
                 "culling": piglets_events_serializers.CullingNewBornPigletsSerializer(culling).data},
                status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=True)
    def culling_gilts(self, request, pk=None):        
        serializer = piglets_events_serializers.CullingPigletsTypesSerializer(data=request.data)
        if serializer.is_valid():
            piglets_group = self.get_object()
            culling = piglets_events_models.CullingNewBornPiglets.objects.create_culling_gilt(
                piglets_group=piglets_group,
                culling_type=serializer.validated_data['culling_type'],
                reason=serializer.validated_data['reason'],
                initiator=request.user
                )

            return Response(
                {"piglets_group": piglets_serializers.NewBornPigletsGroupSerializer(piglets_group).data,
                 "message": '%s gilt from piglet group' % serializer.validated_data['culling_type'],
                 "culling": piglets_events_serializers.CullingNewBornPigletsSerializer(culling).data},
                status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False)
    def create_nomad_group_from_merge(self, request):
        serializer = serializers.NewBornGroupsToMerge(data=request.data)
        if serializer.is_valid():
            groups_to_merge = serializer.validated_data['piglets_groups']
            merger, nomad_group = piglets_events_models.NewBornPigletsMerger.objects.create_merger_and_return_nomad_piglets_group(
            new_born_piglets_groups=groups_to_merge,
            part_number=serializer.validated_data['part_number'],
            initiator=request.user)     

            return Response(
                {
                 "nomad_group": piglets_serializers.NomadPigletsGroupSerializer(nomad_group).data,
                 "merger": piglets_events_serializers.NewBornPigletsGroupMergerSerializer(merger).data
                 },
                status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=True)
    def create_gilt(self, request, pk=None):
        serializer = serializers.NewGiltBirthIdSerializer(data=request.data)
        if serializer.is_valid():
            new_born_group = self.get_object()
            gilt = Gilt.objects.create_gilt(
                    birth_id=serializer.validated_data['birth_id'],
                    new_born_group=new_born_group,
                )
            return Response(
                {"piglets_group": piglets_serializers. \
                    NewBornPigletsGroupSerializer(new_born_group).data,
                 "message": 'ok',
                 "gilt": sows_serializers.GiltSerializer(gilt).data,
                 },
                status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=True)
    def recount(self, request, pk=None):
        serializer = serializers.CreateRecountSerializer(data=request.data)
        if serializer.is_valid():
            new_born_group = self.get_object()
            recount = piglets_events_models.NewBornPigletsGroupRecount.objects.create_recount(
                    piglets_group=new_born_group,
                    quantity=serializer.validated_data['quantity'],
                    initiator=request.user
                )
            return Response(
                {"piglets_group": piglets_serializers. \
                    NewBornPigletsGroupSerializer(new_born_group).data,
                 "message": 'ok',
                 "recount": piglets_events_serializers. \
                    NewBornPigletsGroupRecountSerializer(recount).data,
                 },
                status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


class WorkshopInfo(viewsets.ViewSet):
    @action(methods=['get'], detail=False)
    def info(self, request, format=None):
        # to move to models
        data = dict()
        data['Цех'] = dict()
        for section in locations_models.Section.objects.filter(workshop__number=3):
            data[str(section.number)] = locations_models.Location.objects \
                .get_sowandpiglets_cells_by_section(section) \
                .get_cells_data()
            data[str(section.number)]['sow_count'] = Sow.objects.filter( \
                location__sowAndPigletsCell__section=section).count()
            piglets_count = NewBornPigletsGroup.objects.filter( \
                location__sowAndPigletsCell__section=section).aggregate(Sum('quantity'))['quantity__sum']
            data[str(section.number)]['piglets_count'] = piglets_count if piglets_count else 0

            for key in data[str(section.number)].keys():
                if data['Цех'].get(key):
                    data['Цех'][key] = data['Цех'][key] + data[str(section.number)][key]
                else:
                    data['Цех'][key] = data[str(section.number)][key]

        return Response(data)