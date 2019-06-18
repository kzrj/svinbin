# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models

# from transactions.models import Location
import transactions


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
    name = models.CharField(max_length=20)
    number = models.IntegerField()

    def __str__(self):
        return '{}, {}'.format(self.name, self.workshop.title)


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

class SowSingleCell(Cell):
    sow = models.OneToOneField('sows.Sow', on_delete=models.SET_NULL, null=True)


class SowGroupCell(Cell):
    sows = models.ManyToManyField('sows.Sow', related_name='sows_in_cell')
    sows_quantity = models.IntegerField(default=0)


class PigletsGroupCell(Cell):
    # piglets_groups = models.ManyToManyField('sows.NomadPigletsGroup', related_name='piglets_groups_in_cell')
    # quantity = models.IntegerField(default=0)

    def __str__(self):
        return 'Групповая клетка № {}, {}'.format(self.number, str(self.section))

    def get_all_locations(self):
        print('get all locations')
        return self.locations.all()

    def get_residents(self):
        print('get_residents')
        return self.locations.get_with_active_nomad_group()


class SowAndPigletsCell(Cell):
    sow = models.OneToOneField('sows.Sow', on_delete=models.SET_NULL, null=True)
    # piglets_groups = models.ManyToManyField('sows.NewBornPigletsGroup', related_name='piglets_groups_in_sow_cell')


# class WeighingCell(Cell):
#     piglets_groups = models.ManyToManyField('sows.PigletsGroup', related_name='piglets_groups_in_cell')
#     sows = models.ManyToManyField('sows.Sow', related_name='sows_in_cell')
