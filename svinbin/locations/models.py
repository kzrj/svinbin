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

        alive_sup_sows = Count('sow', filter=Q(sow__alive=True,
                            sow__status__title__in=['Супорос 28', 'Супорос 35']))
        subquery_sows_sup_count = self.get_workshop_location(OuterRef('workshop')) \
                        .annotate(flag=Value(0)) \
                        .values('flag') \
                        .annotate(all=alive_sup_sows)\
                        .values('all')

        alive_sem_sows = Count('sow', filter=Q(sow__alive=True,
             sow__status__title__in=['Осеменена 1', 'Осеменена 2']))
        subquery_sows_sem_count = self.get_workshop_location(OuterRef('workshop')) \
                        .annotate(flag=Value(0)) \
                        .values('flag') \
                        .annotate(all=alive_sem_sows)\
                        .values('all')

        alive_wait_sows = Count('sow', filter=Q(sow__alive=True,
             sow__status__title__in=['Ожидает осеменения', 'Прохолост', 'Аборт']))
        subquery_sows_wait_count = self.get_workshop_location(OuterRef('workshop')) \
                        .annotate(flag=Value(0)) \
                        .values('flag') \
                        .annotate(all=alive_wait_sows)\
                        .values('all')

        alive_rem_sows = Count('sow', filter=Q(sow__alive=True,
             sow__status__title__in=['Ремонтная']))
        subquery_sows_rem_count = self.get_workshop_location(OuterRef('workshop')) \
                        .annotate(flag=Value(0)) \
                        .values('flag') \
                        .annotate(all=alive_rem_sows)\
                        .values('all')

        alive_far_sows = Count('sow', filter=Q(sow__alive=True,
             sow__status__title__in=['Опоросилась']))
        subquery_sows_far_count = self.get_workshop_location(OuterRef('workshop')) \
                        .annotate(flag=Value(0)) \
                        .values('flag') \
                        .annotate(all=alive_far_sows)\
                        .values('all')

        alive_nurse_sows = Count('sow', filter=Q(sow__alive=True,
             sow__status__title__in=['Кормилица', 'Отъем']))
        subquery_sows_nurse_count = self.get_workshop_location(OuterRef('workshop')) \
                        .annotate(flag=Value(0)) \
                        .values('flag') \
                        .annotate(all=alive_nurse_sows)\
                        .values('all')

        return self.annotate(
            sows_count=models.Subquery(subquery, output_field=models.IntegerField()),
            sows_sup_count=models.Subquery(subquery_sows_sup_count, output_field=models.IntegerField()),
            sows_sem_count=models.Subquery(subquery_sows_sem_count, output_field=models.IntegerField()),
            sows_wait_count=models.Subquery(subquery_sows_wait_count, output_field=models.IntegerField()),
            sows_rem_count=models.Subquery(subquery_sows_rem_count, output_field=models.IntegerField()),
            sows_far_count=models.Subquery(subquery_sows_far_count, output_field=models.IntegerField()),
            sows_nurse_count=models.Subquery(subquery_sows_nurse_count, output_field=models.IntegerField()),
        )

    def add_pigs_count_by_workshop(self):    
        alive_piglets = Sum('piglets__quantity', filter=Q(piglets__active=True))    
        subquery = self.get_workshop_location(OuterRef('workshop')) \
                        .annotate(flag=Value(0)) \
                        .values('flag') \
                        .annotate(all=alive_piglets)\
                        .values('all')

        return self.annotate(
            pigs_count=models.Subquery(subquery, output_field=models.IntegerField()),
            )

    def gen_piglets_count_by_age_subquery(self, locs, date, start_age_days, end_age_days=None):
        if end_age_days:
            all_subquery = Sum('piglets__quantity',
                                     filter=Q(
                                        piglets__active=True,
                                        piglets__birthday__gte=(date-timedelta(days=end_age_days)),
                                        piglets__birthday__lte=(date-timedelta(days=start_age_days))
                                        )
                                     )
        else:
            all_subquery = Sum('piglets__quantity',
                                     filter=Q(
                                        piglets__active=True,
                                        piglets__birthday__lte=(date-timedelta(days=start_age_days))
                                        )
                                     )
        return models.Subquery(
            locs \
                .annotate(flag=Value(0)) \
                .values('flag') \
                .annotate(all=all_subquery)\
                .values('all'), output_field=models.IntegerField())

    def gen_piglets_count_by_age_subqueries_locs(self, locs, date, age_intervals):
        data = dict()
        for interval in age_intervals:
            end_age = interval[1] if interval[1] else 'plus'
            data[f'count_piglets_{interval[0]}_{end_age}'] = self.gen_piglets_count_by_age_subquery(
                locs=locs, date=date, start_age_days=interval[0], end_age_days=interval[1])

        return data

    def add_pigs_count_by_workshop_by_age(self, date, age_intervals):
        locs = self.get_workshop_location(OuterRef('workshop'))
        data = self.gen_piglets_count_by_age_subqueries_locs(locs=locs, date=date, 
            age_intervals=age_intervals)

        return self.annotate(**data)

    def add_pigs_count_by_sections(self):
        alive_piglets = Sum('piglets__quantity', filter=Q(piglets__active=True))
        subquery_piglets_count = self.get_locations_in_section(OuterRef('section')) \
                        .values('workshop') \
                        .annotate(all=alive_piglets)\
                        .values('all')

        return self.annotate(
            pigs_count=models.Subquery(subquery_piglets_count),
            )

    def add_pigs_count_by_ws_sections_by_age(self, date, age_intervals):
        locs = self.get_locations_in_section(OuterRef('section'))
        data = self.gen_piglets_count_by_age_subqueries_locs(locs=locs, date=date, 
            age_intervals=age_intervals)

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

    def add_section_fullness(self):
        subquery_full_cells = Location.objects.all().filter(
                Q(Q(pigletsGroupCell__section=OuterRef('section')) |
                  Q(sowAndPigletsCell__section=OuterRef('section'))),
                  piglets__active=True) \
            .values('section') \
            .annotate(count_full=Count('id', distinct=True))\
            .values('count_full')

        subquery_all_cells = Location.objects.all().filter(
                Q(Q(pigletsGroupCell__section=OuterRef('section')) |
                  Q(sowAndPigletsCell__section=OuterRef('section')))) \
            .values('section') \
            .annotate(count_all=Count('*'))\
            .values('count_all')

        return self.annotate(
            count_full=models.Subquery(subquery_full_cells),
            count_all=models.Subquery(subquery_all_cells),
            )

    def add_sows_culls_count(self):
        locs = self.get_workshop_location(OuterRef('workshop')) \
            .annotate(flag=Value(0)) \
            .values('flag') \
            .annotate(count_sow_culls=Count('sow_cullings_here',
                 filter=Q(sow_cullings_here__culling_type='padej')))\
            .values('count_sow_culls')

        return self.annotate(count_sow_culls_padej=Subquery(locs, output_field=models.IntegerField()))

        

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

    @property
    def ws_aggregate_piglets_by_tours(self):
        if self.workshop and self.workshop.number not in [1, 2]:
            return self.piglets.aggregate_by_tour_in_ws(ws_number=self.workshop.number)
        return None