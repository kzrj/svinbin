# -*- coding: utf-8 -*-
from django.test import TestCase
from django.db import models

import locations.testing_utils as locations_testing
import sows.testing_utils as sows_testing
import piglets.testing_utils as piglets_testing

from locations.models import Location, WorkShop, Section, SowSingleCell, PigletsGroupCell, SowGroupCell, \
SowAndPigletsCell
from transactions.models import PigletsTransaction


# class TestingUtilsTest(TestCase):
#     def setUp(self):
#         locations_testing.create_workshops()

#     def test_create_workshops(self):
#         self.assertEqual(WorkShop.objects.all().count(), 10)
#         self.assertEqual(Location.objects.all().count(), 10)
#         self.assertEqual(Location.objects.filter(~(models.Q(workshop=None))).count(), 10)
#         self.assertEqual(Location.objects.filter(workshop=WorkShop.objects.get(number=1)).count(), 1)

#     def test_create_workshop_one(self):
#         locations_testing.create_sections_and_cell_for_workshop_one()
#         workshop = WorkShop.objects.get(number=1)

#         self.assertEqual(Section.objects.filter(workshop=workshop).count(), 3)
#         self.assertEqual(Location.objects.filter(~(models.Q(section=None))).count(), 3)

#         section1 = Section.objects.filter(workshop=workshop).first()
#         self.assertEqual(SowSingleCell.objects.filter(section=section1).count(), 480)
#         self.assertEqual(Location.objects.filter(~(models.Q(sowSingleCell=None))).count(), 480)

#     def test_create_workshop_two(self):
#         locations_testing.create_sections_and_cell_for_workshop_two()
#         workshop = WorkShop.objects.get(number=2)

#         self.assertEqual(Section.objects.filter(workshop=workshop).count(), 2)

#         section1 = Section.objects.filter(workshop=workshop).first()
#         self.assertEqual(SowGroupCell.objects.filter(section=section1).count(), 6)

#     def test_create_workshop_three(self):
#         locations_testing.create_sections_and_cell_for_workshop_three()
#         workshop = WorkShop.objects.get(number=3)

#         self.assertEqual(Section.objects.filter(workshop=workshop).count(), 2)

#         section1 = Section.objects.filter(workshop=workshop).first()
#         self.assertEqual(SowAndPigletsCell.objects.filter(section=section1).count(), 6)

#     def test_create_sections_and_cell_for_workshop_with_group_cells(self):
#         locations_testing.create_sections_and_cell_for_workshop_with_group_cells(4)
#         workshop = WorkShop.objects.get(number=4)

#         self.assertEqual(Section.objects.filter(workshop=workshop).count(), 5)

#         section1 = Section.objects.filter(workshop=workshop).first()
#         self.assertEqual(PigletsGroupCell.objects.filter(section=section1).count(), 6)


class LocationModelManagerQuerysetTest(TestCase):
    def setUp(self):
        locations_testing.create_workshops_sections_and_cells()
        sows_testing.create_statuses()
        piglets_testing.create_piglets_statuses()


class WorkshopModelTest(TestCase):
    def setUp(self):
        locations_testing.create_workshops_sections_and_cells()
        sows_testing.create_statuses()
        piglets_testing.create_piglets_statuses()
