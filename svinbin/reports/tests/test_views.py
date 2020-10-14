# -*- coding: utf-8 -*-
import datetime
from datetime import timedelta, date
import copy

from django.utils import timezone

from rest_framework.test import APITestCase, APIClient

import locations.testing_utils as locations_testing
import sows.testing_utils as sows_testing
import sows_events.utils as sows_events_testings
import piglets.testing_utils as piglets_testing
import staff.testing_utils as staff_testing

from piglets.models import Piglets
from locations.models import Location
from tours.models import Tour, MetaTour
from reports.models import ReportDate, gen_operations_dict
from piglets_events.models import WeighingPiglets, CullingPiglets

from reports.serializers import ReportTourSerializer


class ReportDateViewSetTest(APITestCase):
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
        self.loc_ws3 = Location.objects.get(workshop__number=3)
        self.loc_ws3_cells = Location.objects.filter(sowAndPigletsCell__isnull=False)

        self.ops_dict = gen_operations_dict()

        operations = dict()
        for op_key in self.ops_dict.keys():
            operations[op_key] = False

        self.request_json = {
            'operations': operations,
            'filters': {'start_date': None, 'end_date': None, 'farm_id': None},
            'target': None
        } 

    def test_report_date_view(self):
        response = self.client.get('/api/reports/director/')
        self.assertEqual(len(response.data['results']) > 0, True)

    def test_report_date_view(self):
        request_json = copy.deepcopy(self.request_json)
        request_json['operations']['ws1_semination'] = True

        response = self.client.post('/api/reports/operations/', request_json, format='json')
        # print(response.data)
        # self.assertEqual(len(response.data['results']) > 0, True)


class TourReportV2ViewSetTest(APITestCase):
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

        self.loc_ws4 = Location.objects.get(workshop__number=4)
        self.loc_ws5_cells = Location.objects.filter(pigletsGroupCell__workshop__number=5)
        self.loc_ws3_cells = Location.objects.filter(sowAndPigletsCell__workshop__number=3)

    def test_weights_data(self):
        piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(
            tour=self.tour1,
            location=self.loc_ws4,
            quantity=100,
            birthday=datetime.datetime(2020,5,5,0,0)
            )
        piglets2 = piglets_testing.create_new_group_with_metatour_by_one_tour(
            tour=self.tour1,
            location=self.loc_ws4,
            quantity=100,
            birthday=datetime.datetime(2020,5,8,0,0)
            )

        WeighingPiglets.objects.create_weighing(piglets_group=piglets1, total_weight=120,
            place='3/4', date=datetime.datetime.today())
        WeighingPiglets.objects.create_weighing(piglets_group=piglets1, total_weight=150,
            place='3/4', date=datetime.datetime(2020,9,25,0,0))

        WeighingPiglets.objects.create_weighing(piglets_group=piglets2, total_weight=360,
            place='4/8', date=datetime.datetime(2020,9,15,0,0))

        piglets3 = piglets_testing.create_new_group_with_metatour_by_one_tour(
            tour=self.tour1,
            location=self.loc_ws5_cells[0],
            quantity=100,
            birthday=datetime.datetime(2020,5,5,0,0))
        piglets4 = piglets_testing.create_new_group_with_metatour_by_one_tour(
            tour=self.tour1,
            location=self.loc_ws5_cells[0],
            quantity=100,
            birthday=datetime.datetime(2020,5,5,0,0))

        CullingPiglets.objects.create_culling_piglets(
            piglets_group=piglets3, culling_type='spec', reason='xz', quantity=10, 
            total_weight=100, date='2020-12-09'
            )
        CullingPiglets.objects.create_culling_piglets(
            piglets_group=piglets4, culling_type='spec', reason='xz', quantity=1, 
            total_weight=9.5, date='2020-12-09'
            )

        piglets_testing.create_from_sow_farrow(tour=self.tour1, location=self.loc_ws3_cells[0],
            quantity=15, date=datetime.datetime(2020,8,5,0,0))

        response = self.client.get('/api/reports/tours_v2/%s/weights_data/' % self.tour1.pk)
        self.assertEqual(response.data['3/4']['total']['total_quantity'], 200)
        self.assertEqual(response.data['farrow_data']['total_alive'], 15)
        self.assertEqual(response.data['spec_5']['total']['total_quantity'], 11)
