# -*- coding: utf-8 -*-
from django.db import models

from workshops.models import WorkShopEmployee, WorkShop, SingleCell, Section, GroupCell,
    SowAndPigletsCell
from sows.models import SowLocation, Sow, Gilt


class Location(models.Model):
    workshop = models.ForeingKey(WorkShop, null=True, on_delete=models.SET_NULL)
    section = models.ForeingKey(Section, null=True, on_delete=models.SET_NULL)
    singleCell = models.ForeingKey(SingleCell, null=True, on_delete=models.SET_NULL)
    groupCell = models.ForeingKey(groupCell, null=True, on_delete=models.SET_NULL)
    sowAndPigletsCell = models.ForeingKey(SowAndPigletsCell, null=True, on_delete=models.SET_NULL)


class Transaction(models.Model):
    date = models.DateTimefield(auto_now_add=True)
    initiator = models.ForeingKey(WorkShopEmployee, on_delete=models.SET_NULL, null=True)
    from_location = models.ForeingKey(Location, on_delete=models.CASCADE, related_name="from_location")
    to_location = models.ForeingKey(Location, on_delete=models.CASCADE, related_name="to_location")
    finished = models.BooleanField(default=False)
    # reason = models.CharField(max_lenght=)

    class Meta:
        abstract = True


class SowTransaction(Transaction):
    sow = models.ForeingKey(Sow, on_delete=models.CASCADE)


class PigletsTransaction(Transaction):
    quantity = models.IntegerField()


class GiltTransaction(Transaction):
    gilt = models.ForeingKey(Gilt, on_delete=models.CASCADE)