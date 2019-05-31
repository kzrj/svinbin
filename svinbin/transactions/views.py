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
from transactions import serializers



class SowTransactionsViewSet(viewsets.ModelViewSet):
    queryset = SowTransaction.objects.all()
    serializer_class = serializers.SowTransactionSerializer


class WorkShopSowTransactionViewSet(viewsets.ViewSet):
    # queryset = None
    # serializer_class = FarmIdSerializer
    # permission_classes = (TotalOrderPermissions,)
    pass


class WorkShopOneTwoSowTransactionViewSet(WorkShopSowTransactionViewSet):

    def get_serializer_class(self):
        if self.action == 'from_semination_row_to_cell':
            return SowFarmIdAndCellSerializer
        return SowFarmIdAndCellSerializer

    @action(methods=['post'], detail=False)
    def put_in_semination_row(self, request):
        # put sows in semination row from anywhere.
        serializer = serializers.FarmIdSerializer(data=request.data)
        # initiator = request.user.workshopemployee
        if serializer.is_valid():
            Sow.objects.move_to_by_farm_id(serializer.validated_data['farm_id'],
             Section.objects.get(workshop__number=1, number=2))
            return Response({'msg': 'success'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False)
    def put_in_cell_for_ultrasound(self, request):
        serializer = serializers.SowFarmIdAndCellSerializer(data=request.data)
        # initiator = request.user.workshopemployee
        if serializer.is_valid():
            sow = Sow.objects.move_to_by_farm_id(serializer.validated_data['farm_id'],
                SowSingleCell.objects.get(number=serializer.validated_data['cell_number']))
            sow.change_status_waiting_ultrasound
            return Response({'msg': 'success'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def from_semination_row_to_cell(self, request):
        # put sows in semination row from anywhere.
        serializer = serializers.SowFarmIdAndCellSerializer(data=request.data)
        # initiator = request.user.workshopemployee
        if serializer.is_valid():
            sow = Sow.objects.move_to_by_farm_id(serializer.validated_data['farm_id'],
                SowSingleCell.objects.get(number=serializer.validated_data['cell_number']))
            return Response({'msg': 'success'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False)
    def move_all_pregnant_to_workshop_two(self, request):
        serializer = WeekNumberSerializer()
        if serializer.is_valid():
            # initiator = request.user.workshopemployee    
            sows = Sow.objects.get_all_pregnant_in_workshop_one()
            Sow.objects.move_many(sows, WorkShop.objects.get(number=2), initiator=None)
            return Response({'msg': 'success'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False)
    def move_pregnant_to_workshop_two(self, request):
        serializer = serializers.WeekNumberFarmIdSerializer()
        if serializer.is_valid():
            # initiator = request.user.workshopemployee    
            sow = Sow.objects.move_to_by_farm_id(serializer.validated_data['farm_id'],
                WorkShop.objects.get(number=2))
            return Response({'msg': 'success'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

   # делает сотрудник 3 цеха
    @action(methods=['post'], detail=False)
    def move_to_workshop_three(self, request):
        serializer = serializers.WeekNumberFarmIdSerializer()
        if serializer.is_valid():
            # initiator = request.user.workshopemployee    
            sow = Sow.objects.move_to_by_farm_id(serializer.validated_data['farm_id'],
                WorkShop.objects.get(number=3))
            return Response({'msg': 'success'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # делает сотрудник 1 цеха
    @action(methods=['post'], detail=False)
    def move_to_workshop_one(self, request):
        serializer = serializers.WeekNumberFarmIdSerializer()
        if serializer.is_valid():
            # initiator = request.user.workshopemployee    
            sow = Sow.objects.move_to_by_farm_id(serializer.validated_data['farm_id'],
                WorkShop.objects.get(number=1))
            return Response({'msg': 'success'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)