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

        self.loc_ws1 = Location.objects.get(workshop__number=1)
        self.loc_ws3 = Location.objects.get(workshop__number=3)
        self.loc_ws4 = Location.objects.get(workshop__number=4)

        self.ws3_locs = Location.objects.all().get_workshop_location_by_number(workshop_number=3)

        self.loc_ws3_cells = Location.objects.filter(sowAndPigletsCell__isnull=False)

    def test_count_sows_ws3(self):
        sow1 = sows_testings.create_sow_and_put_in_workshop_one()
        sow2 = sows_testings.create_sow_and_put_in_workshop_one()

        with freeze_time("2020-01-14"):
            sows = Sow.objects.all()
            sows.update_status('Супорос 35')
            SowTransaction.objects.create_many_transactions([sow1, sow2],
                self.loc_ws3)

        with freeze_time("2020-01-25"):
            sows = Sow.objects.all()
            sows.update_status('Опоросилась')

        with freeze_time("2020-02-14"):
            SowTransaction.objects.create_many_transactions([sow1, sow2],
                self.loc_ws1)
            # ststus changed to Ожидает

        with freeze_time("2020-03-14"):
            sows = Sow.objects.all()
            sows.update_status('Супорос 35')
            SowTransaction.objects.create_many_transactions([sow1, sow2],
                self.loc_ws3)

        with freeze_time("2020-03-25"):
            sows = Sow.objects.all()
            sows.update_status('Опоросилась')

        with freeze_time("2020-04-14"):
            SowTransaction.objects.create_many_transactions([sow1, sow2],
                self.loc_ws1)
            # ststus changed to Ожидает

        with freeze_time("2020-05-14"):
            sows = Sow.objects.all()
            sows.update_status('Супорос 35')
            SowTransaction.objects.create_many_transactions([sow1, sow2],
                self.loc_ws3)

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

        with freeze_time("2020-05-14"):
            sows = Sow.objects.all()
            sows.update_status('Супорос 35')
            SowTransaction.objects.create_many_transactions([sow1, sow2, sow3],
                self.loc_ws3)

        with freeze_time("2020-05-24"):
            sow3.refresh_from_db()
            sow3.change_status_to('Опоросилась')
            CullingSow.objects.create_culling(sow=sow2, culling_type='padej')

        today_rd = ReportDate.objects.get(date=date(2020,5,24))

        sows = today_rd.count_sows_ws3(day=today_rd.date - timedelta(1))

        count_sows_start = today_rd.count_sows_ws3_start_date
        self.assertEqual(count_sows_start['suporos'], 3)
        self.assertEqual(count_sows_start['podsos'], 0)

        count_sows_end = today_rd.count_sows_ws3_end_date
        self.assertEqual(count_sows_end['suporos'], 1)
        self.assertEqual(count_sows_end['podsos'], 1)

    def test_count_sows_ws3_past_day(self):
        sow1 = sows_testings.create_sow_and_put_in_workshop_one()
        sow2 = sows_testings.create_sow_and_put_in_workshop_one()
        sow3 = sows_testings.create_sow_and_put_in_workshop_one()
        sow4 = sows_testings.create_sow_and_put_in_workshop_one()

        with freeze_time("2020-05-14"):
            sows = Sow.objects.all()
            sows.update_status('Супорос 35')
            SowTransaction.objects.create_many_transactions([sow1, sow2, sow3, sow4],
                self.loc_ws3)

        with freeze_time("2020-05-25"):
            sows = Sow.objects.filter(pk__in=[sow1.pk, sow2.pk])
            sows.update_status('Опоросилась')

        with freeze_time("2020-06-2"):
            sows = Sow.objects.filter(pk__in=[sow3.pk, sow4.pk])
            sows.update_status('Опоросилась')

        with freeze_time("2020-06-10"):
            SowTransaction.objects.create_many_transactions([sow1, sow2],
                self.loc_ws1)

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

    def test_add_ws3_sow_cullings_data(self):
        sow1 = sows_testings.create_sow_and_put_in_workshop_one()
        sow2 = sows_testings.create_sow_and_put_in_workshop_one()
        sow3 = sows_testings.create_sow_and_put_in_workshop_one()
        sow4 = sows_testings.create_sow_and_put_in_workshop_one()

        with freeze_time("2020-05-14"):
            sows = Sow.objects.all()
            sows.update_status('Супорос 35')
            SowTransaction.objects.create_many_transactions(sows, self.loc_ws3)

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

        day1_rd = ReportDate.objects.all().add_ws3_sow_cullings_data(ws_locs=self.ws3_locs) \
                    .filter(date=date(2020, 6, 10)).first()

        self.assertEqual(day1_rd.padej_sup_count, 2)
        self.assertEqual(day1_rd.padej_sup_weight, 200)
        self.assertEqual(day1_rd.padej_podsos_count, 2)
        self.assertEqual(day1_rd.padej_podsos_weight, 200)

    def test_add_ws3_sow_trs_in_data(self):
        sow1 = sows_testings.create_sow_and_put_in_workshop_one()
        sow2 = sows_testings.create_sow_and_put_in_workshop_one()
        sow3 = sows_testings.create_sow_and_put_in_workshop_one()
        sow4 = sows_testings.create_sow_and_put_in_workshop_one()

        with freeze_time("2020-05-14"):
            sows = Sow.objects.all()
            sows.update_status('Супорос 35')
            SowTransaction.objects.create_many_transactions(sows, self.loc_ws3)

        day1_rd = ReportDate.objects.all().add_ws3_sow_trs_data(ws_locs=self.ws3_locs) \
                    .filter(date=date(2020, 5, 14)).first()

        self.assertEqual(day1_rd.tr_in_from_1_sup_count, 4)

    def test_add_ws3_sow_trs_out_data(self):
        sow1 = sows_testings.create_sow_and_put_in_workshop_one()
        sow2 = sows_testings.create_sow_and_put_in_workshop_one()
        sow3 = sows_testings.create_sow_and_put_in_workshop_one()
        sow4 = sows_testings.create_sow_and_put_in_workshop_one()

        with freeze_time("2020-05-14"):
            sows = Sow.objects.all()
            sows.update_status('Супорос 35')
            SowTransaction.objects.create_many_transactions(sows, self.loc_ws3)

        with freeze_time("2020-05-25"):
            sows = Sow.objects.all()
            sows.update_status('Опоросилась')
            SowTransaction.objects.create_many_transactions(sows, self.loc_ws1)

        day1_rd = ReportDate.objects.all().add_ws3_sow_trs_data(ws_locs=self.ws3_locs) \
                    .filter(date=date(2020, 5, 25)).first()

        self.assertEqual(day1_rd.tr_out_podsos_count, 4)

    def test_add_ws3_sow_farrow_data(self):
        sow1 = sows_testings.create_sow_and_put_in_workshop_one()
        sow2 = sows_testings.create_sow_and_put_in_workshop_one()
        sow3 = sows_testings.create_sow_and_put_in_workshop_one()
        sow4 = sows_testings.create_sow_and_put_in_workshop_one()

        with freeze_time("2020-05-14"):
            sows = Sow.objects.all()
            sows.update_status('Супорос 35')
            SowTransaction.objects.create_many_transactions(sows, self.loc_ws3)

        with freeze_time("2020-05-25"):
            sow1.tour = self.tour1
            sow1.location = self.loc_ws3_cells[0]
            sow1.save()
            sow2.tour = self.tour1
            sow2.location = self.loc_ws3_cells[1]
            sow2.save()
            SowFarrow.objects.create_sow_farrow(sow=sow1, alive_quantity=10)
            SowFarrow.objects.create_sow_farrow(sow=sow2, alive_quantity=15)

        with self.assertNumQueries(1):
            day1_rd = ReportDate.objects.all().add_ws3_sow_farrow_data() \
                        .filter(date=date(2020, 5, 25)).first()

            self.assertEqual(day1_rd.count_oporos, 2)
            self.assertEqual(day1_rd.count_alive, 25)

    def test_add_ws3_count_piglets_start_day(self):
        sow1 = sows_testings.create_sow_and_put_in_workshop_one()
        sow2 = sows_testings.create_sow_and_put_in_workshop_one()
        sow3 = sows_testings.create_sow_and_put_in_workshop_one()
        sow4 = sows_testings.create_sow_and_put_in_workshop_one()

        with freeze_time("2020-05-14"):
            sows = Sow.objects.all()
            sows.update_status('Супорос 35')
            SowTransaction.objects.create_many_transactions(sows, self.loc_ws3)

        with freeze_time("2020-05-25"):
            for idx, sow in enumerate(Sow.objects.all()):
                sow.tour = self.tour1
                sow.location = self.loc_ws3_cells[idx]
                sow.save()
                SowFarrow.objects.create_sow_farrow(sow=sow, alive_quantity=10)
                # 40

        with freeze_time("2020-05-27"):
            for p in Piglets.objects.all():
                PigletsTransaction.objects.transaction_with_split_and_merge(
                    piglets=p, to_location=self.loc_ws4, new_amount=2
                    )
                # 40 - 8 = 32

        with freeze_time("2020-06-1"):
            # move 2 to ws3
            p = Piglets.objects.filter(location=self.loc_ws4).first()
            PigletsTransaction.objects.create_transaction(
                piglets_group=p, to_location=self.loc_ws3
                )
            # 32 + 2 = 34

        with freeze_time("2020-06-3"):
            # Piglets.objects.filter(location__in=wslocs).count() = 5
            for p in Piglets.objects.filter(location__in=self.ws3_locs):
                CullingPiglets.objects.create_culling_piglets(
                    piglets_group=p, culling_type='padej', quantity=1
                    )
            # 34 - 5 = 29

        rds = ReportDate.objects.all().add_ws3_count_piglets_start_day(ws_locs=self.ws3_locs, add_live=False)
        
        day1_rd = rds.filter(date=date(2020, 5, 14)).first()
        self.assertEqual(day1_rd.count_piglets_at_start, 0)

        day2_rd = rds.filter(date=date(2020, 5, 26)).first()
        self.assertEqual(day2_rd.count_piglets_at_start, 40)

        day3_rd = rds.filter(date=date(2020, 5, 28)).first()
        self.assertEqual(day3_rd.count_piglets_at_start, 32)

        day4_rd = rds.filter(date=date(2020, 6, 2)).first()
        self.assertEqual(day4_rd.count_piglets_at_start, 34)

        day5_rd = rds.filter(date=date(2020, 6, 4)).first()
        self.assertEqual(day5_rd.count_piglets_at_start, 29)

        day6_rd = rds.filter(date=datetime.today()).first()
        self.assertEqual(day6_rd.count_piglets_at_start, 29)

    def test_add_ws3_piglets_trs_out_aka_weighing(self):
        piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(
            tour=self.tour1, location=self.loc_ws3_cells[0], quantity=10)
        piglets2 = piglets_testing.create_new_group_with_metatour_by_one_tour(
            tour=self.tour1, location=self.loc_ws3_cells[1], quantity=10)
        piglets3 = piglets_testing.create_new_group_with_metatour_by_one_tour(
            tour=self.tour1, location=self.loc_ws3_cells[2], quantity=10)

        with freeze_time("2020-06-3"):
            for p in Piglets.objects.all():
                WeighingPiglets.objects.create_weighing(
                    piglets_group=p, total_weight=100, place='3/4')

        rds = ReportDate.objects.all().add_ws3_piglets_trs_out_aka_weighing()

        day1_rd = rds.filter(date=date(2020, 6, 3)).first()
        self.assertEqual(day1_rd.tr_out_aka_weight_qnty, 30)
        self.assertEqual(day1_rd.tr_out_aka_weight_total, 300)
        self.assertEqual(day1_rd.tr_out_aka_weight_avg, 10)

        day0_rd = rds.filter(date=date(2020, 6, 1)).first()
        self.assertEqual(day0_rd.tr_out_aka_weight_qnty, None)
        self.assertEqual(day0_rd.tr_out_aka_weight_total, None)
        self.assertEqual(day0_rd.tr_out_aka_weight_avg, None)

    def test_add_ws3_piglets_cullings(self):
        piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(
            tour=self.tour1, location=self.loc_ws3_cells[0], quantity=10)
        piglets2 = piglets_testing.create_new_group_with_metatour_by_one_tour(
            tour=self.tour1, location=self.loc_ws3_cells[1], quantity=10)
        piglets3 = piglets_testing.create_new_group_with_metatour_by_one_tour(
            tour=self.tour1, location=self.loc_ws3_cells[2], quantity=10)

        with freeze_time("2020-06-3"):
            for p in Piglets.objects.all():
                CullingPiglets.objects.create_culling_piglets(
                    piglets_group=p, culling_type='padej', total_weight=1.5)


        rds = ReportDate.objects.all().add_ws3_piglets_cullings(ws_locs=self.ws3_locs)

        day1_rd = rds.filter(date=date(2020, 6, 3)).first()
        self.assertEqual(day1_rd.ws3_piglets_padej_qnty, 3)
        self.assertEqual(day1_rd.ws3_piglets_padej_weight, 4.5)

        day0_rd = rds.filter(date=date(2020, 6, 1)).first()
        self.assertEqual(day0_rd.ws3_piglets_padej_qnty, None)
        self.assertEqual(day0_rd.ws3_piglets_padej_weight, None)

    def test_serializer(self):
        qs = ReportDate.objects.all()\
                .add_ws3_sow_cullings_data(ws_locs=self.ws3_locs) \
                .add_ws3_sow_trs_data(ws_locs=self.ws3_locs) \
                .add_ws3_sow_farrow_data() \
                .add_ws3_count_piglets_start_day(ws_locs=self.ws3_locs) \
                .add_ws3_piglets_trs_out_aka_weighing() \
                .add_ws3_piglets_cullings(ws_locs=self.ws3_locs)

        sow1 = sows_testings.create_sow_and_put_in_workshop_one()
        sow2 = sows_testings.create_sow_and_put_in_workshop_one()
        sow3 = sows_testings.create_sow_and_put_in_workshop_one()
        sow4 = sows_testings.create_sow_and_put_in_workshop_one()

        with freeze_time("2020-05-14"):
            sows = Sow.objects.all()
            sows.update_status('Супорос 35')
            SowTransaction.objects.create_many_transactions(sows, self.loc_ws3)

        qs = qs.filter(date__gte=date(2020, 5, 1), date__lte=date(2020, 5, 30))

        # with self.assertNumQueries(1):
        #     serializer = ReportDateWs3Serializer(qs, many=True)
        #     print(serializer.data)