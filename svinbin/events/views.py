# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action, api_view
from rest_framework import status, exceptions

from events.models import Semination, Ultrasound
from events.serializers import SeminationSerializer, UltrasoundSerializer


class SeminationViewSet(viewsets.ModelViewSet):
    queryset = Semination.objects.all()
    serializer_class = SeminationSerializer

    def create(self, request):
        serializer = SeminationSerializer(data=request.data)
        # initiator = request.user.workshopemployee
        if serializer.is_valid():
            Semination.objects.create_semination(
                sow_farm_id=serializer.validated_data['farm_id'],
                week=serializer.validated_data['week'],
                # initiator=request.user.workshopemployee,
                # semination_employee=request.user.workshopemployee,
                )
            return Response({'msg': 'success'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UltrasoundViewSet(viewsets.ModelViewSet):
    queryset = Ultrasound.objects.all()
    serializer_class = UltrasoundSerializer

    def create(self, request):
        serializer = UltrasoundSerializer(data=request.data)
        # initiator = request.user.workshopemployee
        if serializer.is_valid():
            Ultrasound.objects.create_ultrasound(
                sow_farm_id=serializer.validated_data['farm_id'],
                week=serializer.validated_data['week'],
                result=serializer.validated_data['result'],
                # initiator=request.user.workshopemployee,
                )
            return Response({'msg': 'success'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)