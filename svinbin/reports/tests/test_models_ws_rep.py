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
from piglets_events.models import CullingPiglets, WeighingPiglets
from tours.models import Tour
from locations.models import Location
from transactions.models import PigletsTransaction, SowTransaction

import locations.testing_utils as locations_testing
import piglets.testing_utils as piglets_testing
import sows.testing_utils as sows_testings
import sows_events.utils as sows_events_testings
import staff.testing_utils as staff_testings

from reports.serializers import ReportDateWs3Serializer


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

        self.loc_ws3 = Location.objects.get(workshop__number=3)
        self.loc_ws4 = Location.objects.get(workshop__number=4)
        self.loc_ws8 = Location.objects.get(workshop__number=8)

        self.ws3_locs = Location.objects.all().get_workshop_location_by_number(workshop_number=3)
        self.ws4_locs = Location.objects.all().get_workshop_location_by_number(workshop_number=4)

        self.loc_ws3_cells = Location.objects.filter(sowAndPigletsCell__isnull=False)
        self.loc_ws4_cells = Location.objects.filter(pigletsGroupCell__isnull=False)

    def test_add_ws_count_piglets_start_day(self):
        piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(
            tour=self.tour1, location=self.loc_ws3_cells[0], quantity=10)
        piglets2 = piglets_testing.create_new_group_with_metatour_by_one_tour(
            tour=self.tour1, location=self.loc_ws3_cells[1], quantity=10)
        piglets3 = piglets_testing.create_new_group_with_metatour_by_one_tour(
            tour=self.tour1, location=self.loc_ws3_cells[2], quantity=10)

        with freeze_time("2020-06-3"):
            for p in Piglets.objects.all():
                PigletsTransaction.objects.create_transaction(
                    piglets_group=p, to_location=self.loc_ws4)

        with freeze_time("2020-06-5"):
            for p in Piglets.objects.all():
                CullingPiglets.objects.create_culling_piglets(
                    piglets_group=p, culling_type='padej', total_weight=10)

        with freeze_time("2020-06-10"):
            for p in Piglets.objects.all():
                PigletsTransaction.objects.transaction_with_split_and_merge(
                    piglets=p, to_location=self.loc_ws8, new_amount=2)

        rds = ReportDate.objects.all().add_ws_count_piglets_start_day(ws_locs=self.ws4_locs)

        day0_rd = rds.filter(date=date(2020, 6, 1)).first()
        self.assertEqual(day0_rd.count_piglets_at_start, 0)

        day1_rd = rds.filter(date=date(2020, 6, 4)).first()
        self.assertEqual(day1_rd.count_piglets_at_start, 30)

        day2_rd = rds.filter(date=date(2020, 6, 6)).first()
        self.assertEqual(day2_rd.count_piglets_at_start, 27)

        day3_rd = rds.filter(date=date(2020, 6, 11)).first()
        self.assertEqual(day3_rd.count_piglets_at_start, 21)

        day4_rd = rds.filter(date=date(2020, 6, 20)).first()
        self.assertEqual(day4_rd.count_piglets_at_start, 21)

    def test_add_ws_weighing_in(self):
        piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(
            tour=self.tour1, location=self.loc_ws3_cells[0], quantity=10)
        piglets2 = piglets_testing.create_new_group_with_metatour_by_one_tour(
            tour=self.tour1, location=self.loc_ws3_cells[1], quantity=10)
        piglets3 = piglets_testing.create_new_group_with_metatour_by_one_tour(
            tour=self.tour1, location=self.loc_ws3_cells[2], quantity=10)

        with freeze_time("2020-06-3"):
            for p in Piglets.objects.all():
                PigletsTransaction.objects.create_transaction(
                    piglets_group=p, to_location=self.loc_ws4)
                WeighingPiglets.objects.create_weighing(
                    piglets_group=p, total_weight=100, place='3/4')
        
        rds = ReportDate.objects.all().add_ws_weighing_in(ws_number=4)

        day0_rd = rds.filter(date=date(2020, 6, 3)).first()
        self.assertEqual(day0_rd.tr_in_aka_weight_in_qnty, 30)
        self.assertEqual(day0_rd.tr_in_aka_weight_in_total, 300)
        self.assertEqual(day0_rd.tr_in_aka_weight_in_avg, 10)

        day1_rd = rds.filter(date=date(2020, 6, 4)).first()
        self.assertEqual(day1_rd.tr_in_aka_weight_in_qnty, None)
        self.assertEqual(day1_rd.tr_in_aka_weight_in_total, None)
        self.assertEqual(day1_rd.tr_in_aka_weight_in_avg, None)

    def test_add_ws_weighing_out(self):
        piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(
            tour=self.tour1, location=self.loc_ws3_cells[0], quantity=10)
        piglets2 = piglets_testing.create_new_group_with_metatour_by_one_tour(
            tour=self.tour1, location=self.loc_ws3_cells[1], quantity=10)
        piglets3 = piglets_testing.create_new_group_with_metatour_by_one_tour(
            tour=self.tour1, location=self.loc_ws3_cells[2], quantity=10)

        with freeze_time("2020-06-3"):
            for p in Piglets.objects.all():
                PigletsTransaction.objects.create_transaction(
                    piglets_group=p, to_location=self.loc_ws4)
                WeighingPiglets.objects.create_weighing(
                    piglets_group=p, total_weight=100, place='3/4')

        with freeze_time("2020-06-6"):
            for p in Piglets.objects.all():
                PigletsTransaction.objects.create_transaction(
                    piglets_group=p, to_location=self.loc_ws8)
                WeighingPiglets.objects.create_weighing(
                    piglets_group=p, total_weight=150, place='4/8')
        
        rds = ReportDate.objects.all().add_ws_weighing_out(ws_number=4)

        day0_rd = rds.filter(date=date(2020, 6, 3)).first()
        self.assertEqual(day0_rd.tr_out_aka_weight_in_qnty, None)
        self.assertEqual(day0_rd.tr_out_aka_weight_in_total, None)
        self.assertEqual(day0_rd.tr_out_aka_weight_in_avg, None)

        day1_rd = rds.filter(date=date(2020, 6, 6)).first()
        self.assertEqual(day1_rd.tr_out_aka_weight_in_qnty, 30)
        self.assertEqual(day1_rd.tr_out_aka_weight_in_total, 450)
        self.assertEqual(day1_rd.tr_out_aka_weight_in_avg, 15)

        # self.assertEqual(day0_rd.count_piglets_at_start, 0)

    # def test_serializer(self):
    #     qs = ReportDate.objects.all()\
    #             .add_ws3_sow_cullings_data(ws_locs=self.ws3_locs) \
    #             .add_ws3_sow_trs_data(ws_locs=self.ws3_locs) \
    #             .add_ws3_sow_farrow_data() \
    #             .add_ws3_count_piglets_start_day(ws_locs=self.ws3_locs) \
    #             .add_ws3_piglets_trs_out_aka_weighing() \
    #             .add_ws3_piglets_cullings(ws_locs=self.ws3_locs)

    #     sow1 = sows_testings.create_sow_and_put_in_workshop_one()
    #     sow2 = sows_testings.create_sow_and_put_in_workshop_one()
    #     sow3 = sows_testings.create_sow_and_put_in_workshop_one()
    #     sow4 = sows_testings.create_sow_and_put_in_workshop_one()

    #     with freeze_time("2020-05-14"):
    #         sows = Sow.objects.all()
    #         sows.update_status('Супорос 35')
    #         SowTransaction.objects.create_many_transactions(sows, self.loc_ws3)

    #     qs = qs.filter(date__gte=date(2020, 5, 1), date__lte=date(2020, 5, 30))

    #     # with self.assertNumQueries(1):
    #     #     serializer = ReportDateWs3Serializer(qs, many=True)
    #     #     print(serializer.data)