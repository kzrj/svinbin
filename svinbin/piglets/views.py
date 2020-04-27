# # -*- coding: utf-8 -*-
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

import piglets.serializers as piglets_serializers
import piglets_events.serializers as piglets_events_serializers
import sows.serializers as sows_serializers

import piglets.models as piglets_models
import piglets_events.models as piglets_events_models
import sows.models as sows_models
import transactions.models as transactions_models
import locations.models as locations_models

from piglets.filters import PigletsFilter


class PigletsViewSet(viewsets.ModelViewSet):
    queryset = piglets_models.Piglets.objects.all()
    serializer_class = piglets_serializers.PigletsSerializer
    filter_class = PigletsFilter

    def list(self, request):
        queryset = self.filter_queryset(
            self.get_queryset() \
                .prefetch_related('metatour__records__tour__sowfarrow_set')
        )

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = piglets_serializers.PigletsSimpleSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = piglets_serializers.PigletsSimpleSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['post'], detail=False)
    def merge_init_list_and_move_merged_to_ws4(self, request):
        serializer = piglets_serializers.MergeFromInitListSerializer(data=request.data)
        if serializer.is_valid():
            merged_piglets = piglets_events_models.PigletsMerger.objects.merge_piglets_from_init_list(
                init_list=serializer.validated_data['records'], initiator=request.user)

            if serializer.validated_data.get('transfer_part_number', None):
                merged_piglets.assign_transfer_part_number(serializer.validated_data['transfer_part_number'])

            to_location = locations_models.Location.objects.get(workshop__number=4)
            transaction = transactions_models.PigletsTransaction.objects.create_transaction(
                to_location=to_location, piglets_group=merged_piglets, initiator=request.user)
            return Response(
                {
                  "message": 'Партия создана и перемещена в Цех4.',
                 },
                 
                status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False)
    def create_from_merging_list_and_move_to_ws4(self, request):
        serializer = piglets_serializers.MergeFromListSerializer(data=request.data)
        if serializer.is_valid():
            new_location = locations_models.Location.objects.get(workshop__number=3)
            merged_piglets = piglets_events_models.PigletsMerger.objects.create_from_merging_list(
                merging_list=serializer.validated_data['records'], new_location=new_location,
                initiator=request.user)

            if serializer.validated_data.get('transfer_part_number', None):
                merged_piglets.assign_transfer_part_number(serializer.validated_data['transfer_part_number'])
                merged_piglets.change_status_to('Готовы ко взвешиванию')

            to_location = locations_models.Location.objects.get(workshop__number=4)
            transaction = transactions_models.PigletsTransaction.objects.create_transaction(
                to_location=to_location, piglets_group=merged_piglets, initiator=request.user)
            return Response(
                {
                  "message": 'Партия создана и перемещена в Цех4.',
                 },
                 
                status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=True)
    def culling(self, request, pk=None):
        serializer = piglets_events_serializers.CullingPigletsSerializer(data=request.data)
        if serializer.is_valid():
            piglets_events_models.CullingPiglets.objects.create_culling_piglets(
                piglets_group=self.get_object(),
                culling_type=serializer.validated_data['culling_type'],
                reason=serializer.validated_data['reason'],
                is_it_gilt=serializer.validated_data['is_it_gilt'],
                quantity=serializer.validated_data['quantity'],
                total_weight=serializer.validated_data['total_weight'],
                date=serializer.validated_data['date'],
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
                initiator=request.user
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
            if serializer.validated_data.get('new_amount', None) or serializer.validated_data.get('new_amount', 0):
                transaction, moved_piglets, piglets_to_weight, split_event, merge_event = \
                    transactions_models.PigletsTransaction.objects.transaction_with_split_and_merge(
                        piglets=piglets_group,
                        to_location=serializer.validated_data['to_location'],
                        new_amount=serializer.validated_data['new_amount'],
                        reverse=True,
                        merge=False,
                        gilts_contains=True,
                        initiator=request.user
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
                initiator=request.user
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
            # piglets = self.get_object()
            transaction, moved_piglets, stayed_piglets, split_event, merge_event = \
                transactions_models.PigletsTransaction.objects.transaction_with_split_and_merge(
                    piglets= self.get_object(),
                    to_location=serializer.validated_data['to_location'],
                    new_amount=serializer.validated_data.get('new_amount', None),
                    gilts_contains=serializer.validated_data.get('gilts_contains', False),
                    merge=serializer.validated_data['merge'],
                    initiator=request.user
                    )

            return Response(
                {
                 "message": 'Перевод прошел успешно.',
                 },
                status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=True)
    def move_gilts_to_ws75(self, request, pk=None):        
        serializer = piglets_serializers.MoveGiltsToWs75Serializer(data=request.data)
        if serializer.is_valid():
            piglets = piglets_models.Piglets.objects.select_related('location', 'status').get(pk=pk)
            
            transaction = transactions_models.PigletsTransaction.objects.transaction_gilts_to_7_5(
                    piglets= self.get_object(),
                    gilts_amount=serializer.validated_data.get('gilts_amount', None),                    
                    initiator=request.user
                    )

            return Response(
                {
                 "message": 'Перевод прошел успешно.',
                 },
                status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=True)
    def move_gilts_to_ws1(self, request, pk=None):        
        serializer = piglets_serializers.MovePigletsSerializer(data=request.data)
        if serializer.is_valid():
            transaction, moved_piglets, stayed_piglets, split_event, merge_event = \
                transactions_models.PigletsTransaction.objects.transaction_with_split_and_merge(
                    piglets= self.get_object(),
                    to_location=serializer.validated_data['to_location'],
                    new_amount=serializer.validated_data.get('new_amount', None),
                    )

            # create sows-gilts count = moved_piglets.quantity. location ws1
            sows_models.Sow.objects.create_from_gilts_group(moved_piglets)

            # moved_piglets deactivate
            moved_piglets.deactivate()

            return Response(
                {
                 "message": 'Перевод прошел успешно. Ремонтные свинки стали свиноматками.',
                 },
                status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False)
    def init_piglets_from_farrow(self, request, pk=None):        
        serializer = piglets_serializers.InitPigletsSerializer(data=request.data)
        if serializer.is_valid():
            location = serializer.validated_data['location']

            if serializer.validated_data.get('from_location', None) and \
              serializer.validated_data.get('transaction_date', None):
                location = serializer.validated_data['from_location']

            piglets = piglets_models.Piglets.objects.init_piglets_by_farrow_date(
                serializer.validated_data['farrow_date'],
                location,
                serializer.validated_data['quantity'],
                serializer.validated_data.get('gilts_quantity', 0)
                )

            if serializer.validated_data.get('from_location', None) and \
              serializer.validated_data.get('transaction_date', None):
                transactions_models.PigletsTransaction.objects.create_transaction(
                    serializer.validated_data['location'], piglets,
                    request.user, serializer.validated_data.get('transaction_date', None))
                
            piglets.change_status_to('Готовы ко взвешиванию')

            return Response(
                {
                 "message": 'Свиньи успешно созданы.',
                 },
                status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @action(methods=['post'], detail=True)
    def recount_piglets(self, request, pk=None):        
        serializer = piglets_events_serializers.RecountPigletsSerializer(data=request.data)
        if serializer.is_valid():
            piglets_group = self.get_object()
            piglets_events_models.Recount.objects.create_recount(piglets_group,
              serializer.validated_data['new_quantity'],
              serializer.validated_data.get('comment', None),
              request.user)
            return Response(
                {
                 "message": 'Пересчет прошел успешно.',
                 },
                status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @action(methods=['post'], detail=True)
    def create_gilt(self, request, pk=None):        
        serializer = sows_serializers.GiltCreateSerializer(data=request.data)
        if serializer.is_valid():

            sows_models.Gilt.objects.create_gilt(
              birth_id=serializer.validated_data['birth_id'],
              mother_sow_farm_id=serializer.validated_data['mother_sow_farm_id'],
              piglets=self.get_object()              
              )

            return Response(
                {
                 "message": 'Ремонтная свинка создана успешно.',
                 },
                status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)