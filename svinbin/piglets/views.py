# # -*- coding: utf-8 -*-
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

import piglets.serializers as piglets_serializers
# import piglets_events.serializers as piglets_events_serializers
# import transactions.serializers as transactions_serializers
# import locations.serializers as locations_serializers

import piglets.models as piglets_models
import piglets_events.models as piglets_events_models
import transactions.models as transactions_models
import locations.models as locations_models

# from piglets.filters import PigletsFilter


class PigletsViewSet(viewsets.ModelViewSet):
    queryset = piglets_models.Piglets.objects.all()
    serializer_class = piglets_serializers.PigletsSerializer
    # filter_class = NomadPigletsGroupFilter

    @action(methods=['post'], detail=False)
    def create_from_merging_list_and_move_to_ws4(self, request):
        serializer = piglets_serializers.MergeFromListRecordSerializer(data=request.data, many=True)
        if serializer.is_valid():
            new_location = locations_models.Location.objects.get(workshop__number=3)
            merged_piglets = piglets_events_models.PigletsMerger.objects.create_from_merging_list(
                merging_list=serializer.validated_data, new_location=new_location, initiator=request.user)
            
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



















# class WorkShopNomadPigletsViewSet(NomadPigletsGroupViewSet):
#     @action(methods=['post'], detail=True)
#     def create_gilt(self, request, pk=None):
#         serializer = serializers.NewGiltBirthIdSerializer(data=request.data)
#         if serializer.is_valid():
#             new_born_group = self.get_object()
#             gilt = Gilt.objects.create_gilt(
#                     birth_id=serializer.validated_data['birth_id'],
#                     new_born_group=new_born_group,
#                 )
#             return Response(
#                 {"piglets_group": piglets_serializers. \
#                     NewBornPigletsGroupSerializer(new_born_group).data,
#                  "message": 'Ремонтная свинка пронумерована.',
#                  "gilt": sows_serializers.GiltSerializer(gilt).data,
#                  },
#                 status=status.HTTP_200_OK)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     @action(methods=['post'], detail=True)
#     def recount(self, request, pk=None):
#         serializer = serializers.CreateRecountSerializer(data=request.data)
#         if serializer.is_valid():
#             new_born_group = self.get_object()
#             recount = piglets_events_models.NewBornPigletsGroupRecount.objects.create_recount(
#                     piglets_group=new_born_group,
#                     quantity=serializer.validated_data['quantity'],
#                     initiator=request.user
#                 )
#             return Response(
#                 {"piglets_group": piglets_serializers. \
#                     NewBornPigletsGroupSerializer(new_born_group).data,
#                  "message": 'ok',
#                  "recount": piglets_events_serializers. \
#                     NewBornPigletsGroupRecountSerializer(recount).data,
#                  },
#                 status=status.HTTP_200_OK)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     @action(methods=['post'], detail=True)
#     def weighing_piglets(self, request, pk=None):        
#         serializer = piglets_events_serializers.WeighingPigletsCreateSerializer(data=request.data)
#         if serializer.is_valid():
#             piglets_group = self.get_object()
#             weighing_record = piglets_events_models.WeighingPiglets.objects.create_weighing(
#                 piglets_group=piglets_group,
#                 total_weight=serializer.validated_data['total_weight'],
#                 place=serializer.validated_data['place'],
#                 initiator=request.user
#                 )

#             return Response(
#                 {
#                  "piglets_group": piglets_serializers.NomadPigletsGroupSerializer(piglets_group).data,
#                  "weighing_record": piglets_events_serializers.WeighingPigletsSerializer(weighing_record).data,
#                  "message": 'Взвешивание прошло успешно.',
#                  },
#                 status=status.HTTP_200_OK)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     @action(methods=['post'], detail=True)
#     def move_one_group_to_cell(self, request, pk=None):        
#         serializer = piglets_serializers.MoveToSerializer(data=request.data)
#         if serializer.is_valid():
#             piglets_group = self.get_object()
#             location = serializer.validated_data['to_location']
#             quantity = serializer.validated_data['quantity']
#             gilts_quantity = serializer.validated_data['gilts_quantity']

