# # -*- coding: utf-8 -*-
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from piglets_events.models import Recount
from locations.models import Section, Location


class RecountViewSet(viewsets.ViewSet):

    @action(methods=['get'], detail=False)
    def ws_balance(self, request):
        ws_number = request.GET.get('ws_number')
        data = dict()

        ws_locations = Location.objects.all().get_workshop_location_by_number(workshop_number=ws_number)
        data['ws_balance'] = Recount.objects.sum_balances_by_locations(locations=ws_locations)
        data['sections'] = list()

        for section in Section.objects.filter(workshop__number=ws_number):
            sec_locations = Location.objects.all().get_locations_in_section(section=section)
            data['sections'].append(
                {'number': section.number,
                 'balance': Recount.objects.sum_balances_by_locations(locations=sec_locations)}
                )

        return Response(data)