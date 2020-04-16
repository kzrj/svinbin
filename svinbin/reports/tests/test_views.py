# -*- coding: utf-8 -*-
import datetime
import random

from django.contrib.auth.models import User
from django.db import connection

from rest_framework.test import APIClient
from rest_framework.test import APITestCase

import locations.testing_utils as locations_testing
import sows.testing_utils as sows_testing
import sows_events.utils as sows_events_testings
import piglets.testing_utils as piglets_testing
import staff.testing_utils as staff_testing

from piglets.models import Piglets
from locations.models import Location
from tours.models import Tour, MetaTour
from piglets_events.models import WeighingPiglets
from sows.models import Sow
from sows_events.models import SowFarrow
from transactions.models import PigletsTransaction, SowTransaction

from reports.serializers import ReportTourSerializer, ReportTourSerializer2


class TourReportsViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        locations_testing.create_workshops_sections_and_cells()
        sows_testing.create_statuses()
        piglets_testing.create_piglets_statuses()
        sows_events_testings.create_types()

        self.user = staff_testing.create_employee()
        self.client.force_authenticate(user=self.user)

        self.tour1 = Tour.objects.get_or_create_by_week_in_current_year(week_number=1)
        self.tour2 = Tour.objects.get_or_create_by_week_in_current_year(week_number=2)
        self.tour3 = Tour.objects.get_or_create_by_week_in_current_year(week_number=3)
        self.tour4 = Tour.objects.get_or_create_by_week_in_current_year(week_number=4)
        self.loc_ws3 = Location.objects.get(workshop__number=3)
        self.loc_ws3_sec1 = Location.objects.get(section__workshop__number=3, section__number=1)
        self.loc_ws3_sec2 = Location.objects.get(section__workshop__number=3, section__number=2)

        self.loc_ws4 = Location.objects.get(workshop__number=4)
        self.loc_ws4_cell1 = Location.objects.filter(pigletsGroupCell__isnull=False)[0]
        self.loc_ws4_cell2 = Location.objects.filter(pigletsGroupCell__isnull=False)[1]

        self.loc_ws_5 = Location.objects.get(workshop__number=5)
        self.loc_ws_6 = Location.objects.get(workshop__number=6)

    def test_create_from_merging_list(self):
        piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws3_sec1, 10)
        piglets2 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws3_sec1, 10)
        piglets3 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws3_sec1, 10)

        tours = Tour.objects.all() \
                .add_sow_data() \
                .add_farrow_data() \
                .add_current_not_mixed_piglets_quantity() \
                .add_current_mixed_piglets_quantity() \
                .add_weight_data_not_mixed() \
                .add_weight_data_mixed() \
                .add_weight_date() \
                .add_avg_weight_data() \
                .add_age_at_weight_date() \
                .add_culling_weight_not_mixed_piglets() \
                .add_culling_qnty_not_mixed_piglets() \
                .add_culling_avg_weight_not_mixed_piglets() \
                .add_culling_percentage_not_mixed_piglets() \
                .add_current_piglets_age()

        # serializer = ReportTourSerializer2(tours[0])
        # print(serializer.data)

        # serializer = ReportTourSerializer(tours, many=True)
        # print(serializer.data)

        response = self.client.get('/api/reports/tours/')
        print(response.data)
        print(response.data['results'][0]['age_at_3_4'])
        print(response.data['results'][0]['piglets_age'])