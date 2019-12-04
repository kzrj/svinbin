from mixer.backend.django import mixer

from django.test import TestCase
from django.utils import timezone
from django.core.exceptions import ValidationError

import locations.testing_utils as locations_testing
import sows.testing_utils as sows_testing
import piglets.testing_utils as piglets_testing

from locations.models import Location
from sows.models import Sow
from piglets.models import Piglets
from tours.models import Tour
from transactions.models import SowTransaction, PigletsTransaction


class SowTransactionManagerTest(TestCase):
    def setUp(self):
        locations_testing.create_workshops_sections_and_cells()

    def test_create_transaction(self):
        sow = sows_testing.create_sow_and_put_in_workshop_one()
        to_location = Location.objects.get(workshop__number='2')
        transaction = SowTransaction.objects.create_transaction(
            to_location=to_location,
            initiator=None,
            sow=sow
            )

        self.assertEqual(transaction.sow, sow)
        self.assertEqual(transaction.initiator, None)
        self.assertEqual(transaction.from_location,
         Location.objects.get(workshop__number=1))
        self.assertEqual(transaction.to_location, to_location)

    # def test_create_transaction_to_not_empty_cell(self):
    #     sow1 = sows_testing.create_sow_and_put_in_workshop_three(section_number=1, cell_number=1)
    #     sow2 = sows_testing.create_sow_and_put_in_workshop_three(section_number=1, cell_number=2)
    #     with self.assertRaises(ValidationError):
    #         transaction = SowTransaction.objects.create_transaction(
    #             to_location=sow2.location,
    #             sow=sow1
    #             )

    def test_create_many_transaction(self):
        sow1 = sows_testing.create_sow_and_put_in_workshop_one()
        sow2 = sows_testing.create_sow_and_put_in_workshop_one()
        to_location = Location.objects.get(workshop__number=3)

        transactions = SowTransaction.objects.create_many_transactions([sow1, sow2],
            to_location)
        self.assertEqual(transactions, [1,2])
           

class PigletsTransactionManagerTest(TestCase):
    def setUp(self):
        locations_testing.create_workshops_sections_and_cells()
        sows_testing.create_statuses()
        piglets_testing.create_piglets_statuses()

        self.tour1 = Tour.objects.get_or_create_by_week_in_current_year(week_number=1)
        self.tour2 = Tour.objects.get_or_create_by_week_in_current_year(week_number=2)

        self.loc_ws3 = Location.objects.get(workshop__number=3)
        self.loc_ws3_sec1 = Location.objects.get(section__workshop__number=3, section__number=1)
        self.loc_ws3_sec2 = Location.objects.get(section__workshop__number=3, section__number=2)

        self.loc_ws4 = Location.objects.get(workshop__number=4)

    def test_create_transaction(self):
        piglets = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws3, 10)

        transaction = PigletsTransaction.objects.create_transaction(self.loc_ws4, piglets)

        self.assertEqual(transaction.from_location.workshop.number, 3)
        self.assertEqual(transaction.to_location.workshop.number, 4)
        self.assertEqual(transaction.piglets_group, piglets)

        piglets.refresh_from_db()
        self.assertEqual(piglets.location, self.loc_ws4)
