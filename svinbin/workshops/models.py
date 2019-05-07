# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models

from sows.models import Sow


class WorkShop(models.Model):
    number = models.IntegerField()
    title = models.CharField(max_length=128)

    def __str__(self):
        return self.title


class WorkShopEmployee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    workshop = models.ForeignKey(WorkShop, on_delete=models.CASCADE)

    def __str__(self):
        return 'Employee {} at workshop {}'.format(self.user.username, self.workshop.title)


class Section(models.Model):
    workshop = models.ForeignKey(WorkShop, on_delete=models.CASCADE)
    name = models.CharField(max_length=5)

    def __str__(self):
        return 'Section {} at workshop {}'.format(self.name, self.workshop.title)


class Cell(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    number = models.CharField(max_length=4)
    # pigletsQuantity = models.IntegerField(default=0)
    # sow = models.OneToOneField(Sow, null=True)
    
    class Meta:
        abstract = True

    # @property
    # def is_empty(self):
    #     if self.sowlocation:
    #         return True

# Here I can create just one cell class for all types instead separation.

class SingleCell(Cell):
    sow = models.OneToOneField(Sow, on_delete=models.SET_NULL, null=True)


class GroupCell(Cell):
    quantity = models.IntegerField(default=0)


class SowAndPigletsCell(Cell):
    sow = models.OneToOneField(Sow, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0)
