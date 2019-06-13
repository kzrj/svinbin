# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone

from workshops.models import WorkShopEmployee, WorkShop, SowSingleCell, Section, \
    PigletsGroupCell, SowAndPigletsCell, SowGroupCell
    # WeighingCell



class LocationManager(models.Manager):
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
        # elif isinstance(pre_location, WeighingCell):
        #     location = self.create(weighingCell=pre_location)
        # else:
        #     raise error?
        return location


class Location(models.Model):
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

    def __str__(self):
        return str(self.get_location)


class Transaction(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    initiator = models.ForeignKey(WorkShopEmployee, on_delete=models.SET_NULL, null=True)
    finished = models.BooleanField(default=False)
    returned = models.BooleanField(default=False)
    # reason = models.CharField(max_lenght=)

    class Meta:
        abstract = True


class SowTransactionManager(models.Manager):
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


class SowTransaction(Transaction):
    from_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="sow_from_location")
    to_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="sow_to_location")
    sow = models.ForeignKey('pigs.Sow', on_delete=models.CASCADE)

    objects = SowTransactionManager()

    @property
    def to_empty_from_location(self):
        if self.from_location.sowSingleCell:
            self.from_location.sowSingleCell.sow = None
            self.from_location.sowSingleCell.save()

        if self.from_location.sowGroupCell:
            self.from_location.sowGroupCell.sows.remove(self.sow)

        if self.from_location.sowAndPigletsCell:
            self.from_location.sowAndPigletsCell.sows.remove(self.sow)

    @property
    def to_fill_to_location(self):
        if self.to_location.sowSingleCell:
            self.to_location.sowSingleCell.sow = self.sow
            self.to_location.sowSingleCell.save()

        if self.to_location.sowGroupCell:
            self.to_location.sowGroupCell.sows.add(self.sow)

        if self.to_location.sowAndPigletsCell:
            self.to_location.sowAndPigletsCell.sows.add(self.sow)



class PigletsTransactionManager(models.Manager):
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


class PigletsTransaction(Transaction):
    from_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="piglets_from_location")
    to_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="piglets_to_location")
    piglets_group = models.ForeignKey('pigs.NomadPigletsGroup', on_delete=models.CASCADE)

    objects = PigletsTransactionManager()

    
class GiltTransaction(Transaction):
    from_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="gilt_from_location")
    to_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="gilt_to_location")
    gilt = models.ForeignKey('pigs.Gilt', on_delete=models.CASCADE)