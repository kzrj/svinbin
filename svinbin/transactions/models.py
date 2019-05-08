# -*- coding: utf-8 -*-
from django.db import models

from sows.models import Sow, Gilt
from workshops.models import WorkShopEmployee, WorkShop, SowSingleCell, Section, PigletsGroupCell, \
    SowAndPigletsCell, SowGroupCell


class Location(models.Model):
    workshop = models.ForeignKey(WorkShop, null=True, on_delete=models.SET_NULL)
    section = models.ForeignKey(Section, null=True, on_delete=models.SET_NULL)
    sowSingleCell = models.ForeignKey(SowSingleCell, null=True, on_delete=models.SET_NULL)
    pigletsGroupCell = models.ForeignKey(PigletsGroupCell, null=True, on_delete=models.SET_NULL)
    sowAndPigletsCell = models.ForeignKey(SowAndPigletsCell, null=True, on_delete=models.SET_NULL)
    sowGroupCell = models.ForeignKey(SowGroupCell, null=True, on_delete=models.SET_NULL)


class Transaction(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    initiator = models.ForeignKey(WorkShopEmployee, on_delete=models.SET_NULL, null=True)
    # from_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="from_location")
    # to_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="to_location")
    finished = models.BooleanField(default=False)
    # reason = models.CharField(max_lenght=)

    class Meta:
        abstract = True


class SowTransaction(Transaction):
    from_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="sow_from_location")
    to_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="sow_to_location")
    sow = models.ForeignKey(Sow, on_delete=models.CASCADE)


class PigletsTransaction(Transaction):
    from_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="piglets_from_location")
    to_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="piglets_to_location")
    quantity = models.IntegerField()


class GiltTransaction(Transaction):
    from_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="gilt_from_location")
    to_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="gilt_to_location")
    gilt = models.ForeignKey(Gilt, on_delete=models.CASCADE)