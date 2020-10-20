# -*- coding: utf-8 -*-
from datetime import datetime
from django.utils import timezone

from rest_framework import viewsets, status, generics, mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from workshopthree import serializers
from sows import serializers as sows_serializers
from sows_events import serializers as sows_events_serializers

from sows.models import Sow, Gilt
from sows_events import models as sows_events_models
from transactions.models import SowTransaction, PigletsTransaction

from sows.views import WorkShopSowViewSet
from core.permissions import ObjAndUserSameLocationPermissions, WS3Permissions, ReadOrAdminOnlyPermissions


class WorkShopThreeSowsViewSet(WorkShopSowViewSet):
    permission_classes = [IsAuthenticated, WS3Permissions]

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
                initiator=request.user,
                date=serializer.validated_data['date']
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
            sow.markasnurse_set.create_nurse_event(sow=sow, initiator=request.user, date=timezone.now())
            sow.refresh_from_db()
            
            return Response(
                {
                 "sow": sows_serializers.SowSerializer(sow).data,
                 "message": 'Свинья помечена как кормилица.',
                },
                status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @action(methods=['post'], detail=False)
    def transfer_sow_and_piglets(self, request):
        serializer = serializers.MoveSowAndPigletsSerializer(data=request.data)
        if serializer.is_valid():
            sow = serializer.validated_data['from_location'].get_sow
            piglets = serializer.validated_data['from_location'].get_piglets

            SowTransaction.objects.create_transaction(
                sow=sow,
                to_location=serializer.validated_data['to_location'],
                initiator=request.user)

            PigletsTransaction.objects.create_transaction(
                piglets_group=piglets,
                to_location=serializer.validated_data['to_location'],
                initiator=request.user)
            
            return Response(
                {
                 "message": f"Свиноматка {sow.farm_id} и поросята №{piglets.id} перемещены.",
                },
                status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=True)
    def mark_as_gilt(self, request, pk=None):
        mother_sow = self.get_object()
        serializer = serializers.MarkAsGiltCreateSerializer(data=request.data)
        
        if serializer.is_valid():
            gilt = Gilt.objects.create_gilt(
                birth_id=serializer.validated_data['birth_id'],
                mother_sow_farm_id=mother_sow.farm_id
                )
            sows_events_models.MarkAsGilt.objects.create_init_gilt_event(
                gilt=gilt, initiator=request.user, date=serializer.validated_data['date'])
            return Response(
                {
                    'message': f'Ремонтная свинка {gilt.birth_id} создана.'
                },
                status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MarksAsGiltListView(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = sows_events_models.MarkAsGilt.objects.all().select_related('gilt', 'sow', 'tour') \
        .order_by('-date')
    serializer_class = serializers.SowMarkAsGiltSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        sows_pk_list = self.filter_queryset(self.get_queryset()) \
            .values_list('sow__pk', flat=True)

        sows_qs = Sow.objects.get_queryset_with_not_alive() \
            .filter(pk__in=sows_pk_list) \
            .add_mark_as_gilt_last_date_and_last_tour() \
            .order_by('-last_date_mark')

        page = self.paginate_queryset(sows_qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(sows_qs, many=True)
        return Response(serializer.data)