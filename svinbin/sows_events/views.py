# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action, api_view
from rest_framework import status, exceptions

from sows_events.models import Semination, Ultrasound, CullingSow, SowFarrow, SemenBoar
from sows_events import serializers
from sows_events.filters import SemenBoarFilter



class SeminationViewSet(viewsets.ModelViewSet):
    queryset = Semination.objects.all()
    serializer_class = serializers.SeminationSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.CreateSeminationSerializer
        return serializers.SeminationSerializer

    def create(self, request):
        serializer = serializers.CreateSeminationSerializer(data=request.data)
        if serializer.is_valid():
            semination = Semination.objects.create_semination(
                sow_farm_id=serializer.validated_data['farm_id'],
                week=serializer.validated_data['week'],
                initiator=request.user,
                semination_employee=serializer.validated_data['semination_employee'],
                )
            return Response(serializers.SeminationSerializer(semination).data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UltrasoundViewSet(viewsets.ModelViewSet):
    queryset = Ultrasound.objects.all()
    serializer_class = serializers.UltrasoundSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.CreateUltrasoundSerializer
        return serializers.UltrasoundSerializer

    def create(self, request):
        serializer = serializers.CreateUltrasoundSerializer(data=request.data)
        if serializer.is_valid():
            ultrasound = Ultrasound.objects.create_ultrasound(
                sow_farm_id=serializer.validated_data['farm_id'],
                week=serializer.validated_data['week'],
                result=serializer.validated_data['result'],
                initiator=request.user,
                )
            return Response(serializers.UltrasoundSerializer(ultrasound).data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CullingSowViewSet(viewsets.ModelViewSet):
    queryset = CullingSow.objects.all()
    serializer_class = serializers.CullingSowSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.CreateCullingSowSerializer
        return serializers.CullingSowSerializer

    def create(self, request):
        serializer = serializers.CreateCullingSowSerializer(data=request.data)
        if serializer.is_valid():
            culling = CullingSow.objects.create_culling(
                sow_farm_id=serializer.validated_data['farm_id'],
                culling_type=serializer.validated_data['culling_type'],
                initiator=request.user,
                )
            return Response(serializers.CullingSowSerializer(culling).data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SowFarrowViewSet(viewsets.ModelViewSet):
    queryset = SowFarrow.objects.all()
    serializer_class = serializers.SowFarrowSerializer


class SemenBoarViewSet(viewsets.ModelViewSet):
    queryset = SemenBoar.objects.all()
    serializer_class = serializers.SemenBoarSerializer
    filter_class = SemenBoarFilter