# -*- coding: utf-8 -*-
from django.test import TestCase, TransactionTestCase

import piglets.models as piglets_models
import tours.models as tours_models
import locations.models as locations_models

import locations.testing_utils as locations_testing
import piglets.testing_utils as piglets_testing


class PigletsModelManagerQuerysetTest(TestCase):
    def setUp(self):
        locations_testing.create_workshops_sections_and_cells()

    def test_create_new_group_with_metatour_by_one_tour(self):
        tour = tours_models.Tour.objects.get_or_create_by_week_in_current_year(1)
        location = locations_models.Location.objects.get(section__number=1, section__workshop__number=3)
        piglets = piglets_testing.create_new_group_with_metatour_by_one_tour(tour, location, 10)
        record = piglets.metatour.records.first()

        self.assertEqual(record.tour, tour)
        self.assertEqual(record.quantity, 10)
        self.assertEqual(record.percentage, 100.0)
        
       