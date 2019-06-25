# -*- coding: utf-8 -*-
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action

from workshopfour import serializers
import sows.serializers as sows_serializers
import sows_events.serializers as sows_events_serializers
import piglets.serializers as piglets_serializers
import piglets_events.serializers as piglets_events_serializers
import transactions.serializers as transactions_serializers
import workshops.serializers as workshops_serializers

import sows.models as sows_models
import sows_events.models as sows_events_models
import piglets.models as piglets_models
import piglets_events.models as piglets_events_models
import transactions.models as transactions_models
import workshops.models as workshops_models

from piglets.views import WorkShopNomadPigletsViewSet


class WorkShopFourPigletsViewSet(WorkShopNomadPigletsViewSet):
    @action(methods=['get'], detail=False)
    def waiting_for_weighing_piglets_outside_cells(self, request):
        workshop = workshops_models.WorkShop.objects.get(number=4)        
        piglets = piglets_models.NomadPigletsGroup.objects \
                    .piglets_in_workshop_not_in_cells(workshop) \
                    .filter(status__title='Готовы ко взвешиванию')

        return Response(
            {
             "piglets_groups": piglets_serializers.NomadPigletsGroupSerializer(piglets, many=True).data,
             "message": 'Поросята ожидающие взвешивания.',
             },
            status=status.HTTP_200_OK)
       
    @action(methods=['post'], detail=True)
    def weighing_piglets(self, request, pk=None):        
        serializer = piglets_events_serializers.WeighingPigletsCreateSerializer(data=request.data)
        if serializer.is_valid():
            piglets_group = self.get_object()
            weighing_record = piglets_events_models.WeighingPiglets.objects.create_weighing(
                piglets_group=piglets_group,
                total_weight=serializer.validated_data['total_weight'],
                place=serializer.validated_data['place'],
                initiator=None
                )

            return Response(
                {
                 "piglets_group": piglets_serializers.NomadPigletsGroupSerializer(piglets_group).data,
                 "weighing_record": piglets_events_serializers.WeighingPigletsSerializer(weighing_record).data,
                 "message": 'Взвешивание прошло успешно.',
                 },
                status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=False)
    def get_weighted_piglets_outside_cells(self, request):
        workshop = workshops_models.WorkShop.objects.get(number=4)        
        piglets = piglets_models.NomadPigletsGroup.objects \
                    .piglets_in_workshop_not_in_cells(workshop) \
                    .filter(status__title='Взвешены, готовы к заселению')
        return Response(
            {
             "piglets_groups": piglets_serializers.NomadPigletsGroupSerializer(piglets, many=True).data,
             "message": 'Взвешенные поросята, готовые к заселению в клетки.',
             },
            status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True)
    def move_one_group_to_cell(self, request, pk=None):        
        serializer = workshops_serializers.PigletsGroupCellPkSerializer(data=request.data)
        if serializer.is_valid():
            piglets_group = self.get_object()
            cell = serializer.validated_data['cell']
            to_location = transactions_models.Location.objects.create_location(cell)

            if cell.is_empty:
                transaction = transactions_models.PigletsTransaction \
                    .objects.create_transaction_without_merge(
                        to_location=to_location, piglets_group=piglets_group, initiator=None)
                piglets_group.change_status_to('Кормятся')
            
                return Response(
                    {
                     "piglets_group": piglets_serializers.NomadPigletsGroupSerializer(piglets_group).data,
                     "cell": workshops_serializers.PigletsGroupCellSerializer(cell).data,
                     "transaction": transactions_serializers \
                        .NomadPigletsTransactionSerializer(transaction).data,
                     "message": 'Клетка была пустая.',
                     },
                    status=status.HTTP_200_OK)
            else:
                transaction = transactions_models.PigletsTransaction \
                    .objects.create_transaction_without_merge(
                        to_location=to_location, piglets_group=piglets_group, initiator=None)

                new_to_location = transactions_models.Location.objects.duplicate_location(to_location)
                merged_group = piglets_events_models.NomadPigletsGroupMerger.objects \
                    .create_merger_and_return_nomad_piglets_group(
                        nomad_groups=cell.get_list_of_residents(),
                        new_location=new_to_location,
                        initiator=None
                        )

                return Response(
                    {                     
                     "merged_group": piglets_serializers.NomadPigletsGroupSerializer(merged_group).data,
                     "transaction": transactions_serializers.NomadPigletsTransactionSerializer(transaction).data,
                     "cell": workshops_serializers.PigletsGroupCellSerializer(cell).data,

                     "message": 'Клетка была не пустая.',
                     },
                    status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @action(methods=['post'], detail=False)
    def move_group_from_cell_to_cell(self, request):        
        serializer = serializers.MoveFromCellToCellSerializer(data=request.data)
        if serializer.is_valid():
            from_cell = serializer.validated_data['from_cell']
            moving_group = from_cell.get_list_of_residents()[0]
            quantity = serializer.validated_data['quantity']
            
            if quantity < moving_group.quantity:
                other_group, moving_group = piglets_events_models.SplitNomadPigletsGroup.objects.split_group(
                    parent_nomad_group=moving_group,
                    new_group_piglets_amount=quantity,
                    initiator=None
                    )

            to_cell = serializer.validated_data['to_cell']
            to_location = transactions_models.Location.objects.create_location(to_cell)

            if to_cell.is_empty:
                transaction = transactions_models.PigletsTransaction \
                    .objects.create_transaction_without_merge(
                        to_location=to_location, piglets_group=moving_group, initiator=None)
            
                return Response(
                    {
                     "moving_group": piglets_serializers.NomadPigletsGroupSerializer(moving_group).data,
                     "from_cell": workshops_serializers.PigletsGroupCellSerializer(from_cell).data,
                     "to_cell": workshops_serializers.PigletsGroupCellSerializer(to_cell).data,
                     "transaction": transactions_serializers \
                        .NomadPigletsTransactionSerializer(transaction).data,
                     "message": 'Клетка была пустая.',
                     },
                    status=status.HTTP_200_OK)
            else:
                transaction = transactions_models.PigletsTransaction \
                    .objects.create_transaction_without_merge(
                        to_location=to_location, piglets_group=moving_group, initiator=None)

                new_to_location = transactions_models.Location.objects.duplicate_location(to_location)
                merged_group = piglets_events_models.NomadPigletsGroupMerger.objects \
                    .create_merger_and_return_nomad_piglets_group(
                        nomad_groups=to_cell.get_list_of_residents(),
                        new_location=new_to_location,
                        initiator=None
                        )

                return Response(
                    {           
                     "moving_group": piglets_serializers.NomadPigletsGroupSerializer(moving_group).data,          
                     "merged_group": piglets_serializers.NomadPigletsGroupSerializer(merged_group).data,
                     "from_cell": workshops_serializers.PigletsGroupCellSerializer(from_cell).data,
                     "to_cell": workshops_serializers.PigletsGroupCellSerializer(to_cell).data,
                     "transaction": transactions_serializers.NomadPigletsTransactionSerializer(transaction).data,
                     "message": 'Клетка была не пустая.',
                     },
                    status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    # @action(methods=['post'], detail=True)
    # def culling_piglets(self, request, pk=None):        
    #     serializer = piglets_events_serializers.CullingPigletsTypesSerializer(data=request.data)
    #     if serializer.is_valid():
    #         piglets_group = self.get_object()
    #         culling = piglets_events_models.CullingNewBornPiglets.objects.create_culling_piglets(
    #             piglets_group=piglets_group,
    #             culling_type=serializer.validated_data['culling_type'],
    #             quantity=1,
    #             reason=serializer.validated_data['reason'],
    #             initiator=None
    #             )

    #         return Response(
    #             {"new_born_piglet_group": piglets_serializers.NewBornPigletsGroupSerializer(piglets_group).data,
    #              "message": '%s piglet from piglet group' % serializer.validated_data['culling_type'],
    #              "culling": piglets_events_serializers.CullingNewBornPigletsSerializer(culling).data},
    #             status=status.HTTP_200_OK)
    #     else:
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # @action(methods=['post'], detail=True)
    # def mark_to_transfer_mark_size_and_recount(self, request, pk=None):
    #     serializer = serializers.NewBornPigletsGroupSizeSerializer(data=request.data)
    #     if serializer.is_valid():
    #         piglets_group = self.get_object()
    #         piglets_group.mark_size_label(serializer.validated_data['size_label'])
    #         piglets_group.mark_for_transfer()

    #         new_amount = serializer.validated_data.get('new_amount')
    #         recount = None
    #         if new_amount:
    #             recount = piglets_events_models.NewBornPigletsGroupRecount.objects.create_recount(piglets_group, new_amount)

    #         return Response(
    #             {"new_born_piglet_group": piglets_serializers.NewBornPigletsGroupSerializer(piglets_group).data,
    #              "message": 'piglets marked for transaction, marked as %s.' % serializer.validated_data['size_label'],
    #              "recount": piglets_events_serializers.NewBornPigletsGroupRecountSerializer(recount).data},
    #             status=status.HTTP_200_OK)
    #     else:
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # @action(methods=['post'], detail=False)
    # def create_nomad_group_from_merge_and_transfer_to_weight(self, request):
    #     serializer = serializers.NewBornGroupsToMerge(data=request.data)
    #     if serializer.is_valid():
    #         groups_to_merge = serializer.validated_data['piglets_groups']
    #         nomad_group = piglets_events_models.NewBornPigletsMerger.objects.create_merger_and_return_nomad_piglets_group(
    #         new_born_piglets_groups=groups_to_merge, initiator=None)     

    #         to_location = transactions_models.Location.objects.create_location(
    #             workshops_models.WorkShop.objects.get(number=11))
    #         transaction = transactions_models.PigletsTransaction.objects.create_transaction_without_merge(
    #             to_location, nomad_group, None)

    #         return Response(
    #             {"nomad_group": piglets_serializers.NomadPigletsGroupSerializer(nomad_group).data,
    #              "transaction": transactions_serializers.NomadPigletsTransactionSerializer(transaction).data},
    #             status=status.HTTP_200_OK)
    #     else:
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


