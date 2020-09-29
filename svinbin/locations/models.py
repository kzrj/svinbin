# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from django.db import models
from django.db.models import Sum, OuterRef, Subquery, Q, Count, Value

from core.models import CoreModel, CoreModelManager


class WorkShop(CoreModel):
    number = models.IntegerField()
    title = models.CharField(max_length=128)

    def __str__(self):
        return self.title


class Section(CoreModel):
    workshop = models.ForeignKey(WorkShop, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    number = models.IntegerField()

    def __str__(self):
        return 'Секция {} {}'.format(self.number, self.workshop)


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


class SowAndPigletsCell(Cell):
    def __str__(self):
        return 'секция {}, клетка {}'.format(str(self.section.number), self.number)
    

class LocationQuerySet(models.QuerySet):
    def get_workshop_location(self, workshop):
        return Location.objects.all().filter(
            Q(
                Q(workshop=workshop) |
                Q(pigletsGroupCell__workshop=workshop) | 
                Q(section__workshop=workshop) |
                Q(sowAndPigletsCell__workshop=workshop)
                )
            )

    def get_workshop_location_by_number(self, workshop_number):
        return self.filter(
            Q(
                Q(workshop__number=workshop_number) |
                Q(pigletsGroupCell__workshop__number=workshop_number) | 
                Q(section__workshop__number=workshop_number) |
                Q(sowAndPigletsCell__workshop__number=workshop_number)
                )
            )

    def get_locations_exclude_workshop_locations(self, workshop_number):
        return self.exclude(
            Q(
                Q(workshop__number=workshop_number) |
                Q(pigletsGroupCell__workshop__number=workshop_number) | 
                Q(section__workshop__number=workshop_number) |
                Q(sowAndPigletsCell__workshop__number=workshop_number)
                )
            )

    def get_locations_in_section(self, section):
        return Location.objects.all().filter(
            Q(
              Q(section=section) |
              Q(sowAndPigletsCell__section=section) |
              Q(pigletsGroupCell__section=section)
              )
            )   

    def add_sows_count_by_sections(self):       
        alive_sows = Count('sow', filter=Q(sow__alive=True))
        subquery_sows_count = self.get_locations_in_section(OuterRef('section')) \
                        .values('workshop') \
                        .annotate(all=alive_sows)\
                        .values('all')

        alive_sup_sows = Count('sow', filter=Q(sow__alive=True, sow__status__title='Супорос 35'))
        subquery_sows_sup_count = self.get_locations_in_section(OuterRef('section')) \
                        .values('workshop') \
                        .annotate(alive_sup_sows=alive_sup_sows)\
                        .values('alive_sup_sows')

        return self.annotate(
            sows_count=models.Subquery(subquery_sows_count, output_field=models.IntegerField()),
            sows_sup_count=models.Subquery(subquery_sows_sup_count, output_field=models.IntegerField())
        )

    def add_sows_count_by_workshop(self):     
        alive_sows = Count('sow', filter=Q(sow__alive=True))   
        subquery = self.get_workshop_location(OuterRef('workshop')) \
                        .annotate(flag=Value(0)) \
                        .values('flag') \
                        .annotate(all=alive_sows)\
                        .values('all')

        alive_sup_sows = Count('sow', filter=Q(sow__alive=True, sow__status__title='Супорос 35'))
        subquery_sows_sup_count = self.get_workshop_location(OuterRef('workshop')) \
                        .annotate(flag=Value(0)) \
                        .values('flag') \
                        .annotate(all=alive_sup_sows)\
                        .values('all')

        return self.annotate(
            sows_count=models.Subquery(subquery, output_field=models.IntegerField()),
            sows_sup_count=models.Subquery(subquery_sows_sup_count, output_field=models.IntegerField())
        )

    def add_pigs_count_by_workshop(self):    
        alive_piglets = Sum('piglets__quantity', filter=Q(piglets__active=True))    
        subquery = self.get_workshop_location(OuterRef('workshop')) \
                        .annotate(flag=Value(0)) \
                        .values('flag') \
                        .annotate(all=alive_piglets)\
                        .values('all')

        alive_gilts = Sum('piglets__gilts_quantity', filter=Q(piglets__active=True))
        subquery_gilts_count = self.get_workshop_location(OuterRef('workshop')) \
                        .annotate(flag=Value(0)) \
                        .values('flag') \
                        .annotate(all=alive_gilts)\
                        .values('all')

        return self.annotate(
            pigs_count=models.Subquery(subquery, output_field=models.IntegerField()),
            gilts_count=models.Subquery(subquery_gilts_count, output_field=models.IntegerField())
            )

    def gen_piglets_count_by_age_subqueries_ws3_locs(self, locs, date):
        data = dict()

        alive_piglets_0_7 = Sum('piglets__quantity',
             filter=Q(
                piglets__active=True,
                piglets__birthday__gte=(date-timedelta(days=7)),
                piglets__birthday__lte=(date-timedelta(days=0))
                )
             )
        subquery_0_7 = locs \
                    .annotate(flag=Value(0)) \
                    .values('flag') \
                    .annotate(all=alive_piglets_0_7)\
                    .values('all')
        data['count_piglets_0_7'] = models.Subquery(subquery_0_7, output_field=models.IntegerField())

        alive_piglets_8_14 = Sum('piglets__quantity',
             filter=Q(
                piglets__active=True,
                piglets__birthday__gte=(date-timedelta(days=14)),
                piglets__birthday__lte=(date-timedelta(days=8))
                )
             )
        subquery_8_14 = locs \
                    .annotate(flag=Value(0)) \
                    .values('flag') \
                    .annotate(all=alive_piglets_8_14)\
                    .values('all')
        data['count_piglets_8_14'] = models.Subquery(subquery_8_14, output_field=models.IntegerField())

        alive_piglets_15_21 = Sum('piglets__quantity',
             filter=Q(
                piglets__active=True,
                piglets__birthday__gte=(date-timedelta(days=21)),
                piglets__birthday__lte=(date-timedelta(days=15))
                )
             )
        subquery_15_21 = locs \
                    .annotate(flag=Value(0)) \
                    .values('flag') \
                    .annotate(all=alive_piglets_15_21)\
                    .values('all')
        data['count_piglets_15_21'] = models.Subquery(subquery_15_21, output_field=models.IntegerField())

        alive_piglets_22_28 = Sum('piglets__quantity',
             filter=Q(
                piglets__active=True,
                piglets__birthday__gte=(date-timedelta(days=28)),
                piglets__birthday__lte=(date-timedelta(days=21))
                )
             )
        subquery_22_28 = locs \
                    .annotate(flag=Value(0)) \
                    .values('flag') \
                    .annotate(all=alive_piglets_22_28)\
                    .values('all')
        data['count_piglets_22_28'] = models.Subquery(subquery_22_28, output_field=models.IntegerField())

        alive_piglets_28_plus = Sum('piglets__quantity',
             filter=Q(
                piglets__active=True,
                piglets__birthday__lte=(date-timedelta(days=28))
                )
             )
        subquery_28_plus = locs \
                    .annotate(flag=Value(0)) \
                    .values('flag') \
                    .annotate(all=alive_piglets_28_plus)\
                    .values('all')
        data['count_piglets_28_plus'] = models.Subquery(subquery_28_plus, output_field=models.IntegerField())

        return data

    def add_pigs_count_by_workshop3_by_age(self, date):
        locs = self.get_workshop_location(OuterRef('workshop'))
        data = self.gen_piglets_count_by_age_subqueries_ws3_locs(locs=locs, date=date)

        return self.annotate(**data)

    def add_pigs_count_by_sections(self):
        alive_piglets = Sum('piglets__quantity', filter=Q(piglets__active=True))
        subquery_piglets_count = self.get_locations_in_section(OuterRef('section')) \
                        .values('workshop') \
                        .annotate(all=alive_piglets)\
                        .values('all')

        alive_gilts = Sum('piglets__gilts_quantity', filter=Q(piglets__active=True))
        subquery_gilts_count = self.get_locations_in_section(OuterRef('section')) \
                        .values('workshop') \
                        .annotate(all=alive_gilts)\
                        .values('all')

        return self.annotate(
            pigs_count=models.Subquery(subquery_piglets_count),
            gilts_count=models.Subquery(subquery_gilts_count),
            )

    def add_pigs_count_by_ws3_sections_by_age(self, date):
        locs = self.get_locations_in_section(OuterRef('section'))
        data = self.gen_piglets_count_by_age_subqueries_ws3_locs(locs=locs, date=date)

        return self.annotate(**data)

    # uses in All population report
    def gen_sections_pigs_count_dict(self):
        secs = Location.objects.all().filter(section__isnull=False) \
            .select_related('section__workshop') \
            .add_pigs_count_by_sections() \
            .add_sows_count_by_sections()
        data = {'sections': {}, 'workshops': {}}

        for sec_number in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
            data['sections'][f'sec_{sec_number}'] = {}
            for ws_number in [1, 2, 3, 4, 5, 6, 7, 8, 11]:
                data['sections'][f'sec_{sec_number}'][f'ws{ws_number}_pigs_count'] = None
                data['sections'][f'sec_{sec_number}'][f'ws{ws_number}_sows_count'] = None

        for sec in secs:
            if hasattr(sec, 'pigs_count'):
                data['sections'][f'sec_{sec.section.number}'][f'ws{sec.section.workshop.number}_pigs_count'] \
                    = sec.pigs_count

            if hasattr(sec, 'sows_count'):
                data['sections'][f'sec_{sec.section.number}'][f'ws{sec.section.workshop.number}_sows_count'] \
                    = sec.sows_count

        workshops = Location.objects.all().filter(workshop__isnull=False) \
            .select_related('workshop') \
            .add_pigs_count_by_workshop() \
            .add_sows_count_by_workshop()

        count_all = 0

        for ws in workshops:
            data['workshops'][f'ws{ws.workshop.number}'] = {}
            data['workshops'][f'ws{ws.workshop.number}']['pigs_count'] = ws.pigs_count
            data['workshops'][f'ws{ws.workshop.number}']['sows_count'] = ws.sows_count
            count_all += ws.pigs_count if ws.pigs_count else 0
            count_all += ws.sows_count if ws.sows_count else 0

        data['ws_total'] = count_all

        return data


class LocationManager(CoreModelManager):
    def get_queryset(self):
        return LocationQuerySet(self.model, using=self._db)


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

    class Meta:
        ordering = ['pk']

    def __str__(self):
        return str(self.pk)

    @property
    def get_location(self):
        if self.workshop:
            return self.workshop

        if self.section:
            return self.section

        if self.pigletsGroupCell:
            return self.pigletsGroupCell

        if self.sowAndPigletsCell:
            return self.sowAndPigletsCell

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

    @property
    def is_empty(self):
        if not self.piglets.all() and \
            not self.sow_set.all():
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
    def get_full_loc(self):
        if self.sowSingleCell:
            return f'{self.sowSingleCell.workshop.number}/{self.sowSingleCell.section.number}/' \
                + f'{self.sowSingleCell.number}'

        if self.pigletsGroupCell:
            return f'{self.pigletsGroupCell.workshop.number}/{self.pigletsGroupCell.section.number}'\
                + f'/{self.pigletsGroupCell.number}'

        if self.sowAndPigletsCell:
            return f'{self.sowAndPigletsCell.workshop.number}/{self.sowAndPigletsCell.section.number}/'\
                + f'{self.sowAndPigletsCell.number}'

        if self.sowGroupCell:
            return f'{self.sowGroupCell.workshop.number}/{self.sowGroupCell.section.number}/'\
                + f'{self.sowGroupCell.number}'

        if self.workshop:
            return f'Цех {self.workshop.number}'

        if self.section:
            return f'Цех {self.section.workshop.number}/секция {self.section.number}'

        return None

    @property
    def get_sow(self):
        return self.sow_set.all().first()

    @property
    def get_piglets(self):
        return self.piglets.all().first()