# -*- coding: utf-8 -*-
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, status

import locations.testing_utils as locations_testing
import sows.testing_utils as sows_testing

from locations.models import PigletsGroupCell
from locations import serializers


class CreateWorkshopsView(APIView):
    # authentication_classes = (authentication.TokenAuthentication,)
    # permission_classes = (permissions.IsAdminUser,)

    def get(self, request, format=None):
        locations_testing.create_workshops_sections_and_cells()
        sows_testing.create_statuses()
        sows_testing.create_nomad_and_move_to_cell_in_workshop_four()
        return Response({'msg': 'success'})


class PigletsGroupCellViewSet(viewsets.ModelViewSet):
    queryset = PigletsGroupCell.objects.all()
    serializer_class = serializers.PigletsGroupCellSerializer