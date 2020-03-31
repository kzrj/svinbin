# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models, connection
from django.db.models import Sum, OuterRef, Subquery

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
        return 'Секция {} {}'.format(self.number, self.workshop)

    def sows_count_by_tour(self):
        # only work for ws3
        if self.workshop.number != 3:
            return None

        return self.location.sows_count_by_tour

    def count_piglets(self):
        if self.workshop.number == 3:
            return None

        return self.location.count_piglets


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

    
class PigletsGroupCell(Cell):
    def __str__(self):
        return 'Групповая клетка № {}, {}'.format(self.number, str(self.section))

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
        return 'секция {}, клетка {}'.format(str(self.section.number), self.number)
    

class LocationQuerySet(models.QuerySet):
    pass
        

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

    def count_piglets_in_section(self, section):
        return self.get_queryset().filter(pigletsGroupCell__section=section) \
            .aggregate(Sum('piglets__quantity'))

    def get_with_count_piglets_in_section(self):
#       >>> users = User.objects.all()
#       >>> UserParent.objects.filter(user_id__in=Subquery(users.values('id')))
        # locs_sections = self.get_queryset().filter(section__isnull=False)
        # locs_sections = self.get_queryset().filter(section__number=1, section__workshop__number=4)
        locs_sections = self.get_queryset().filter(section__workshop__number=4)
        # return self.get_queryset().filter(pigletsGroupCell__section__in=Subquery(locs_sections.values('section')))

        # return self.get_queryset().filter(pigletsGroupCell__section__in=Subquery(locs_sections.values('section'))) \
        #     .aggregate(Sum('piglets__quantity'))

        # pigs_count for all ws
        # return locs_sections.annotate(
        #         pigs_count=models.Value(self.get_queryset() \
        #             .filter(pigletsGroupCell__section__in=Subquery(locs_sections.values('section'))) \
        #             .aggregate(pigs_qty=Sum('piglets__quantity'))['pigs_qty'],
        #             output_field=models.IntegerField()              
        #             )
        #     )

        # piglets_cells_query = self.get_queryset().filter(pigletsGroupCell__section=OuterRef('section'))

        # piglets_cells_query2 = self.get_queryset() \
        #     .filter(pigletsGroupCell__section=OuterRef('section')) \
        #     .annotate(pigs_qty=Sum('piglets__quantity'))

        # return locs_sections.annotate(
        #         pigs_count=models.Sum(
        #             piglets_cells_query2.annotate(p_q=models.Value('pigs_qty', output_field=models.IntegerField()))
        #             )
        #     )

        # piglets = 

        piglets_cells = self.get_queryset().filter(pigletsGroupCell__section=OuterRef('section')).values('piglets__quantity')[:1]
        return locs_sections.annotate(
            pigs_count=models.ExpressionWrapper(
                self.get_queryset().filter(pigletsGroupCell__section=OuterRef('section'))\
                    .aggregate(pigs_qty=Sum('piglets__quantity'))['pigs_qty'],
                output_field=models.IntegerField()
                )
            )

        # return locs_sections.annotate(
        #         pigs_count=models.Sum(
        #             Subquery(piglets_cells)
        #             )
        #     )

        # return self.get_queryset().filter(section__isnull=False) \
        #     .annotate(
        #         piglets_in_section=Subquery(
        #             self.get_queryset()
        #             .filter(section=OuterRef('section')
        #             .aggregate(Sum('piglets__quantity')),
        #             output_field=models.IntegerField()
        #             )
        #         )
        #     )
            # .annotate(
            #     piglets_qnty = Location.objects.count_piglets_in_section(
            #         section=each item in get_queryset
            #         )
                # Subquery(self.get_queryset().filter(section=OuterRef('section')))
                # )


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

        # if self.sowSingleCell:
        #     return self.sowSingleCell

        if self.pigletsGroupCell:
            return self.pigletsGroupCell

        if self.sowAndPigletsCell:
            return self.sowAndPigletsCell

        # if self.sowGroupCell:
        #     return self.sowGroupCell

    @property
    def get_sow_location(self):
        if self.workshop:
            return self.workshop

        if self.section:
            return self.section

        # if self.sowSingleCell:
        #     return self.sowSingleCell

        if self.sowAndPigletsCell:
            return self.sowAndPigletsCell

        # if self.sowGroupCell:
        #     return self.sowGroupCell

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
        return str(self.pk)

    @property
    def is_empty(self):
        if not self.get_located_active_piglets() and \
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
        if not self.piglets.all():
            return True
        return False

    @property
    def get_cell_number(self):
        if self.sowSingleCell:
            return f'{self.sowSingleCell.section.number}/{self.sowSingleCell.number}'

        if self.pigletsGroupCell:
            return f'{self.pigletsGroupCell.section.number}/{self.pigletsGroupCell.number}'

        if self.sowAndPigletsCell:
            return f'{self.sowAndPigletsCell.section.number}/{self.sowAndPigletsCell.number}'

        if self.sowGroupCell:
            return f'{self.sowGroupCell.section.number}/{self.sowGroupCell.number}'

        return None

    @property
    def sows_count_by_tour(self):
        return self.sow_set.get_tours_with_count_sows_by_location(self)

    @property
    def count_piglets(self):
        return Location.objects.filter(pigletsGroupCell__section=self.section) \
            .aggregate(Sum('piglets__quantity'))['piglets__quantity__sum']
