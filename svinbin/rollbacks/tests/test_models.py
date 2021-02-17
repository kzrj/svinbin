# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from django.test import TransactionTestCase
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from locations.models import Location
from tours.models import Tour
from piglets.models import Piglets
from sows.models import Sow, Gilt, SowStatusRecord
from piglets_events.models import (
    PigletsMerger, PigletsSplit, WeighingPiglets,
    CullingPiglets, Recount
)
from sows_events.models import ( PigletsToSowsEvent, MarkAsGilt, MarkAsNurse, WeaningSow,
    SowFarrow, CullingSow, Ultrasound, Semination, AbortionSow )
from transactions.models import PigletsTransaction, SowTransaction
from rollbacks.models import Rollback

import locations.testing_utils as locations_testing
import sows.testing_utils as sows_testing
import piglets.testing_utils as piglets_testing
import sows_events.utils as sows_events_testing
import staff.testing_utils as staff_testings


class PigletsRollbackModelTest(TransactionTestCase):
    def setUp(self):
        locations_testing.create_workshops_sections_and_cells()
        sows_testing.create_statuses()
        sows_events_testing.create_types()
        piglets_testing.create_piglets_statuses()
        staff_testings.create_svinbin_users()

        self.tour1 = Tour.objects.get_or_create_by_week_in_current_year(week_number=1)
        self.tour2 = Tour.objects.get_or_create_by_week_in_current_year(week_number=2)

        self.loc_ws1 = Location.objects.get(workshop__number=1)
        self.locs_ws3 = Location.objects.filter(sowAndPigletsCell__workshop__number=3)
        self.locs_ws4 = Location.objects.filter(pigletsGroupCell__workshop__number=4)
        self.locs_ws5 = Location.objects.filter(pigletsGroupCell__workshop__number=5)

        self.brig3 = User.objects.get(username='brigadir3')
        self.brig4 = User.objects.get(username='brigadir4')
        self.brig5 = User.objects.get(username='brigadir5')
        self.operator = User.objects.get(username='shmigina')

    def test_weighing_piglets_rollback(self):
        piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.locs_ws4[0], 10)

        operation = WeighingPiglets.objects.create_weighing(piglets_group=piglets1, total_weight=100,
            place='3/4', initiator=self.brig4, date=datetime(10,10,20))

        piglets1.refresh_from_db()
        self.assertEqual(piglets1.status.title, 'Взвешены, готовы к заселению')

        rollback = Rollback.objects.create_piglets_weighing_rollback(event_pk=operation.pk,
         initiator=self.operator, operation_name='piglets_weighing')

        piglets1.refresh_from_db()
        self.assertEqual(piglets1.status.title, 'Готовы ко взвешиванию')
        self.assertEqual(WeighingPiglets.objects.all().count(), 0)
        self.assertEqual(rollback.operation_name, 'piglets_weighing')
        self.assertEqual(rollback.workshop.number, 4)
        self.assertEqual(rollback.user_employee, self.brig4)
        self.assertEqual(rollback.date.day, datetime.today().day)

    def test_culling_piglets_rollback(self):
        piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.locs_ws4[0], 10)

        operation = CullingPiglets.objects.create_culling_piglets(piglets_group=piglets1,
            culling_type='padej', quantity=2,
            initiator=self.brig4, date=datetime(10,10,20))

        rollback = Rollback.objects.create_piglets_culling_rollback(event_pk=operation.pk,
         initiator=self.operator, operation_name='piglets_culling')

        piglets1.refresh_from_db()
        self.assertEqual(piglets1.quantity, 10)
        self.assertEqual(CullingPiglets.objects.all().count(), 0)
        self.assertEqual(rollback.operation_name, 'piglets_culling')
        self.assertEqual(rollback.workshop.number, 4)
        self.assertEqual(rollback.user_employee, self.brig4)

    def test_culling_piglets_rollback_v2(self):
        # culling all piglets
        piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.locs_ws4[0], 10)

        operation = CullingPiglets.objects.create_culling_piglets(piglets_group=piglets1,
            culling_type='padej', quantity=10,
            initiator=self.brig4, date=datetime(10,10,20))

        piglets1.refresh_from_db()
        self.assertEqual(piglets1.active, False)
        self.assertEqual(Piglets.objects.all().count(), 0)

        rollback = Rollback.objects.create_piglets_culling_rollback(event_pk=operation.pk,
         initiator=self.operator, operation_name='piglets_culling')

        piglets1.refresh_from_db()
        self.assertEqual(piglets1.quantity, 10)
        self.assertEqual(piglets1.active, True)
        self.assertEqual(CullingPiglets.objects.all().count(), 0)
        self.assertEqual(rollback.operation_name, 'piglets_culling')
        self.assertEqual(rollback.workshop.number, 4)
        self.assertEqual(rollback.user_employee, self.brig4)

    def test_create_piglets_transactions_rollback_v1(self):
        # piglets1 in from_loc and move all to to_loc then merge there
        piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.locs_ws4[0], 10)

        piglets2 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.locs_ws4[1], 15)

        piglets3 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.locs_ws4[2], 33)

        transaction, moved_piglets, stayed_piglets, split_event, merge_event = \
            PigletsTransaction.objects.transaction_with_split_and_merge(
            piglets=piglets1, to_location=self.locs_ws4[1], merge=True, initiator=self.brig4)

        self.assertEqual(Piglets.objects.all().count(), 2)
        self.assertEqual(moved_piglets.quantity, 25)
        piglets1.refresh_from_db()
        piglets2.refresh_from_db()
        self.assertEqual(piglets1.active, False)
        self.assertEqual(piglets2.active, False)

        Rollback.objects.create_piglets_transactions_rollback(
            event_pk=transaction.pk, initiator=self.operator, operation_name='piglets_transaction'
            )

        piglets1.refresh_from_db()
        piglets2.refresh_from_db()
        self.assertEqual(piglets1.active, True)
        self.assertEqual(piglets2.active, True)
        self.assertEqual(Piglets.objects.get_all().filter(pk=moved_piglets.pk).count(), 0)

        self.assertEqual(piglets1.location, self.locs_ws4[0])
        self.assertEqual(piglets2.location, self.locs_ws4[1])

        self.assertEqual(PigletsTransaction.objects.all().filter(pk=transaction.pk).count(), 0)

    def test_create_piglets_transactions_rollback_v2(self):
        # piglets1 splitted in from_loc the one of children move to to_loc then merge there
        piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.locs_ws4[0], 10)

        piglets2 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.locs_ws4[1], 15)

        piglets3 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.locs_ws4[2], 33)

        transaction, to_location_piglets, from_location_piglets, split_event, merge_event = \
            PigletsTransaction.objects.transaction_with_split_and_merge(
            piglets=piglets1, to_location=self.locs_ws4[1], merge=True, initiator=self.brig4,
            new_amount=4)

        self.assertEqual(to_location_piglets.quantity, 19)
        self.assertEqual(from_location_piglets.quantity, 6)

        Rollback.objects.create_piglets_transactions_rollback(
            event_pk=transaction.pk, initiator=self.operator, operation_name='piglets_transaction'
            )

        self.assertEqual(Piglets.objects.get_all().filter(pk=to_location_piglets.pk).count(), 0)
        self.assertEqual(Piglets.objects.get_all().filter(pk=from_location_piglets.pk).count(), 0)
        self.assertEqual(PigletsSplit.objects.filter(pk=split_event.pk).count(), 0)
        self.assertEqual(PigletsMerger.objects.filter(pk=merge_event.pk).count(), 0)

        piglets1.refresh_from_db()
        piglets2.refresh_from_db()
        self.assertEqual(piglets2.active, True)
        self.assertEqual(piglets1.active, True)
        self.assertEqual(piglets1.location, self.locs_ws4[0])
        self.assertEqual(piglets1.quantity, 10)
        self.assertEqual(piglets2.location, self.locs_ws4[1])
        self.assertEqual(piglets2.quantity, 15)

        self.assertEqual(PigletsTransaction.objects.all().filter(pk=transaction.pk).count(), 0)
        self.assertEqual(self.locs_ws4[1].piglets.all().count(), 1)

    def test_create_piglets_transactions_rollback_v3(self):
        # piglets1 splitted in from_loc  one of children move to to_loc then not merge there
        piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.locs_ws4[0], 10)

        piglets2 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.locs_ws4[1], 15)

        piglets3 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.locs_ws4[2], 33)

        transaction, to_location_piglets, from_location_piglets, split_event, merge_event = \
            PigletsTransaction.objects.transaction_with_split_and_merge(
            piglets=piglets1, to_location=self.locs_ws4[3], merge=True, initiator=self.brig4,
            new_amount=4)

        self.assertEqual(to_location_piglets.quantity, 4)
        self.assertEqual(from_location_piglets.quantity, 6)

        Rollback.objects.create_piglets_transactions_rollback(
            event_pk=transaction.pk, initiator=self.operator, operation_name='piglets_transaction'
            )

        self.assertEqual(Piglets.objects.get_all().filter(pk=to_location_piglets.pk).count(), 0)
        self.assertEqual(Piglets.objects.get_all().filter(pk=from_location_piglets.pk).count(), 0)
        self.assertEqual(PigletsSplit.objects.filter(pk=split_event.pk).count(), 0)
        self.assertEqual(merge_event, None)

        piglets1.refresh_from_db()
        self.assertEqual(piglets1.active, True)
        self.assertEqual(piglets1.location, self.locs_ws4[0])
        self.assertEqual(piglets1.quantity, 10)

        self.assertEqual(PigletsTransaction.objects.all().filter(pk=transaction.pk).count(), 0)
        self.assertEqual(self.locs_ws4[3].piglets.all().count(), 0)

    def test_create_piglets_transactions_rollback_v4(self):
        # simple piglets1 transaction to emplty loc
        piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.locs_ws4[0], 10)

        piglets2 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.locs_ws4[1], 15)

        transaction, to_location_piglets, from_location_piglets, split_event, merge_event = \
            PigletsTransaction.objects.transaction_with_split_and_merge(
            piglets=piglets1, to_location=self.locs_ws4[3], merge=True, initiator=self.brig4)

        self.assertEqual(to_location_piglets.quantity, 10)
        self.assertEqual(from_location_piglets, None)

        Rollback.objects.create_piglets_transactions_rollback(
            event_pk=transaction.pk, initiator=self.operator, operation_name='piglets_transaction'
            )

        self.assertEqual(from_location_piglets, None)
        self.assertEqual(split_event, None)
        self.assertEqual(merge_event, None)

        piglets1.refresh_from_db()
        self.assertEqual(piglets1.location, self.locs_ws4[0])
        self.assertEqual(piglets1.quantity, 10)

        self.assertEqual(PigletsTransaction.objects.all().filter(pk=transaction.pk).count(), 0)
        self.assertEqual(self.locs_ws4[3].piglets.all().count(), 0)

    def test_create_piglets_transactions_rollback_v5(self):
        # piglets1 splitted in ws, part settled in loc1 then transacted to loc2
        location1 = Location.objects.get(workshop__number=4)
        piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            location1, 50)

        transaction, moved_piglets, stayed_piglets, split_event, merge_event = \
            PigletsTransaction.objects.transaction_with_split_and_merge(
            piglets=piglets1, to_location=self.locs_ws4[1], merge=True, initiator=self.brig4,
            new_amount=40)

        transaction2, moved_piglets2, stayed_piglets2, split_event2, merge_event2 = \
            PigletsTransaction.objects.transaction_with_split_and_merge(
            piglets=moved_piglets, to_location=self.locs_ws4[2], initiator=self.brig4)

        piglets1.refresh_from_db()
        stayed_piglets.refresh_from_db()
        moved_piglets.refresh_from_db()
        moved_piglets2.refresh_from_db()

        self.assertEqual(piglets1.active, False)
        self.assertEqual(stayed_piglets.active, True)
        self.assertEqual(moved_piglets.active, True)
        self.assertEqual(moved_piglets, moved_piglets2)
        self.assertEqual(stayed_piglets2, None)
        self.assertEqual(PigletsSplit.objects.all().count(), 1)

        Rollback.objects.create_piglets_transactions_rollback(
            event_pk=transaction2.pk, initiator=self.operator, operation_name='piglets_transaction'
            )

        piglets1.refresh_from_db()
        stayed_piglets.refresh_from_db()
        moved_piglets.refresh_from_db()
        self.assertEqual(piglets1.active, False)
        self.assertEqual(stayed_piglets.active, True)
        self.assertEqual(moved_piglets.active, True)
        self.assertEqual(moved_piglets.location, self.locs_ws4[1])
        self.assertEqual(Piglets.objects.get_all().count(), 3)
        self.assertEqual(PigletsSplit.objects.all().count(), 1)
        self.assertEqual(PigletsTransaction.objects.all().count(), 1)

    def test_create_piglets_to_sows_event_rollback_split(self):
        piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.locs_ws5[0], 100)

        piglets2, piglets3_new_amount = PigletsSplit.objects.split_return_groups(
                    parent_piglets=piglets1, new_amount=59)

        WeighingPiglets.objects.create_weighing(piglets_group=piglets3_new_amount,
            total_weight=1560, place='o/2')

        pts_event = PigletsToSowsEvent.objects.create_event(piglets=piglets3_new_amount,
            initiator=self.brig5)
        self.assertEqual(Sow.objects.all().count(), 59)
        self.assertEqual(SowTransaction.objects.all().count(), 59)
        self.assertEqual(WeighingPiglets.objects.all().count(), 1)

        rollback = Rollback.objects.create_piglets_to_sows_event_rollback(event_pk=pts_event.pk,
            initiator=self.operator, operation_name='piglets_to_sows')
        self.assertEqual(Sow.objects.all().count(), 0)
        self.assertEqual(SowTransaction.objects.all().count(), 0)
        self.assertEqual(PigletsToSowsEvent.objects.all().count(), 0)
        self.assertEqual(WeighingPiglets.objects.all().count(), 0)

        self.assertEqual(Piglets.objects.get_all().count(), 1)
        self.assertEqual(Piglets.objects.get_all().first(), piglets1)
        self.assertEqual(Piglets.objects.all().count(), 1)
        self.assertEqual(Piglets.objects.all().first(), piglets1)
        
        piglets1.refresh_from_db()
        self.assertEqual(piglets1.active, True)
        self.assertEqual(PigletsSplit.objects.all().count(), 0)

        self.assertEqual(rollback.user_employee.username, 'brigadir5')
        self.assertEqual(rollback.workshop.number, 5)

    def test_create_piglets_to_sows_event_rollback(self):
        piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.locs_ws5[0], 100)

        WeighingPiglets.objects.create_weighing(piglets_group=piglets1,
            total_weight=1560, place='o/2')

        pts_event = PigletsToSowsEvent.objects.create_event(piglets=piglets1,
            initiator=self.brig5)
        self.assertEqual(Sow.objects.all().count(), 100)
        self.assertEqual(SowTransaction.objects.all().count(), 100)
        self.assertEqual(WeighingPiglets.objects.all().count(), 1)
        piglets1.refresh_from_db()
        self.assertEqual(piglets1.active, False)

        rollback = Rollback.objects.create_piglets_to_sows_event_rollback(event_pk=pts_event.pk,
            initiator=self.operator, operation_name='piglets_to_sows')
        self.assertEqual(Sow.objects.all().count(), 0)
        self.assertEqual(SowTransaction.objects.all().count(), 0)
        self.assertEqual(PigletsToSowsEvent.objects.all().count(), 0)
        self.assertEqual(WeighingPiglets.objects.all().count(), 0)

        piglets1.refresh_from_db()
        self.assertEqual(piglets1.active, True)

        self.assertEqual(rollback.user_employee.username, 'brigadir5')
        self.assertEqual(rollback.workshop.number, 5)

    def test_create_piglets_to_sows_event_rollback_split_before(self):
        piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.locs_ws5[0], 100)

        transaction, moved_piglets, stayed_piglets, split_event, merge_even = \
            PigletsTransaction.objects.transaction_with_split_and_merge(
                    piglets=piglets1,
                    new_amount=60,
                    to_location=self.locs_ws5[1],
                    initiator=self.brig5
                    )

        WeighingPiglets.objects.create_weighing(piglets_group=moved_piglets,
            total_weight=1560, place='o/2')
        pts_event = PigletsToSowsEvent.objects.create_event(piglets=moved_piglets,
            initiator=self.brig5)

        self.assertEqual(Sow.objects.all().count(), 60)
        self.assertEqual(SowTransaction.objects.all().count(), 60)
        self.assertEqual(WeighingPiglets.objects.all().count(), 1)
        self.assertEqual(Piglets.objects.get_all().count(), 3)
        self.assertEqual(Piglets.objects.all().count(), 1)
        self.assertEqual(Piglets.objects.all().first(), stayed_piglets)
        self.assertEqual(PigletsSplit.objects.all().count(), 1)

        rollback = Rollback.objects.create_piglets_to_sows_event_rollback(event_pk=pts_event.pk,
            initiator=self.operator, operation_name='piglets_to_sows')

        self.assertEqual(Sow.objects.all().count(), 0)
        self.assertEqual(SowTransaction.objects.all().count(), 0)
        self.assertEqual(PigletsToSowsEvent.objects.all().count(), 0)
        self.assertEqual(WeighingPiglets.objects.all().count(), 0)
        self.assertEqual(PigletsSplit.objects.all().count(), 1)

        self.assertEqual(Piglets.objects.get_all().count(), 3)
        piglets1.refresh_from_db()
        moved_piglets.refresh_from_db()
        stayed_piglets.refresh_from_db()
        self.assertEqual(piglets1.active, False)
        self.assertEqual(stayed_piglets.active, True)
        self.assertEqual(moved_piglets.active, True)

        self.assertEqual(rollback.user_employee.username, 'brigadir5')
        self.assertEqual(rollback.workshop.number, 5)

    def test_create_mark_as_gilt_rollback(self):
        piglets1 = piglets_testing.create_from_sow_farrow(location=self.locs_ws3[0],
            quantity=15, tour=self.tour1)
        sow = piglets1.farrow.sow

        gilt = Gilt.objects.create_gilt(
          birth_id='123',
          mother_sow_farm_id=sow.farm_id,
          piglets=piglets1              
          )

        event = MarkAsGilt.objects.create_init_gilt_event(gilt=gilt,
         initiator=self.brig3)

        rollback = Rollback.objects.create_mark_as_gilt_rollback(event_pk=event.pk,
            initiator=self.operator, operation_name='mark_as_gilt')
        self.assertEqual(Gilt.objects.all().count(), 0)
        self.assertEqual(MarkAsGilt.objects.all().count(), 0)

    def test_create_ws3_weaning_piglets_rollback(self):
        piglets1 = piglets_testing.create_from_sow_farrow(self.tour1,
            self.locs_ws3[0], 10)
        piglets2 = piglets_testing.create_from_sow_farrow(self.tour1,
            self.locs_ws3[1], 15)
        piglets3 = piglets_testing.create_from_sow_farrow(self.tour1,
            self.locs_ws3[2], 13)
        piglets4 = piglets_testing.create_from_sow_farrow(self.tour1,
            self.locs_ws3[3], 9)

        new_location = Location.objects.get(workshop__number=3)
        merging_list = [
            {'piglets_id': piglets1.pk, 'changed': True, 'quantity': 7 },
            {'piglets_id': piglets2.pk, 'changed': True, 'quantity': 12 },
            {'piglets_id': piglets3.pk, 'changed': False },
        ]
        piglets_to_ws4 = PigletsMerger.objects.create_from_merging_list(
            merging_list=merging_list, new_location=new_location, initiator=self.brig3,
            )
        piglets_to_ws4.change_status_to('Готовы ко взвешиванию')

        to_location = Location.objects.get(workshop__number=4)
        transaction = PigletsTransaction.objects.create_transaction(
            to_location=to_location, piglets_group=piglets_to_ws4,
            initiator=self.brig3)

        self.assertEqual(piglets_to_ws4.quantity, 32)
        self.assertEqual(piglets_to_ws4.location.workshop.number, 4)
        self.assertEqual(WeaningSow.objects.all().count(), 3)

        rollback = Rollback.objects.create_ws3_weaning_piglets_rollback(event_pk=transaction.pk,
            initiator=self.operator, operation_name='ws3_weaning_piglets')

        self.assertEqual(Piglets.objects.get_all().count(), Piglets.objects.all().count())
        self.assertEqual(Piglets.objects.get_all().count(), 4)
        self.assertEqual(PigletsTransaction.objects.all().count(), 0)
        self.assertEqual(PigletsSplit.objects.all().count(), 0)
        self.assertEqual(PigletsMerger.objects.all().count(), 0)
        self.assertEqual(WeaningSow.objects.all().count(), 0)

    def test_check_piglets_permission(self):
        piglets1 = piglets_testing.create_from_sow_farrow(self.tour1,
            self.locs_ws3[0], 100)

        transaction, moved_piglets, stayed_piglets, split_event, merge_event = \
            PigletsTransaction.objects.transaction_with_split_and_merge(
            piglets=piglets1, to_location=self.locs_ws4[1], merge=True, initiator=self.brig4,
            new_amount=40)

        transaction2, moved_piglets, stayed_piglets, split_event, merge_event = \
            PigletsTransaction.objects.transaction_with_split_and_merge(
            piglets=moved_piglets, to_location=self.locs_ws4[2], merge=True, initiator=self.brig4,
            new_amount=10)

        with self.assertRaises(ValidationError):
            rollback = Rollback.objects.create_piglets_transactions_rollback(event_pk=transaction.pk,
                initiator=self.operator, operation_name='piglets_transaction')

    def test_piglets_to_sows_permission(self):
        piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.locs_ws5[0], 100)

        WeighingPiglets.objects.create_weighing(piglets_group=piglets1,
            total_weight=1560, place='o/2')

        pts_event = PigletsToSowsEvent.objects.create_event(piglets=piglets1,
            initiator=self.brig5)

        sow = pts_event.sows.all().first()
        SowTransaction.objects.create_transaction(sow=sow, to_location=self.loc_ws1)

        with self.assertRaises(ValidationError):
            rollback = Rollback.objects.create_piglets_to_sows_event_rollback(event_pk=pts_event.pk,
                initiator=self.operator, operation_name='piglets_to_sows')


