# -*- coding: utf-8 -*-
from datetime import timedelta, date

from django.utils import timezone
from django.db import models
from django.test import TestCase, TransactionTestCase
from django.core.exceptions import ValidationError

from reports.models import ReportDate
from sows.models import Sow
from sows_events.models import CullingSow, SowFarrow
from piglets.models import Piglets
from piglets_events.models import CullingPiglets
from tours.models import Tour
from locations.models import Location
from transactions.models import PigletsTransaction

from piglets.serializers import PigletsSerializer

import locations.testing_utils as locations_testing
import piglets.testing_utils as piglets_testing
import sows.testing_utils as sows_testings
import sows_events.utils as sows_events_testings


class ReportDateTest(TransactionTestCase):
    def test_create_bulk_if_none_from_range(self):
        start_date = date(2020, 1, 1)
        end_date = timezone.now().date()

        ReportDate.objects.create_bulk_if_none_from_range(start_date, end_date)
        current_rds = ReportDate.objects.all()
        current_rds_count = ReportDate.objects.all().count()
        self.assertEqual(current_rds.count() > 0, True)

        # get_exist_from_range
        end_date2 = timezone.now().date() - timedelta(10)
        range_rds = ReportDate.objects.get_exist_from_range(start_date, end_date2)
        self.assertEqual(current_rds.count() - range_rds.count(), 10)


        end_date3 = timezone.now().date() + timedelta(10)
        range_rds2 = ReportDate.objects.get_exist_from_range(start_date, end_date3)
        self.assertEqual(current_rds.count(), range_rds2.count())

        ReportDate.objects.create_bulk_if_none_from_range(start_date, end_date3)
        current_rds2 = ReportDate.objects.all()
        self.assertEqual(current_rds2.count() - current_rds_count, 10)


class ReportDateSowQsTest(TransactionTestCase):
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

    def test_add_today_sows_qnty(self):
        # init 10 sows
        for i in range(0, 20):
            sows_testings.create_sow_with_location(self.loc_ws1)

        for i in range(0, 5):
            sow = Sow.objects.all()[i]
            CullingSow.objects.create_culling(sow, 'padej')

        past_date = timezone.now().date() - timedelta(10)
        for i in range(6, 9):
            sow = Sow.objects.all()[i]
            CullingSow.objects.create_culling(sow=sow, culling_type='padej', date=past_date)
        
        with self.assertNumQueries(1):
            rds = ReportDate.objects.all() \
                        .add_sow_padej_qnty() \
                        .add_sow_vinuzhd_qnty() \
                        .add_today_sows_qnty()
            self.assertEqual(rds[0].today_start_sows_qnty, 17)

    def test_add_sows_quantity_at_date(self):
        # init 10 sows
        for i in range(0, 20):
            sows_testings.create_sow_with_location(self.loc_ws1)

        for i in range(0, 5):
            sow = Sow.objects.all()[i]
            CullingSow.objects.create_culling(sow=sow, culling_type='padej',
                 date=timezone.now().date())

        past_date = timezone.now().date() - timedelta(10)
        for i in range(6, 9):
            sow = Sow.objects.all()[i]
            CullingSow.objects.create_culling(sow=sow, culling_type='padej', date=past_date)

        start_date = date(2020, 4, 20)
        end_date = timezone.now().date()

        culls = CullingSow.objects.filter(date__date__range=(start_date, end_date),
         culling_type='padej') \
            .values('culling_type') \
            .annotate(cnt=models.Count('pk')) \
            .values('cnt')[:1]

        self.assertEqual(culls[0]['cnt'], 5)
        
        start_date = date(2020, 1, 1)
        end_date = date(2020, 1, 2)
        culls = CullingSow.objects.filter(date__date__range=(start_date, end_date),
         culling_type='padej') \
            .values('culling_type') \
            .annotate(cnt=models.Count('pk')) \
            .values('cnt')

        self.assertEqual(culls.count(), 0)

        start_date = date(2020, 1, 1)
        end_date = timezone.now().date()
        culls = CullingSow.objects.filter(date__date__range=(start_date, end_date),
         culling_type='padej') \
            .values('culling_type') \
            .annotate(cnt=models.Count('pk')) \
            .values('cnt')
            
        self.assertEqual(culls[0]['cnt'], 8)
        
        with self.assertNumQueries(3):
            rds = ReportDate.objects.all() \
                    .add_sow_padej_qnty() \
                    .add_sow_vinuzhd_qnty() \
                    .add_today_sows_qnty() \
                    .add_sows_quantity_at_date_start() \
                    .add_sows_quantity_at_date_end()
            bool(rds)
            self.assertEqual(rds[0].today_start_sows_qnty, 17)
            self.assertEqual(rds[0].today_padej_subquery, 5)
            self.assertEqual(rds[0].today_vinuzhd_subquery, 0)
            self.assertEqual(rds[0].sow_qnty_at_date_start, 20)
            self.assertEqual(rds[0].sow_padej_qnty, 0)
            self.assertEqual(rds[0].sow_vinuzhd_qnty, 0)
            self.assertEqual(rds[0].sows_quantity_at_date_end, 20)

            # print('RD')
            # rd = rds.order_by('-date').first()
            # print(rd)
            # print('today_start_sows_qnty', rd.today_start_sows_qnty, 17)
            # print('today_padej_subquery', rd.today_padej_subquery, 5)
            # print('today_vinuzhd_subquery', rd.today_vinuzhd_subquery, 0)
            # print('sow_qnty_at_date_start', rd.sow_qnty_at_date_start, 17)
            # print('cnt_padej_subquery_from_date', rd.cnt_padej_subquery_from_date, 3)
            # print('cnt_vinuzhd_subquery_from_date', rd.cnt_vinuzhd_subquery_from_date, 0)
            # print('cnt_padej_subquery_at_end_date', rd.cnt_padej_subquery_at_end_date, 5)
            # print('cnt_vinuzhd_subquery_at_end_date', rd.cnt_vinuzhd_subquery_at_end_date, 0)
            # print('sows_quantity_at_date_end', rd.sows_quantity_at_date_end, 12)
            # print('__________________________')

            rd_yesterday = rds.order_by('-date')[1]
            self.assertEqual(rd_yesterday.today_start_sows_qnty, 17)
            self.assertEqual(rd_yesterday.today_padej_subquery, 5)
            self.assertEqual(rd_yesterday.today_vinuzhd_subquery, 0)

            self.assertEqual(rd_yesterday.sow_qnty_at_date_start, 17)
            self.assertEqual(rd_yesterday.sow_padej_qnty, 0)
            self.assertEqual(rd_yesterday.sow_vinuzhd_qnty, 0)
            self.assertEqual(rd_yesterday.sows_quantity_at_date_end, 17)
           
            past_culling_date = timezone.now().date() - timedelta(10)
            rd_past_culling_date = rds.filter(date=past_culling_date).first()
            self.assertEqual(rd_past_culling_date.today_start_sows_qnty, 17)
            self.assertEqual(rd_past_culling_date.today_padej_subquery, 5)
            self.assertEqual(rd_past_culling_date.today_vinuzhd_subquery, 0)

            self.assertEqual(rd_past_culling_date.sow_qnty_at_date_start, 20)
            self.assertEqual(rd_past_culling_date.sow_padej_qnty, 3)
            self.assertEqual(rd_past_culling_date.sow_vinuzhd_qnty, 0)
            self.assertEqual(rd_past_culling_date.sows_quantity_at_date_end, 17)


