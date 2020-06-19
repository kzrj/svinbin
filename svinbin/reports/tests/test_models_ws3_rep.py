# -*- coding: utf-8 -*-
from freezegun import freeze_time

from datetime import timedelta, date, datetime

from django.utils import timezone
from django.db import models
from django.test import TransactionTestCase

from reports.models import ReportDate
from sows.models import Sow
from sows_events.models import CullingSow, SowFarrow, Semination, Ultrasound
from piglets.models import Piglets
from piglets_events.models import CullingPiglets
from tours.models import Tour
from locations.models import Location
from transactions.models import PigletsTransaction, SowTransaction

from piglets.serializers import PigletsSerializer

import locations.testing_utils as locations_testing
import piglets.testing_utils as piglets_testing
import sows.testing_utils as sows_testings
import sows_events.utils as sows_events_testings
import staff.testing_utils as staff_testings


class ReportDateWSReportTest(TransactionTestCase):
    def setUp(self):
        locations_testing.create_workshops_sections_and_cells()
        sows_testings.create_statuses()
        sows_events_testings.create_types()
        piglets_testing.create_piglets_statuses()

        start_date = date(2020, 1, 1)
        end_date = timezone.now().date() + timedelta(1)
        ReportDate.objects.create_bulk_if_none_from_range(start_date, end_date)

        self.tour1 = Tour.objects.get_or_create_by_week_in_current_year(week_number=1)
        self.tour2 = Tour.objects.get_or_create_by_week_in_current_year(week_number=2)

        self.loc_ws1 = Location.objects.get(workshop__number=1)
        self.loc_ws3 = Location.objects.get(workshop__number=3)

        self.loc_ws3_cells = Location.objects.filter(sowAndPigletsCell__isnull=False)

    def test_count_sows_ws3(self):
        sow1 = sows_testings.create_sow_and_put_in_workshop_one()
        sow2 = sows_testings.create_sow_and_put_in_workshop_one()
        to_location3 = Location.objects.get(workshop__number=3)
        to_location1 = Location.objects.get(workshop__number=1)

        with freeze_time("2020-01-14"):
            sows = Sow.objects.all()
            sows.update_status('Супорос 35')
            SowTransaction.objects.create_many_transactions([sow1, sow2],
                to_location3)

        with freeze_time("2020-01-25"):
            sows = Sow.objects.all()
            sows.update_status('Опоросилась')

        with freeze_time("2020-02-14"):
            SowTransaction.objects.create_many_transactions([sow1, sow2],
                to_location1)
            # ststus changed to Ожидает

        with freeze_time("2020-03-14"):
            sows = Sow.objects.all()
            sows.update_status('Супорос 35')
            SowTransaction.objects.create_many_transactions([sow1, sow2],
                to_location3)

        with freeze_time("2020-03-25"):
            sows = Sow.objects.all()
            sows.update_status('Опоросилась')

        with freeze_time("2020-04-14"):
            SowTransaction.objects.create_many_transactions([sow1, sow2],
                to_location1)
            # ststus changed to Ожидает

        with freeze_time("2020-05-14"):
            sows = Sow.objects.all()
            sows.update_status('Супорос 35')
            SowTransaction.objects.create_many_transactions([sow1, sow2],
                to_location3)

        with freeze_time("2020-05-25"):
            CullingSow.objects.create_culling(sow=sow2, culling_type='padej')

        today_rd = ReportDate.objects.get(date=datetime.today())

        sows = today_rd.count_sows_ws3()
        sow = sows.first()

        self.assertEqual(sows.count(), 1)
        self.assertEqual(sow.status_at_date, 'Супорос 35')
        self.assertEqual(sow.count_status_sup35, 1)

    def test_count_sows_ws3_today(self):
        sow1 = sows_testings.create_sow_and_put_in_workshop_one()
        sow2 = sows_testings.create_sow_and_put_in_workshop_one()
        sow3 = sows_testings.create_sow_and_put_in_workshop_one()
        to_location3 = Location.objects.get(workshop__number=3)
        to_location1 = Location.objects.get(workshop__number=1)

        with freeze_time("2020-05-14"):
            sows = Sow.objects.all()
            sows.update_status('Супорос 35')
            SowTransaction.objects.create_many_transactions([sow1, sow2, sow3],
                to_location3)

        sow3.refresh_from_db()
        sow3.change_status_to('Опоросилась')
        CullingSow.objects.create_culling(sow=sow2, culling_type='padej')

        today_rd = ReportDate.objects.get(date=datetime.today())

        sows = today_rd.count_sows_ws3(day=today_rd.date - timedelta(1))

        count_sows_start = today_rd.count_sows_ws3_start_date
        self.assertEqual(count_sows_start['suporos'], 3)
        self.assertEqual(count_sows_start['podsos'], 0)

        count_sows_end = today_rd.count_sows_ws3_end_date
        self.assertEqual(count_sows_end['suporos'], 1)
        self.assertEqual(count_sows_end['podsos'], 1)

        count_sows_today = today_rd.count_sows_ws3_today
        self.assertEqual(count_sows_today['suporos'], 1)
        self.assertEqual(count_sows_today['podsos'], 1)

    def test_count_sows_ws3_past_day(self):
        sow1 = sows_testings.create_sow_and_put_in_workshop_one()
        sow2 = sows_testings.create_sow_and_put_in_workshop_one()
        sow3 = sows_testings.create_sow_and_put_in_workshop_one()
        sow4 = sows_testings.create_sow_and_put_in_workshop_one()
        to_location3 = Location.objects.get(workshop__number=3)
        to_location1 = Location.objects.get(workshop__number=1)

        with freeze_time("2020-05-14"):
            sows = Sow.objects.all()
            sows.update_status('Супорос 35')
            SowTransaction.objects.create_many_transactions([sow1, sow2, sow3, sow4],
                to_location3)

        with freeze_time("2020-05-25"):
            sows = Sow.objects.filter(pk__in=[sow1.pk, sow2.pk])
            sows.update_status('Опоросилась')

        with freeze_time("2020-06-2"):
            sows = Sow.objects.filter(pk__in=[sow3.pk, sow4.pk])
            sows.update_status('Опоросилась')

        with freeze_time("2020-06-10"):
            SowTransaction.objects.create_many_transactions([sow1, sow2],
                to_location1)

        day1_rd = ReportDate.objects.get(date=date(2020, 5, 15))
        day2_rd = ReportDate.objects.get(date=date(2020, 5, 25))
        day3_rd = ReportDate.objects.get(date=date(2020, 6, 2))
        day4_rd = ReportDate.objects.get(date=date(2020, 6, 10))

        day1_start = day1_rd.count_sows_ws3_start_date
        self.assertEqual(day1_start['suporos'], 4)
        self.assertEqual(day1_start['podsos'], 0)
        day1_end = day1_rd.count_sows_ws3_end_date
        self.assertEqual(day1_end['suporos'], 4)
        self.assertEqual(day1_end['podsos'], 0)

        day2_start = day2_rd.count_sows_ws3_start_date
        self.assertEqual(day2_start['suporos'], 4)
        self.assertEqual(day2_start['podsos'], 0)
        day2_end = day2_rd.count_sows_ws3_end_date
        self.assertEqual(day2_end['suporos'], 2)
        self.assertEqual(day2_end['podsos'], 2)

        day3_start = day3_rd.count_sows_ws3_start_date
        self.assertEqual(day3_start['suporos'], 2)
        self.assertEqual(day3_start['podsos'], 2)
        day3_end = day3_rd.count_sows_ws3_end_date
        self.assertEqual(day3_end['suporos'], 0)
        self.assertEqual(day3_end['podsos'], 4)

        day4_start = day4_rd.count_sows_ws3_start_date
        self.assertEqual(day4_start['suporos'], 0)
        self.assertEqual(day4_start['podsos'], 4)
        day4_end = day4_rd.count_sows_ws3_end_date
        self.assertEqual(day4_end['suporos'], 0)
        self.assertEqual(day4_end['podsos'], 2)

    def test_count_trs_ws3_today(self):
        sow1 = sows_testings.create_sow_and_put_in_workshop_one()
        sow2 = sows_testings.create_sow_and_put_in_workshop_one()
        sow3 = sows_testings.create_sow_and_put_in_workshop_one()
        sow4 = sows_testings.create_sow_and_put_in_workshop_one()
        to_location3 = Location.objects.get(workshop__number=3)
        to_location1 = Location.objects.get(workshop__number=1)

        with freeze_time("2020-05-14"):
            sows = Sow.objects.all()
            sows.update_status('Супорос 35')
            SowTransaction.objects.create_many_transactions([sow1, sow2, sow3, sow4],
                to_location3)

        with freeze_time("2020-06-10"):
            SowTransaction.objects.create_many_transactions([sow1, sow2],
                to_location1)

        day1_rd = ReportDate.objects.get(date=date(2020, 6, 10))
        
        self.assertEqual(day1_rd.count_trs_out_ws3_today['suporos'], 2)
        self.assertEqual(day1_rd.count_trs_out_ws3_today['podsos'], 0)

        day2_rd = ReportDate.objects.get(date=date(2020, 5, 14))
        self.assertEqual(day2_rd.count_trs_in_ws3_today['suporos'], 4)
        self.assertEqual(day2_rd.count_trs_in_ws3_today['podsos'], 0)

    def test_add_ws3_sow_cullings_data(self):
        sow1 = sows_testings.create_sow_and_put_in_workshop_one()
        sow2 = sows_testings.create_sow_and_put_in_workshop_one()
        sow3 = sows_testings.create_sow_and_put_in_workshop_one()
        sow4 = sows_testings.create_sow_and_put_in_workshop_one()
        to_location3 = Location.objects.get(workshop__number=3)
        to_location1 = Location.objects.get(workshop__number=1)

        with freeze_time("2020-05-14"):
            sows = Sow.objects.all()
            sows.update_status('Супорос 35')
            SowTransaction.objects.create_many_transactions(sows, to_location3)

        with freeze_time("2020-05-30"):
            sows = Sow.objects.filter(pk__in=[sow1.pk, sow2.pk])
            sows.update_status('Опоросилась')

        with freeze_time("2020-06-10"):
            sow1.refresh_from_db()
            sow2.refresh_from_db()
            sow3.refresh_from_db()
            sow4.refresh_from_db()
            CullingSow.objects.create_culling(sow=sow1, culling_type='padej', weight=100)
            CullingSow.objects.create_culling(sow=sow2, culling_type='padej', weight=100)
            CullingSow.objects.create_culling(sow=sow3, culling_type='padej', weight=100)
            CullingSow.objects.create_culling(sow=sow4, culling_type='padej', weight=100)

        day1_rd = ReportDate.objects.all().add_ws3_sow_cullings_data() \
                    .filter(date=date(2020, 6, 10)).first()

        self.assertEqual(day1_rd.padej_sup_count, 2)
        self.assertEqual(day1_rd.padej_sup_weight, 200)
        self.assertEqual(day1_rd.padej_podsos_count, 2)
        self.assertEqual(day1_rd.padej_podsos_weight, 200)

    def test_add_ws3_sow_trs_data(self):
        sow1 = sows_testings.create_sow_and_put_in_workshop_one()
        sow2 = sows_testings.create_sow_and_put_in_workshop_one()
        sow3 = sows_testings.create_sow_and_put_in_workshop_one()
        sow4 = sows_testings.create_sow_and_put_in_workshop_one()
        to_location3 = Location.objects.get(workshop__number=3)
        to_location1 = Location.objects.get(workshop__number=1)

        with freeze_time("2020-05-14"):
            sows = Sow.objects.all()
            sows.update_status('Супорос 35')
            SowTransaction.objects.create_many_transactions(sows, to_location3)

        ws_locs = Location.objects.all().get_workshop_location_by_number(workshop_number=3)
        day1_rd = ReportDate.objects.all().add_ws3_sow_trs_data(ws_locs=ws_locs) \
                    .filter(date=date(2020, 5, 14)).first()

        self.assertEqual(day1_rd.tr_in_from_1_sup_count, 4)
