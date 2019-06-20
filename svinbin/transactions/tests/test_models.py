from mixer.backend.django import mixer

from django.test import TestCase
from django.utils import timezone

import workshops.testing_utils as workshops_testing
import sows.testing_utils as sows_testing
import piglets.testing_utils as piglets_testing

from workshops.models import WorkShop, Section, SowSingleCell, PigletsGroupCell, SowGroupCell, \
SowAndPigletsCell
from sows.models import Sow
from piglets.models import NomadPigletsGroup
from transactions.models import Location, SowTransaction, PigletsTransaction


class SowTransactionModelTest(TestCase):
    def setUp(self):
        workshops_testing.create_workshops_sections_and_cells()

    def test_to_empty_fill_single_cell(self):
        sow = sows_testing.create_sow_and_put_in_workshop_one(1, '100')
        to_location = Location.objects.create_location(SowSingleCell.objects.get(number='2'))

        transaction = SowTransaction(from_location=sow.location, to_location=to_location,
          sow=sow)

        self.assertEqual(sow.location.sowSingleCell.sow, sow)
        transaction.to_empty_from_location
        self.assertEqual(sow.location.sowSingleCell.sow, None)

        transaction.to_fill_to_location
        to_location.refresh_from_db()
        self.assertEqual(to_location.sowSingleCell.sow, sow)

        sow.change_sow_current_location(to_location)
        sow.refresh_from_db()
        self.assertEqual(sow.location, to_location)

    def test_to_empty_fill_group_cell(self):
        sow = sows_testing.create_sow_and_put_in_workshop_two(1, 1)
        section = Section.objects.get(workshop__number=2, number=2)
        to_location = Location.objects.create_location(SowGroupCell.objects.get(section=section, number=2))

        transaction = SowTransaction(from_location=sow.location, to_location=to_location,
          sow=sow)

        self.assertIn(sow, sow.location.sowGroupCell.sows.all())
        transaction.to_empty_from_location
        self.assertNotIn(sow, sow.location.sowGroupCell.sows.all())

        transaction.to_fill_to_location
        to_location.refresh_from_db()
        sow.refresh_from_db()
        self.assertIn(sow, to_location.sowGroupCell.sows.all())

        sow.change_sow_current_location(to_location)
        sow.refresh_from_db()
        self.assertEqual(sow.location, to_location)


class SowTransactionManagerTest(TestCase):
    def setUp(self):
        workshops_testing.create_workshops_sections_and_cells()

    def test_create_transaction(self):
        sow = sows_testing.create_sow_and_put_in_workshop_one(1, '100')
        to_location = Location.objects.create_location(SowSingleCell.objects.get(number='2'))
        transaction = SowTransaction.objects.create_transaction(
            to_location=to_location,
            initiator=None,
            sow=sow
            )

        self.assertNotEqual(transaction.pk, None)


class LocationModelManagerTest(TestCase):
    def setUp(self):
        workshops_testing.create_workshops_sections_and_cells()

    def test_create_location(self):
        location = Location.objects.create_location(WorkShop.objects.get(number=1))
        self.assertEqual(location.workshop.number, 1)

        location = Location.objects.create_location(Section.objects.get(workshop__number=1, \
            number=1))
        self.assertEqual(location.section.number, 1)
        
        location = Location.objects.create_location(SowSingleCell.objects.get(number='1'))
        self.assertEqual(location.sowSingleCell.number, '1')

        location = Location.objects.create_location(SowGroupCell.objects.first())
        self.assertNotEqual(location.sowGroupCell, None)

        location = Location.objects.create_location(SowAndPigletsCell.objects.first())
        self.assertNotEqual(location.sowAndPigletsCell, None)
        

class LocationModelTest(TestCase):
    def setUp(self):
        workshops_testing.create_workshops_sections_and_cells()

    def test_get_location(self):
        workshop = WorkShop.objects.get(number=1)
        location = Location.objects.create_location(workshop)
        self.assertEqual(location.get_location, workshop)

        section = Section.objects.get(workshop__number=1, number=1)
        location = Location.objects.create_location(section)
        self.assertEqual(location.get_location, section)
        
        cell = SowSingleCell.objects.get(number='1')
        location = Location.objects.create_location(cell)
        self.assertEqual(location.get_location, cell)

        cell = SowGroupCell.objects.first()
        location = Location.objects.create_location(cell)
        self.assertEqual(location.get_location, cell)

        cell = PigletsGroupCell.objects.first()
        location = Location.objects.create_location(cell)
        self.assertEqual(location.get_location, cell)

        cell = SowAndPigletsCell.objects.first()
        location = Location.objects.create_location(cell)
        self.assertEqual(location.get_location, cell)

    def test_get_workshop(self):
        workshop = WorkShop.objects.get(number=1)
        location = Location.objects.create_location(workshop)
        self.assertEqual(location.get_workshop, workshop)

        section = Section.objects.get(workshop__number=1, number=1)
        location = Location.objects.create_location(section)
        self.assertEqual(location.get_workshop, workshop)
        
        cell = SowSingleCell.objects.get(number='1')
        location = Location.objects.create_location(cell)
        self.assertEqual(location.get_workshop, workshop)

        cell = SowGroupCell.objects.first()
        location = Location.objects.create_location(cell)
        self.assertEqual(location.get_workshop, cell.section.workshop)

        cell = PigletsGroupCell.objects.first()
        location = Location.objects.create_location(cell)
        self.assertEqual(location.get_workshop, cell.section.workshop)

        cell = SowAndPigletsCell.objects.first()
        location = Location.objects.create_location(cell)
        self.assertEqual(location.get_workshop, cell.section.workshop)


class PigletsTransactionManagerTest(TestCase):
    def setUp(self):
        workshops_testing.create_workshops_sections_and_cells()
        sows_testing.create_statuses()
        piglets_testing.create_piglets_statuses()

    def test_create_transaction_without_merge(self):
        nomad_group = piglets_testing.create_nomad_group_from_three_new_born()
        self.assertEqual(nomad_group.location.get_location, WorkShop.objects.get(number=3))

        to_location = Location.objects.create_location(WorkShop.objects.get(number=4))
        transaction = PigletsTransaction.objects.create_transaction_without_merge(to_location, nomad_group)

        self.assertEqual(transaction.from_location.get_location, WorkShop.objects.get(number=3))
        self.assertEqual(transaction.to_location.get_location, WorkShop.objects.get(number=4))
        self.assertEqual(transaction.piglets_group, nomad_group)

        nomad_group.refresh_from_db()
        self.assertEqual(nomad_group.location.get_location, WorkShop.objects.get(number=4))

    def test_create_transaction_to_group_cell(self):
        nomad_group1 = piglets_testing.create_nomad_group_from_three_new_born()
        nomad_group2 = piglets_testing.create_nomad_group_from_three_new_born()
        nomad_group3 = piglets_testing.create_nomad_group_from_three_new_born()



