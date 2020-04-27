# -*- coding: utf-8 -*-
from datetime import timedelta, date

from django.utils import timezone
from django.db import models
from django.test import TestCase, TransactionTestCase
from django.core.exceptions import ValidationError

from reports.models import ReportDate
from sows.models import Sow
from sows_events.models import CullingSow
from piglets.models import Piglets
from tours.models import Tour
from locations.models import Location

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

        
class ReportDateQsTest(TransactionTestCase):
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
            rds = ReportDate.objects.all().add_today_sows_qnty()
            self.assertEqual(rds[0].today_sows_qnty, 17)

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

        start_date = date(2020, 4, 15)
        end_date = timezone.now().date()

        culls = CullingSow.objects.filter(date__date__range=(start_date, end_date),
         culling_type='padej') \
            .values('culling_type') \
            .annotate(cnt=models.Count('pk')) \
            .values('cnt')[:1]

        print(culls.first(), 5)
        print(culls.first()['cnt'], 5)
        print(culls, 5)
        # self.assertEqual(culls.first()['cnt'], 5)

        start_date = date(2020, 1, 1)
        end_date = date(2020, 1, 2)
        end_date = timezone.now().date()

        culls = CullingSow.objects.filter(date__date__range=(start_date, end_date),
         culling_type='padej') \
            .values('culling_type') \
            .annotate(cnt=models.Count('pk')) \
            .values('cnt')
        # self.assertEqual(culls[:1]['cnt'], 0)
        


        # with self.assertNumQueries(3):
        #     rds = ReportDate.objects.all() \
        #             .add_today_sows_qnty() \
        #             .add_sows_quantity_at_date_start() \
        #             .add_sows_quantity_at_date_end()
        #     bool(rds)
        #     print(rds[0])
        #     print(rds.order_by('-date')[0])
        #     print(timezone.now().date())
        #     rd = rds.filter(date=timezone.now().date() - timedelta(5)).first()
        #     print('RD')
        #     print(rd)
        #     print(rd.sow_qnty_at_date_start, 20)
        #     print(rd.sows_quantity_at_date_end, 17)
        #     print(rd.cnt_padej_subquery_from_date, 17)
        #     print(rd.cnt_vinuzhd_subquery_from_date, 17)
        #     print(rd.cnt_padej_subquery_at_end_date, 17)
        #     print(rd.cnt_vinuzhd_subquery_at_end_date, 17)
        #     print('__________________________')

        #     print('rds[0]')
        #     print(rds[0].sow_qnty_at_date_start, 20)
        #     print(rds[0].sows_quantity_at_date_end, 17)
        #     print(rds[0].cnt_padej_subquery_from_date, 17)
        #     print(rds[0].cnt_vinuzhd_subquery_from_date, 17)
        #     print(rds[0].cnt_padej_subquery_at_end_date, 17)
        #     print(rds[0].cnt_vinuzhd_subquery_at_end_date, 17)

            # self.assertEqual(rds[0].sow_qnty_at_date_start, 20)
            # self.assertEqual(rds[0].sows_quantity_at_date_end, 17)
    # 