#             if quantity < piglets_group.quantity:
#                 other_group, piglets_group = piglets_events_models.SplitNomadPigletsGroup.\
#                     objects.split_group(
#                         parent_nomad_group=piglets_group,
#                         new_group_piglets_amount=quantity,
#                         new_group_gilts_quantity=gilts_quantity,
#                         initiator=request.user
#                         )

#             if location.is_nomad_piglet_group_cell_empty():
#                 transaction = transactions_models.PigletsTransaction \
#                     .objects.create_transaction(
#                         to_location=location,
#                         piglets_group=piglets_group, initiator=request.user)
#                 piglets_group.change_status_to('Кормятся')
            
#                 return Response(
#                     {
#                      "piglets_group": piglets_serializers.NomadPigletsGroupSerializer(piglets_group).data,
#                      "location": locations_serializers.LocationPigletsGrouspCellSerializer(location).data,
#                      "transaction": transactions_serializers \
#                         .NomadPigletsTransactionSerializer(transaction).data,
#                      "message": 'Клетка была пустая.',
#                      },
#                     status=status.HTTP_200_OK)
#             else:
#                 transaction = transactions_models.PigletsTransaction \
#                     .objects.create_transaction(
#                         to_location=location,
#                         piglets_group=piglets_group, initiator=request.user)

#                 merged_group = piglets_events_models.NomadPigletsGroupMerger.objects \
#                     .create_merger_and_return_nomad_piglets_group(
#                         nomad_groups=location.get_located_active_nomad_groups(),
#                         new_location=location,
#                         initiator=request.user
#                         )

#                 return Response(
#                     {                     
#                      "merged_group": piglets_serializers.NomadPigletsGroupSerializer(merged_group).data,
#                      "transaction": transactions_serializers.NomadPigletsTransactionSerializer(transaction).data,
#                      "location": locations_serializers.LocationPigletsGrouspCellSerializer(location).data,
#                      "message": 'Клетка была не пустая.',
#                      },
#                     status=status.HTTP_200_OK)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#     @action(methods=['post'], detail=False)
#     def move_group_from_cell_to_cell(self, request):        
#         serializer = piglets_serializers.MoveFromCellToCellSerializer(data=request.data)
#         if serializer.is_valid():
#             from_location = serializer.validated_data['from_location']
#             moving_group = from_location.get_located_active_nomad_groups()[0]
#             quantity = serializer.validated_data['quantity']
#             gilts_quantity = serializer.validated_data['gilts_quantity']
            
#             if quantity < moving_group.quantity:
#                 other_group, moving_group = piglets_events_models.SplitNomadPigletsGroup.objects.split_group(
#                     parent_nomad_group=moving_group,
#                     new_group_piglets_amount=quantity,
#                     new_group_gilts_quantity=gilts_quantity,
#                     initiator=request.user
#                     )

#             to_location = serializer.validated_data['to_location']
#             if to_location.is_nomad_piglet_group_cell_empty():
#                 transaction = transactions_models.PigletsTransaction \
#                     .objects.create_transaction(
#                         to_location=to_location, piglets_group=moving_group, initiator=request.user)
            
#                 return Response(
#                     {
#                      "moving_group": piglets_serializers.NomadPigletsGroupSerializer(moving_group).data,
#                      "from_location": locations_serializers.LocationPigletsGrouspCellSerializer(from_location).data,
#                      "to_location": locations_serializers.LocationPigletsGrouspCellSerializer(to_location).data,
#                      "transaction": transactions_serializers \
#                         .NomadPigletsTransactionSerializer(transaction).data,
#                      "message": 'Клетка была пустая.',
#                      },
#                     status=status.HTTP_200_OK)
#             else:
#                 transaction = transactions_models.PigletsTransaction \
#                     .objects.create_transaction(
#                         to_location=to_location, piglets_group=moving_group, initiator=request.user)

#                 merged_group = piglets_events_models.NomadPigletsGroupMerger.objects \
#                     .create_merger_and_return_nomad_piglets_group(
#                         nomad_groups=to_location.get_located_active_nomad_groups(),
#                         new_location=to_location,
#                         initiator=request.user
#                         )

