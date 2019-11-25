# -*- coding: utf-8 -*-
from django.test import TestCase, TransactionTestCase
from django.core.exceptions import ValidationError

from piglets.models import Piglets
from tours.models import Tour
from locations.models import Location

import locations.testing_utils as locations_testing
import piglets.testing_utils as piglets_testing


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
   