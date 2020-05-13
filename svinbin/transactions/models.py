# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
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
            raise DjangoValidationError(message='Клетка №{} не пустая'. \
                format(to_location.sowAndPigletsCell.number))

        transaction = self.create(
                date=timezone.now(),
                initiator=initiator,
                from_location=sow.location,
                to_location=to_location,
                sow=sow
                )

        if sow.status and sow.status.title == 'Опоросилась' and to_location.workshop:
            if to_location.workshop.number == 1  and sow.location.sowAndPigletsCell:
                sow.tour = None
                sow.change_status_to('Ожидает осеменения')

        if sow.status and sow.status.title != 'Супорос 35' and to_location.workshop: 
            if to_location.workshop.number == 3 and sow.location.workshop and \
                sow.location.workshop.number in [1, 2]:
                raise DjangoValidationError(message=f'Свиноматка №{sow.farm_id} супорос' )

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
    def create_transaction(self, to_location, piglets_group, initiator=None, date=timezone.now()):
        transaction = PigletsTransaction.objects.create(
                date=date,
                initiator=initiator,
                from_location=piglets_group.location,
                to_location=to_location,
                piglets_group=piglets_group,
                quantity=piglets_group.quantity
                )

        # we should remove status "взвешены"
        if piglets_group.location.workshop and to_location.pigletsGroupCell:
            piglets_group.change_status_to_without_save('Кормятся')

        if piglets_group.location.pigletsGroupCell and to_location.workshop:
            piglets_group.change_status_to_without_save('Готовы ко взвешиванию')

        if piglets_group.location.workshop and to_location.workshop \
            and to_location.workshop.number != 4 \
            and piglets_group.location.workshop.number != 3:
            piglets_group.change_status_to_without_save('Взвешены, готовы к заселению')

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

    def dercrease_gilts_from_ws(self, piglets, gilts_amount):
        if piglets.gilts_quantity >= gilts_amount:
            piglets.gilts_quantity = piglets.gilts_quantity - gilts_amount
        else:
            gilts_to_decrease = gilts_amount - piglets.gilts_quantity
            piglets.gilts_quantity = 0

            workshop = piglets.location.get_workshop
            piglets_in_ws_with_gilts = Piglets.objects.all().all_in_workshop(workshop.number)\
                    .filter(gilts_quantity__gt=0).exclude(pk=piglets.pk)

            for piglets_with_gilts in piglets_in_ws_with_gilts:
                if piglets_with_gilts.gilts_quantity >= gilts_to_decrease:
                    piglets_with_gilts.gilts_quantity = piglets_with_gilts.gilts_quantity - gilts_to_decrease
                    piglets_with_gilts.save()
                    break
                else:
                    gilts_to_decrease = gilts_to_decrease - piglets_with_gilts.gilts_quantity
                    piglets_with_gilts.gilts_quantity = 0
                    piglets_with_gilts.save()

        piglets.save()

        return piglets

    def transaction_gilts_to_7_5(self, piglets, gilts_amount=None, initiator=None):
        # split or not
        if gilts_amount and gilts_amount < piglets.quantity:
            # split check amount
            piglets = self.dercrease_gilts_from_ws(piglets=piglets, gilts_amount=gilts_amount)

            stayed_piglets, piglets_to_transfer = PigletsSplit.objects.split_return_groups( \
                parent_piglets=piglets, new_amount=gilts_amount, gilts_to_new=None, initiator=initiator)
        else:
            gilts_amount = piglets.quantity
            piglets_to_transfer = self.dercrease_gilts_from_ws(piglets=piglets, gilts_amount=piglets.quantity)
        
        piglets_to_transfer.gilts_quantity = gilts_amount
        piglets_to_transfer.save()

        to_location = Location.objects.get(workshop__number=11)
        return self.create_transaction(to_location, piglets_to_transfer, initiator)


class PigletsTransaction(Transaction):
    from_location = models.ForeignKey('locations.Location', on_delete=models.CASCADE,
     related_name="piglets_transaction_from")
    to_location = models.ForeignKey('locations.Location', on_delete=models.CASCADE,
     related_name="piglets_transaction_to")
    piglets_group = models.ForeignKey('piglets.Piglets', on_delete=models.CASCADE,
     related_name="transactions")

    quantity = models.IntegerField(null=True)

    objects = PigletsTransactionManager()