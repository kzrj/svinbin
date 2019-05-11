# -*- coding: utf-8 -*-
from django.db import models

from workshops.models import WorkShopEmployee, WorkShop, SowSingleCell, Section, \
    PigletsGroupCell, SowAndPigletsCell, SowGroupCell


class Location(models.Model):
    workshop = models.ForeignKey(WorkShop, null=True, on_delete=models.SET_NULL)
    section = models.ForeignKey(Section, null=True, on_delete=models.SET_NULL)
    sowSingleCell = models.ForeignKey(SowSingleCell, null=True, on_delete=models.SET_NULL)
    pigletsGroupCell = models.ForeignKey(PigletsGroupCell, null=True, on_delete=models.SET_NULL)
    sowAndPigletsCell = models.ForeignKey(SowAndPigletsCell, null=True, on_delete=models.SET_NULL)
    sowGroupCell = models.ForeignKey(SowGroupCell, null=True, on_delete=models.SET_NULL)

    # def __str__(self):
    #     return self.title

    @property
    def get_location2(self):
        for field in self._meta.get_fields():
            if field:

                yield field.name

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

# class TransactionObject(models.Model):
#     sow = models.ForeignKey('sows.Sow', on_delete=models.SET_NULL, null=True)
#     gilt = models.ForeignKey('sows.Gilt', on_delete=models.SET_NULL, null=True)
#     pigletsQuantity = models.IntegerField(null=True)


class Transaction(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    initiator = models.ForeignKey(WorkShopEmployee, on_delete=models.SET_NULL, null=True)
    # from_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="from_location")
    # to_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="to_location")
    finished = models.BooleanField(default=False)
    returned = models.BooleanField(default=False)
    # reason = models.CharField(max_lenght=)
    # transactionObject = models.OneToOneField(TransactionObject)

    class Meta:
        abstract = True

    def return_transaction(self):
        pass


class SowTransaction(Transaction):
    from_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="sow_from_location")
    to_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="sow_to_location")
    sow = models.ForeignKey('sows.Sow', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.sow.location = self.to_location
        self.sow.save()
        super(SowTransaction, self).save(*args, **kwargs)


class PigletsTransaction(Transaction):
    from_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="piglets_from_location")
    to_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="piglets_to_location")
    quantity = models.IntegerField()


class GiltTransaction(Transaction):
    from_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="gilt_from_location")
    to_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="gilt_to_location")
    gilt = models.ForeignKey('sows.Gilt', on_delete=models.CASCADE)