#                 return Response(
#                     {           
#                      "moving_group": piglets_serializers.NomadPigletsGroupSerializer(moving_group).data,          
#                      "merged_group": piglets_serializers.NomadPigletsGroupSerializer(merged_group).data,
#                      "from_location": locations_serializers.LocationPigletsGrouspCellSerializer(from_location).data,
#                      "to_location": locations_serializers.LocationPigletsGrouspCellSerializer(to_location).data,
#                      "transaction": transactions_serializers.NomadPigletsTransactionSerializer(transaction).data,
#                      "message": 'Клетка была не пустая.',
#                      },
#                     status=status.HTTP_200_OK)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     @action(methods=['post'], detail=True)
#     def culling_piglets(self, request, pk=None):        
#         serializer = piglets_events_serializers.CullingPigletsTypesSerializer(data=request.data)
#         if serializer.is_valid():
#             piglets_group = self.get_object()
#             culling = piglets_events_models.CullingNomadPiglets.objects.create_culling_piglets(
#                 piglets_group=piglets_group,
#                 culling_type=serializer.validated_data['culling_type'],
#                 reason=serializer.validated_data['reason'],
#                 initiator=request.user
#                 )

#             return Response(
#                 {"piglets_group": piglets_serializers.NomadPigletsGroupSerializer(piglets_group).data,
#                  "message": '%s piglet from piglet group' % serializer.validated_data['culling_type'],
#                  "culling": piglets_events_serializers.CullingNomadPigletsSerializer(culling).data},
#                 status=status.HTTP_200_OK)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     @action(methods=['post'], detail=True)
#     def culling_gilts(self, request, pk=None):        
#         serializer = piglets_events_serializers.CullingPigletsTypesSerializer(data=request.data)
#         if serializer.is_valid():
#             piglets_group = self.get_object()
#             culling = piglets_events_models.CullingNomadPiglets.objects.create_culling_gilt(
#                 piglets_group=piglets_group,
#                 culling_type=serializer.validated_data['culling_type'],
#                 reason=serializer.validated_data['reason'],
#                 initiator=request.user
#                 )

#             return Response(
#                 {"piglets_group": piglets_serializers.NomadPigletsGroupSerializer(piglets_group).data,
#                  "message": '%s gilt from piglet group' % serializer.validated_data['culling_type'],
#                  "culling": piglets_events_serializers.CullingNomadPigletsSerializer(culling).data},
#                 status=status.HTTP_200_OK)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     @action(methods=['post'], detail=True)
#     def move_to(self, request, pk=None):        
#         serializer = piglets_serializers.MoveToSerializer(data=request.data)
#         if serializer.is_valid():
#             moving_group = self.get_object()
#             quantity = serializer.validated_data['quantity']
#             gilts_quantity = serializer.validated_data['gilts_quantity']

#             if quantity < moving_group.quantity:
#                 other_group, moving_group = piglets_events_models.SplitNomadPigletsGroup.objects.split_group(
#                     parent_nomad_group=moving_group,
#                     new_group_piglets_amount=quantity,
#                     new_group_gilts_quantity=gilts_quantity,
#                     initiator=request.user
#                     )

#             transaction = transactions_models.PigletsTransaction.objects.create_transaction(
#                 piglets_group=moving_group,
#                 to_location=serializer.validated_data['to_location'],
#                 initiator=request.user
#                 )
#             return Response(
#                 {"piglets_group": piglets_serializers.NomadPigletsGroupSerializer(moving_group).data,
#                  "message": 'ok',
#                  "transaction": transactions_serializers.NomadPigletsTransactionSerializer(transaction).data,
#                  "split_event": piglets_events_serializers.SplitPigletsSerializer(moving_group.split_record).data
#                  },
#                 status=status.HTTP_200_OK)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class NewBornPigletsViewSet(viewsets.ModelViewSet):
#     queryset = piglets_models.NewBornPigletsGroup.objects.all()
#     serializer_class = piglets_serializers.NewBornPigletsGroupSerializer