# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
from django.conf import settings

from core.models import CoreModel, CoreModelManager
from workshops.models import WorkShopEmployee, WorkShop, SowSingleCell, Section, \
    PigletsGroupCell, SowAndPigletsCell, SowGroupCell
    # WeighingCell
# import piglets_events.models


class LocationManager(CoreModelManager):
    def create_location(self, pre_location):
        if isinstance(pre_location, WorkShop):
            location = self.create(workshop=pre_location)
        elif isinstance(pre_location, Section):
            location = self.create(section=pre_location)
        elif isinstance(pre_location, SowSingleCell):
            location = self.create(sowSingleCell=pre_location)
        elif isinstance(pre_location, SowGroupCell):
            location = self.create(sowGroupCell=pre_location)
        elif isinstance(pre_location, PigletsGroupCell):
            location = self.create(pigletsGroupCell=pre_location)
        elif isinstance(pre_location, SowAndPigletsCell):
            location = self.create(sowAndPigletsCell=pre_location)
        return location

    def get_with_active_nomad_group(self):
        return self.filter(nomadpigletsgroup__active=True).select_related('nomadpigletsgroup')

    def create_workshop_location(self, workshop_number):
        return self.create_location(WorkShop.objects.get(number=workshop_number))

    def duplicate_location(self, location):
        return self.create_location(location.get_location)


class Location(CoreModel):
    workshop = models.ForeignKey(WorkShop, null=True, on_delete=models.SET_NULL, related_name='locations')
    section = models.ForeignKey(Section, null=True, on_delete=models.SET_NULL, related_name='locations')
    sowSingleCell = models.ForeignKey(SowSingleCell, null=True, on_delete=models.SET_NULL, related_name='locations')
    pigletsGroupCell = models.ForeignKey(PigletsGroupCell, null=True, on_delete=models.SET_NULL, related_name='locations')
    sowAndPigletsCell = models.ForeignKey(SowAndPigletsCell, null=True, on_delete=models.SET_NULL, related_name='locations')
    sowGroupCell = models.ForeignKey(SowGroupCell, null=True, on_delete=models.SET_NULL, related_name='locations')

    objects = LocationManager()

    @property
    def get_location(self):
        if self.workshop:
            return self.workshop

        if self.section:
            return self.section

        if self.sowSingleCell:
            return self.sowSingleCell

        if self.pigletsGroupCell:
            return self.pigletsGroupCell

        if self.sowAndPigletsCell:
            return self.sowAndPigletsCell

        if self.sowGroupCell:
            return self.sowGroupCell

        if self.weighingCell:
            return self.weighingCell

    @property
    def get_workshop(self):
        if self.workshop:
            return self.workshop

        if self.section:
            return self.section.workshop

        if self.sowSingleCell:
            return self.sowSingleCell.section.workshop

        if self.pigletsGroupCell:
            return self.pigletsGroupCell.section.workshop

        if self.sowAndPigletsCell:
            return self.sowAndPigletsCell.section.workshop

        if self.sowGroupCell:
            return self.sowGroupCell.section.workshop

    def duplicate_location_from_model(self):
        return Location.objects.create_location(self.get_location)

    def __str__(self):
        return str(self.get_location)


class Transaction(CoreModel):
    date = models.DateTimeField(auto_now_add=True)
    initiator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    finished = models.BooleanField(default=False)
    returned = models.BooleanField(default=False)
    # reason = models.CharField(max_lenght=)

    class Meta:
        abstract = True


class SowTransactionManager(CoreModelManager):
    def create_transaction(self, to_location, sow, initiator):
        # need to refractor to atomic transactions.
        transaction = SowTransaction.objects.create(
                date=timezone.now(),
                initiator=initiator,
                from_location=sow.location,
                to_location=to_location,
                sow=sow
                )

        transaction.to_empty_from_location
        transaction.to_fill_to_location

        sow.change_sow_current_location(to_location)

        return transaction

    def create_many_transactions(self, sows, to_location, initiator):
        transactions_ids = list()
        for sow in sows:
            location = Location.objects.duplicate_location(to_location)
            transaction = self.create_transaction(location, sow, initiator)
            transactions_ids.append(transaction.pk)
        return transactions_ids


class SowTransaction(Transaction):
    from_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="sow_from_location")
    to_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="sow_to_location")
    sow = models.ForeignKey('sows.Sow', on_delete=models.CASCADE)

    objects = SowTransactionManager()

    @property
    def to_empty_from_location(self):
        if self.from_location.sowSingleCell:
            self.from_location.sowSingleCell.sow = None
            self.from_location.sowSingleCell.save()

        if self.from_location.sowGroupCell:
            self.from_location.sowGroupCell.sows.remove(self.sow)

        if self.from_location.sowAndPigletsCell:
            self.from_location.sowAndPigletsCell.sow = None
            self.from_location.sowAndPigletsCell.save()

    @property
    def to_fill_to_location(self):
        if self.to_location.sowSingleCell:
            self.to_location.sowSingleCell.sow = self.sow
            self.to_location.sowSingleCell.save()

        if self.to_location.sowGroupCell:
            self.to_location.sowGroupCell.sows.add(self.sow)

        if self.to_location.sowAndPigletsCell:
            self.to_location.sowAndPigletsCell.sow = self.sow
            self.to_location.sowAndPigletsCell.save()


class PigletsTransactionManager(CoreModelManager):
    def create_transaction_without_merge(self, to_location, piglets_group, initiator=None):
        transaction = PigletsTransaction.objects.create(
                date=timezone.now(),
                initiator=initiator,
                from_location=piglets_group.location,
                to_location=to_location,
                piglets_group=piglets_group
                )

        piglets_group.change_current_location(to_location)

        return transaction

    # def create_transactions_with_nomad_merge(self, to_location, piglets_group, initiator=None):
    #     transaction = self.create_transaction_without_merge(to_location, piglets_group, initiator)
        
    #     cell = to_location.get_location
    #     # nomad_group_in_cell = cell.get_residents().first()
    #     nomad_group_in_cell = cell.get_list_of_residents()[0]
    #     new_location = Location.objects.duplicate_location(to_location)
        
    #     new_created_group = piglets_events.models.NomadGroupPigletsMerger.create_merger_and_return_nomad_piglets_group(
    #         nomad_groups=[piglets_group, nomad_group_in_cell],
    #         new_location=new_location,
    #         initiator=initiator
    #         )

    #     return transaction

    def create_transaction_to_group_cell(self, to_location, piglets_group, initiator=None):
        cell = to_location.get_location
        if cell.is_empty:
            return self.create_transaction_without_merge(to_location, piglets_group, initiator)
        else:
            return self.create_transactions_with_nomad_merge(to_location, piglets_group, initiator)


class PigletsTransaction(Transaction):
    from_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="piglets_from_location")
    to_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="piglets_to_location")
    piglets_group = models.ForeignKey('piglets.NomadPigletsGroup', on_delete=models.CASCADE, related_name="transactions")

    objects = PigletsTransactionManager()

    
class GiltTransaction(Transaction):
    from_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="gilt_from_location")
    to_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="gilt_to_location")
    gilt = models.ForeignKey('sows.Gilt', on_delete=models.CASCADE)