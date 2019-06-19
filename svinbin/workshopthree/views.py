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
from workshops import serializers as workshops_serializers

from sows.models import Sow
from sows_events import models as sows_events_models
from piglets.models import NomadPigletsGroup, NewBornPigletsGroup
from piglets_events import models as piglets_events_models
from transactions import models as transactions_models
from workshops import models as workshops_models

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
                initiator=None
                )

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
            nomad_group = piglets_events_models.NewBornPigletsMerger.objects.create_merger_and_return_nomad_piglets_group(
            new_born_piglets_groups=groups_to_merge, initiator=None)     

            to_location = transactions_models.Location.objects.create_location(
                workshops_models.WorkShop.objects.get(number=11))
            transaction = transactions_models.PigletsTransaction.objects.create_transaction_without_merge(
                to_location, nomad_group, None)

            return Response(
                {"nomad_group": piglets_serializers.NomadPigletsGroupSerializer(nomad_group).data,
                 "transaction": transactions_serializers.NomadPigletsTransactionSerializer(transaction).data},
                status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WorkShopThreeSowsViewSet(WorkShopSowViewSet):
    @action(methods=['post'], detail=True)
    def sow_farrow(self, request, pk=None):
        serializer = sows_events_serializers.CreateSowFarrowSerializer(data=request.data)
        if serializer.is_valid():
            sow = self.get_object()
            farrow = sows_events_models.SowFarrow.objects.create_sow_farrow_by_sow_object(
                sow=sow,
                week=serializer.validated_data['week'],
                alive_quantity=serializer.validated_data['alive_quantity'],
                dead_quantity=serializer.validated_data['dead_quantity'],
                mummy_quantity=serializer.validated_data['mummy_quantity'],
                initiator=None
                )
            
            return Response(
                {"sow": sows_serializers.SowSerializer(sow).data,
                 "message": 'Свинья успешно опоросилась.',
                 "farrow": sows_events_serializers.SowFarrowSerializer(farrow).data},
                status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=True)
    def occupy_sow_to_cell(self, request, pk=None):
        serializer = workshops_serializers.SowAndPigletsCellIdSerializer(data=request.data)
        if serializer.is_valid():
            sow = self.get_object()
            to_location = transactions_models.Location.objects.create_location(
                workshops_models.SowAndPigletsCell.objects.get(pk=serializer.validated_data['cell_number'])
                )
            transaction = transactions_models.SowTransaction.objects.create_transaction(
                sow=sow, to_location=to_location, initiator=None)
            
            return Response(
                {"sow": sows_serializers.SowSerializer(sow).data,
                 "message": 'Свинья заселена в клетку',
                 "transaction": transactions_serializers.SowTransactionSerializer(transaction).data
                 },
                status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=True)
    def move_sow_to_workshop_one(self, request, pk=None):
        sow = self.get_object()
        to_location = transactions_models.Location.objects.create_workshop_location(1)
        transaction = transactions_models.SowTransaction.objects.create_transaction(
                sow=sow, to_location=to_location, initiator=None)

        return Response(
                {"sow": sows_serializers.SowSerializer(sow).data,
                 "message": 'Свинья перемещена в цех 1',
                 "transaction": transactions_serializers.SowTransactionSerializer(transaction).data
                 },
                status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False)
    def move_many_sows_to_workshop_one(self, request):
        serializer = serializers.SowsIdsSerializer(data=request.data)
        if serializer.is_valid():
            to_location = transactions_models.Location.objects.create_workshop_location(1)
            transactions_ids = transactions_models.SowTransaction.objects.create_many_transactions(
                sows=serializer.validated_data['sows'],
                to_location=to_location,
                initiator=None
                )
            return Response(
                {
                 "sows": sows_serializers.SowSerializer(serializer.validated_data['sows'], many=True).data,
                 "message": 'Свиньи перемещены',
                 "transaction_ids": transactions_ids
                 },
                status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=True)
    def culling_sow(self, request, pk=None):        
        serializer = sows_events_serializers.CreateCullingSowPkSerializer(data=request.data)
        if serializer.is_valid():
            sow = self.get_object()
            culling = sows_events_models.CullingSow.objects.create_culling(
                sow=sow,
                culling_type=serializer.validated_data['culling_type'],
                reason=serializer.validated_data['reason'],
                initiator=None
                )

            return Response(
                {"sow": sows_serializers.SowSerializer(sow).data,
                 "message": '%s sow ' % serializer.validated_data['culling_type'],
                 "culling": sows_events_serializers.CullingSowSerializer(culling).data},
                status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)