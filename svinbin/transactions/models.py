# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.core.exceptions import ValidationError as DjangoValidationError

from core.models import CoreModel, CoreModelManager, Event
from locations.models import SowAndPigletsCell, Location
from piglets.models import Piglets
from piglets_events.models import PigletsMerger, PigletsSplit


class Transaction(Event):
    class Meta:
        abstract = True


class SowTransactionManager(CoreModelManager):
    def create_transaction(self, sow, to_location,  initiator=None):
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

        sow.change_sow_current_location(to_location)

        return transaction

    def create_transaction_with_resetellment(self, sow_in, to_location, initiator=None):
        sow_out = None
        if sow_in.status.title != 'Супорос 35':
            raise DjangoValidationError(message=f'Свинья {sow_out.farm_id} не Супорос 35.') 

        if isinstance(to_location.get_location, SowAndPigletsCell) and not to_location.is_sow_empty:
            sow_out = to_location.sow_set.all().first()

        if sow_out:
            if sow_out.status.title != 'Супорос 35':
                raise DjangoValidationError(message=f'Свинья {sow_out.farm_id} в клетке не Супорос 35.')
            self.create_transaction(sow_out, Location.objects.get(workshop__number=3), initiator)

        return self.create_transaction(sow_in, to_location, initiator)

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
    def create_transaction(self, to_location, piglets_group, initiator=None, date=timezone.now()):
        transaction = PigletsTransaction.objects.create(
                date=date,
                initiator=initiator,
                from_location=piglets_group.location,
                to_location=to_location,
                piglets_group=piglets_group
                )

        # we should remove status "взвешены"
        if piglets_group.location.workshop and to_location.pigletsGroupCell:
            piglets_group.change_status_to_without_save('Кормятся')

        if piglets_group.location.pigletsGroupCell and to_location.workshop:
            piglets_group.change_status_to_without_save('Готовы ко взвешиванию')

        piglets_group.change_location(to_location)

        return transaction

    def transaction_with_split_and_merge(self, piglets, to_location, new_amount=None, gilts_contains=False,
         reverse=False, merge=False, initiator=None):
        # move second piglets from split, new_amount piglets

        split_event = None
        merge_event = None
        stayed_piglets = None
        moved_piglets = piglets

        if new_amount:
            piglets1, piglets2_new_amount = PigletsSplit.objects.split_return_groups( \
                parent_piglets=piglets, new_amount=new_amount, gilts_to_new=gilts_contains,\
                initiator=initiator)
            
            moved_piglets = piglets2_new_amount
            stayed_piglets = piglets1
            split_event = piglets.split_as_parent
            
            if reverse:
                moved_piglets = piglets1
                stayed_piglets = piglets2_new_amount

        transaction = self.create_transaction(to_location, moved_piglets, initiator)

        if merge:            
            moved_piglets = PigletsMerger.objects.merge_piglets_in_location(
                location=to_location, initiator=initiator)
            if hasattr(moved_piglets, 'merger_as_child'):
                merge_event = moved_piglets.merger_as_child

        return transaction, moved_piglets, stayed_piglets, split_event, merge_event


class PigletsTransaction(Transaction):
    from_location = models.ForeignKey('locations.Location', on_delete=models.CASCADE,
     related_name="piglets_transaction_from")
    to_location = models.ForeignKey('locations.Location', on_delete=models.CASCADE,
     related_name="piglets_transaction_to")
    piglets_group = models.ForeignKey('piglets.Piglets', on_delete=models.CASCADE,
     related_name="transactions")

    objects = PigletsTransactionManager()