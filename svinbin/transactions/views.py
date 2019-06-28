# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.decorators import action

from sows.models import Sow
from piglets.models import NomadPigletsGroup
from locations.models import WorkShop, Section, SowSingleCell, SowGroupCell, SowAndPigletsCell, \
    Location
from transactions.models import SowTransaction, PigletsTransaction
from transactions import serializers
from sows import serializers as sows_serializers
from piglets import serializers as piglets_serializers


class SowTransactionsViewSet(viewsets.ModelViewSet):
    queryset = SowTransaction.objects.all()
    serializer_class = serializers.SowTransactionSerializer


class WorkShopSowTransactionViewSet(viewsets.ModelViewSet):
    queryset = Sow.objects.all()
    serializer_class = serializers.FarmIdSerializer
    # permission_classes = (TotalOrderPermissions,)
    

class WorkShopOneTwoSowTransactionViewSet(WorkShopSowTransactionViewSet):

    def get_serializer_class(self):
        if self.action == 'from_semination_row_to_cell':
            return serializers.SowFarmIdAndCellSerializer
        if self.action == 'put_in_cell_for_ultrasound' or self.action == 'move_to_workshop_three':
            return serializers.SowFarmIdAndCellSerializer
        return serializers.FarmIdSerializer

    @action(methods=['post'], detail=False)
    def put_in_semination_row(self, request):
        # put sows in semination row from anywhere.
        serializer = serializers.FarmIdSerializer(data=request.data)
        # initiator = request.user.workshopemployee
        if serializer.is_valid():
            sow, transaction = Sow.objects.create_and_move_to_by_farm_id(serializer.validated_data['farm_id'],
             Section.objects.get(workshop__number=1, number=2))
            return Response(
                {"transaction": serializers.SowTransactionSerializer(transaction).data,
                 "sow": sows_serializers.SowSerializer(sow).data, },
                status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False)
    def put_in_cell_for_ultrasound(self, request):
        serializer = serializers.SowFarmIdAndCellSerializer(data=request.data)
        # initiator = request.user.workshopemployee
        if serializer.is_valid():
            sow, transaction = Sow.objects.move_to_by_farm_id(serializer.validated_data['farm_id'],
                SowSingleCell.objects.get(number=serializer.validated_data['cell_number']))
            sow.change_status_to('waiting ultrasound')
            return Response(
                {"transaction": serializers.SowTransactionSerializer(transaction).data,
                 "sow": sows_serializers.SowSerializer(sow).data, },
                status=status.HTTP_200_OK)
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
    def move_pregnant_to_workshop_two(self, request):
        serializer = serializers.FarmIdSerializer(data=request.data)
        if serializer.is_valid():
            # initiator = request.user.workshopemployee    
            sow, transaction = Sow.objects.move_to_by_farm_id(serializer.validated_data['farm_id'],
                WorkShop.objects.get(number=2))
            sow.change_status_to("pregnant in workshop two")
            return Response(
                {"transaction": serializers.SowTransactionSerializer(transaction).data,
                 "sow": sows_serializers.SowSerializer(sow).data, },
                status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
   # делает сотрудник 3 цеха
    @action(methods=['post'], detail=False)
    def move_to_workshop_three(self, request):
        serializer = serializers.SowFarmIdAndCellSerializer(data=request.data)
        if serializer.is_valid():
            # initiator = request.user.workshopemployee    
            sow, transaction = Sow.objects.move_to_by_farm_id(serializer.validated_data['farm_id'],
                SowAndPigletsCell.objects.get(number=serializer.validated_data['cell_number']))
            sow.change_status_to("waiting delivery in workshop three")
            return Response(
                {"transaction": serializers.SowTransactionSerializer(transaction).data,
                 "sow": sows_serializers.SowSerializer(sow).data, },
                status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # делает сотрудник 1 цеха
    @action(methods=['post'], detail=False)
    def move_to_workshop_one(self, request):
        serializer = serializers.FarmIdSerializer()
        if serializer.is_valid():
            # initiator = request.user.workshopemployee    
            sow = Sow.objects.move_to_by_farm_id(serializer.validated_data['farm_id'],
                WorkShop.objects.get(number=1))
            return Response({'msg': 'success'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NomadPigletsGroupTransactionsViewSet(viewsets.ModelViewSet):
    queryset = PigletsTransaction.objects.all()
    serializer_class = serializers.NomadPigletsTransactionSerializer


class WorkShopNomadPigletsTransactionViewSet(viewsets.ModelViewSet):
    queryset = NomadPigletsGroup.objects.all()
    serializer_class = piglets_serializers.NomadPigletsGroupPkSerializer
    # permission_classes = (TotalOrderPermissions,)
    
    # def get_serializer_class(self):
    #     pass

    # делает сотрудник 3 цеха
    @action(methods=['post'], detail=False)
    def move_to_workshop_four(self, request):
        serializer = serializers.NomadPigletsGroupPkSerializer(data=request.data)
        if serializer.is_valid():
            # initiator = request.user.workshopemployee    
            nomad_piglets_group, transaction = \
                NomadPigletsGroup.objects.move_to(
                    serializer.validated_data['pk'],
                    WorkShop.objects.get(number=4))
            # sow.change_status_to("waiting delivery in workshop three")
            return Response(
                {"transaction": serializers.NomadPigletsTransactionSerializer(transaction).data,
                 "nomad_piglets_group": sows_serializers.NomadPigletsGroupSerializer(nomad_piglets_group).data, },
                status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)