# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action, api_view
from rest_framework import status, exceptions

from workshops.models import WorkShop, Section, SowSingleCell, SowGroupCell
from transactions.models import SowTransaction, Location
from transactions.serializers import MoveToWorshopOneSerializer, PutSowInCellSerializer


class WorkShopSowTransactionViewSet(viewsets.ViewSet):
    queryset = SowTransaction.objects.all()
    # serializer_class = SowTransactionSerializer
    # permission_classes = (TotalOrderPermissions,)

    def _move_to(self, sow, pre_location, initiator=None):
        print('move_to')
        location = Location()
        if isinstance(pre_location, WorkShop):
            location.workshop = pre_location
        elif isinstance(pre_location, Section):
            location.section = pre_location
        elif isinstance(pre_location, SowSingleCell):
            location.sowSingleCell = pre_location
        elif isinstance(pre_location, SowGroupCell):
            location.sowGroupCell = pre_location
        else:
            raise exceptions.ValidationError
        location.save()

        SowTransaction.objects.create(
                date=timezone.now(),
                initiator=initiator,
                from_location=sow.location,
                to_location=location,
                sow=sow
                )

class WorkShopOneSowTransactionViewSet(WorkShopSowTransactionViewSet):

    @action(methods=['post'], detail=False)
    def move_to_workshop_one(self, request):
        serializer = MoveToWorshopOneSerializer(data=request.data)
        # where should I do validation? Here or in serializer?
        # sow not dead, not sick, etc
        if serializer.is_valid():
            sow  = serializer.validated_data['sow']
            pre_location = WorkShop.objects.get(number=1)
            # initiator = request.user.workshopemployee
            self._move_to(sow, pre_location)
            return Response({'msg': 'serializer valid'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False)
    def put_sow_in_cell(self, request):
        serializer = PutSowInCellSerializer(data=request.data)
        # where should I do validation? Here or in serializer?
        # sow not dead, not sick, etc
        if serializer.is_valid():
            sow  = serializer.validated_data['sow']
            pre_location = SowSingleCell.objects.get(number=serializer.validated_data['cell_number'])
            # initiator = request.user.workshopemployee
            self._move_to(sow, pre_location)
            
            return Response({'msg': 'success'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False)
    def put_in_semination_row(self, request):
        serializer = MoveToWorshopOneSerializer(data=request.data)
        # where should I do validation? Here or in serializer?
        # sow not dead, not sick, etc
        if serializer.is_valid():
            sow  = serializer.validated_data['sow']
            pre_location = Section.objects.get(workshop__number=1, number=2)
            # initiator = request.user.workshopemployee
            self._move_to(sow, pre_location)

            return Response({'msg': 'success'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False)
    def move_to_workshop_two(self, request):
        serializer = MoveToWorshopOneSerializer(data=request.data)
        # where should I do validation? Here or in serializer?
        # sow not dead, not sick, etc
        if serializer.is_valid():
            sow  = serializer.validated_data['sow']
            pre_location = WorkShop.objects.get(number=2)
            # initiator = request.user.workshopemployee
            self._move_to(sow, pre_location)
            
            return Response({'msg': 'serializer valid'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False)
    def return_sow(self, request):
        serializer = MoveToWorshopOneSerializer(data=request.data)
        # where should I do validation? Here or in serializer?
        # sow not dead, not sick, etc
        if serializer.is_valid():
            sow  = serializer.validated_data['sow']
            previous_transaction = SowTransaction.objects.get(sow=sow, to_location=sow.location)
            # if it already returned raise error
            pre_location = previous_transaction.from_location.get_workshop
            # initiator = request.user.workshopemployee
            self._move_to(sow, pre_location)

            return Response({'msg': 'success'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WorkShopTwoSowTransactionViewSet(viewsets.ViewSet):
    queryset = SowTransaction.objects.all()
    # serializer_class = SowTransactionSerializer
    # permission_classes = (TotalOrderPermissions,)

    @action(methods=['post'], detail=False)
    def move_to_workshop_one(self, request):
        serializer = MoveToWorshopOneSerializer(data=request.data)
        # where should I do validation? Here or in serializer?
        # sow not dead, not sick, etc
        if serializer.is_valid():
            sow  = serializer.validated_data['sow']
            location = Location.objects.create(workshop=WorkShop.objects.get(number=1))
            SowTransaction.objects.create(
                date=timezone.now(),
                # initiator=request.user.workshopemployee,
                from_location=sow.location,
                to_location=location,
                sow=sow
                )
            return Response({'msg': 'serializer valid'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False)
    def put_sow_in_cell(self, request):
        serializer = PutSowInCellSerializer(data=request.data)
        # where should I do validation? Here or in serializer?
        # sow not dead, not sick, etc
        if serializer.is_valid():
            sow  = serializer.validated_data['sow']
            cell = SowGroupCell.objects.get(number=serializer.validated_data['cell_number'])
            location = Location.objects.create(sowSingleCell=cell)
            SowTransaction.objects.create(
                date=timezone.now(),
                # initiator=request.user.workshopemployee,
                from_location=sow.location,
                to_location=location,
                sow=sow
                )
            return Response({'msg': 'success'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False)
    def move_to_workshop_three(self, request):
        serializer = MoveToWorshopOneSerializer(data=request.data)
        # where should I do validation? Here or in serializer?
        # sow not dead, not sick, etc
        if serializer.is_valid():
            sow  = serializer.validated_data['sow']
            location = Location.objects.create(workshop=WorkShop.objects.get(number=3))
            SowTransaction.objects.create(
                date=timezone.now(),
                # initiator=request.user.workshopemployee,
                from_location=sow.location,
                to_location=location,
                sow=sow
                )
            return Response({'msg': 'serializer valid'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False)
    def return_sow(self, request):
        serializer = MoveToWorshopOneSerializer(data=request.data)
        # where should I do validation? Here or in serializer?
        # sow not dead, not sick, etc
        if serializer.is_valid():
            sow  = serializer.validated_data['sow']
            previous_transaction = SowTransaction.objects.get(sow=sow, to_location=sow.location)
            # if it already returned raise error

            location = Location.objects.create(workshop=previous_transaction.from_location.get_workshop)
            SowTransaction.objects.create(
                date=timezone.now(),
                # initiator=request.user.workshopemployee,
                from_location=sow.location,
                to_location=location,
                sow=sow,
                returned=True
                )
            return Response({'msg': 'success'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)