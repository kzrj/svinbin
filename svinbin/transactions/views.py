# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action, api_view

from workshops.models import WorkShop, SowSingleCell
from transactions.models import SowTransaction, Location
from transactions.serializers import MoveToWorshopOneSerializer, PutSowInCellSerializer


class WorkShopOneSowTransactionViewSet(viewsets.ViewSet):
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
            cell = SowSingleCell.objects.get(number=serializer.validated_data['cell_number'])
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
    def put_in_semination_row(self, request):
        serializer = MoveToWorshopOneSerializer(data=request.data)
        # where should I do validation? Here or in serializer?
        # sow not dead, not sick, etc
        if serializer.is_valid():
            sow  = serializer.validated_data['sow']
            location = Location.objects.create(section=Section.objects.get(workshop__number=1, number=2))
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
    def move_to_workshop_two(self, request):
        serializer = MoveToWorshopOneSerializer(data=request.data)
        # where should I do validation? Here or in serializer?
        # sow not dead, not sick, etc
        if serializer.is_valid():
            sow  = serializer.validated_data['sow']
            location = Location.objects.create(workshop=WorkShop.objects.get(number=2))
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