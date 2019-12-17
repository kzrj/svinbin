# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.core.exceptions import ValidationError

from core.models import CoreModel, CoreModelManager, Event
from sows_events.models import WeaningSow
from locations.models import SowAndPigletsCell, Location
from piglets.models import Piglets
from piglets_events.models import PigletsMerger, PigletsSplit


class Transaction(Event):
    class Meta:
        abstract = True


class SowTransactionManager(CoreModelManager):
    def create_transaction(self, sow, to_location,  initiator=None):
        # need to refractor to atomic transactions.

        if isinstance(to_location.get_location, SowAndPigletsCell) and not to_location.is_sow_empty:
            raise ValidationError(message='Клетка №{} не пустая'. \
                format(to_location.sowAndPigletsCell.number))

        transaction = SowTransaction.objects.create(
                date=timezone.now(),
                initiator=initiator,
                from_location=sow.location,
                to_location=to_location,
                sow=sow
                )

        if sow.is_farrow_in_current_tour:
            WeaningSow.objects.create_weaning(sow=sow, transaction=transaction,
                initiator=initiator)

        sow.change_sow_current_location(to_location)

        return transaction

    def create_many_transactions(self, sows, to_location, initiator=None):
        transactions_ids = list()
        for sow in sows:
            transaction = self.create_transaction(sow, to_location, initiator)
            transactions_ids.append(transaction.pk)
        return transactions_ids


class SowTransaction(Transaction):
    from_location = models.ForeignKey('locations.Location', on_delete=models.CASCADE,
     related_name="sow_transactions_from")
    to_location = models.ForeignKey('locations.Location', on_delete=models.CASCADE,
     related_name="sow_transactions_to")
    sow = models.ForeignKey('sows.Sow', on_delete=models.CASCADE, related_name='transactions')

    objects = SowTransactionManager()


class PigletsTransactionManager(CoreModelManager):
    def create_transaction(self, to_location, piglets_group, initiator=None):
        transaction = PigletsTransaction.objects.create(
                date=timezone.now(),
                initiator=initiator,
                from_location=piglets_group.location,
                to_location=to_location,
                piglets_group=piglets_group
                )

        piglets_group.change_location(to_location)

        return transaction

    # def split_then_move_first(self, piglets, to_location, new_amount=None, initiator=None):
    #     # stayed = new_amount
    #     moved_piglets, stayed_piglets = PigletsSplit.objects.split_return_groups( \
    #             parent_piglets=piglets, new_amount=new_amount, initiator=initiator)

    #     transaction = self.create_transaction(to_location, moved_piglets, initiator)

    #     return transaction, moved_piglets, stayed_piglets

    # def split_then_move_second(self, piglets, to_location, new_amount=None, initiator=None):
    #     # moved = new_amount
    #     stayed_piglets, moved_piglets = PigletsSplit.objects.split_return_groups( \
    #             parent_piglets=piglets, new_amount=new_amount, initiator=initiator)
        
    #     transaction = self.create_transaction(to_location, moved_piglets, initiator)

    #     return transaction, moved_piglets, stayed_piglets


    def transaction_with_split_and_merge(self, piglets, to_location, new_amount=None, reverse=False,
            merge=False, initiator=None):
        # move second piglets from split, new_amount piglets

        split_event = None
        merge_event = None

        if new_amount:
            piglets1, piglets2_new_amount = PigletsSplit.objects.split_return_groups( \
                parent_piglets=piglets, new_amount=new_amount, initiator=initiator)
            
            if reverse:
                moved_piglets = piglets1
                stayed_piglets = piglets2_new_amount
            else:
                moved_piglets = piglets2_new_amount
                stayed_piglets = piglets1

        transaction = self.create_transaction(to_location, moved_piglets, initiator)

        if merge:
            # to merger manager
            in_cell_piglets = to_location.piglets.all()
            if in_cell_piglets.count() > 1:
                moved_piglets = PigletsMerger.objects.create_merger_return_group(
                    parent_piglets=in_cell_piglets, new_location=to_location,
                    initiator=initiator)

        return transaction, moved_piglets, stayed_piglets, split_event, merge_event

    # def transaction_with_split_and_merge_v2(self, piglets, to_location, new_amount=None, merge=False,
    #      initiator=None):
    #     # move first piglets from split, not new_amount piglets

    #     split_event = None
    #     merge_event = None

    #     if new_amount:
    #         piglets1, piglets2_new_amount = PigletsSplit.objects.split_return_groups( \
    #             parent_piglets=piglets, new_amount=new_amount, initiator=initiator)
    #         piglets = piglets1

    #     transaction = self.create_transaction(to_location, piglets, initiator)

    #     if merge:
    #         in_cell_piglets = to_location.piglets.all()
    #         if in_cell_piglets.count() > 1:
    #             piglets = PigletsMerger.objects.create_merger_return_group(
    #                 parent_piglets=in_cell_piglets, new_location=to_location,
    #                 initiator=initiator)

    #     return transaction, piglets, split_event, merge_event


class PigletsTransaction(Transaction):
    from_location = models.ForeignKey('locations.Location', on_delete=models.CASCADE,
     related_name="piglets_transaction_from")
    to_location = models.ForeignKey('locations.Location', on_delete=models.CASCADE,
     related_name="piglets_transaction_to")
    piglets_group = models.ForeignKey('piglets.Piglets', on_delete=models.CASCADE,
     related_name="transactions")

    objects = PigletsTransactionManager()