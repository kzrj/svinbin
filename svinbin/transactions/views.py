# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action, api_view
from rest_framework import status, exceptions

from pigs.models import Sow, PigletsGroup
from workshops.models import WorkShop, Section, SowSingleCell, SowGroupCell
from transactions.models import SowTransaction, Location
from transactions.serializers import MoveToWorshopOneSerializer, PutSowInCellSerializer, \
    MoveToSeminationRowSerializer, SowFarmIdAndCellSerializer


class WorkShopSowTransactionViewSet(viewsets.ModelViewSet):
    queryset = Sow.objects.all()
    # serializer_class = SowTransactionSerializer
    # permission_classes = (TotalOrderPermissions,)

    # @action(methods=['post'], detail=True)
    # def return_sow(self, request):
    #     sow = self.get_object()
    #     serializer = MoveToWorshopOneSerializer(data=request.data)
    #     # where should I do validation? Here or in serializer?
    #     # sow not dead, not sick, etc
    #     if serializer.is_valid():
    #         previous_transaction = SowTransaction.objects.get(sow=sow, to_location=sow.location)
    #         # if it already returned raise error
    #         # pre_location = previous_transaction.from_location.get_workshop
    #         # initiator = request.user.workshopemployee
    #         self.move_to(sow, previous_transaction.from_location.get_workshop)

    #         return Response({'msg': 'success'}, status=status.HTTP_200_OK)
    #     else:
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WorkShopOneSowTransactionViewSet(WorkShopSowTransactionViewSet):

    @action(methods=['post'], detail=False)
    def put_in_semination_row(self, request):
        # put sows in semination row from anywhere.
        serializer = MoveToSeminationRowSerializer(data=request.data)
        # initiator = request.user.workshopemployee
        if serializer.is_valid():
            Sow.objects.move_to(serializer.validation_data['farm_id'],
             Section.objects.get(workshop__number=1, number=2))
            return Response({'msg': 'success'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False)
    def put_in_cell_for_ultrasound(self, request):
        # put sows in semination row from anywhere.
        serializer = SowFarmIdAndCellSerializer(data=request.data)
        # initiator = request.user.workshopemployee
        if serializer.is_valid():
            Sow.objects.move_to(serializer.validated_data['farm_id'],
                SowSingleCell.objects.get(number=serializer.validated_data['cell_number']))
            sow.change_status_waiting_ultrasound
            return Response({'msg': 'success'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # @action(methods=['post'], detail=True)
    # def move_to_workshop_two(self, request, pk=None):
    #     sow = self.get_object()
    #     # validate sow
    #     # initiator = request.user.workshopemployee
    #     self.move_to(sow, WorkShop.objects.get(number=2))
    #     return Response({'msg': 'success'}, status=status.HTTP_200_OK)

    # @action(methods=['post'], detail=True)
    # def put_sow_in_cell(self, request, pk=None):
    #     serializer = PutSowInCellSerializer(data=request.data)
    #     sow = self.get_object()
    #     # where should I do validation? Here or in serializer?
    #     # sow not dead, not sick, etc
    #     if serializer.is_valid():
    #         pre_location = SowSingleCell.objects.get(number=serializer.validated_data['cell_number'])
    #         # initiator = request.user.workshopemployee
    #         self.move_to(sow, pre_location)
            
    #         return Response({'msg': 'success'}, status=status.HTTP_200_OK)
    #     else:
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class WorkShopTwoSowTransactionViewSet(WorkShopSowTransactionViewSet):

#     @action(methods=['post'], detail=True)
#     def put_sow_in_cell(self, request, pk=None):
#         sow = self.get_object()
#         serializer = PutSowInCellSerializer(data=request.data)
#         # where should I do validation? Here or in serializer?
#         # sow not dead, not sick, etc
#         if serializer.is_valid():
#             pre_location = SowGroupCell.objects.get(number=serializer.validated_data['cell_number'])
#             # initiator = request.user.workshopemployee
#             self.move_to(sow, pre_location)
#             return Response({'msg': 'success'}, status=status.HTTP_200_OK)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     @action(methods=['post'], detail=True)
#     def move_to_workshop_three(self, request, pk=None):
#         sow = self.get_object()
#         # initiator = request.user.workshopemployee
#         self.move_to(sow, WorkShop.objects.get(number=3))
#         return Response({'msg': 'success'}, status=status.HTTP_200_OK)


# class WorkShopThreeSowTransactionViewSet(WorkShopSowTransactionViewSet):

#     @action(methods=['post'], detail=True)
#     def put_sow_in_cell(self, request, pk=None):
#         sow = self.get_object()
#         serializer = PutSowInCellSerializer(data=request.data)
#         # where should I do validation? Here or in serializer?
#         # sow not dead, not sick, etc
#         if serializer.is_valid():
#             pre_location = SowAndPigletsCell.objects.get(number=serializer.validated_data['cell_number'])
#             # initiator = request.user.workshopemployee
#             self.move_to(sow, pre_location)
#             return Response({'msg': 'success'}, status=status.HTTP_200_OK)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class WorkShopPigletsTransactionViewSet(viewsets.ViewSet):
#     # permission_classes = (TotalOrderPermissions,)
    
#     # It should be in transaction model manager >
#     def move_to(self, piglets_group, pre_location, initiator=None):
#         to_location = Location.objects.create_location(pre_location)
#         PigletsTransaction.objects.create(
#                 date=timezone.now(),
#                 initiator=initiator,
#                 from_location=piglets_group.location,
#                 to_location=location,
#                 piglets_group=piglets_group
#                 )

#     # to model manager
#     def create_new_group_from_parent_group(self, parent_piglets_group, quantity):
#         new_piglets_group = PigletsGroup.objetcs.create(quantity=quantity, \
#             location=parent_piglets_group.location,
#             )
#         parent_piglets_group.quantity = parent_piglets_group.quantity - quantity
#         parent_piglets_group.save()
#         new_piglets_group.parent_groups.add(parent_piglets_group)
#         # fix
#         new_piglets_group.tours.add(parent_piglets_group.tours)
#         return new_piglets_group

#     def union_groups(self, cell):
#         # If there are two or more groups in same cell we need to union these groups in one.
#         # Assing tour of biggert group to new group
#         # Create mixing record in db.



# class WorkShopThreePigletsTransactionViewSet(WorkShopPigletsTransactionViewSet):

# # methods could be detail. Piglets_group by pk

#     @action(methods=['post'], detail=False)
#     def move_to_workshop_four(self, request):
#         serializer = PutSowInCellSerializer(data=request.data)
        
#         if serializer.is_valid():
#             to_location = WorkShop.objects.get(number=4)
#             piglets_group = serializer.validated_data['piglets_group']
#             # initiator = request.user.workshopemployee
#             self.move_from_to(piglets_group, to_location)
#             return Response({'msg': 'success'}, status=status.HTTP_200_OK)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     @action(methods=['post'], detail=False)
#     def move_to_workshop_four_split_group(self, request):
#         serializer = PutSowInCellSerializer(data=request.data)
        
#         if serializer.is_valid():
#             to_location = WorkShop.objects.get(number=4)
#             parent_piglets_group = serializer.validated_data['piglets_group']

#             # quantity should be equal or less than piglet_group quantity
#             quantity = serializer.validated_data['quantity']

#             # move to model manager
#             # decrease parent_piglets_group quantity.
#             new_piglets_group = self.split_group_return_child_group(parent_piglets_group, quantity)

#             # initiator = request.user.workshopemployee
#             self.move_from_to(new_piglets_group, to_location)
#             return Response({'msg': 'success'}, status=status.HTTP_200_OK)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#     @action(methods=['post'], detail=False)
#     def move_to_workshop_four_mixed_cell(self, request):
#         serializer = PutSowInCellSerializer(data=request.data)
        
#         if serializer.is_valid():
#             to_location = WorkShop.objects.get(number=4)
#             parent_piglets_group = serializer.validated_data['piglets_group']

#             # quantity should be equal or less than piglet_group quantity
#             quantity = serializer.validated_data['quantity']

#             # move to model manager
#             # decrease parent_piglets_group quantity.
#             new_piglets_group = self.split_group_return_child_group(parent_piglets_group, quantity)

#             # initiator = request.user.workshopemployee
#             self.move_from_to(new_piglets_group, to_location)
#             return Response({'msg': 'success'}, status=status.HTTP_200_OK)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     @action(methods=['post'], detail=False)
#     def internal_move_from_cell_to_cell(self, request):
#         serializer = PutSowInCellSerializer(data=request.data)
        
#         if serializer.is_valid():
#             piglets_group = serializer.validated_data['piglets_group']
#             to_location = SowAndPigletsCell.objects.get(number=serializer.validated_data['to_cell_number'])
            
#             # initiator = request.user.workshopemployee
#             self.move_from_to(piglets_group, to_location)
#             return Response({'msg': 'success'}, status=status.HTTP_200_OK)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     @action(methods=['post'], detail=False)
#     def internal_move_from_cell_to_cell_split_group(self, request):
#         serializer = PutSowInCellSerializer(data=request.data)
        
#         if serializer.is_valid():
#             to_location = SowAndPigletsCell.objects.get(number=serializer.validated_data['to_cell_number'])
#             parent_piglets_group = serializer.validated_data['piglets_group']

#             # quantity should be equal or less than piglet_group quantity
#             quantity = serializer.validated_data['quantity']

#             # move to model manager
#             # decrease parent_piglets_group quantity.
#             new_piglets_group = PigletsGroup.objetcs.create(quantity=quantity, location=parent_piglets_group.location)
#             parent_piglets_group.quantity = parent_piglets_group.quantity - quantity
#             parent_piglets_group.save()
#             new_piglets_group.parent_groups.add(parent_piglets_group)

#             # initiator = request.user.workshopemployee
#             self.move_from_to(new_piglets_group, to_location)
#             return Response({'msg': 'success'}, status=status.HTTP_200_OK)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class WorkShopFourPigletsTransactionViewSet(WorkShopPigletsTransactionViewSet):
#     @action(methods=['post'], detail=False)
#     def move_to_workshop_eight(self, request):
#         serializer = PutSowInCellSerializer(data=request.data)
        
#         if serializer.is_valid():
#             from_cell = SowAndPigletsCell.objects.get(number=serializer.validated_data['cell_number'])
#             to_location = WorkShop.objects.get(number=4)
#             quantity = serializer.validated_data['quantity']
#             # initiator = request.user.workshopemployee
#             self.move_from_to(quantity, from_cell, to_location)
#             return Response({'msg': 'success'}, status=status.HTTP_200_OK)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     @action(methods=['post'], detail=True)
#     def put_piglets_in_cell(self, request):
#         serializer = PutPigletsInCellSerializer(data=request.data)
#         if serializer.is_valid():
#             previous_transaction = PigletsTransaction.objects.get(pk=serializer.validated_data['piglets_transaction_id'])
#             # check in serializer or in model serializer.validated_data.quantity < prev trans quantity
            
#             to_cell = PigletsGroupCell.objects.get(number=serializer.validated_data['to_cell_number'])
#             quantity = serializer.validated_data['quantity']
#             # initiator = request.user.workshopemployee
#             self.move_from_to(quantity, from_cell, to_cell)
#             return Response({'msg': 'success'}, status=status.HTTP_200_OK)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)