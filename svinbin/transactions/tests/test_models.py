from mixer.backend.django import mixer

from django.test import TestCase
from django.utils import timezone
from django.core.exceptions import ValidationError

import locations.testing_utils as locations_testing
import sows.testing_utils as sows_testing
import sows_events.utils as sows_events_testing
import piglets.testing_utils as piglets_testing

from locations.models import Location
from sows.models import Sow
from piglets.models import Piglets
from tours.models import Tour
from piglets_events.models import PigletsSplit, PigletsMerger, WeighingPiglets
from transactions.models import SowTransaction, PigletsTransaction


class SowTransactionManagerTest(TestCase):
    def setUp(self):
        locations_testing.create_workshops_sections_and_cells()
        sows_testing.create_statuses()
        sows_events_testing.create_types()
        piglets_testing.create_piglets_statuses()

        self.tour1 = Tour.objects.get_or_create_by_week_in_current_year(week_number=1)
        self.loc_ws3 = Location.objects.filter(sowAndPigletsCell__isnull=False)

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

    def test_create_many_transaction(self):
        sow1 = sows_testing.create_sow_and_put_in_workshop_one()
        sow2 = sows_testing.create_sow_and_put_in_workshop_one()
        to_location = Location.objects.get(workshop__number=3)

        transactions = SowTransaction.objects.create_many_transactions([sow1, sow2],
            to_location)
        self.assertEqual(len(transactions), 2)

    def test_create_many_without_status_check(self):
        sow1 = sows_testing.create_sow_and_put_in_workshop_one()
        sow2 = sows_testing.create_sow_and_put_in_workshop_one()
        to_location = Location.objects.get(workshop__number=3)

        transactions = SowTransaction.objects.create_many_transactions([sow1, sow2],
            to_location)
        
        sow1.refresh_from_db()
        sow2.refresh_from_db()
        self.assertEqual(sow1.location.workshop.number, 3)
        self.assertEqual(sow2.location.workshop.number, 3)

    def test_trs_in_ws(self):
        sow1 = sows_testing.create_sow_and_put_in_workshop_one()
        sow2 = sows_testing.create_sow_and_put_in_workshop_one()
        sow3 = sows_testing.create_sow_and_put_in_workshop_one()
        to_location = Location.objects.get(workshop__number=3)

        transactions = SowTransaction.objects.create_many_transactions([sow1, sow2],
            to_location)

        ws_locs2 = Location.objects.all().get_workshop_location_by_number(workshop_number=2)
        ws_locs1 = Location.objects.all().get_workshop_location_by_number(workshop_number=1)
        ws_locs3 = Location.objects.all().get_workshop_location_by_number(workshop_number=3)

        to_location2 = Location.objects.get(workshop__number=2)
        transaction2 = SowTransaction.objects.create_transaction(
            to_location=to_location2,
            initiator=None,
            sow=sow3
            )

        self.assertEqual(SowTransaction.objects.trs_in_ws(ws_number=3, ws_locs=ws_locs3).count(), 2)
        self.assertEqual(SowTransaction.objects.trs_out_ws(ws_locs=ws_locs1).count(), 3)

    def test_weaning_trs_from_ws3_to_ws1(self):
        piglets =  piglets_testing.create_from_sow_farrow(tour=self.tour1, location=self.loc_ws3[0],
         quantity=10)
        sow = piglets.farrow.sow
        self.assertEqual(sow.status.title, 'Опоросилась')
        self.assertEqual(sow.tour, self.tour1)
        to_location = Location.objects.get(workshop__number=1)
        transaction = SowTransaction.objects.create_transaction(sow=sow, to_location=to_location)

        sow.refresh_from_db()
        self.assertEqual(sow.status.title, 'Ожидает осеменения')
        self.assertEqual(sow.tour, None)
                 

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

        self.loc_ws7 = Location.objects.get(workshop__number=7)

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

        transaction, piglets2, stayed_piglets, split_event, merge_event = PigletsTransaction.objects \
            .transaction_with_split_and_merge(piglets=piglets, to_location=self.loc_ws4_cell1)

        self.assertEqual(transaction.from_location.workshop.number, 3)
        self.assertEqual(transaction.to_location, self.loc_ws4_cell1)
        self.assertEqual(transaction.piglets_group, piglets2)

        piglets2.refresh_from_db()
        self.assertEqual(piglets2.location, self.loc_ws4_cell1)

    def test_transaction_with_split_and_merge_v1_reverse(self):
        # transaction with split reverse
        piglets = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws3, 10)

        transaction, moved_piglets, stayed_piglets, split_event, merge_event = PigletsTransaction.objects. \
            transaction_with_split_and_merge(piglets=piglets, to_location=self.loc_ws4, new_amount=4,
                reverse=True)

        self.assertEqual(transaction.from_location.workshop.number, 3)
        self.assertEqual(transaction.to_location, self.loc_ws4)
        self.assertEqual(transaction.piglets_group, moved_piglets)

        moved_piglets.refresh_from_db()
        stayed_piglets.refresh_from_db()
        self.assertEqual(moved_piglets.location, self.loc_ws4)
        self.assertEqual(moved_piglets.quantity, 6)
        self.assertEqual(moved_piglets.metatour.records.all().first().percentage, 100)
        self.assertEqual(moved_piglets.metatour.records.all().count(), 1)

        self.assertEqual(stayed_piglets.location, self.loc_ws3)
        self.assertEqual(stayed_piglets.quantity, 4)
        self.assertEqual(stayed_piglets.metatour.records.all().first().percentage, 100)
        self.assertEqual(stayed_piglets.metatour.records.all().count(), 1)

    def test_transaction_with_split_and_merge_v2(self):
        # transaction with split
        piglets = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws3, 10)

        transaction, piglets2, stayed_piglets, split_event, merge_event = PigletsTransaction.objects. \
            transaction_with_split_and_merge(piglets=piglets, to_location=self.loc_ws4, new_amount=4)

        self.assertEqual(Piglets.objects.all().count(), 2)
        self.assertEqual(piglets.active, False)
        self.assertEqual(piglets2.quantity, 4)
        self.assertEqual(piglets2.location, self.loc_ws4)
        self.assertEqual(piglets2.metatour.records.all().first().percentage, 100)
        self.assertEqual(piglets2.metatour.records.all().count(), 1)

        piglets1 = piglets.split_as_parent.piglets_as_child.all().first()
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

        transaction, moved_merged_piglets, stayed_piglets, split_event, merge_event = PigletsTransaction.objects. \
            transaction_with_split_and_merge(piglets=piglets, to_location=self.loc_ws4_cell1, merge=True)

        piglets.refresh_from_db()
        piglets_in_cell.refresh_from_db()
        # active piglets should be 1
        self.assertEqual(Piglets.objects.all().count(), 1)
        self.assertEqual(piglets.active, False)
        self.assertEqual(piglets_in_cell.active, False)

        moved_merged_piglets.refresh_from_db()
        self.assertEqual(moved_merged_piglets.quantity, 20)
        self.assertEqual(moved_merged_piglets.active, True)
        self.assertEqual(moved_merged_piglets.location, self.loc_ws4_cell1)
        self.assertEqual(moved_merged_piglets.metatour.records.all().first().percentage, 100)
        self.assertEqual(moved_merged_piglets.metatour.records.all().first().quantity, 20)
        self.assertEqual(moved_merged_piglets.metatour.records.all().count(), 1)

        self.assertEqual(Piglets.objects.get_all().filter(merger_as_parent=moved_merged_piglets.merger_as_child). \
            first(), piglets)

        self.assertEqual(Piglets.objects.get_all().filter(merger_as_parent=moved_merged_piglets.merger_as_child)[1], \
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

        transaction, moved_merged_piglets, stayed_piglets, split_event, merge_event = PigletsTransaction.objects. \
            transaction_with_split_and_merge(piglets=piglets, to_location=self.loc_ws4_cell1, \
                new_amount=4, merge=True)

        piglets.refresh_from_db()
        piglets_in_cell.refresh_from_db()
        self.assertEqual(Piglets.objects.all().count(), 2)
        self.assertEqual(piglets.active, False)
        self.assertEqual(piglets_in_cell.active, False)

        moved_merged_piglets.refresh_from_db()
        self.assertEqual(moved_merged_piglets.quantity, 14)
        self.assertEqual(moved_merged_piglets.active, True)
        self.assertEqual(moved_merged_piglets.location, self.loc_ws4_cell1)
        self.assertEqual(moved_merged_piglets.metatour.records.all().first().percentage, 100)
        self.assertEqual(moved_merged_piglets.metatour.records.all().first().quantity, 14)
        self.assertEqual(moved_merged_piglets.metatour.records.all().count(), 1)

        stayed_piglets.refresh_from_db()
        self.assertEqual(stayed_piglets.quantity, 6)
        self.assertEqual(stayed_piglets.active, True)
        self.assertEqual(stayed_piglets.location, self.loc_ws3)
        self.assertEqual(stayed_piglets.metatour.records.all().first().percentage, 100)
        self.assertEqual(stayed_piglets.metatour.records.all().first().quantity, 6)
        self.assertEqual(stayed_piglets.metatour.records.all().count(), 1)

        child_split_piglets1 = Piglets.objects.get_all() \
            .filter(split_as_child=piglets.split_as_parent, quantity=6).first()
        child_split_piglets2 = Piglets.objects.get_all() \
            .filter(split_as_child= piglets.split_as_parent, quantity=4).first()

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
        transaction, moved_merged_piglets, stayed_piglets, split_event, merge_event = PigletsTransaction.objects. \
            transaction_with_split_and_merge(piglets=piglets, to_location=self.loc_ws4_cell1, \
                new_amount=4, merge=True)

        piglets.refresh_from_db()
        piglets_in_cell.refresh_from_db()
        self.assertEqual(Piglets.objects.all().count(), 2)
        self.assertEqual(piglets.active, False)
        self.assertEqual(piglets_in_cell.active, False)

        moved_merged_piglets.refresh_from_db()
        self.assertEqual(moved_merged_piglets.quantity, 14)
        self.assertEqual(moved_merged_piglets.active, True)
        self.assertEqual(moved_merged_piglets.location, self.loc_ws4_cell1)
        self.assertEqual(moved_merged_piglets.metatour.records.all().count(), 2)

        self.assertEqual(round(moved_merged_piglets.metatour.records_repr()[0]['percentage'], 2), 28.57)
        self.assertEqual(moved_merged_piglets.metatour.records.all()[0].quantity, 4)

        self.assertEqual(round(moved_merged_piglets.metatour.records_repr()[1]['percentage'], 2), 71.43)
        self.assertEqual(moved_merged_piglets.metatour.records.all()[1].quantity, 10)

        stayed_piglets.refresh_from_db()
        self.assertEqual(stayed_piglets.quantity, 6)
        self.assertEqual(stayed_piglets.active, True)
        self.assertEqual(stayed_piglets.location, self.loc_ws3)
        self.assertEqual(stayed_piglets.metatour.records.all().count(), 1)
        self.assertEqual(round(stayed_piglets.metatour.records_repr()[0]['percentage'], 2), 100.00)
        self.assertEqual(stayed_piglets.metatour.records.all()[0].quantity, 6)
       
        child_split_piglets1 = Piglets.objects.get_all() \
            .filter(split_as_child=piglets.split_as_parent, quantity=6).first()
        child_split_piglets2 = Piglets.objects.get_all() \
            .filter(split_as_child=piglets.split_as_parent, quantity=4).first()

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
        transaction, final_in_cell_piglets1, stayed_piglets, split_event, merge_event = PigletsTransaction.objects. \
            transaction_with_split_and_merge(piglets=piglets1, to_location=self.loc_ws4_cell1, \
                new_amount=4, merge=True)

        piglets1.refresh_from_db()
        piglets_in_cell.refresh_from_db()
        self.assertEqual(round(final_in_cell_piglets1.metatour.records_repr()[0]['percentage'], 2), 28.57)
        self.assertEqual(final_in_cell_piglets1.metatour.records.all()[0].quantity, 4)
        self.assertEqual(round(final_in_cell_piglets1.metatour.records_repr()[1]['percentage'], 2), 71.43)
        self.assertEqual(final_in_cell_piglets1.metatour.records.all()[1].quantity, 10)

        stayed_piglets.refresh_from_db()
        self.assertEqual(stayed_piglets.quantity, 6)
        self.assertEqual(stayed_piglets.active, True)
        self.assertEqual(stayed_piglets.location, self.loc_ws3)
        self.assertEqual(stayed_piglets.metatour.records.all().count(), 1)
        self.assertEqual(round(stayed_piglets.metatour.records_repr()[0]['percentage'], 2), 100.00)
        self.assertEqual(stayed_piglets.metatour.records.all()[0].quantity, 6)

        # round 2
        piglets2 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws3, 10)

        # second transaction in same cell
        transaction, final_in_cell_piglets2, stayed_piglets2, split_event, merge_event = PigletsTransaction.objects. \
            transaction_with_split_and_merge(piglets=piglets2, to_location=self.loc_ws4_cell1, \
                new_amount=2, merge=True)

        self.assertEqual(final_in_cell_piglets2.metatour.records_repr()[0]['percentage'], 37.5)
        self.assertEqual(final_in_cell_piglets2.metatour.records.all()[0].quantity, 6)
        self.assertEqual(final_in_cell_piglets2.metatour.records_repr()[1]['percentage'], 62.5)
        self.assertEqual(final_in_cell_piglets2.metatour.records.all()[1].quantity, 10)

        stayed_piglets2.refresh_from_db()
        self.assertEqual(stayed_piglets2.quantity, 8)
        self.assertEqual(stayed_piglets2.active, True)
        self.assertEqual(stayed_piglets2.location, self.loc_ws3)
        self.assertEqual(stayed_piglets2.metatour.records.all().count(), 1)
        self.assertEqual(round(stayed_piglets2.metatour.records_repr()[0]['percentage'], 2), 100.00)
        self.assertEqual(stayed_piglets2.metatour.records.all()[0].quantity, 8)

        # round 3
        piglets3 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws3, 10)

        # third transaction in same cell
        transaction, final_in_cell_piglets3, stayed_piglets3, split_event, merge_event = PigletsTransaction.objects. \
            transaction_with_split_and_merge(piglets=piglets3, to_location=self.loc_ws4_cell1, \
                new_amount=1, merge=True)

        self.assertEqual(final_in_cell_piglets3.metatour.records_repr()[0]['percentage'], 41.18)
        self.assertEqual(final_in_cell_piglets3.metatour.records.all()[0].quantity, 7)
        self.assertEqual(final_in_cell_piglets3.metatour.records_repr()[1]['percentage'], 58.82)
        self.assertEqual(final_in_cell_piglets3.metatour.records.all()[1].quantity, 10)

        stayed_piglets3.refresh_from_db()
        self.assertEqual(stayed_piglets3.quantity, 9)
        self.assertEqual(stayed_piglets3.active, True)
        self.assertEqual(stayed_piglets3.location, self.loc_ws3)
        self.assertEqual(stayed_piglets3.metatour.records.all().count(), 1)
        self.assertEqual(round(stayed_piglets3.metatour.records_repr()[0]['percentage'], 2), 100.00)
        self.assertEqual(stayed_piglets3.metatour.records.all()[0].quantity, 9)

        # round 4
        piglets4 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws3, 100)

        # four transaction in same cell
        transaction, final_in_cell_piglets4, stayed_piglets4, split_event, merge_event = PigletsTransaction.objects. \
            transaction_with_split_and_merge(piglets=piglets4, to_location=self.loc_ws4_cell1, \
                new_amount=86, merge=True)

        self.assertEqual(final_in_cell_piglets4.metatour.records_repr()[0]['percentage'], 90.29)
        self.assertEqual(final_in_cell_piglets4.metatour.records.all()[0].quantity, 93)
        self.assertEqual(final_in_cell_piglets4.metatour.records_repr()[1]['percentage'], 9.71)
        self.assertEqual(final_in_cell_piglets4.metatour.records.all()[1].quantity, 10)

        stayed_piglets4.refresh_from_db()
        self.assertEqual(stayed_piglets4.quantity, 14)
        self.assertEqual(stayed_piglets4.active, True)
        self.assertEqual(stayed_piglets4.location, self.loc_ws3)
        self.assertEqual(stayed_piglets4.metatour.records.all().count(), 1)
        self.assertEqual(round(stayed_piglets4.metatour.records_repr()[0]['percentage'], 2), 100.00)
        self.assertEqual(stayed_piglets4.metatour.records.all()[0].quantity, 14)

        piglets5 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour3,
            self.loc_ws3, 100)

        # five transaction in same cell, tour3
        transaction, final_in_cell_piglets5, stayed_piglets5, split_event, merge_event = PigletsTransaction.objects. \
            transaction_with_split_and_merge(piglets=piglets5, to_location=self.loc_ws4_cell1, \
                new_amount=75, merge=True)

        self.assertEqual(final_in_cell_piglets5.metatour.records_repr()[0]['percentage'], 52.25)
        self.assertEqual(final_in_cell_piglets5.metatour.records.all()[0].quantity, 93)
        self.assertEqual(final_in_cell_piglets5.metatour.records_repr()[1]['percentage'], 5.62)
        self.assertEqual(final_in_cell_piglets5.metatour.records.all()[1].quantity, 10)
        self.assertEqual(final_in_cell_piglets5.metatour.records_repr()[2]['percentage'], 42.13)
        self.assertEqual(final_in_cell_piglets5.metatour.records.all()[2].quantity, 75)

        stayed_piglets5.refresh_from_db()
        self.assertEqual(stayed_piglets5.quantity, 25)
        self.assertEqual(stayed_piglets5.active, True)
        self.assertEqual(stayed_piglets5.location, self.loc_ws3)
        self.assertEqual(stayed_piglets5.metatour.records.all().count(), 1)
        self.assertEqual(round(stayed_piglets5.metatour.records_repr()[0]['percentage'], 2), 100.00)
        self.assertEqual(stayed_piglets5.metatour.records.all()[0].quantity, 25)

    def test_transaction_with_split_and_merge_v7(self):
        # transaction from cell to cell
        piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws3, 50)

        piglets2 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour2,
            self.loc_ws3, 75)

        piglets3 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour3,
            self.loc_ws3, 100)

        piglets_qs = [piglets1, piglets2, piglets3]

        final_in_cell_piglets1 = PigletsMerger.objects.create_merger_return_group(
            parent_piglets=piglets_qs,
            new_location=self.loc_ws4_cell1)

        self.assertEqual(final_in_cell_piglets1.location, self.loc_ws4_cell1)
        self.assertEqual(final_in_cell_piglets1.metatour.records_repr()[0]['tour'], 1)
        self.assertEqual(final_in_cell_piglets1.metatour.records_repr()[0]['percentage'], 22.22)
        self.assertEqual(final_in_cell_piglets1.metatour.records_repr()[1]['tour'], 2)
        self.assertEqual(final_in_cell_piglets1.metatour.records_repr()[1]['percentage'], 33.33)
        self.assertEqual(final_in_cell_piglets1.metatour.records_repr()[2]['tour'], 3)
        self.assertEqual(final_in_cell_piglets1.metatour.records_repr()[2]['percentage'], 44.44)

        transaction, final_in_cell_piglets2, stayed_piglets1, split_event1, merge_event1 = \
            PigletsTransaction.objects.transaction_with_split_and_merge(
                piglets=final_in_cell_piglets1,
                to_location=self.loc_ws4_cell2,
                new_amount=1, merge=True)

        self.assertEqual(final_in_cell_piglets2.location, self.loc_ws4_cell2)
        self.assertEqual(final_in_cell_piglets2.metatour.records_repr()[0]['tour'], 1)
        self.assertEqual(final_in_cell_piglets2.metatour.records_repr()[0]['percentage'], 22.22)
        self.assertEqual(final_in_cell_piglets2.metatour.records_repr()[0]['quantity'], 0.22)
        self.assertEqual(final_in_cell_piglets2.metatour.records_repr()[1]['tour'], 2)
        self.assertEqual(final_in_cell_piglets2.metatour.records_repr()[1]['percentage'], 33.33)
        self.assertEqual(final_in_cell_piglets2.metatour.records_repr()[1]['quantity'], 0.33)

        self.assertEqual(final_in_cell_piglets2.metatour.records_repr()[2]['tour'], 3)
        self.assertEqual(final_in_cell_piglets2.metatour.records_repr()[2]['percentage'], 44.44)
        self.assertEqual(final_in_cell_piglets2.metatour.records_repr()[2]['quantity'], 0.44)

        self.assertEqual(split_event1.piglets_as_child.all().first(), stayed_piglets1)

        transaction, final_in_cell_piglets3, stayed_piglets2, split_event2, merge_event2 = \
          PigletsTransaction.objects.transaction_with_split_and_merge(
            piglets=stayed_piglets1, 
            to_location=self.loc_ws4_cell2, 
            new_amount=9, merge=True)

        self.assertEqual(final_in_cell_piglets3.location, self.loc_ws4_cell2)
        self.assertEqual(final_in_cell_piglets3.metatour.records_repr()[0]['tour'], 1)
        self.assertEqual(final_in_cell_piglets3.metatour.records_repr()[0]['percentage'], 22.22)
        self.assertEqual(final_in_cell_piglets3.metatour.records_repr()[0]['quantity'], 2.22)
        self.assertEqual(final_in_cell_piglets3.metatour.records_repr()[1]['tour'], 2)
        self.assertEqual(final_in_cell_piglets3.metatour.records_repr()[1]['percentage'], 33.33)
        self.assertEqual(final_in_cell_piglets3.metatour.records_repr()[1]['quantity'], 3.33)
        self.assertEqual(final_in_cell_piglets3.metatour.records_repr()[2]['tour'], 3)
        self.assertEqual(final_in_cell_piglets3.metatour.records_repr()[2]['percentage'], 44.44)
        self.assertEqual(final_in_cell_piglets3.metatour.records_repr()[2]['quantity'], 4.44)