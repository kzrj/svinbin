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


class SowTransactionManagerTest(TestCase):
    def setUp(self):
        workshops_testing.create_workshops_sections_and_cells()

    def test_create_transaction(self):
        sow = sows_testing.create_sow_and_put_in_workshop_one(1, '100')
        to_location = Location.objects.get(sowSingleCell__number='2')
        transaction = SowTransaction.objects.create_transaction(
            to_location=to_location,
            initiator=None,
            sow=sow
            )

        self.assertEqual(transaction.sow, sow)
        self.assertEqual(transaction.initiator, None)
        self.assertEqual(transaction.from_location,
         Location.objects.get(sowSingleCell__number=100))
        self.assertEqual(transaction.to_location, to_location)

    def test_create_many_transaction(self):
        sow1 = sows_testing.create_sow_and_put_in_workshop_one(1, '100')
        sow2 = sows_testing.create_sow_and_put_in_workshop_one(1, '101')
        to_location = Location.objects.get(workshop__number=3)

        transactions = SowTransaction.objects.create_many_transactions([sow1, sow2],
            to_location)
        self.assertEqual(transactions, [1,2])


class LocationModelManagerTest(TestCase):
    def test_create_location(self):
        workshop = WorkShop.objects.create(number=1)
        location = Location.objects.create_location(workshop)
        self.assertEqual(location.workshop.number, 1)

        section = Section.objects.create(workshop=workshop, number=1)
        location = Location.objects.create_location(section)
        self.assertEqual(location.section.number, 1)
        
        location = Location.objects.create_location(
            SowSingleCell.objects.create(workshop=workshop, section=section, number='1'))
        self.assertEqual(location.sowSingleCell.number, '1')
       

# class LocationModelTest(TestCase):
#     def setUp(self):
#         workshops_testing.create_workshops_sections_and_cells()
#         sows_testing.create_statuses()

#     def test_get_location(self):
#         workshop = WorkShop.objects.get(number=1)
#         location = Location.objects.create_location(workshop)
#         self.assertEqual(location.get_location, workshop)

#         section = Section.objects.get(workshop__number=1, number=1)
#         location = Location.objects.create_location(section)
#         self.assertEqual(location.get_location, section)
        
#         cell = SowSingleCell.objects.get(number='1')
#         location = Location.objects.create_location(cell)
#         self.assertEqual(location.get_location, cell)

#         cell = SowGroupCell.objects.first()
#         location = Location.objects.create_location(cell)
#         self.assertEqual(location.get_location, cell)

#         cell = PigletsGroupCell.objects.first()
#         location = Location.objects.create_location(cell)
#         self.assertEqual(location.get_location, cell)

#         cell = SowAndPigletsCell.objects.first()
#         location = Location.objects.create_location(cell)
#         self.assertEqual(location.get_location, cell)

#     def test_get_workshop(self):
#         workshop = WorkShop.objects.get(number=1)
#         location = Location.objects.create_location(workshop)
#         self.assertEqual(location.get_workshop, workshop)

#         section = Section.objects.get(workshop__number=1, number=1)
#         location = Location.objects.create_location(section)
#         self.assertEqual(location.get_workshop, workshop)
        
#         cell = SowSingleCell.objects.get(number='1')
#         location = Location.objects.create_location(cell)
#         self.assertEqual(location.get_workshop, workshop)

#         cell = SowGroupCell.objects.first()
#         location = Location.objects.create_location(cell)
#         self.assertEqual(location.get_workshop, cell.section.workshop)

#         cell = PigletsGroupCell.objects.first()
#         location = Location.objects.create_location(cell)
#         self.assertEqual(location.get_workshop, cell.section.workshop)

#         cell = SowAndPigletsCell.objects.first()
#         location = Location.objects.create_location(cell)
#         self.assertEqual(location.get_workshop, cell.section.workshop)

#     def test_get_with_active_new_born_group(self):
#         new_born_group = piglets_testing.create_new_born_group()

#         location = new_born_group.location
        

class PigletsTransactionManagerTest(TestCase):
    def setUp(self):
        workshops_testing.create_workshops_sections_and_cells()
        sows_testing.create_statuses()
        piglets_testing.create_piglets_statuses()

    def test_create_transaction(self):
        nomad_group = piglets_testing.create_nomad_group_from_three_new_born()
        self.assertEqual(nomad_group.location.workshop.number, 3)

        to_location = Location.objects.get(workshop__number=4)
        transaction = PigletsTransaction.objects.create_transaction(to_location, nomad_group)

        self.assertEqual(transaction.from_location.workshop.number, 3)
        self.assertEqual(transaction.to_location.workshop.number, 4)
        self.assertEqual(transaction.piglets_group, nomad_group)

        nomad_group.refresh_from_db()
        self.assertEqual(nomad_group.location.workshop.number, 4)
