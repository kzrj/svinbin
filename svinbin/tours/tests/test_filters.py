# -*- coding: utf-8 -*-
import datetime

from django.test import TestCase
from tours.models import Tour

import locations.testing_utils as locations_testing
import sows.testing_utils as pigs_testings
import sows_events.utils as sows_events_testing
import piglets.testing_utils as piglets_testing

from piglets_events.models import CullingPiglets, WeighingPiglets
from locations.models import Location

from tours import filters


class TourFiltersTest(TestCase):
    def setUp(self):
        locations_testing.create_workshops_sections_and_cells()
        pigs_testings.create_statuses()
        sows_events_testing.create_types()
        piglets_testing.create_piglets_statuses()

        self.tour1 = Tour.objects.get_or_create_by_week_in_current_year(week_number=1)
        self.tour2 = Tour.objects.get_or_create_by_week_in_current_year(week_number=2)
        self.tour3 = Tour.objects.get_or_create_by_week_in_current_year(week_number=3)

        self.loc_ws4 = Location.objects.get(workshop__number=4)
        self.loc_ws5_cells = Location.objects.filter(pigletsGroupCell__workshop__number=5)
        self.loc_ws3_cells = Location.objects.filter(sowAndPigletsCell__workshop__number=3)

    def test_filter_has_weights_in_range(self):
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
            tour=self.tour3,
            location=self.loc_ws5_cells[0],
            quantity=100,
            birthday=datetime.datetime(2020,5,5,0,0))
        piglets4 = piglets_testing.create_new_group_with_metatour_by_one_tour(
            tour=self.tour3,
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

        qs = Tour.objects.all().add_weighing_first_dates()
        # print(qs[0].first_date_3_4)

        f = filters.TourFilter({
            'has_weights_in_range_after': '2020-09-01',
            'has_weights_in_range_before': '2020-10-01'
            }, queryset=qs)
        self.assertEqual(f.qs.count(), 1)
        self.assertEqual(f.qs.first().week_number, 1)

        f = filters.TourFilter({
            'has_weights_in_range_after': '2020-12-01',
            'has_weights_in_range_before': '2020-12-10'
            }, queryset=qs)
        self.assertEqual(f.qs.count(), 1)
        self.assertEqual(f.qs.first().week_number, 3)
   
    def test_filter_has_weights_in_ws(self):
        piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(
            tour=self.tour1,
            location=self.loc_ws4,
            quantity=100,
            birthday=datetime.datetime(2020,5,5,0,0)
            )
        piglets2 = piglets_testing.create_new_group_with_metatour_by_one_tour(
            tour=self.tour2,
            location=self.loc_ws4,
            quantity=100,
            birthday=datetime.datetime(2020,5,8,0,0)
            )
        piglets3 = piglets_testing.create_new_group_with_metatour_by_one_tour(
            tour=self.tour3,
            location=self.loc_ws4,
            quantity=100,
            birthday=datetime.datetime(2020,5,8,0,0)
            )

        WeighingPiglets.objects.create_weighing(piglets_group=piglets1, total_weight=120,
            place='8/5', date=datetime.datetime.today())
        WeighingPiglets.objects.create_weighing(piglets_group=piglets2, total_weight=150,
            place='8/6', date=datetime.datetime(2020,9,25,0,0))
        WeighingPiglets.objects.create_weighing(piglets_group=piglets3, total_weight=120,
            place='8/5', date=datetime.datetime.today())

        qs = Tour.objects.all()

        f = filters.TourFilter({'has_weights_in_ws': '8/5'}, queryset=qs)
        self.assertEqual(f.qs.count(), 2)
        self.assertTrue(f.qs[0].week_number in [1,3])
        self.assertTrue(f.qs[1].week_number in [1,3])