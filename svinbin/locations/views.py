# -*- coding: utf-8 -*-
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, status

import locations.testing_utils as locations_testing
import sows.testing_utils as sows_testing
import piglets.testing_utils as piglets_testing
import staff.testing_utils as staff_testing

from locations.models import PigletsGroupCell, Location
from locations import serializers
from locations.filters import LocationFilter


class CreateWorkshopsView(APIView):
    # authentication_classes = (authentication.TokenAuthentication,)
    # permission_classes = (permissions.IsAdminUser,)

    def get(self, request, format=None):
        locations_testing.create_workshops_sections_and_cells()
        sows_testing.create_statuses()
        piglets_testing.create_piglets_statuses()
        sows_testing.create_sow_and_put_in_workshop_three()
        sows_testing.create_some_sows_with_tours_put_in_ws_one()
        piglets_testing.create_nomad_group_from_three_new_born()
        staff_testing.create_test_users()

        return Response({'msg': 'success'})


class PigletsGroupCellViewSet(viewsets.ModelViewSet):
    queryset = PigletsGroupCell.objects.all()
    serializer_class = serializers.PigletsGroupCellSerializer


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = serializers.LocationSerializer
    filter_class = LocationFilter

    # def create()