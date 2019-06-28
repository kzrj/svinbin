# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models

from core.models import CoreModel, CoreModelManager


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


class SowSingleCell(Cell):
    pass
    

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
    def get_newborn_groups(self):
        print(self.location)


    # def get_locations_with_residents(self):
    #     return self.location.get_with_active_new_born_group()

    # def get_list_of_residents(self):
    #     residents = list()
    #     for location in self.locations.get_with_active_new_born_group():
    #         residents.append(location.newbornpigletsgroup)
    #     return residents

    # def get_first_piglets_group(self):
    #     return self.get_locations_with_residents().first().newbornpigletsgroup


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


class Location(CoreModel):
    workshop = models.OneToOneField(WorkShop, null=True, on_delete=models.SET_NULL,
     related_name='location')
    section = models.OneToOneField(Section, null=True, on_delete=models.SET_NULL,
     related_name='location')
    sowSingleCell = models.OneToOneField(SowSingleCell, null=True, on_delete=models.SET_NULL,
     related_name='location')
    pigletsGroupCell = models.OneToOneField(PigletsGroupCell, null=True, on_delete=models.SET_NULL,
     related_name='location')
    sowAndPigletsCell = models.OneToOneField(SowAndPigletsCell, null=True, on_delete=models.SET_NULL,
     related_name='location')
    sowGroupCell = models.OneToOneField(SowGroupCell, null=True, on_delete=models.SET_NULL,
     related_name='location')

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

    def get_located_active_new_born_groups(self):
        return self.newbornpigletsgroup_set.all()