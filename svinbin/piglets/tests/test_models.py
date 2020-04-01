# -*- coding: utf-8 -*-
from django.test import TestCase, TransactionTestCase
from django.core.exceptions import ValidationError

from piglets.models import Piglets
from tours.models import Tour
from locations.models import Location

from piglets.serializers import PigletsSerializer

import locations.testing_utils as locations_testing
import piglets.testing_utils as piglets_testing
import sows.testing_utils as sows_testings
import sows_events.utils as sows_events_testings


class PigletsModelTest(TestCase):
    def setUp(self):
        locations_testing.create_workshops_sections_and_cells()
        piglets_testing.create_piglets_statuses()

        self.tour1 = Tour.objects.get_or_create_by_week_in_current_year(week_number=1)
        self.tour2 = Tour.objects.get_or_create_by_week_in_current_year(week_number=2)
        self.loc_ws3 = Location.objects.get(workshop__number=3)
        self.piglets = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws3, 101)
        self.piglets.gilts_quantity = 10
        self.piglets.save()

        self.piglets2 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour2,
            self.loc_ws3, 232)

    def test_deactivate(self):
        self.piglets.deactivate()
        self.assertEqual(self.piglets.active, False)

    def test_remove_piglets(self):
        self.piglets.remove_piglets(1)
        self.assertEqual(self.piglets.quantity, 100)

    def test_remove_gilts(self):
        self.piglets.remove_gilts(1)
        self.assertEqual(self.piglets.quantity, 100)
        self.assertEqual(self.piglets.gilts_quantity, 9)

    def test_change_status_to(self):
        self.piglets.change_status_to('Родились, кормятся')
        self.assertEqual(self.piglets.status.title, 'Родились, кормятся')


class PigletsModelmanagerTest(TestCase):
    def setUp(self):
        locations_testing.create_workshops_sections_and_cells()
        piglets_testing.create_piglets_statuses()

        self.tour1 = Tour.objects.get_or_create_by_week_in_current_year(week_number=1)
        self.tour2 = Tour.objects.get_or_create_by_week_in_current_year(week_number=2)
        self.loc_ws3 = Location.objects.get(workshop__number=3)
        self.piglets = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws3, 101)
        self.piglets.gilts_quantity = 10
        self.piglets.save()

        self.piglets2 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour2,
            self.loc_ws3, 232)
        
    def test_manager_get_total_quantity(self):
        total = Piglets.objects.all().get_total_quantity()
        self.assertEqual(total, 333)

    def test_manager_get_total_gilts_quantity(self):
        total_gilts = Piglets.objects.all().get_total_gilts_quantity()
        self.assertEqual(total_gilts, 10)

    def test_init_piglets_with_metatour(self):
        piglets = Piglets.objects.init_piglets_with_metatour(self.tour1, self.loc_ws3, 100, 5)
        self.assertEqual(piglets.quantity, 100)
        self.assertEqual(piglets.gilts_quantity, 5)
        self.assertEqual(piglets.location, self.loc_ws3)

        self.assertEqual(piglets.metatour.records.all().count(), 1)
        self.assertEqual(piglets.metatour.records.all().first().tour, self.tour1)

    def test_init_piglets_by_week(self):
        piglets = Piglets.objects.init_piglets_by_week(week=5, location=self.loc_ws3,
         quantity=100, gilts_quantity=10)
        self.assertEqual(piglets.metatour.records.all().first().tour.week_number, 5)

    def test_init_piglets_by_farrow_date(self):
        piglets = Piglets.objects.init_piglets_by_farrow_date(farrow_date='2019-12-31', location=self.loc_ws3,
         quantity=100, gilts_quantity=10)
        self.assertEqual(piglets.quantity, 100)
        self.assertEqual(piglets.gilts_quantity, 10)        
        self.assertEqual(piglets.metatour.records.all().first().tour.week_number, 33)


class PigletsQueryTest(TransactionTestCase):
    def setUp(self):
        locations_testing.create_workshops_sections_and_cells()
        sows_testings.create_statuses()
        sows_events_testings.create_types()
        piglets_testing.create_piglets_statuses()

        location_cell1 = Location.objects.filter(sowAndPigletsCell__section__number=1)[0]
        piglets1 = piglets_testing.create_from_sow_farrow_by_week(location=location_cell1,
            week=1)

        location_cell2 = Location.objects.filter(sowAndPigletsCell__section__number=1)[1]
        piglets1 = piglets_testing.create_from_sow_farrow_by_week(location=location_cell2,
            week=1)

        location_cell3 = Location.objects.filter(sowAndPigletsCell__section__number=1)[2]
        piglets1 = piglets_testing.create_from_sow_farrow_by_week(location=location_cell3,
            week=2)

    def test_queryset_serializer(self):
        with self.assertNumQueries(4):
            data = Piglets.objects.all() \
                .prefetch_related('metatour__records__tour__sowfarrow_set') 
            serializer = PigletsSerializer(data, many=True)
            serializer.data

    def test_with_tour(self):
        
        self.assertEqual(Piglets.objects.all().with_tour(tour_week=1).count())
