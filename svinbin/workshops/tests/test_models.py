from mixer.backend.django import mixer

from django.test import TestCase

import workshops.testing_utils as workshops_testing
import sows.testing_utils as sows_testing
import piglets.testing_utils as piglets_testing

from workshops.models import WorkShop, Section, SowSingleCell, PigletsGroupCell, SowGroupCell, \
SowAndPigletsCell
from transactions.models import Location, PigletsTransaction


class TestingUtilsTest(TestCase):
    def setUp(self):
        workshops_testing.create_workshops()

    def test_create_workshops(self):
        self.assertEqual(WorkShop.objects.all().count(), 10)

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
        sows_testing.create_statuses()
        piglets_testing.create_piglets_statuses()

    def test_get_all_locations(self):
        section = Section.objects.get(workshop__number=4, number=1)
        piglet_group_cell1 = PigletsGroupCell.objects.get(section=section, number=1)
        piglet_group_cell2 = PigletsGroupCell.objects.get(section=section, number=2)

        location1 = Location.objects.create_location(piglet_group_cell1)
        location2 = Location.objects.create_location(WorkShop.objects.get(number=4))
        location3 = Location.objects.create_location(piglet_group_cell2)

        self.assertEqual(piglet_group_cell1.get_all_locations()[0],
         Location.objects.filter(pk=location1.pk)[0])

    def test_get_residents(self):
        nomad_group1 = piglets_testing.create_nomad_group_from_three_new_born()
        nomad_group2 = piglets_testing.create_nomad_group_from_three_new_born()

        section = Section.objects.get(workshop__number=4, number=1)
        piglet_group_cell = PigletsGroupCell.objects.get(section=section, number=1)

        to_location1 = Location.objects.create_location(piglet_group_cell)
        transaction1 = PigletsTransaction.objects.create_transaction_without_merge(to_location1,
            nomad_group1)

        to_location2 = Location.objects.create_location(piglet_group_cell)
        transaction2 = PigletsTransaction.objects.create_transaction_without_merge(to_location2,
            nomad_group2)

        print(nomad_group1.location)
        print(piglet_group_cell.locations.filter(nomadpigletsgroup=nomad_group1).first().nomadpigletsgroup)
        print(piglet_group_cell.get_residents())

        # nomad_group.active = False
        # nomad_group.save()
        # print(piglet_group_cell.get_residents())
