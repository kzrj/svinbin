# -*- coding: utf-8 -*-
from freezegun import freeze_time

from datetime import timedelta, date, datetime

from django.utils import timezone
from django.db import models
from django.test import TransactionTestCase

from reports.models import ReportDate
from sows.models import Sow, Boar, SowStatus
from sows_events.models import CullingSow, SowFarrow, Semination, Ultrasound, PigletsToSowsEvent, \
     CullingBoar
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

    def test_add_ws_piglets_culling_data(self):
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

        with freeze_time("2020-06-5"):
            for p in Piglets.objects.all():
                CullingPiglets.objects.create_culling_piglets(
                    piglets_group=p, culling_type='padej', total_weight=10)

        with freeze_time("2020-06-7"):
            for p in Piglets.objects.all():
                CullingPiglets.objects.create_culling_piglets(
                    piglets_group=p, culling_type='prirezka', total_weight=10)

        with freeze_time("2020-06-10"):
            for p in Piglets.objects.all():
                CullingPiglets.objects.create_culling_piglets(
                    piglets_group=p, culling_type='vinuzhd', total_weight=10)

        rds = ReportDate.objects.all().add_ws_piglets_culling_data(ws_locs=self.ws4_locs)

        day0_rd = rds.filter(date=date(2020, 6, 3)).first()
        self.assertEqual(day0_rd.padej_qnty, None)
        self.assertEqual(day0_rd.padej_total_weight, None)
        self.assertEqual(day0_rd.prirezka_qnty, None)
        self.assertEqual(day0_rd.prirezka_total_weight, None)
        self.assertEqual(day0_rd.vinuzhd_qnty, None)
        self.assertEqual(day0_rd.vinuzhd_total_weight, None)

        day1_rd = rds.filter(date=date(2020, 6, 5)).first()
        self.assertEqual(day1_rd.padej_qnty, 3)
        self.assertEqual(day1_rd.padej_total_weight, 30)
        self.assertEqual(day1_rd.prirezka_qnty, None)
        self.assertEqual(day1_rd.prirezka_total_weight, None)
        self.assertEqual(day1_rd.vinuzhd_qnty, None)
        self.assertEqual(day1_rd.vinuzhd_total_weight, None)
    
    def test_add_ws_piglets_trs_in_out(self):
        piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(
            tour=self.tour1, location=self.loc_ws3_cells[0], quantity=10)
        piglets2 = piglets_testing.create_new_group_with_metatour_by_one_tour(
            tour=self.tour1, location=self.loc_ws3_cells[1], quantity=10)
        piglets3 = piglets_testing.create_new_group_with_metatour_by_one_tour(
            tour=self.tour1, location=self.loc_ws3_cells[2], quantity=10)
        piglets4 = piglets_testing.create_new_group_with_metatour_by_one_tour(
            tour=self.tour1, location=self.loc_ws3_cells[3], quantity=20)

        with freeze_time("2020-06-3"):
            for p in Piglets.objects.filter(pk__in=[piglets1.pk, piglets2.pk, piglets3.pk]):
                PigletsTransaction.objects.create_transaction(
                    piglets_group=p, to_location=self.loc_ws4)
                WeighingPiglets.objects.create_weighing(
                    piglets_group=p, total_weight=100, place='3/4')

        with freeze_time("2020-06-6"):
            PigletsTransaction.objects.create_transaction(
                    piglets_group=piglets4, to_location=self.loc_ws4)

        with freeze_time("2020-06-10"):
            piglets1.refresh_from_db()
            piglets2.refresh_from_db()
            PigletsTransaction.objects.create_transaction(
                    piglets_group=piglets1, to_location=self.loc_ws8)
            PigletsTransaction.objects.create_transaction(
                    piglets_group=piglets2, to_location=self.loc_ws8)

        rds = ReportDate.objects.all().add_ws_piglets_trs_in_out(ws_locs=self.ws4_locs)

        day0_rd = rds.filter(date=date(2020, 6, 3)).first()
        self.assertEqual(day0_rd.tr_in_qnty, 30)
        self.assertEqual(day0_rd.tr_out_qnty, None)

        day1_rd = rds.filter(date=date(2020, 6, 6)).first()
        self.assertEqual(day1_rd.tr_in_qnty, 20)
        self.assertEqual(day1_rd.tr_out_qnty, None)

        day2_rd = rds.filter(date=date(2020, 6, 10)).first()
        self.assertEqual(day2_rd.tr_in_qnty, None)
        self.assertEqual(day2_rd.tr_out_qnty, 20)

        day3_rd = rds.filter(date=date(2020, 6, 12)).first()
        self.assertEqual(day3_rd.tr_in_qnty, None)
        self.assertEqual(day3_rd.tr_out_qnty, None)