class ReportDatePigletsQsTest(TransactionTestCase):
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

    def test_add_piglets_today_quantity_v1(self):
        # not cullings and farrows today
        for i in range(0, 20):
            piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1, self.loc_ws1, 10)

        with self.assertNumQueries(1):
            rds = ReportDate.objects.all() \
                    .add_piglets_today_quantity()
            bool(rds)
            self.assertEqual(rds[0].piglets_today_qnty,  200)

    def test_add_piglets_today_quantity_v2(self):
        # cullings and farrows today
        for i in range(0, 20):
            piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1, self.loc_ws1, 10)

        piglets = Piglets.objects.all()
        for i in range(0, 5):
            CullingPiglets.objects.create_culling_piglets(piglets_group=piglets[i],
             culling_type='padej', quantity=2)

        self.assertEqual(CullingPiglets.objects.all().count(), 5)
        self.assertEqual(CullingPiglets.objects.all() \
            .aggregate(qnty=models.Sum('quantity'))['qnty'], 10)


        sow = sows_testings.create_sow_with_semination_usound(self.loc_ws3_cells[0])
        SowFarrow.objects.create_sow_farrow(sow=sow, alive_quantity=15)

        self.assertEqual(piglets.aggregate(qnty=models.Sum('quantity'))['qnty'], 205)

        with self.assertNumQueries(1):
            rds = ReportDate.objects.all() \
                    .add_piglets_today_quantity()
            bool(rds)
            # 205 + 10 - 15
            self.assertEqual(rds[0].piglets_today_qnty,  200)

    def test_add_piglets_target_date_quantity_v3(self):
        # calc at date
        for i in range(0, 20):
            piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1, self.loc_ws1, 10)

        piglets = Piglets.objects.all()
        for i in range(0, 5):
            CullingPiglets.objects.create_culling_piglets(piglets_group=piglets[i],
             culling_type='padej', quantity=2)

        sow = sows_testings.create_sow_with_semination_usound(self.loc_ws3_cells[0])
        SowFarrow.objects.create_sow_farrow(sow=sow, alive_quantity=15)

        past_date = timezone.now().date() - timedelta(10)
        for i in range(6, 9):
            CullingPiglets.objects.create_culling_piglets(piglets_group=piglets[i],
             culling_type='padej', quantity=2, date=past_date)

        target_date = timezone.now().date() - timedelta(5)
        sow2 = sows_testings.create_sow_with_semination_usound(self.loc_ws3_cells[1])
        SowFarrow.objects.create_sow_farrow(sow=sow2, alive_quantity=13, date=target_date)

        with self.assertNumQueries(1):
            rds = ReportDate.objects.all() \
                    .add_piglets_padej_qnty() \
                    .add_piglets_prirezka_qnty() \
                    .add_piglets_vinuzhd_qnty() \
                    .add_piglets_spec_qnty() \
                    .add_born_alive() \
                    .add_piglets_today_quantity() \
                    .add_piglets_quantity_at_date_start() \
                    .add_piglets_quantity_at_date_end() \
                    .filter(date=target_date)
            bool(rds)
            self.assertEqual(rds[0].piglets_today_qnty,  207)
            self.assertEqual(rds[0].piglets_qnty_start_date,  194)
            self.assertEqual(rds[0].piglets_qnty_start_end,  207)

    def test_add_piglets_target_date_quantity_v4(self):
        # calc at date
        for i in range(0, 20):
            piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1, self.loc_ws1, 10)

        piglets = Piglets.objects.all()
        for i in range(0, 5):
            CullingPiglets.objects.create_culling_piglets(piglets_group=piglets[i],
             culling_type='padej', quantity=2)

        sow = sows_testings.create_sow_with_semination_usound(self.loc_ws3_cells[0])
        SowFarrow.objects.create_sow_farrow(sow=sow, alive_quantity=15)

        past_date = timezone.now().date() - timedelta(10)
        for i in range(6, 9):
            CullingPiglets.objects.create_culling_piglets(piglets_group=piglets[i],
             culling_type='padej', quantity=2, date=past_date)

        target_date = timezone.now().date() - timedelta(5)
        sow2 = sows_testings.create_sow_with_semination_usound(self.loc_ws3_cells[1])
        SowFarrow.objects.create_sow_farrow(sow=sow2, alive_quantity=13, date=target_date)

        CullingPiglets.objects.create_culling_piglets(piglets_group=piglets[0],
             culling_type='spec', quantity=4, date=target_date, total_weight=43)
        CullingPiglets.objects.create_culling_piglets(piglets_group=piglets[1],
             culling_type='spec', quantity=3, date=target_date, total_weight=32)

        with self.assertNumQueries(1):
            rds = ReportDate.objects.all() \
                    .add_piglets_padej_qnty() \
                    .add_piglets_prirezka_qnty() \
                    .add_piglets_vinuzhd_qnty() \
                    .add_piglets_spec_qnty() \
                    .add_piglets_spec_total_weight() \
                    .add_born_alive() \
                    .add_piglets_today_quantity() \
                    .add_piglets_quantity_at_date_start() \
                    .add_piglets_quantity_at_date_end() \
                    .filter(date=target_date)
            bool(rds)
            self.assertEqual(rds[0].piglets_today_qnty,  200)
            self.assertEqual(rds[0].piglets_qnty_start_date,  194)
            self.assertEqual(rds[0].piglets_qnty_start_end,  200)
            self.assertEqual(rds[0].piglets_spec_total_weight,  75)
            self.assertEqual(rds[0].piglets_spec_qnty,  7)

    def test_add_priplod_by_sow(self):
        for i in range(0, 5):
            sow = sows_testings.create_sow_with_semination_usound(self.loc_ws3_cells[i])
            SowFarrow.objects.create_sow_farrow(sow=sow, alive_quantity=(10 + i))

        with self.assertNumQueries(1):
            rds = ReportDate.objects.all() \
                    .add_born_alive() \
                    .add_priplod_by_sow() \
                    .order_by('-date')
            bool(rds)
            self.assertEqual(rds[0].born_alive,  60)
            self.assertEqual(rds[0].priplod_by_sow,  12)

    def test_add_piglets_qnty_in_transactions(self):
        for i in range(0, 20):
            piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1, self.loc_ws1,
             10)

        piglets = Piglets.objects.all()
        for i in range(0, 10):
            PigletsTransaction.objects.create_transaction(self.loc_ws3, piglets[i])

        with self.assertNumQueries(1):
            rds = ReportDate.objects.all() \
                    .add_piglets_qnty_in_transactions() \
                    .order_by('-date')
            bool(rds)
            self.assertEqual(rds[0].piglets_transfered,  100)


class ReportCurrentDataTest(TransactionTestCase):
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

    def test_add_today_rep_sows_count(self):
        # not cullings and farrows today
        