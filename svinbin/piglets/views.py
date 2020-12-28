# # -*- coding: utf-8 -*-
from django.utils import timezone

from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

import piglets.serializers as piglets_serializers
import piglets_events.serializers as piglets_events_serializers
import sows.serializers as sows_serializers

import piglets.models as piglets_models
import piglets_events.models as piglets_events_models
import sows.models as sows_models
import sows_events.models as sows_events_models
import transactions.models as transactions_models
import locations.models as locations_models

from piglets.filters import PigletsFilter
from core.permissions import ObjAndUserSameLocationPermissions, WS3Permissions, ReadOrAdminOnlyPermissions


class PigletsViewSet(viewsets.ModelViewSet):
    queryset = piglets_models.Piglets.objects.all()
    serializer_class = piglets_serializers.PigletsSerializer
    filter_class = PigletsFilter
    permission_classes = [ObjAndUserSameLocationPermissions]

    # if overwrite get_permissions then permissions on actions will not work
    
    # def get_permissions(self):
    #     if self.action == 'list':
    #         permission_classes = [IsAuthenticated]
    #     elif self.action == 'create' or self.action == 'delete' or self.action == 'put' \
    #         or self.action == 'patch':
    #         permission_classes = [ReadOrAdminOnlyPermissions]
    #     else:
    #         permission_classes = [IsAuthenticated, ObjAndUserSameLocationPermissions]
    #     return [permission() for permission in permission_classes]

    def list(self, request):
        queryset = self.filter_queryset(
            self.get_queryset() \
                .prefetch_related('metatour__week_tour')
        )

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = piglets_serializers.PigletsSimpleSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = piglets_serializers.PigletsSimpleSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['post'], detail=False, permission_classes=[IsAuthenticated, WS3Permissions])
    def create_from_merging_list_and_move_to_ws4(self, request):
        serializer = piglets_serializers.MergeFromListSerializer(data=request.data)
        if serializer.is_valid():
            new_location = locations_models.Location.objects.get(workshop__number=3)
            merged_piglets = piglets_events_models.PigletsMerger.objects.create_from_merging_list(
                merging_list=serializer.validated_data['records'], new_location=new_location,
                initiator=request.user, date=timezone.now())
            merged_piglets.change_status_to('Готовы ко взвешиванию')

            if serializer.validated_data.get('transfer_part_number', None):
                merged_piglets.assign_transfer_part_number(serializer.validated_data['transfer_part_number'])

            to_location = locations_models.Location.objects.get(workshop__number=4)
            transaction = transactions_models.PigletsTransaction.objects.create_transaction(
                to_location=to_location, piglets_group=merged_piglets,
                initiator=request.user, date=timezone.now())
            return Response(
                {
                  "message": 'Партия создана и перемещена в Цех4.',
                  "piglets": piglets_serializers.PigletsSimpleSerializer(merged_piglets).data
                 },
                 
                status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=True)
    def culling(self, request, pk=None):
        serializer = piglets_events_serializers.CullingPigletsSerializer(data=request.data)
        if serializer.is_valid():
            date = timezone.now()
            if not serializer.validated_data['date']:
                date = serializer.validated_data['date']

            piglets_events_models.CullingPiglets.objects.create_culling_piglets(
                piglets_group=self.get_object(),
                culling_type=serializer.validated_data['culling_type'],
                reason=serializer.validated_data['reason'],
                is_it_gilt=serializer.validated_data['is_it_gilt'],
                quantity=serializer.validated_data['quantity'],
                total_weight=serializer.validated_data['total_weight'],
                date=date,
                initiator=request.user
                )
            return Response(
                {
                  "message": 'Выбраковка прошла успешно.',
                 },
                 
                status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=True)
    def weighing_piglets(self, request, pk=None):        
        serializer = piglets_events_serializers.WeighingPigletsCreateSerializer(data=request.data)
        if serializer.is_valid():
            piglets_group = self.get_object()
            weighing_record = piglets_events_models.WeighingPiglets.objects.create_weighing(
                piglets_group=piglets_group,
                total_weight=serializer.validated_data['total_weight'],
                place=serializer.validated_data['place'],
                initiator=request.user,
                date=timezone.now()
                )

            return Response(
                {
                 "weighing_record": piglets_events_serializers.WeighingPigletsSerializer(weighing_record).data,
                 "message": 'Взвешивание прошло успешно.',
                 },
                status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=True)
    def weighing_piglets_split_return(self, request, pk=None):        
        serializer = piglets_events_serializers.WeighingReturnPigletsCreateSerializer(data=request.data)
        if serializer.is_valid():
            piglets_group = self.get_object()
            piglets_to_weight = self.get_object()
            message = "Взвешивание прошло успешно"
            
            # mb to model
            new_amount = serializer.validated_data.get('new_amount', None)
            if new_amount and new_amount > 0 and new_amount < piglets_group.quantity:
                transaction, moved_piglets, piglets_to_weight, split_event, merge_event = \
                    transactions_models.PigletsTransaction.objects.transaction_with_split_and_merge(
                        piglets=piglets_group,
                        to_location=serializer.validated_data['to_location'],
                        new_amount=serializer.validated_data['new_amount'],
                        reverse=True,
                        merge=False,
                        gilts_contains=True,
                        initiator=request.user,
                        date=timezone.now()
                    )
                moved_piglets.change_status_to('Взвешены, готовы к заселению')
                message = "Взвешивание прошло успешно. Возврат поросят прошел успешно."

            weighing_record = piglets_events_models.WeighingPiglets.objects.create_weighing(
                piglets_group=piglets_to_weight,
                total_weight=serializer.validated_data['total_weight'],
                place=serializer.validated_data['place'],
                initiator=request.user
                )

            return Response(
                {
                 "weighing_record": piglets_events_serializers.WeighingPigletsSerializer(weighing_record).data,
                 "message": message,
                 },
                status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=True)
    def recount_and_weighing_piglets(self, request, pk=None):        
        serializer = piglets_events_serializers.RecountWeighingPigletsSerializer(data=request.data)
        if serializer.is_valid():
            piglets_group = self.get_object()

            if serializer.validated_data.get('new_quantity', None):
                recount = piglets_events_models.Recount.objects.create_recount(piglets_group, 
                    serializer.validated_data['new_quantity'], request.user)

            weighing_record = piglets_events_models.WeighingPiglets.objects.create_weighing(
                piglets_group=piglets_group,
                total_weight=serializer.validated_data['total_weight'],
                place=serializer.validated_data['place'],
                initiator=request.user,
                date=timezone.now()
                )

            return Response(
                {
                 "weighing_record": piglets_events_serializers.WeighingPigletsSerializer(weighing_record).data,
                 "message": 'Взвешивание прошло успешно.',
                 },
                status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=True)
    def move_piglets(self, request, pk=None):        
        serializer = piglets_serializers.MovePigletsSerializer(data=request.data)
        if serializer.is_valid():
            piglets = piglets_models.Piglets.objects.select_related('location', 'status').get(pk=pk)
            transaction, moved_piglets, stayed_piglets, split_event, merge_event = \
                transactions_models.PigletsTransaction.objects.transaction_with_split_and_merge(
                    piglets= self.get_object(),
                    to_location=serializer.validated_data['to_location'],
                    new_amount=serializer.validated_data.get('new_amount', None),
                    gilts_contains=serializer.validated_data.get('gilts_contains', False),
                    merge=serializer.validated_data['merge'],
                    initiator=request.user,
                    date=timezone.now()
                    )

            return Response(
                {
                 "message": 'Перевод прошел успешно.',
                 },
                status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=True, permission_classes=[ObjAndUserSameLocationPermissions])
    def recount_piglets(self, request, pk=None):        
        serializer = piglets_events_serializers.RecountPigletsSerializer(data=request.data)
        if serializer.is_valid():
            piglets_group = self.get_object()
            piglets_events_models.Recount.objects.create_recount(
              piglets=piglets_group,
              new_quantity=serializer.validated_data['new_quantity'],
              comment=serializer.validated_data.get('comment', None),
              initiator=request.user,
              date=timezone.now()
              )
            return Response(
                {
                 "message": 'Пересчет прошел успешно.',
                 },
                status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @action(methods=['post'], detail=True, permission_classes=[IsAuthenticated, WS3Permissions])
    def create_gilt(self, request, pk=None):        
        serializer = sows_serializers.GiltCreateSerializer(data=request.data)
        if serializer.is_valid():

            gilt = sows_models.Gilt.objects.create_gilt(
              birth_id=serializer.validated_data['birth_id'],
              mother_sow_farm_id=serializer.validated_data['mother_sow_farm_id'],
              piglets=self.get_object()              
              )
            sows_events_models.MarkAsGilt.objects.create_init_gilt_event(gilt=gilt,
             initiator=request.user, date=timezone.now())

            return Response(
                {
                 "message": 'Ремонтная свинка создана успешно.',
                 },
                status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=True)
    def move_gilts_to_12(self, request, pk=None):        
        serializer = piglets_serializers.MoveGiltsToWs12Serializer(data=request.data)
        if serializer.is_valid():
            piglets = self.get_object()

            stayed_piglets, moved_piglets = piglets_events_models.PigletsSplit.split_return_groups(
                parent_piglets=piglets,
                new_amount=serializer.validated_data.get('new_amount', None),
                gilts_to_new=True,
                initiator=request.user,
                date=timezone.now(),
                )

            piglets_events_models.WeighingPiglets.objects.create_weighing(
                piglets_group=moved_piglets,
                total_weight=serializer.validated_data['total_weight'],
                place='o/2',
                date=timezone.now(),
                initiator=request.user
                )

            sows_events_models.PigletsToSowsEvent.objects.create_event(piglets=moved_piglets,
             initiator=request.user, date=timezone.now())

            return Response(
                {
                 "message": 'Ремонтные свинки переведены успешно.',
                 },
                status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)