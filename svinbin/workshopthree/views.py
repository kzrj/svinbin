# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.utils import timezone

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

from sows.models import Sow
from sows_events import models as sows_events_models
from piglets.models import NomadPigletsGroup, NewBornPigletsGroup
from piglets_events import models as piglets_events_models
from transactions import models as transactions_models
from locations import models as locations_models

from sows.views import WorkShopSowViewSet


class WorkShopThreePigletsViewSet(viewsets.GenericViewSet):
    queryset = NewBornPigletsGroup.objects.all()
    serializer_class = piglets_serializers.NewBornPigletsGroupSerializer

    # def get_serializer_class(self):
    #     if self.action == 'mark_to_transfer_and_mark_size':
    #         return piglets_serializers.NewBornPigletsGroupSerializer
    #     return piglets_serializers.NewBornPigletsGroupSerializer

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
                initiator=request.usesr
                )
            # piglets_group.change_status_to()

            return Response(
                {"new_born_piglet_group": piglets_serializers.NewBornPigletsGroupSerializer(piglets_group).data,
                 "message": '%s piglet from piglet group' % serializer.validated_data['culling_type'],
                 "culling": piglets_events_serializers.CullingNewBornPigletsSerializer(culling).data},
                status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=True)
    def mark_to_transfer_mark_size_and_recount(self, request, pk=None):
        serializer = serializers.NewBornPigletsGroupSizeSerializer(data=request.data)
        if serializer.is_valid():
            piglets_group = self.get_object()
            piglets_group.mark_size_label(serializer.validated_data['size_label'])
            piglets_group.mark_for_transfer()

            new_amount = serializer.validated_data.get('new_amount')
            recount = None
            if new_amount:
                recount = piglets_events_models.NewBornPigletsGroupRecount.objects.create_recount(piglets_group, new_amount)

            return Response(
                {"new_born_piglet_group": piglets_serializers.NewBornPigletsGroupSerializer(piglets_group).data,
                 "message": 'piglets marked for transaction, marked as %s.' % serializer.validated_data['size_label'],
                 "recount": piglets_events_serializers.NewBornPigletsGroupRecountSerializer(recount).data},
                status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False)
    def create_nomad_group_from_merge_and_transfer_to_weight(self, request):
        serializer = serializers.NewBornGroupsToMerge(data=request.data)
        if serializer.is_valid():
            groups_to_merge = serializer.validated_data['piglets_groups']
            merger, nomad_group = piglets_events_models.NewBornPigletsMerger.objects.create_merger_and_return_nomad_piglets_group(
            new_born_piglets_groups=groups_to_merge, initiator=None)     

            to_location = locations_models.Location.objects.get(workshop__number=4)
            transaction = transactions_models.PigletsTransaction.objects.create_transaction(
                to_location, nomad_group, request.user)

            return Response(
                {
                 "nomad_group": piglets_serializers.NomadPigletsGroupSerializer(nomad_group).data,
                 "transaction": transactions_serializers.NomadPigletsTransactionSerializer(transaction).data,
                 "merger": piglets_events_serializers.NewBornPigletsGroupMergerSerializer(merger).data
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
                week=serializer.validated_data['week'],
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
