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
from piglets_events.models import PigletsSplit, PigletsMerger
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
        self.tour3 = Tour.objects.get_or_create_by_week_in_current_year(week_number=3)

        self.loc_ws3 = Location.objects.get(workshop__number=3)
        self.loc_ws3_sec1 = Location.objects.get(section__workshop__number=3, section__number=1)
        self.loc_ws3_sec2 = Location.objects.get(section__workshop__number=3, section__number=2)

        self.loc_ws4 = Location.objects.get(workshop__number=4)
        self.loc_ws4_cell1 = Location.objects.filter(pigletsGroupCell__isnull=False)[0]
        self.loc_ws4_cell2 = Location.objects.filter(pigletsGroupCell__isnull=False)[1]

    def test_create_transaction(self):
        piglets = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws3, 10)

        transaction = PigletsTransaction.objects.create_transaction(self.loc_ws4, piglets)

        self.assertEqual(transaction.from_location.workshop.number, 3)
        self.assertEqual(transaction.to_location.workshop.number, 4)
        self.assertEqual(transaction.piglets_group, piglets)

        piglets.refresh_from_db()
        self.assertEqual(piglets.location, self.loc_ws4)

    def test_transaction_with_split_and_merge_v1(self):
        # simple transaction
        piglets = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws3, 10)

        transaction, piglets2, split_event, merge_event = PigletsTransaction.objects \
            .transaction_with_split_and_merge(piglets, self.loc_ws4_cell1)

        self.assertEqual(transaction.from_location.workshop.number, 3)
        self.assertEqual(transaction.to_location, self.loc_ws4_cell1)
        self.assertEqual(transaction.piglets_group, piglets2)

        piglets2.refresh_from_db()
        self.assertEqual(piglets2.location, self.loc_ws4_cell1)

    def test_transaction_with_split_and_merge_v2(self):
        # transaction with split
        piglets = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws3, 10)

        transaction, piglets2, split_event, merge_event = PigletsTransaction.objects. \
            transaction_with_split_and_merge(piglets=piglets, to_location=self.loc_ws4, new_amount=4)

        self.assertEqual(Piglets.objects.all().count(), 2)
        self.assertEqual(piglets.active, False)
        self.assertEqual(piglets2.quantity, 4)
        self.assertEqual(piglets2.location, self.loc_ws4)
        self.assertEqual(piglets2.metatour.records.all().first().percentage, 100)
        self.assertEqual(piglets2.metatour.records.all().count(), 1)

        piglets1 = piglets.split_as_parent.all().first().piglets_as_child.all().first()
        self.assertEqual(piglets1.location, self.loc_ws3)
        self.assertEqual(piglets1.metatour.records.all().first().percentage, 100)
        self.assertEqual(piglets1.metatour.records.all().count(), 1)

        self.assertEqual(transaction.from_location.workshop.number, 3)
        self.assertEqual(transaction.to_location, self.loc_ws4)
        self.assertEqual(transaction.piglets_group, piglets2)


    def test_transaction_with_split_and_merge_v3(self):
        # transaction with merge
        piglets = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws3, 10)

        piglets_in_cell = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws4_cell1, 10)

        transaction, piglets2, split_event, merge_event = PigletsTransaction.objects. \
            transaction_with_split_and_merge(piglets=piglets, to_location=self.loc_ws4_cell1, merge=True)

        piglets.refresh_from_db()
        piglets_in_cell.refresh_from_db()
        self.assertEqual(Piglets.objects.all().count(), 1)
        self.assertEqual(piglets.active, False)
        self.assertEqual(piglets_in_cell.active, False)

        piglets2.refresh_from_db()
        self.assertEqual(piglets2.quantity, 20)
        self.assertEqual(piglets2.active, True)
        self.assertEqual(piglets2.location, self.loc_ws4_cell1)

        self.assertEqual(Piglets.objects.get_all().filter(merger_as_parent=piglets2.merger_as_child). \
            first(), piglets)

        self.assertEqual(Piglets.objects.get_all().filter(merger_as_parent=piglets2.merger_as_child)[1], \
            piglets_in_cell)

        self.assertEqual(transaction.from_location.workshop.number, 3)
        self.assertEqual(transaction.to_location, self.loc_ws4_cell1)
        self.assertEqual(transaction.piglets_group, piglets)


    def test_transaction_with_split_and_merge_v4(self):
        # transaction with merge and split
        piglets = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws3, 10)

        piglets_in_cell = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws4_cell1, 10)

        transaction, piglets2, split_event, merge_event = PigletsTransaction.objects. \
            transaction_with_split_and_merge(piglets=piglets, to_location=self.loc_ws4_cell1, \
                new_amount=4, merge=True)

        piglets.refresh_from_db()
        piglets_in_cell.refresh_from_db()
        self.assertEqual(Piglets.objects.all().count(), 2)
        self.assertEqual(piglets.active, False)
        self.assertEqual(piglets_in_cell.active, False)

        piglets2.refresh_from_db()
        self.assertEqual(piglets2.quantity, 14)
        self.assertEqual(piglets2.active, True)
        self.assertEqual(piglets2.location, self.loc_ws4_cell1)

        child_split_piglets1 = Piglets.objects.get_all() \
            .filter(split_as_child__in=piglets.split_as_parent.all(), quantity=6).first()
        child_split_piglets2 = Piglets.objects.get_all() \
            .filter(split_as_child__in= piglets.split_as_parent.all(), quantity=4).first()

        self.assertEqual(child_split_piglets1.active, True)
        self.assertEqual(child_split_piglets1.location, self.loc_ws3)

        self.assertEqual(child_split_piglets2.active, False)
        self.assertEqual(child_split_piglets2.location, self.loc_ws4_cell1)

        self.assertEqual(transaction.from_location.workshop.number, 3)
        self.assertEqual(transaction.to_location, self.loc_ws4_cell1)
        self.assertEqual(transaction.piglets_group, child_split_piglets2)

    def test_transaction_with_split_and_merge_v5(self):
        # transaction with merge and split. diff tours
        piglets = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws3, 10)

        piglets_in_cell = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour2,
            self.loc_ws4_cell1, 10)

        # split piglets = 6 and 4. thane merge 4 with piglets_in_cell, return merged piglets 14
        transaction, piglets2, split_event, merge_event = PigletsTransaction.objects. \
            transaction_with_split_and_merge(piglets=piglets, to_location=self.loc_ws4_cell1, \
                new_amount=4, merge=True)

        piglets.refresh_from_db()
        piglets_in_cell.refresh_from_db()
        self.assertEqual(Piglets.objects.all().count(), 2)
        self.assertEqual(piglets.active, False)
        self.assertEqual(piglets_in_cell.active, False)

        piglets2.refresh_from_db()
        self.assertEqual(piglets2.quantity, 14)
        self.assertEqual(piglets2.active, True)
        self.assertEqual(piglets2.location, self.loc_ws4_cell1)
        self.assertEqual(round(piglets2.metatour.records_repr()[0]['percentage'], 2), 28.57)
        self.assertEqual(round(piglets2.metatour.records_repr()[1]['percentage'], 2), 71.43)

        child_split_piglets1 = Piglets.objects.get_all() \
            .filter(split_as_child__in= piglets.split_as_parent.all(), quantity=6).first()
        child_split_piglets2 = Piglets.objects.get_all() \
            .filter(split_as_child__in= piglets.split_as_parent.all(), quantity=4).first()

        self.assertEqual(child_split_piglets1.active, True)
        self.assertEqual(child_split_piglets1.location, self.loc_ws3)

        self.assertEqual(child_split_piglets2.active, False)
        self.assertEqual(child_split_piglets2.location, self.loc_ws4_cell1)

        self.assertEqual(transaction.from_location.workshop.number, 3)
        self.assertEqual(transaction.to_location, self.loc_ws4_cell1)
        self.assertEqual(transaction.piglets_group, child_split_piglets2)

    def test_transaction_with_split_and_merge_v6(self):
        # transaction with merge and split. diff tours. multiple transaction to cell
        piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws3, 10)

        piglets_in_cell = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour2,
            self.loc_ws4_cell1, 10)

        # split piglets1 = 6 and 4. thane merge 4 with piglets_in_cell, return merged piglets 14
        transaction, final_in_cell_piglets1, split_event, merge_event = PigletsTransaction.objects. \
            transaction_with_split_and_merge(piglets=piglets1, to_location=self.loc_ws4_cell1, \
                new_amount=4, merge=True)

        piglets1.refresh_from_db()
        piglets_in_cell.refresh_from_db()
        self.assertEqual(round(final_in_cell_piglets1.metatour.records_repr()[0]['percentage'], 2), 28.57)
        self.assertEqual(round(final_in_cell_piglets1.metatour.records_repr()[1]['percentage'], 2), 71.43)

        piglets2 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws3, 10)

        # second transaction in same cell
        transaction, final_in_cell_piglets2, split_event, merge_event = PigletsTransaction.objects. \
            transaction_with_split_and_merge(piglets=piglets2, to_location=self.loc_ws4_cell1, \
                new_amount=2, merge=True)

        self.assertEqual(final_in_cell_piglets2.metatour.records_repr()[0]['percentage'], 37.5)
        self.assertEqual(final_in_cell_piglets2.metatour.records_repr()[1]['percentage'], 62.5)


        piglets3 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws3, 10)

        # third transaction in same cell
        transaction, final_in_cell_piglets3, split_event, merge_event = PigletsTransaction.objects. \
            transaction_with_split_and_merge(piglets=piglets3, to_location=self.loc_ws4_cell1, \
                new_amount=1, merge=True)

        self.assertEqual(final_in_cell_piglets3.metatour.records_repr()[0]['percentage'], 41.18)
        self.assertEqual(final_in_cell_piglets3.metatour.records_repr()[1]['percentage'], 58.82)

        piglets4 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws3, 100)

        # four transaction in same cell
        transaction, final_in_cell_piglets4, split_event, merge_event = PigletsTransaction.objects. \
            transaction_with_split_and_merge(piglets=piglets4, to_location=self.loc_ws4_cell1, \
                new_amount=86, merge=True)

        self.assertEqual(final_in_cell_piglets4.metatour.records_repr()[0]['percentage'], 90.29)
        self.assertEqual(final_in_cell_piglets4.metatour.records_repr()[1]['percentage'], 9.71)

        piglets5 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour3,
            self.loc_ws3, 100)

        # five transaction in same cell, tour3
        transaction, final_in_cell_piglets5, split_event, merge_event = PigletsTransaction.objects. \
            transaction_with_split_and_merge(piglets=piglets5, to_location=self.loc_ws4_cell1, \
                new_amount=75, merge=True)

        self.assertEqual(final_in_cell_piglets5.metatour.records_repr()[0]['percentage'], 52.25)
        self.assertEqual(final_in_cell_piglets5.metatour.records_repr()[1]['percentage'], 5.62)
        self.assertEqual(final_in_cell_piglets5.metatour.records_repr()[2]['percentage'], 42.13)


    def test_transaction_with_split_and_merge_v6(self):
        # transaction from cell to cell
        piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws3, 50)

        piglets2 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour2,
            self.loc_ws3, 75)

        piglets3 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour3,
            self.loc_ws3, 100)

        piglets_qs = [piglets1, piglets2, piglets3]

        final_in_cell_piglets1 = PigletsMerger.objects.create_merger_return_group(parent_piglets=piglets_qs,
            new_location=self.loc_ws4_cell1)

        self.assertEqual(final_in_cell_piglets1.location, self.loc_ws4_cell1)
        print(final_in_cell_piglets1.metatour.records_repr())

        transaction, final_in_cell_piglets2, split_event, merge_event = PigletsTransaction.objects. \
            transaction_with_split_and_merge(piglets=final_in_cell_piglets1, to_location=self.loc_ws4_cell2, \
                new_amount=1, merge=True)

        print(final_in_cell_piglets2.metatour.records_repr())

        transaction, final_in_cell_piglets3, split_event, merge_event = PigletsTransaction.objects. \
            transaction_with_split_and_merge(piglets=final_in_cell_piglets1, to_location=self.loc_ws4_cell2, \
                new_amount=9, merge=True)

        print(final_in_cell_piglets3.metatour.records_repr())
