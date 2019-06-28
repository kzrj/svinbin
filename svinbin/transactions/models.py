# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
from django.conf import settings

from core.models import CoreModel, CoreModelManager, Event


class Transaction(Event):
    class Meta:
        abstract = True


class SowTransactionManager(CoreModelManager):
    def create_transaction(self, to_location, sow, initiator=None):
        # need to refractor to atomic transactions.
        transaction = SowTransaction.objects.create(
                date=timezone.now(),
                initiator=initiator,
                from_location=sow.location,
                to_location=to_location,
                sow=sow
                )

        sow.change_sow_current_location(to_location)

        return transaction

    def create_many_transactions(self, sows, to_location, initiator=None):
        transactions_ids = list()
        for sow in sows:
            transaction = self.create_transaction(to_location, sow, initiator)
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

        piglets_group.change_current_location(to_location)

        return transaction


class PigletsTransaction(Transaction):
    from_location = models.ForeignKey('locations.Location', on_delete=models.CASCADE,
     related_name="piglets_transaction_from")
    to_location = models.ForeignKey('locations.Location', on_delete=models.CASCADE,
     related_name="piglets_transaction_to")
    piglets_group = models.ForeignKey('piglets.NomadPigletsGroup',
     on_delete=models.CASCADE, related_name="transactions")

    objects = PigletsTransactionManager()

    
# class GiltTransaction(Transaction):
#     from_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="gilt_from_location")
#     to_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="gilt_to_location")
#     gilt = models.ForeignKey('sows.Gilt', on_delete=models.CASCADE)