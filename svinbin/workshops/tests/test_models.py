from mixer.backend.django import mixer

from django.test import TestCase

import workshops.testing_utils as workshops_testing

from workshops.models import WorkShop, Section, SowSingleCell, PigletsGroupCell, SowGroupCell, \
SowAndPigletsCell
from transactions.models import Location


class TestingUtilsTest(TestCase):
    def setUp(self):
        workshops_testing.create_workshops()

    def test_create_workshops(self):
        self.assertEqual(WorkShop.objects.all().count(), 11)

    def test_create_workshop_one(self):
        workshops_testing.create_sections_and_cell_for_workshop_one()
        workshop = WorkShop.objects.get(number=1)

        self.assertEqual(Section.objects.filter(workshop=workshop).count(), 3)

        section1 = Section.objects.filter(workshop=workshop).first()
        self.assertEqual(SowSingleCell.objects.filter(section=section1).count(), 480)

    def test_create_workshop_two(self):
        workshops_testing.create_sections_and_cell_for_workshop_two()
        workshop = WorkShop.objects.get(number=2)

        self.assertEqual(Section.objects.filter(workshop=workshop).count(), 2)

        section1 = Section.objects.filter(workshop=workshop).first()
        self.assertEqual(SowGroupCell.objects.filter(section=section1).count(), 6)

    def test_create_workshop_three(self):
        workshops_testing.create_sections_and_cell_for_workshop_three()
        workshop = WorkShop.objects.get(number=3)

        self.assertEqual(Section.objects.filter(workshop=workshop).count(), 2)

        section1 = Section.objects.filter(workshop=workshop).first()
        self.assertEqual(SowAndPigletsCell.objects.filter(section=section1).count(), 6)

    def test_create_sections_and_cell_for_workshop_with_group_cells(self):
        workshops_testing.create_sections_and_cell_for_workshop_with_group_cells(4)
        workshop = WorkShop.objects.get(number=4)

        self.assertEqual(Section.objects.filter(workshop=workshop).count(), 5)

        section1 = Section.objects.filter(workshop=workshop).first()
        self.assertEqual(PigletsGroupCell.objects.filter(section=section1).count(), 6)


class PigletsGroupCelltest(TestCase):
    def setUp(self):
        workshops_testing.create_workshops_sections_and_cells()

    def test_get_residents(self):
        section = Section.objects.get(workshop__number=4, number=1)
        piglet_group_cell = PigletsGroupCell.objects.get(section=section, number=1)
        print(piglet_group_cell)

        location1 = Location.objects.create_location(piglet_group_cell)
        location2 = Location.objects.create_location(WorkShop.objects.get(number=4))

        print(piglet_group_cell.get_residents())

        print(piglet_group_cell.locations.all())

