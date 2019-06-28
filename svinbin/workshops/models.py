# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models

from core.models import CoreModel, CoreModelManager
# from piglets_events.models import NomadGroupPigletsMerger
# from django.apps import apps

# NomadGroupPigletsMerger = apps.get_model('piglets_events', 'NomadGroupPigletsMerger')


class WorkShop(CoreModel):
    number = models.IntegerField()
    title = models.CharField(max_length=128)

    def __str__(self):
        return self.title


class WorkShopEmployee(CoreModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    workshop = models.ForeignKey(WorkShop, on_delete=models.CASCADE)

    def __str__(self):
        return 'Employee {} at workshop {}'.format(self.user.username, self.workshop.title)


class Section(CoreModel):
    workshop = models.ForeignKey(WorkShop, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    number = models.IntegerField()

    def __str__(self):
        return '{}, {}'.format(self.name, self.workshop.title)


class Cell(CoreModel):
    workshop = models.ForeignKey(WorkShop, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    number = models.CharField(max_length=4)
    
    class Meta:
        abstract = True


# Here I can create just one cell class for all types instead separation.

class SowSingleCell(Cell):
    sow = models.OneToOneField('sows.Sow', on_delete=models.SET_NULL, null=True)


class SowGroupCell(Cell):
    sows = models.ManyToManyField('sows.Sow', related_name='sows_in_cell')
    sows_quantity = models.IntegerField(default=0)

    def get_locations_with_residents(self):
        return self.locations.get_with_active_new_born_group()

    def get_list_of_residents(self):
        residents = list()
        for location in self.locations.get_with_active_nomad_group():
            residents.append(location.newbornpigletsgroup)
        return residents

    def get_first_piglets_group(self):
        return self.get_locations_with_residents().first().newbornpigletsgroup


class PigletsGroupCell(Cell):
    # piglets_groups = models.ManyToManyField('sows.NomadPigletsGroup', related_name='piglets_groups_in_cell')
    # quantity = models.IntegerField(default=0)

    def __str__(self):
        return 'Групповая клетка № {}, {}'.format(self.number, str(self.section))

    def get_all_locations(self):
        return self.locations.all()

    def get_locations_with_residents(self):
        return self.locations.get_with_active_nomad_group()

    def get_list_of_residents(self):
        residents = list()
        for location in self.locations.get_with_active_nomad_group():
            residents.append(location.nomadpigletsgroup)

        return residents

    @property
    def is_empty(self):
        if self.get_locations_with_residents().first() == None:
            return True
        return False


class SowAndPigletsCell(Cell):
    sow = models.OneToOneField('sows.Sow', on_delete=models.SET_NULL, null=True)
    # piglets_groups = models.ManyToManyField('sows.NewBornPigletsGroup', related_name='piglets_groups_in_sow_cell')

    def get_locations_with_residents(self):
        return self.locations.get_with_active_new_born_group()

    def get_list_of_residents(self):
        residents = list()
        for location in self.locations.get_with_active_new_born_group():
            residents.append(location.newbornpigletsgroup)
        return residents

    def get_first_piglets_group(self):
        return self.get_locations_with_residents().first().newbornpigletsgroup


# class WeighingCell(Cell):
#     piglets_groups = models.ManyToManyField('sows.PigletsGroup', related_name='piglets_groups_in_cell')
#     sows = models.ManyToManyField('sows.Sow', related_name='sows_in_cell')