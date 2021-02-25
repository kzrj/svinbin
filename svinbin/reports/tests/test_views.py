# -*- coding: utf-8 -*-
import datetime
from datetime import timedelta, date
from freezegun import freeze_time

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
from sows_events.models import PigletsToSowsEvent, CullingSow
from sows.models import Sow, SowStatus, Boar
from transactions.models import SowTransaction

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


class TourReportFilterViewSetTest(APITestCase):
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

    def test_tour_filter_ids(self):
        response = self.client.get('/api/reports/tours/?ids=1,2')
        # print(response.data)


class ReportWS12Test(APITestCase):
    def setUp(self):
        self.client = APIClient()
        locations_testing.create_workshops_sections_and_cells()
        sows_testing.create_statuses()
        piglets_testing.create_piglets_statuses()
        sows_events_testings.create_types()

        self.user = staff_testing.create_employee()
        self.client.force_authenticate(user=self.user)

        self.tour1 = Tour.objects.get_or_create_by_week(week_number=1, year=2020)
        self.cells = Location.objects.filter(pigletsGroupCell__isnull=False)
        self.piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(tour=self.tour1, 
            location=self.cells[0], quantity=100, birthday=date(2020, 1, 1))
        self.piglets2 = piglets_testing.create_new_group_with_metatour_by_one_tour(tour=self.tour1, 
            location=self.cells[1], quantity=100, birthday=date(2020, 1, 1))

        self.loc1 = Location.objects.get(workshop__number=1)
        self.loc2 = Location.objects.get(workshop__number=2)
        self.loc3 = Location.objects.get(workshop__number=3)

        start_date = date(2020, 1, 1)
        end_date = timezone.now().date()
        ReportDate.objects.create_bulk_if_none_from_range(start_date, end_date)

        to_gilts_date = date(2020, 5, 5)
        to_gilt_event = PigletsToSowsEvent.objects.create_event(piglets=self.piglets1, date=to_gilts_date)

        for sow1 in Sow.objects.all()[:37]:
            SowTransaction.objects.create_transaction(sow=sow1, to_location=self.loc1,
             date=date(2020, 6, 15))

        sows_ws1 = Sow.objects.filter(location__workshop__number=1)
        status1 = SowStatus.objects.get(title='Супорос 35')
        sows_ws1.filter(pk__in=sows_ws1.values_list('pk', flat=True)[:20]).update(status=status1)

        with freeze_time("2020-06-25"):
            for sow in Sow.objects.filter(location__workshop__number=1, status__title='Супорос 35')[:7]:
                CullingSow.objects.create_culling(sow=sow, culling_type='padej', weight=100)

            for sow in Sow.objects.filter(location__workshop__number=1, status__title='Ремонтная')[:2]:
                CullingSow.objects.create_culling(sow=sow, culling_type='padej', weight=101)

    def test_ws12_report(self):
        response = self.client.get('/api/reports/director/ws12_report/?ws_number=1')
        self.assertEqual(response.data['total_info']['total_padej_rem_weight'], 202)


class SowDowntimeReportTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        locations_testing.create_workshops_sections_and_cells()
        sows_testing.create_statuses()
        piglets_testing.create_piglets_statuses()
        sows_events_testings.create_types()

        self.user = staff_testing.create_employee()
        self.client.force_authenticate(user=self.user)

        self.tour1 = Tour.objects.get_or_create_by_week_in_current_year(week_number=1)

    def test_get_data(self):
        loc = Location.objects.get(workshop__number=1)
        sow1 = sows_testing.create_sow_with_location(location=loc)
        with freeze_time("2021-01-5T10:00"):
            sow1.change_status_to('Ремонтная')

        sow2 = sows_testing.create_sow_with_location(location=loc)
        with freeze_time("2021-01-5T10:00"):
            sow2.change_status_to('Осеменена 2')

        sow3 = sows_testing.create_sow_with_location(location=loc)
        with freeze_time("2021-01-5T10:00"):
            sow3.change_status_to('Супорос 35')

        sow4 = sows_testing.create_sow_with_location(location=loc)
        with freeze_time("2021-01-5T10:00"):
            sow4.change_status_to('Опоросилась')

        response = self.client.get('/api/reports/sows_downtime/')
        
        self.assertEqual(response.data['wait']['count_all'], 1)
        self.assertEqual(response.data['wait']['downtime_sows'][0]['id'], sow1.pk)

        self.assertEqual(response.data['sem']['count_all'], 1)
        self.assertEqual(response.data['sem']['downtime_sows'][0]['id'], sow2.pk)

        self.assertEqual(response.data['sup35']['count_all'], 1)
        self.assertEqual(response.data['sup35']['downtime_sows'][0]['id'], sow3.pk)

        self.assertEqual(response.data['farr']['count_all'], 1)
        self.assertEqual(response.data['farr']['downtime_sows'][0]['id'], sow4.pk)