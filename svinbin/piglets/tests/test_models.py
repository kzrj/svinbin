# -*- coding: utf-8 -*-
from django.test import TestCase

import sows.models as sows_models
import piglets.models as piglets_models

import locations.testing_utils as locations_testing
import sows.testing_utils as sows_testing
import piglets.testing_utils as piglets_testing


class NewBornModelManagerTest(TestCase):
    def setUp(self):
        locations_testing.create_workshops_sections_and_cells()
        sows_testing.create_statuses()

    def test_groups_with_gilts(self):
        new_born_group1 = piglets_testing.create_new_born_group(cell_number=5)
        sow1 = new_born_group1.farrows.first().sow
        gilt1 = sows_models.Gilt.objects.create_gilt(1, sow1)
        new_born_group1.refresh_from_db()
        
        new_born_group2 = piglets_testing.create_new_born_group(cell_number=6)
        sow2 = new_born_group2.farrows.first().sow
        gilt2 = sows_models.Gilt.objects.create_gilt(2, sow2)

        new_born_group3 = piglets_testing.create_new_born_group(cell_number=4)

        self.assertEqual(piglets_models.NewBornPigletsGroup.objects.groups_with_gilts().count(), 2)
        self.assertEqual(piglets_models.NewBornPigletsGroup.objects.all().count(), 3)


# class NomadPigletsModelManagerTest(TestCase):
#     def setUp(self):
#         locations_testing.create_workshops_sections_and_cells()
#         piglets_testing.create_statuses()

#     def test_groups_with_gilts(self):
#         new_born_group1 = piglets_testing.create_new_born_group(cell_number=5)