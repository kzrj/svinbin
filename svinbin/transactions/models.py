# -*- coding: utf-8 -*-
from datetime import timedelta, date, datetime

from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError as DjangoValidationError

from core.models import CoreModel, CoreModelManager, Event, CoreQuerySet
from locations.models import SowAndPigletsCell, Location
from piglets.models import Piglets
from piglets_events.models import PigletsMerger, PigletsSplit


class Transaction(Event):
    class Meta:
        abstract = True


class SowTransactionQuerySet(CoreQuerySet):
    pass


class SowTransactionManager(CoreModelManager):
    def get_queryset(self):
        return SowTransactionQuerySet(self.model, using=self._db)

    def reset_related(self):
        return SowTransactionQuerySet(self.model, using=self._db).all()

    def create_transaction(self, sow, to_location,  initiator=None, date=None):
        if isinstance(to_location.get_location, SowAndPigletsCell) and not to_location.is_sow_empty:
            raise DjangoValidationError(message='Клетка №{} не пустая'. \
                format(to_location.sowAndPigletsCell.number))

        if not date:
            date = timezone.now()

        transaction = self.create(
                date=date,
                initiator=initiator,
                from_location=sow.location,
                to_location=to_location,
                sow=sow,
                tour=sow.tour,
                sow_status=sow.status,
                sow_group=sow.sow_group
                )

        if transaction.is_weaning_transaction_from_ws3_to_ws12():
            sow.tour = None
            sow.change_group_to(group_title='С опоросом', date=date)
            sow.change_status_to('Ожидает осеменения')

        if sow.status and sow.status.title != 'Супорос 35' and to_location.workshop: 
            if to_location.workshop.number == 3 and sow.location.workshop and \
                sow.location.workshop.number in [1, 2]:
                raise DjangoValidationError(message=f'Свиноматка №{sow.farm_id} не супорос' )

        sow.change_sow_current_location(to_location)

        return transaction

    def create_many_transactions(self, sows, to_location, initiator=None, date=None):
        if not date:
            date = timezone.now()

        transactions_ids = list()
        for sow in sows:
            transaction = self.create_transaction(sow=sow, to_location=to_location, initiator=initiator,
                date=date)
            transactions_ids.append(transaction.pk)
        return transactions_ids

    def create_many_without_status_check(self, sows, to_location, initiator=None, date=None):
        if not date:
            date = timezone.now()

        trs = list()
        for sow in sows:
            trs.append(
                SowTransaction(
                    date=date,
                    initiator=initiator,
                    from_location=sow.location,
                    to_location=to_location,
                    sow=sow,
                    tour=sow.tour,
                    sow_status=sow.status,
                    sow_group=sow.sow_group)
                )
        self.bulk_create(trs)
        sows.update(location=to_location)

    def trs_in_ws(self, ws_number, ws_locs, start_date=date(2020, 1, 1), end_date=datetime.today()):
        return self.filter(date__date__gte=start_date, date__date__lte=end_date,
            to_location__workshop__number=ws_number).exclude(from_location__in=ws_locs)

    def trs_out_ws(self, ws_locs, start_date=date(2020, 1, 1), end_date=datetime.today()):
        return self.filter(date__date__gte=start_date, date__date__lte=end_date,
            from_location__in=ws_locs).exclude(to_location__in=ws_locs)


class SowTransaction(Transaction):
    from_location = models.ForeignKey('locations.Location', on_delete=models.CASCADE,
     related_name="sow_transactions_from")
    to_location = models.ForeignKey('locations.Location', on_delete=models.CASCADE,
     related_name="sow_transactions_to")
    sow = models.ForeignKey('sows.Sow', on_delete=models.CASCADE, related_name='transactions')

    tour = models.ForeignKey('tours.Tour', on_delete=models.SET_NULL, null=True,
        related_name='sow_transactions')

    sow_status = models.ForeignKey('sows.SowStatus', on_delete=models.SET_NULL, null=True)
    sow_group = models.ForeignKey('sows.SowGroup', on_delete=models.SET_NULL, null=True, blank=True)

    objects = SowTransactionManager()

    def is_weaning_transaction_from_ws3_to_ws12(self):
        if self.sow_status \
          and (self.sow_status.title == 'Опоросилась' or self.sow_status.title == 'Отъем') \
          and self.to_location.workshop and self.to_location.workshop.number in [1, 2] \
          and self.from_location.sowAndPigletsCell:
                return True
        return False

class PigletsTransactionManager(CoreModelManager):
    def create_transaction(self, to_location, piglets_group, initiator=None, date=None, 
        split_event=None):
        if not date:
            date= timezone.now()

        transaction = PigletsTransaction.objects.create(
                date=date,
                initiator=initiator,
                from_location=piglets_group.location,
                to_location=to_location,
                piglets_group=piglets_group,
                quantity=piglets_group.quantity,
                week_tour=piglets_group.metatour.week_tour,
                split_event=split_event
                )

        if piglets_group.location.pigletsGroupCell and to_location.workshop:
            piglets_group.change_status_to_without_save('Готовы ко взвешиванию')

        if piglets_group.location.workshop and to_location.workshop \
            and to_location.workshop.number != 4 \
            and piglets_group.location.workshop.number != 3:
            piglets_group.change_status_to_without_save('Взвешены, готовы к заселению')

        piglets_group.change_location(to_location)

        return transaction

    def transaction_with_split_and_merge(self, piglets, to_location, new_amount=None, reverse=False,
         merge=False, initiator=None, date=None):
        # move second piglets from split, new_amount piglets
        split_event = None
        merge_event = None
        stayed_piglets = None
        moved_piglets = piglets

        if new_amount:
            piglets1, piglets2_new_amount = PigletsSplit.objects.split_return_groups( \
                parent_piglets=piglets, new_amount=new_amount, initiator=initiator)
            
            moved_piglets = piglets2_new_amount
            stayed_piglets = piglets1
            split_event = piglets.split_as_parent
            
            if reverse:
                moved_piglets = piglets1
                stayed_piglets = piglets2_new_amount

        transaction = self.create_transaction(to_location=to_location, piglets_group=moved_piglets,
         initiator=initiator, date=date, split_event=split_event)

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

    split_event = models.OneToOneField('piglets_events.PigletsSplit', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='transaction')

    week_tour = models.ForeignKey('tours.Tour', on_delete=models.SET_NULL, null=True, blank=True,
        related_name="piglets_transactions")

    quantity = models.IntegerField(null=True)

    objects = PigletsTransactionManager()