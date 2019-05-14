# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action, api_view
from rest_framework import status, exceptions

from sows.models import Sow
from workshops.models import WorkShop, Section, SowSingleCell, SowGroupCell
from transactions.models import SowTransaction, Location
from transactions.serializers import MoveToWorshopOneSerializer, PutSowInCellSerializer


class WorkShopSowTransactionViewSet(viewsets.ModelViewSet):
    queryset = Sow.objects.all()
    # serializer_class = SowTransactionSerializer
    # permission_classes = (TotalOrderPermissions,)

    def move_to(self, sow, pre_location, initiator=None):
        location = Location.objects.create_location(pre_location)
        SowTransaction.objects.create(
                date=timezone.now(),
                initiator=initiator,
                from_location=sow.location,
                to_location=location,
                sow=sow
                )

    @action(methods=['post'], detail=True)
    def move_to_workshop_one(self, request, pk=None):
        sow = self.get_object()
        # initiator = request.user.workshopemployee
        self.move_to(sow, WorkShop.objects.get(number=1))
        return Response({'msg': 'success'}, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True)
    def return_sow(self, request):
        sow = self.get_object()
        serializer = MoveToWorshopOneSerializer(data=request.data)
        # where should I do validation? Here or in serializer?
        # sow not dead, not sick, etc
        if serializer.is_valid():
            previous_transaction = SowTransaction.objects.get(sow=sow, to_location=sow.location)
            # if it already returned raise error
            # pre_location = previous_transaction.from_location.get_workshop
            # initiator = request.user.workshopemployee
            self.move_to(sow, previous_transaction.from_location.get_workshop)

            return Response({'msg': 'success'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WorkShopOneSowTransactionViewSet(WorkShopSowTransactionViewSet):

    @action(methods=['post'], detail=True)
    def put_sow_in_cell(self, request, pk=None):
        serializer = PutSowInCellSerializer(data=request.data)
        sow = self.get_object()
        # where should I do validation? Here or in serializer?
        # sow not dead, not sick, etc
        if serializer.is_valid():
            pre_location = SowSingleCell.objects.get(number=serializer.validated_data['cell_number'])
            # initiator = request.user.workshopemployee
            self.move_to(sow, pre_location)
            
            return Response({'msg': 'success'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=True)
    def put_in_semination_row(self, request, pk=None):
        sow = self.get_object()
        # validate sow
        # initiator = request.user.workshopemployee
        self.move_to(sow, Section.objects.get(workshop__number=1, number=2))
        return Response({'msg': 'success'}, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True)
    def move_to_workshop_two(self, request, pk=None):
        sow = self.get_object()
        # validate sow
        # initiator = request.user.workshopemployee
        self.move_to(sow, WorkShop.objects.get(number=2))
        return Response({'msg': 'success'}, status=status.HTTP_200_OK)


class WorkShopTwoSowTransactionViewSet(WorkShopSowTransactionViewSet):

    @action(methods=['post'], detail=True)
    def put_sow_in_cell(self, request, pk=None):
        sow = self.get_object()
        serializer = PutSowInCellSerializer(data=request.data)
        # where should I do validation? Here or in serializer?
        # sow not dead, not sick, etc
        if serializer.is_valid():
            pre_location = SowGroupCell.objects.get(number=serializer.validated_data['cell_number'])
            # initiator = request.user.workshopemployee
            self.move_to(sow, pre_location)
            return Response({'msg': 'success'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=True)
    def move_to_workshop_three(self, request, pk=None):
        sow = self.get_object()
        # initiator = request.user.workshopemployee
        self.move_to(sow, WorkShop.objects.get(number=3))
        return Response({'msg': 'success'}, status=status.HTTP_200_OK)


class WorkShopThreeSowTransactionViewSet(WorkShopSowTransactionViewSet):

    @action(methods=['post'], detail=True)
    def put_sow_in_cell(self, request, pk=None):
        sow = self.get_object()
        serializer = PutSowInCellSerializer(data=request.data)
        # where should I do validation? Here or in serializer?
        # sow not dead, not sick, etc
        if serializer.is_valid():
            pre_location = SowAndPigletsCell.objects.get(number=serializer.validated_data['cell_number'])
            # initiator = request.user.workshopemployee
            self.move_to(sow, pre_location)
            return Response({'msg': 'success'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WorkShopPigletsTransactionViewSet(viewsets.ViewSet):
    # permission_classes = (TotalOrderPermissions,)
    
    # It should be in transaction model manager >
    def move_from_to(self, quantity, from_location, to_location, initiator=None):
        from_location = Location.objects.create_location(from_location)
        to_location = Location.objects.create_location(to_location)
        PigletsTransaction.objects.create(
                date=timezone.now(),
                initiator=initiator,
                from_location=sow.location,
                to_location=location,
                quantity=quantity
                )


class WorkShopThreePigletsTransactionViewSet(WorkShopSowTransactionViewSet):

    @action(methods=['post'], detail=False)
    def move_to_workshop_four(self, request):
        serializer = PutSowInCellSerializer(data=request.data)
        
        if serializer.is_valid():
            from_cell = SowAndPigletsCell.objects.get(number=serializer.validated_data['cell_number'])
            to_location = WorkShop.objects.get(number=4)
            quantity = serializer.validated_data['quantity']
            # initiator = request.user.workshopemployee
            self.move_from_to(quantity, from_cell, to_location)
            return Response({'msg': 'success'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False)
    def internal_move_from_cell_to_cell(self, request):
        serializer = PutSowInCellSerializer(data=request.data)
        
        if serializer.is_valid():
            from_cell = SowAndPigletsCell.objects.get(number=serializer.validated_data['from_cell_number'])
            to_cell = SowAndPigletsCell.objects.get(number=serializer.validated_data['to_cell_number'])
            quantity = serializer.validated_data['quantity']
            # initiator = request.user.workshopemployee
            self.move_from_to(quantity, from_cell, to_cell)
            return Response({'msg': 'success'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WorkShopFourPigletsTransactionViewSet(WorkShopSowTransactionViewSet):
    @action(methods=['post'], detail=False)
    def move_to_workshop_eight(self, request):
        serializer = PutSowInCellSerializer(data=request.data)
        
        if serializer.is_valid():
            from_cell = SowAndPigletsCell.objects.get(number=serializer.validated_data['cell_number'])
            to_location = WorkShop.objects.get(number=4)
            quantity = serializer.validated_data['quantity']
            # initiator = request.user.workshopemployee
            self.move_from_to(quantity, from_cell, to_location)
            return Response({'msg': 'success'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=True)
    def put_piglets_in_cell(self, request):
        serializer = PutPigletsInCellSerializer(data=request.data)
        if serializer.is_valid():
            previous_transaction = PigletsTransaction.objects.get(pk=serializer.validated_data['piglets_transaction_id'])
            # check in serializer or in model serializer.validated_data.quantity < prev trans quantity
            
            to_cell = PigletsGroupCell.objects.get(number=serializer.validated_data['to_cell_number'])
            quantity = serializer.validated_data['quantity']
            # initiator = request.user.workshopemployee
            self.move_from_to(quantity, from_cell, to_cell)
            return Response({'msg': 'success'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)