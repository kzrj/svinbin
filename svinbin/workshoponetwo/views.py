# -*- coding: utf-8 -*-
from django.db import models

from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from core import wsxlrd

from workshoponetwo import serializers
import sows.serializers as sows_serializers
import sows_events.serializers as sows_events_serializers
import piglets.serializers as piglets_serializers
import piglets_events.serializers as piglets_events_serializers
import transactions.serializers as transactions_serializers
import locations.serializers as locations_serializers
import tours.serializers as tours_serializers

import sows.models as sows_models
import sows_events.models as sows_events_models
import piglets.models as piglets_models
import piglets_events.models as piglets_events_models
import transactions.models as transactions_models
import locations.models as locations_models
import tours.models as tours_models

from sows.views import WorkShopSowViewSet
    

class WorkShopOneTwoSowViewSet(WorkShopSowViewSet):
    @action(methods=['post'], detail=False)
    def create_new(self, request):
        workshop = locations_models.WorkShop.objects.get(number=1)
        serializer = serializers.CreateFarmIdSerializer(data=request.data)
        if serializer.is_valid():
            sow = sows_models.Sow.objects.create_new_from_noname(
                serializer.validated_data['farm_id'],
                workshop
                )
            if sow:
                return Response(
                    {
                        "sow": sows_serializers.SowSerializer(sow).data,
                        "message": 'Создана свиноматка с номером {}.' \
                            .format(serializer.validated_data['farm_id']),
                    },
                    status=status.HTTP_200_OK)
            else:
                return Response(
                    {
                        "sow": None,
                        "message": 'Нет ремонтных свиноматок. Создайте свиноматку без номера.',
                    },
                    status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False)
    def create_new_without_farm_id(self, request):
        workshop = locations_models.WorkShop.objects.get(number=1)    
        sow = sows_models.Sow.objects.create_new_from_gilt_without_farm_id()
        noname_sows = sows_models.Sow.objects.get_without_farm_id_in_workshop(workshop)
        return Response(
            {
                "sow": sows_serializers.SowSerializer(sow).data,
                "noname_sows_count": noname_sows.count(), 
                "message": 'Создана ремонтная свиноматка.',
            },
            status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True)
    def assing_farm_id(self, request, pk=None):
        sow = self.get_object()
        serializer = serializers.FarmIdSerializer(data=request.data)
        # initiator = request.user.workshopemployee
        if serializer.is_valid():
            sow.assing_farm_id(serializer.validated_data['farm_id'])
            return Response(
                {
                    "sow": sows_serializers.SowSerializer(sow).data,
                    "message": 'ok',
                },
                status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=True)
    def put_in_semination_row(self, request, pk=None):
        sow = self.get_object()        
        transaction = transactions_models.SowTransaction.objects.create_transaction(
            sow, locations_models.Location.objects.get(section__name="Ряд осеменения"),
            request.user)
        return Response(
            {
                "transaction": transactions_serializers.SowTransactionSerializer(transaction).data,
                "sow": sows_serializers.SowSerializer(sow).data, 
            },
            status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True)
    def semination(self, request, pk=None):
        sow = self.get_object() 
        serializer = sows_events_serializers.CreateSeminationSerializer(data=request.data)
        if serializer.is_valid():
            # semination employee is request user. TODO: need to choose semination employee
            semination = sows_events_models.Semination.objects.create_semination(
                sow, serializer.validated_data['week'], request.user, request.user,
                serializer.validated_data['boar'] )
            return Response(
                {
                    "semination": sows_events_serializers.SeminationSerializer(semination).data,
                    "sow": sows_serializers.SowSerializer(sow).data, 
                    "message": "ok"
                },
                status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=True)
    def ultrasound(self, request, pk=None):
        sow = self.get_object() 
        serializer = sows_events_serializers.CreateUltrasoundSerializer(data=request.data)
        if serializer.is_valid():
            ultrasound = sows_events_models.Ultrasound.objects.create_ultrasound(
                 sow,
                 request.user,
                 serializer.validated_data['result'],
                 serializer.validated_data['days'],)
            return Response(
                {
                    "ultrasound": sows_events_serializers.UltrasoundSerializer(ultrasound).data,
                    "sow": sows_serializers.SowSerializer(sow).data, 
                    "message": "ok"
                },
                status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=False)
    def sows_by_tours(self, request):
        data = list()
        workshop = locations_models.WorkShop.objects.get(number=1)
        tours = tours_models.Tour.objects.get_tours_in_workshop_by_sows(workshop)
        for tour in tours:
            qs = tour.sows.get_suporos_in_workshop(workshop)
            if qs.count() > 0:
                data.append(
                    {   
                        'title': str(tour),
                        'tour': tours_serializers.TourSerializer(tour).data,
                        'sows': sows_serializers.SowSerializer(qs, many=True).data,
                        'count': qs.count()
                    }
                )
        qs = sows_models.Sow.objects.get_not_seminated_not_suporos_in_workshop(workshop)
        if qs.count() > 0:
            data.append({
                    'title': 'Не супорос, не осеменена, есть Id',
                    'tour': {'id': 'Не супорос, не осеменена, есть Id'},
                    'sows': sows_serializers.SowSerializer(qs, many=True).data,
                    'count': qs.count()
                    })

        qs = sows_models.Sow.objects.get_without_farm_id_in_workshop(workshop)
        if qs.count() > 0:
            data.append({
                    'title': 'Ремонтные',
                    'tour': {'id': 'Нет Id'},
                    'sows': sows_serializers.SowSerializer(qs, many=True).data,
                    'count': qs.count()
                    })

        return Response(data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False)
    def sows_by_tours_ws2(self, request):
        data = list()
        workshop = locations_models.WorkShop.objects.get(number=2)
        tours = tours_models.Tour.objects.get_tours_in_workshop_by_sows(workshop)
        for tour in tours:
            qs = tour.sows.get_suporos_in_workshop(workshop)
            if qs.count() > 0:
                data.append(
                    {   
                        'title': str(tour),
                        'tour': tours_serializers.TourSerializer(tour).data,
                        'sows': sows_serializers.SowSerializer(qs, many=True).data,
                        'count': qs.count()
                    }
                )
        qs = sows_models.Sow.objects.get_not_suporos_in_workshop(workshop)
        if qs.count() > 0:
            data.append({
                    'title': 'Не супорос',
                    'tour': {'id': 'Не супорос'},
                    'sows': sows_serializers.SowSerializer(qs, many=True).data,
                    'count': qs.count()
                    })

        return Response(data, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False)
    def mass_semination(self, request):
        serializer = sows_serializers.SowsMassSeminationSerializer(data=request.data)
        if serializer.is_valid():
            sows_qs = sows_models.Sow.objects.filter(pk__in=serializer.validated_data['sows'])
            sows_events_models.Semination.objects.mass_semination(
                sows_qs=sows_qs,
                week=serializer.validated_data['week'],
                semination_employee=serializer.validated_data['semination_employee'],
                boar=serializer.validated_data['boar'],
                initiator=request.user
                )

            return Response(
                {
                    "message": "ok"
                },
                status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False)
    def mass_ultrasound(self, request):
        serializer = sows_serializers.SowsMassUltrasoundSerializer(data=request.data)
        if serializer.is_valid():
            sows_qs = sows_models.Sow.objects.filter(pk__in=serializer.validated_data['sows'])
            sows_events_models.Ultrasound.objects.mass_ultrasound(
                sows_qs=sows_qs,
                days=serializer.validated_data['days'],
                result=serializer.validated_data['result'],
                initiator=request.user
                )

            return Response(
                {
                    "message": "ok"
                },
                status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False)
    def mass_init_and_transfer(self, request):
        serializer = serializers.MassSowCreateSerializer(data=request.data)
        if serializer.is_valid():
            create_sows, existed_sows = sows_models.Sow.objects.create_bulk_at_ws(
                farm_ids=serializer.validated_data['sows'],
                location=locations_models.Location.objects.get(workshop__number=2)
                )
            sows_to_create = sows_models.Sow.objects.filter(farm_id__in=create_sows)

            sows_events_models.Semination.objects.mass_semination(
                sows_qs=sows_to_create,
                week=serializer.validated_data['week'],
                semination_employee=request.user,
                initiator=request.user
                )

            sows_events_models.Semination.objects.mass_semination(
                sows_qs=sows_to_create,
                week=serializer.validated_data['week'],
                semination_employee=request.user,
                initiator=request.user
                )

            sows_events_models.Ultrasound.objects.mass_ultrasound(
                sows_qs=sows_to_create,
                days=30,
                result=True,
                initiator=request.user
                )

            sows_events_models.Ultrasound.objects.mass_ultrasound(
                sows_qs=sows_to_create,
                days=60,
                result=True,
                initiator=request.user
                )
            
            to_location = locations_models.Location.objects.get(workshop__number=3)
            transactions_models.SowTransaction.objects.create_many_transactions(
                sows_to_create, to_location, request.user)

            return Response(
                {
                    "created": create_sows,
                    "not_created": existed_sows,
                    "message": "Созданы и переведены {}, не созданы {}". \
                        format(str(create_sows), str(existed_sows)), 
                },
                status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=True)
    def double_semination(self, request, pk=None):
        sow = self.get_object() 
        serializer = serializers.DoubleSeminationSerializer(data=request.data)
        if serializer.is_valid():
            semination1 = sows_events_models.Semination.objects.create_semination(
                sow=sow, week=serializer.validated_data['week'],
                initiator=request.user, 
                semination_employee=serializer.validated_data['semination_employee'],
                boar=serializer.validated_data['boar1'])

            semination2 = sows_events_models.Semination.objects.create_semination(
                sow=sow, week=serializer.validated_data['week'],
                initiator=request.user, 
                semination_employee=serializer.validated_data['semination_employee'],
                boar=serializer.validated_data['boar2'])
            return Response(
                {
                    "semination1": sows_events_serializers.SeminationSerializer(semination1).data,
                    "semination2": sows_events_serializers.SeminationSerializer(semination2).data,
                    "sow": sows_serializers.SowSerializer(sow).data, 
                    "message": "Свиноматка {} осеменена 2 раза".format(sow.farm_id)
                },
                status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    # @action(methods=['post'], detail=False)
    # def import_seminations_from_farm(self, request):
    #     serializer = serializers.ImportSeminationsFile(data=request.data)
    #     if serializer.is_valid():
    #         with open('seminations.xls', 'wb') as file:
    #             for chunk in serializer.validated_data['file'].chunks():
    #                 file.write(chunk)

    #         wb = wsxlrd.init_wb('seminations.xls')
    #         rows = wsxlrd.get_semenation_rows(wb)
    #         for row in rows:
    #             print(row)
    #             sow, created = sows_models.Sow.objects.create_or_return(row[0])
    #             tour = tours_models.Tour.objects.create_or_return_by_raw(row[3])
    #             print(sow, created)
    #             print('_______________________________')


        

    #     return Response({'opa'}, status=status.HTTP_400_BAD_REQUEST)