class ReportDateWS12ReportTest(TransactionTestCase):
    def setUp(self):
        locations_testing.create_workshops_sections_and_cells()
        sows_testings.create_statuses()
        sows_events_testings.create_types()
        piglets_testing.create_piglets_statuses()

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

    def test_add_count_sows_ws12(self):
        for sow in Sow.objects.all()[:50]:
            SowTransaction.objects.create_transaction(sow=sow, to_location=self.loc1,
             date=date(2020, 5, 20))

        self.assertEqual(Sow.objects.filter(location__workshop__number=1).count(), 50)
        self.assertEqual(Sow.objects.filter(location__workshop__number=2).count(), 50)

        Sow.objects.filter(location__workshop__number=2).update(location=self.loc3)

        for sow1 in Sow.objects.filter(location__workshop__number=1)[:17]:
            SowTransaction.objects.create_transaction(sow=sow1, to_location=self.loc2,
             date=date(2020, 6, 15))

        for sow3 in Sow.objects.filter(location__workshop__number=3)[:20]:
            SowTransaction.objects.create_transaction(sow=sow3, to_location=self.loc1,
             date=date(2020, 7, 5))

        sows_qs = Sow.objects.filter(pk__in=Sow.objects.filter(location__workshop__number=1) \
                .values_list('pk', flat=True)[:5])
        CullingSow.objects.mass_culling(sows_qs=sows_qs, culling_type='padej', date=date(2020, 7, 10))

        sows_qs = Sow.objects.filter(pk__in=Sow.objects.filter(location__workshop__number=2) \
                .values_list('pk', flat=True)[:15])
        CullingSow.objects.mass_culling(sows_qs=sows_qs, culling_type='padej', date=date(2020, 7, 10))

        rds = ReportDate.objects.all().add_count_sows_ws12(ws_number=1)
        self.assertEqual(rds.filter(date=date(2020, 5, 4)).first().ws1_count_sows, 0)
        self.assertEqual(rds.get(date=date(2020, 5, 5)).ws1_count_sows, 0)
        self.assertEqual(rds.get(date=date(2020, 5, 6)).ws1_count_sows, 0)
        self.assertEqual(rds.get(date=date(2020, 5, 20)).ws1_count_sows, 0)
        self.assertEqual(rds.get(date=date(2020, 5, 21)).ws1_count_sows, 50)
        self.assertEqual(rds.get(date=date(2020, 5, 25)).ws1_count_sows, 50)
        self.assertEqual(rds.get(date=date(2020, 6, 25)).ws1_count_sows, 33)
        self.assertEqual(rds.get(date=date(2020, 7, 10)).ws1_count_sows, 53)
        self.assertEqual(rds.get(date=date(2020, 7, 11)).ws1_count_sows, 48)
        self.assertEqual(rds.get(date=date(2020, 9, 25)).ws1_count_sows, 48)

    def test_add_count_boars(self):
        with freeze_time("2020-01-3"):
            sows_testings.create_boar()

        with freeze_time("2020-04-3"):
            sows_testings.create_boar()

        with freeze_time("2020-05-3"):
            sows_testings.create_boar()

        with freeze_time("2020-06-3"):
            sows_testings.create_boar()

        rds = ReportDate.objects.all().add_count_boars()
        self.assertEqual(rds.get(date=date(2020, 1, 1)).count_boars, 0)
        self.assertEqual(rds.get(date=date(2020, 1, 3)).count_boars, 0)
        self.assertEqual(rds.get(date=date(2020, 1, 4)).count_boars, 1)
        self.assertEqual(rds.get(date=date(2020, 4, 4)).count_boars, 2)
        self.assertEqual(rds.get(date=date(2020, 5, 4)).count_boars, 3)
        self.assertEqual(rds.get(date=date(2020, 6, 4)).count_boars, 4)

        with freeze_time("2020-05-6"):
            boar = Boar.objects.all().first()
            CullingBoar.objects.create_culling_boar(boar=boar, culling_type='padej', reason=None)

        rds = ReportDate.objects.all().add_count_boars()
        self.assertEqual(rds.get(date=date(2020, 1, 1)).count_boars, 0)
        self.assertEqual(rds.get(date=date(2020, 1, 3)).count_boars, 0)
        self.assertEqual(rds.get(date=date(2020, 1, 4)).count_boars, 1)
        self.assertEqual(rds.get(date=date(2020, 4, 4)).count_boars, 2)
        self.assertEqual(rds.get(date=date(2020, 5, 4)).count_boars, 3)
        self.assertEqual(rds.get(date=date(2020, 5, 6)).count_boars, 3)
        self.assertEqual(rds.get(date=date(2020, 5, 7)).count_boars, 2)
        self.assertEqual(rds.get(date=date(2020, 6, 4)).count_boars, 3)

    def test_add_ws12_sow_cullings_data(self):
        for sow in Sow.objects.all()[:50]:
            SowTransaction.objects.create_transaction(sow=sow, to_location=self.loc1,
             date=date(2020, 5, 20))

        sows_ws1 = Sow.objects.filter(location__workshop__number=1)
        status1 = SowStatus.objects.get(title='Ожидает осеменения')

        # 30 rem 20 osn
        sows_ws1.filter(pk__in=sows_ws1.values_list('pk', flat=True)[:20]).update(status=status1)

        with freeze_time("2020-07-6"):
            sow_osn = sows_ws1.filter(status__title='Ожидает осеменения').first()
            CullingSow.objects.create_culling(sow=sow_osn, culling_type='padej', weight=200)

        with freeze_time("2020-07-7"):
            sow_osn = sows_ws1.filter(status__title='Ожидает осеменения').first()
            CullingSow.objects.create_culling(sow=sow_osn, culling_type='padej', weight=202)

            sow_rem = sows_ws1.filter(status__title='Ремонтная').first()
            CullingSow.objects.create_culling(sow=sow_rem, culling_type='vinuzhd', weight=203)

        with freeze_time("2020-07-17"):
            sow_rem = sows_ws1.filter(status__title='Ремонтная').first()
            CullingSow.objects.create_culling(sow=sow_rem, culling_type='padej', weight=204)

        with freeze_time("2020-08-10"):
            sow_osn = sows_ws1.filter(status__title='Ожидает осеменения').first()
            CullingSow.objects.create_culling(sow=sow_osn, culling_type='vinuzd', weight=205)

        rds = ReportDate.objects.all().add_ws12_sow_cullings_data(
            ws_locs=Location.objects.filter(workshop__number=1), ws_number=1)
        self.assertEqual(rds.get(date=date(2020, 1, 1)).ws1_padej_osn_count, None)
        self.assertEqual(rds.get(date=date(2020, 1, 1)).ws1_padej_osn_weight, None)
        self.assertEqual(rds.get(date=date(2020, 1, 1)).ws1_vinuzhd_osn_count, None)
        self.assertEqual(rds.get(date=date(2020, 1, 1)).ws1_vinuzhd_osn_weight, None)

        self.assertEqual(rds.get(date=date(2020, 1, 1)).ws1_padej_rem_count, None)
        self.assertEqual(rds.get(date=date(2020, 1, 1)).ws1_padej_rem_weight, None)
        self.assertEqual(rds.get(date=date(2020, 1, 1)).ws1_vinuzhd_rem_count, None)
        self.assertEqual(rds.get(date=date(2020, 1, 1)).ws1_vinuzhd_rem_weight, None)

        self.assertEqual(rds.get(date=date(2020, 7, 6)).ws1_padej_osn_count, 1)
        self.assertEqual(rds.get(date=date(2020, 7, 6)).ws1_padej_osn_weight, 200)
        self.assertEqual(rds.get(date=date(2020, 7, 6)).ws1_vinuzhd_osn_count, None)
        self.assertEqual(rds.get(date=date(2020, 7, 6)).ws1_vinuzhd_osn_weight, None)

        self.assertEqual(rds.get(date=date(2020, 7, 6)).ws1_padej_rem_count, None)
        self.assertEqual(rds.get(date=date(2020, 7, 6)).ws1_padej_rem_weight, None)
        self.assertEqual(rds.get(date=date(2020, 7, 6)).ws1_vinuzhd_rem_count, None)
        self.assertEqual(rds.get(date=date(2020, 7, 6)).ws1_vinuzhd_rem_weight, None)

        self.assertEqual(rds.get(date=date(2020, 7, 7)).ws1_padej_osn_count, 1)
        self.assertEqual(rds.get(date=date(2020, 7, 7)).ws1_padej_osn_weight, 202)
        self.assertEqual(rds.get(date=date(2020, 7, 7)).ws1_vinuzhd_osn_count, None)
        self.assertEqual(rds.get(date=date(2020, 7, 7)).ws1_vinuzhd_osn_weight, None)

        self.assertEqual(rds.get(date=date(2020, 7, 7)).ws1_padej_rem_count, None)
        self.assertEqual(rds.get(date=date(2020, 7, 7)).ws1_padej_rem_weight, None)
        self.assertEqual(rds.get(date=date(2020, 7, 7)).ws1_vinuzhd_rem_count, 1)
        self.assertEqual(rds.get(date=date(2020, 7, 7)).ws1_vinuzhd_rem_weight, 203)

        self.assertEqual(rds.get(date=date(2020, 7, 17)).ws1_padej_osn_count, None)
        self.assertEqual(rds.get(date=date(2020, 7, 17)).ws1_padej_osn_weight, None)
        self.assertEqual(rds.get(date=date(2020, 7, 17)).ws1_vinuzhd_osn_count, None)
        self.assertEqual(rds.get(date=date(2020, 7, 17)).ws1_vinuzhd_osn_weight, None)

        self.assertEqual(rds.get(date=date(2020, 7, 17)).ws1_padej_rem_count, 1)
        self.assertEqual(rds.get(date=date(2020, 7, 17)).ws1_padej_rem_weight, 204)
        self.assertEqual(rds.get(date=date(2020, 7, 17)).ws1_vinuzhd_rem_count, None)
        self.assertEqual(rds.get(date=date(2020, 7, 17)).ws1_vinuzhd_rem_weight, None)
        
    def test_add_culling_boar_data(self):
        for i in range(1, 10):
            sows_testings.create_boar()

        with freeze_time("2020-05-6"):
            boar = Boar.objects.all().first()
            CullingBoar.objects.create_culling_boar(boar=boar, culling_type='padej',
                reason=None, weight=100)

        with freeze_time("2020-05-10"):
            boar = Boar.objects.all().first()
            CullingBoar.objects.create_culling_boar(boar=boar, culling_type='padej',
                reason=None, weight=101)

        rds = ReportDate.objects.all().add_culling_boar_data()
        self.assertEqual(rds.get(date=date(2020, 1, 1)).padej_boar_count, None)
        self.assertEqual(rds.get(date=date(2020, 1, 1)).padej_boar_weight, None)

        self.assertEqual(rds.get(date=date(2020, 5, 6)).padej_boar_count, 1)
        self.assertEqual(rds.get(date=date(2020, 5, 6)).padej_boar_weight, 100)

        self.assertEqual(rds.get(date=date(2020, 5, 10)).padej_boar_count, 1)
        self.assertEqual(rds.get(date=date(2020, 5, 10)).padej_boar_weight, 101)

    def test_add_ws12_sow_trs_data(self):
        self.assertEqual(Sow.objects.filter(location__workshop__number=2).count(), 100)
        
        for sow1 in Sow.objects.all()[:17]:
            SowTransaction.objects.create_transaction(sow=sow1, to_location=self.loc1,
             date=date(2020, 6, 15))

        sows_ws1 = Sow.objects.filter(location__workshop__number=2)
        status1 = SowStatus.objects.get(title='Супорос 35')

        sows_ws1.filter(pk__in=sows_ws1.values_list('pk', flat=True)[:20]).update(status=status1)
        for sow1 in Sow.objects.filter(location__workshop__number=2)[:15]:
            SowTransaction.objects.create_transaction(sow=sow1, to_location=self.loc3,
             date=date(2020, 6, 25))

        rds = ReportDate.objects.all().add_ws12_sow_trs_data()
        self.assertEqual(rds.get(date=date(2020, 1, 1)).trs_from_1_to_2, None)
        self.assertEqual(rds.get(date=date(2020, 1, 1)).trs_from_1_to_3, None)
        self.assertEqual(rds.get(date=date(2020, 1, 1)).trs_from_2_to_1, None)
        self.assertEqual(rds.get(date=date(2020, 1, 1)).trs_from_3_to_1, None)
        self.assertEqual(rds.get(date=date(2020, 1, 1)).trs_from_3_to_2, None)
        self.assertEqual(rds.get(date=date(2020, 1, 1)).trs_from_2_to_3, None)

        self.assertEqual(rds.get(date=date(2020, 6, 15)).trs_from_1_to_2, None)
        self.assertEqual(rds.get(date=date(2020, 6, 15)).trs_from_1_to_3, None)
        self.assertEqual(rds.get(date=date(2020, 6, 15)).trs_from_2_to_1, 17)
        self.assertEqual(rds.get(date=date(2020, 6, 15)).trs_from_3_to_1, None)
        self.assertEqual(rds.get(date=date(2020, 6, 15)).trs_from_3_to_2, None)
        self.assertEqual(rds.get(date=date(2020, 6, 15)).trs_from_2_to_3, None)

        self.assertEqual(rds.get(date=date(2020, 6, 25)).trs_from_1_to_2, None)
        self.assertEqual(rds.get(date=date(2020, 6, 25)).trs_from_1_to_3, None)
        self.assertEqual(rds.get(date=date(2020, 6, 25)).trs_from_2_to_1, None)
        self.assertEqual(rds.get(date=date(2020, 6, 25)).trs_from_3_to_1, None)
        self.assertEqual(rds.get(date=date(2020, 6, 25)).trs_from_3_to_2, None)
        self.assertEqual(rds.get(date=date(2020, 6, 25)).trs_from_2_to_3, 15)

        self.assertEqual(rds.get(date=date(2020, 5, 5)).trs_from_otkorm_to_2, 100)
        self.assertEqual(
            SowTransaction.objects.filter(from_location__pigletsGroupCell__isnull=False).count(), 100)

    def test_ws12_aggregate_total(self):
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

        ws1_locs = Location.objects.all().get_workshop_location_by_number(workshop_number=1)
        rds = ReportDate.objects.all() \
                    .add_count_sows_ws12(ws_number=1) \
                    .add_count_boars() \
                    .add_ws12_sow_cullings_data(ws_locs=ws1_locs, ws_number=1) \
                    .add_culling_boar_data() \
                    .add_ws12_sow_trs_data() 

        total_data = rds.ws12_aggregate_total(ws_number=1)

        self.assertEqual(total_data['total_trs_from_2_to_1'], 37)
        self.assertEqual(total_data['total_padej_osn_count'], 7)
        self.assertEqual(total_data['total_padej_osn_weight'], 700)
        self.assertEqual(total_data['total_padej_rem_count'], 2)
        self.assertEqual(total_data['total_padej_rem_weight'], 202)

        self.assertEqual(total_data['total_padej_boar_count'], None)
        self.assertEqual(total_data['total_padej_boar_weight'], None)
        self.assertEqual(total_data['total_vinuzhd_rem_count'], None)
        self.assertEqual(total_data['total_vinuzhd_rem_weight'], None)
