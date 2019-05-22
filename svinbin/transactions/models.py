# -*- coding: utf-8 -*-
from django.db import models

from workshops.models import WorkShopEmployee, WorkShop, SowSingleCell, Section, \
    PigletsGroupCell, SowAndPigletsCell, SowGroupCell, WeighingCell



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
        elif isinstance(pre_location, WeighingCell):
            location = self.create(weighingCell=pre_location)
        # else:
        #     raise error?
        return location


class Location(models.Model):
    workshop = models.ForeignKey(WorkShop, null=True, on_delete=models.SET_NULL)
    section = models.ForeignKey(Section, null=True, on_delete=models.SET_NULL)
    sowSingleCell = models.ForeignKey(SowSingleCell, null=True, on_delete=models.SET_NULL)
    pigletsGroupCell = models.ForeignKey(PigletsGroupCell, null=True, on_delete=models.SET_NULL)
    sowAndPigletsCell = models.ForeignKey(SowAndPigletsCell, null=True, on_delete=models.SET_NULL)
    sowGroupCell = models.ForeignKey(SowGroupCell, null=True, on_delete=models.SET_NULL)
    weighingCell = models.ForeignKey(WeighingCell, null=True, on_delete=models.SET_NULL)

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


class Transaction(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    initiator = models.ForeignKey(WorkShopEmployee, on_delete=models.SET_NULL, null=True)
    finished = models.BooleanField(default=False)
    returned = models.BooleanField(default=False)
    # reason = models.CharField(max_lenght=)

    class Meta:
        abstract = True

    def return_transaction(self):
        pass


class SowTransaction(Transaction):
    from_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="sow_from_location")
    to_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="sow_to_location")
    sow = models.ForeignKey('sows.Sow', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # need to refractor to atomic transactions.
        self.to_empty_from_location_single_cell
        self.to_fill_to_location_single_cell

        self.to_empty_from_location_group_cell
        self.to_fill_to_location_group_cell        

        self.change_sow_current_location
        super(SowTransaction, self).save(*args, **kwargs)

    # to model manager
    @property
    def to_empty_from_location_single_cell(self):
        if self.from_location.sowSingleCell:
            self.from_location.sowSingleCell.sow = None
            self.from_location.sowSingleCell.save()

    # to model manager
    @property
    def to_fill_to_location_single_cell(self):
        if self.to_location.sowSingleCell:
            self.to_location.sowSingleCell.sow = self.sow
            self.to_location.sowSingleCell.save()

    # to model manager
    @property
    def to_empty_from_location_group_cell(self):
        if self.from_location.sowGroupCell:
            self.from_location.sowGroupCell.sows_in_cell.remove(self.sow)

    # to model manager
    @property
    def to_fill_to_location_group_cell(self):
        if self.to_location.sowGroupCell:
            self.from_location.sowGroupCell.sows_in_cell.add(self.sow)

    # add empty , fill for SowAndPigletsCell

    # to model manager
    @property
    def change_sow_current_location(self):
        self.sow.location = self.to_location
        self.sow.save()


class PigletsTransaction(Transaction):
    from_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="piglets_from_location")
    to_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="piglets_to_location")
    piglets_group = models.ForeignKey('sows.PigletsGroup', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # need to refractor to atomic transactions.
        # self.to_empty_from_location_cell
        # self.to_fill_to_location_cell
        self.change_piglets_group_current_location
        super(PigletsTransaction, self).save(*args, **kwargs)

    @property
    def change_piglets_group_current_location(self):
        self.piglets_group.location = self.to_location
        self.piglets_group.save()

    # def to_empty_from_location_cell(self):
    #     self.from_location.sowAndPigletsCell.quantity = self.from_location.sowAndPigletsCell.quantity - self.quantity
    #     self.from_location.sowAndPigletsCell.save()

    # @property
    # def to_fill_to_location_cell(self):
    #     self.to_location.sowAndPigletsCell.quantity = self.from_location.sowAndPigletsCell.quantity + self.quantity
    #     self.to_location.sowAndPigletsCell.save()


class GiltTransaction(Transaction):
    from_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="gilt_from_location")
    to_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="gilt_to_location")
    gilt = models.ForeignKey('sows.Gilt', on_delete=models.CASCADE)