# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models, connection

from core.models import CoreModel, CoreModelManager


class WorkShop(CoreModel):
    number = models.IntegerField()
    title = models.CharField(max_length=128)

    def __str__(self):
        return self.title

    # def get_info_data_ws3(self):
    #     data = dict()
    #     data['workshop'] = dict()
    #     for section in Section.objects.filter(workshop=self):
    #         data[str(section.number)] = Location.objects \
    #             .get_sowandpiglets_cells_by_section(section) \
    #             .get_cells_data()
    #         data[str(section.number)]['sow_count'] = 0
            # data[str(section.number)]['sow_count'] = Sow.objects.filter( \
            #     location__sowAndPigletsCell__section=section).count()
            # locations = Location.objects.filter(sowAndPigletsCell__section=section) \
            #     .prefetch_related('sow_set', 'newbornpigletsgroup_set')
            # print(locations.sow_set.count())
            # print(locations.annotate(num_sows=models.Count('sow'))[0].num_sows)
            # for loc_cell in Location.objects.filter(sowAndPigletsCell__section=section) \
            #     .prefetch_related('sow_set', 'newbornpigletsgroup_set'):
            #     data[str(section.number)]['sow_count'] = data[str(section.number)]['sow_count'] + 


            # data[str(section.number)]['piglets_count'] = NewBornPigletsGroup.objects.filter( \
            #     location__sowAndPigletsCell__section=section).count()

            # for key in data[str(section.number)].keys():
            #     if data['workshop'].get(key):
            #         data['workshop'][key] = data['workshop'][key] + data[str(section.number)][key]
            #     else:
            #         data['workshop'][key] = data[str(section.number)][key]


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
    def __str__(self):
        return 'section {}, cell {}'.format(str(self.section.number), self.number)
    

class LocationQuerySet(models.QuerySet):
    def get_cells_data(self):
        empty, not_empty, with_piglets, sow_only = 0, 0, 0, 0
        for location in self.prefetch_related('sow_set', 'newbornpigletsgroup_set',
            'nomadpigletsgroup_set', 'gilt_set'):
            if location.is_empty:
                empty += 1
            else:
                not_empty += 1
                if location.get_located_active_new_born_groups():
                    with_piglets += 1
                else:
                    sow_only += 1

        return {'empty':empty, 'not_empty': not_empty, 'with_piglets': with_piglets, 'sow_only': sow_only}
        

class LocationManager(CoreModelManager):
    def get_queryset(self):
        return LocationQuerySet(self.model, using=self._db)

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

    def get_sowandpiglets_cells_by_section(self, section):
            return self.get_queryset().filter(sowAndPigletsCell__section=section)

    def get_sowandpiglets_cells_by_workshop(self, workshop):
            return self.get_queryset().filter(sowAndPigletsCell__workshop=workshop)


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
        # return str(self.get_location)
        return 'location {}'.format(self.pk)

    def get_located_active_new_born_groups(self):
        return self.newbornpigletsgroup_set.all()

    def get_located_active_nomad_groups(self):
        return self.nomadpigletsgroup_set.all()

    def is_nomad_piglet_group_cell_empty(self):
        if self.get_located_active_nomad_groups():
            return False
        return True

    @property
    def is_empty(self):
        if not self.get_located_active_nomad_groups() and \
            not self.get_located_active_new_born_groups() and \
            not self.sow_set.all() and \
            not self.gilt_set.all():
                return True
        return False

    @property
    def is_sow_empty(self):
        if not self.sow_set.all():
            return True
        return False

    @property
    def is_piglets_empty(self):
        if not self.get_located_active_nomad_groups() and \
            not self.get_located_active_new_born_groups():
                return True
        return False

    @property
    def get_cell_number(self):
        if self.sowSingleCell:
            return self.sowSingleCell.number

        if self.pigletsGroupCell:
            return self.pigletsGroupCell.number

        if self.sowAndPigletsCell:
            return self.sowAndPigletsCell.number

        if self.sowGroupCell:
            return self.sowGroupCell.number

        return None