class SowsRollbackModelTest(TransactionTestCase):
    def setUp(self):
        locations_testing.create_workshops_sections_and_cells()
        sows_testing.create_statuses()
        sows_events_testing.create_types()
        piglets_testing.create_piglets_statuses()
        staff_testings.create_svinbin_users()

        self.tour1 = Tour.objects.get_or_create_by_week_in_current_year(week_number=1)
        self.tour2 = Tour.objects.get_or_create_by_week_in_current_year(week_number=2)

        self.loc_ws1 = Location.objects.get(workshop__number=1)
        self.loc_ws2 = Location.objects.get(workshop__number=2)
        self.locs_ws3 = Location.objects.filter(sowAndPigletsCell__workshop__number=3)
        self.locs_ws4 = Location.objects.filter(pigletsGroupCell__workshop__number=4)
        self.locs_ws5 = Location.objects.filter(pigletsGroupCell__workshop__number=5)

        self.brig3 = User.objects.get(username='brigadir3')
        self.brig4 = User.objects.get(username='brigadir4')
        self.brig5 = User.objects.get(username='brigadir5')
        self.operator = User.objects.get(username='shmigina')

    def test_create_mark_as_nurse_rollback(self):
        piglets1 = piglets_testing.create_from_sow_farrow(location=self.locs_ws3[0],
            quantity=15, tour=self.tour1)
        sow = piglets1.farrow.sow
        self.assertEqual(sow.status.title, 'Опоросилась')

        mas_event = MarkAsNurse.objects.create_nurse_event(sow=sow, initiator=self.brig3, 
            date=datetime.now() + timedelta(seconds=10))
        self.assertEqual(sow.status.title, 'Кормилица')
        self.assertEqual(sow.tour, None)
        self.assertEqual(SowStatusRecord.objects.filter(status_after__title='Кормилица').count(),
            1)

        rollback = Rollback.objects.create_mark_as_nurse_rollback(event_pk=mas_event.pk,
            initiator=self.operator, operation_name='mark_as_nurse')

        sow.refresh_from_db()
        self.assertEqual(sow.status.title, 'Опоросилась')
        self.assertEqual(sow.tour, self.tour1)
        self.assertEqual(SowStatusRecord.objects.filter(status_after__title='Кормилица').count(),
            0)

    def test_create_farrow_rollback(self):
        # piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
        #     self.locs_ws5[0], 100)

        sow = sows_testing.create_sow_with_semination_usound(location=self.locs_ws3[0],
         week=self.tour1.week_number)
        farrow = SowFarrow.objects.create_sow_farrow(sow=sow, alive_quantity=15,
         initiator=self.brig3)
        piglets1 = farrow.piglets_group
        
        self.assertEqual(SowFarrow.objects.all().count(), 1)
        self.assertEqual(sow.status.title, 'Опоросилась')

        rollback = Rollback.objects.create_farrow_rollback(event_pk=farrow.pk,
            initiator=self.operator, operation_name='farrow')

        self.assertEqual(Piglets.objects.filter(pk=piglets1.pk).count(), 0)

        sow.refresh_from_db()
        self.assertEqual(sow.status.title, 'Супорос 35')
        self.assertEqual(SowFarrow.objects.all().count(), 0)

    def test_create_farrow_with_merge_rollback(self):
        piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.locs_ws3[0], 10)

        sow = sows_testing.create_sow_with_semination_usound(location=self.locs_ws3[0],
         week=self.tour1.week_number)
        farrow = SowFarrow.objects.create_sow_farrow(sow=sow, alive_quantity=15,
         initiator=self.brig3)
        piglets2 = farrow.piglets_group
        
        self.assertEqual(SowFarrow.objects.all().count(), 1)
        self.assertEqual(sow.status.title, 'Опоросилась')
        self.assertEqual(Piglets.objects.all().count(), 1)
        self.assertEqual(Piglets.objects.all().first().quantity, 25)

        rollback = Rollback.objects.create_farrow_rollback(event_pk=farrow.pk,
            initiator=self.operator, operation_name='farrow')

        sow.refresh_from_db()
        self.assertEqual(sow.status.title, 'Супорос 35')
        self.assertEqual(SowFarrow.objects.all().count(), 0)

        self.assertEqual(Piglets.objects.all().count(), 1)
        self.assertEqual(Piglets.objects.filter(pk=piglets2.pk).first(), None)
        piglets1.refresh_from_db()
        self.assertEqual(piglets1.quantity, 10)
        self.assertEqual(piglets2.quantity, 15)
        self.assertEqual(piglets1.active, True)

    def test_create_sow_culling_rollback(self):
        sow = sows_testing.create_sow_with_semination_usound(location=self.locs_ws3[0],
         week=self.tour1.week_number)

        culling = CullingSow.objects.create_culling(sow=sow, culling_type='padej', initiator=self.brig3)
        self.assertEqual(Sow.objects.all().count(), 0)
        self.assertEqual(Sow.objects.get_queryset_with_not_alive().first().status.title, 'Брак')

        rollback = Rollback.objects.create_sow_culling_rollback(event_pk=culling.pk,
            initiator=self.operator, operation_name='sow_culling')

        sow.refresh_from_db()
        self.assertEqual(sow.alive, True)
        self.assertEqual(sow.status.title, 'Супорос 35')
        self.assertEqual(CullingSow.objects.filter(pk=culling.pk).count(), 0)

    def test_create_ultrasound_rollback(self):
        sow = sows_testing.create_sow_with_semination(location=self.locs_ws3[0],
            week=self.tour1.week_number, date=datetime(2020,12,20))
        self.assertEqual(sow.status.title, 'Осеменена 1')

        usound = Ultrasound.objects.create_ultrasound(sow=sow, result=True, days=30, initiator=self.brig3)
        self.assertEqual(sow.status.title, 'Супорос 28')

        rollback = Rollback.objects.create_ultrasound_rollback(event_pk=usound.pk,
            initiator=self.operator, operation_name='ultrasound')
        sow.refresh_from_db()
        self.assertEqual(sow.status.title, 'Осеменена 1')
        self.assertEqual(Ultrasound.objects.filter(pk=usound.pk).count(), 0)

        usound2 = Ultrasound.objects.create_ultrasound(sow=sow, result=False, days=30,
         initiator=self.brig3)
        self.assertEqual(sow.status.title, 'Прохолост')
        self.assertEqual(sow.tour, None)

        rollback2 = Rollback.objects.create_ultrasound_rollback(event_pk=usound2.pk,
            initiator=self.operator, operation_name='ultrasound')
        sow.refresh_from_db()
        self.assertEqual(sow.status.title, 'Осеменена 1')
        self.assertEqual(sow.tour, self.tour1)
        self.assertEqual(Ultrasound.objects.filter(pk=usound2.pk).count(), 0)

    def test_create_semination_rollback(self):
        sow = sows_testing.create_sow_with_location(location=self.locs_ws3[0])

        semination = Semination.objects.create_semination_tour(sow=sow, tour=self.tour1,
         initiator=self.brig3)
        self.assertEqual(sow.status.title, 'Осеменена 1')

        rollback = Rollback.objects.create_semination_rollback(event_pk=semination.pk,
            initiator=self.operator, operation_name='semination')

        sow.refresh_from_db()
        self.assertEqual(sow.status, None)
        self.assertEqual(sow.tour, None)
        self.assertEqual(Semination.objects.filter(pk=semination.pk).count(), 0)

        semination1 = Semination.objects.create_semination_tour(sow=sow, tour=self.tour1,
         initiator=self.brig3)
        self.assertEqual(sow.status.title, 'Осеменена 1')

        semination2 = Semination.objects.create_semination_tour(sow=sow, tour=self.tour1,
         initiator=self.brig3)
        self.assertEqual(sow.status.title, 'Осеменена 2')

        rollback = Rollback.objects.create_semination_rollback(event_pk=semination2.pk,
            initiator=self.operator, operation_name='semination')

        sow.refresh_from_db()
        self.assertEqual(sow.status.title, 'Осеменена 1')
        self.assertEqual(sow.tour, self.tour1)
        self.assertEqual(Semination.objects.filter(pk=semination2.pk).count(), 0)

    def test_create_sow_transaction_rollback(self):
        sow = sows_testing.create_sow_with_location(location=self.loc_ws1)

        transaction = SowTransaction.objects.create_transaction(sow=sow, to_location=self.loc_ws2,
            initiator=self.operator)

        rollback = Rollback.objects.create_sow_transaction_rollback(event_pk=transaction.pk,
            initiator=self.operator, operation_name='sow_transaction')

        sow.refresh_from_db()
        self.assertEqual(sow.location, self.loc_ws1)
        self.assertEqual(SowTransaction.objects.all().count(), 0)

    def test_create_sow_transaction_rollback_v2(self):
        # weaning transaction from cell to ws 1-2
        piglets = piglets_testing.create_from_sow_farrow(location=self.locs_ws3[0], tour=self.tour1,
            quantity=10)
        sow = piglets.farrow.sow
        self.assertEqual(sow.status.title, 'Опоросилась')
        self.assertEqual(sow.tour, self.tour1)

        transaction = SowTransaction.objects.create_transaction(sow=sow, to_location=self.loc_ws1,
            initiator=self.operator, date=(datetime.now() + timedelta(minutes=1)))

        sow.refresh_from_db()
        self.assertEqual(sow.status.title, 'Ожидает осеменения')
        self.assertEqual(sow.tour, None)

        rollback = Rollback.objects.create_sow_transaction_rollback(event_pk=transaction.pk,
            initiator=self.operator, operation_name='sow_transaction')

        sow.refresh_from_db()
        self.assertEqual(sow.status.title, 'Опоросилась')
        self.assertEqual(sow.tour, self.tour1)
        self.assertEqual(sow.location, self.locs_ws3[0])
        self.assertEqual(SowTransaction.objects.all().count(), 0)

    def test_create_sow_abort_rollback(self):
        # weaning transaction from cell to ws 1-2
        piglets = piglets_testing.create_from_sow_farrow(location=self.locs_ws3[0], tour=self.tour1,
            quantity=10)
        sow = piglets.farrow.sow
        self.assertEqual(sow.status.title, 'Опоросилась')
        self.assertEqual(sow.tour, self.tour1)

        abortion = AbortionSow.objects.create_abortion(sow=sow, initiator=self.operator)

        sow.refresh_from_db()
        self.assertEqual(sow.status.title, 'Аборт')
        self.assertEqual(sow.tour, None)

        rollback = Rollback.objects.create_abort_rollback(event_pk=abortion.pk,
            initiator=self.operator, operation_name='sow_abort')

        sow.refresh_from_db()
        self.assertEqual(sow.status.title, 'Опоросилась')
        self.assertEqual(sow.tour, self.tour1)
        self.assertEqual(sow.location, self.locs_ws3[0])
        self.assertEqual(SowTransaction.objects.all().count(), 0)

    def test_check_sow_permission(self):
        sow = sows_testing.create_sow_with_location(location=self.loc_ws1)

        transaction = SowTransaction.objects.create_transaction(sow=sow, to_location=self.loc_ws2,
            initiator=self.operator, date=datetime(2021, 2, 3, 0, 0))

        semination1 = Semination.objects.create_semination_tour(sow=sow, tour=self.tour1,
         initiator=self.brig3, date=datetime(2021, 2, 3, 15, 0))

        with self.assertRaises(ValidationError):
            rollback = Rollback.objects.create_sow_transaction_rollback(event_pk=transaction.pk,
                initiator=self.operator, operation_name='sow_transaction')