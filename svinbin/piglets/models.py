# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import Q, Sum, Avg
from django.core.exceptions import ValidationError as DjangoValidationError

from core.models import CoreModel, CoreModelManager
from tours.models import MetaTour, MetaTourRecord, Tour


class PigletsStatus(CoreModel):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class PigletsQuerySet(models.QuerySet):
    def get_total_quantity(self):
        return self.aggregate(models.Sum('quantity'))['quantity__sum']

    def get_total_gilts_quantity(self):
        return self.aggregate(models.Sum('gilts_quantity'))['gilts_quantity__sum']

    def active(self):
        return self.filter(active=True)

    def inactive(self):
        return self.filter(active=False)

    def piglets_with_weighing_record(self, place):
        return self.prefetch_related('weighing_records') \
                    .filter(weighing_records__place=place) \
                    .distinct()

    def piglets_without_weighing_record(self, place):
        return self.prefetch_related('weighing_records') \
                    .filter(~Q(weighing_records__place=place)) \
                    .distinct()

    def with_tour(self, week_number):
        return self.filter(metatour__records__tour__week_number=week_number)

    def with_tour_not_mixed(self, week_number):
        return self.filter(metatour__records__tour__week_number=week_number, metatour__records__percentage=100)

    def with_tour_mixed(self, week_number):
        return self.filter(metatour__records__tour__week_number=week_number, metatour__records__percentage__lt=100)

    def count_piglets_in_mixed_groups(self, week_number):
        subquery = MetaTourRecord.objects.filter(metatour__piglets__pk=models.OuterRef('pk'), tour__week_number=week_number) \
            .values('quantity')

        return self.with_tour_mixed(week_number=week_number).annotate(
            count_piglets=models.Subquery(subquery, output_field=models.IntegerField())
            ).aggregate(models.Sum('count_piglets'))['count_piglets__sum']

    def count_piglets_in_mixed_group_annotate(self, week_number):
        subquery = MetaTourRecord.objects.filter(metatour__piglets__pk=models.OuterRef('pk'), 
                                                    tour__week_number=week_number) \
                                        .values('quantity')

        return self.with_tour_mixed(week_number=week_number) \
                    .annotate(
                        count_piglets=models.Subquery(subquery, output_field=models.IntegerField())
                    ) 
                    # .annotate(cnt=models.Sum('count_piglets')).values('cnt')[:1]


    def all_in_workshop(self, workshop_number):
        return self.filter(Q(
            Q(location__workshop__number=workshop_number) |
            Q(location__section__workshop__number=workshop_number) |
            Q(location__pigletsGroupCell__workshop__number=workshop_number) |
            Q(location__sowAndPigletsCell__workshop__number=workshop_number)
            )
        )

    def all_in_section(self, section):
        return self.filter(Q(
            Q(location__section=section) |
            Q(location__pigletsGroupCell__section=section) |
            Q(location__sowAndPigletsCell__section=section)
            )
        )


class PigletsManager(CoreModelManager):
    def get_queryset(self):
        return PigletsQuerySet(self.model, using=self._db).select_related('metatour').active()

    def get_all(self):
        return PigletsQuerySet(self.model, using=self._db)

    # for init and test only
    def init_piglets_with_metatour(self, tour, location, quantity, gilts_quantity=0, created_at=None):
    	piglets = self.create(location=location,
                start_quantity=quantity,
                quantity=quantity,
                gilts_quantity=gilts_quantity)
    	metatour = MetaTour.objects.create(piglets=piglets)
    	MetaTourRecord.objects.create_record(metatour, tour, quantity, quantity)
    	return piglets

    # test use kwargs
    def init_piglets_by_week(self, *args, **kwargs):
    	tour = Tour.objects.get_or_create_by_week_in_current_year(kwargs['week'])
    	kwargs.pop('week')
    	kwargs['tour'] = tour
    	return self.init_piglets_with_metatour(**kwargs)

    def init_piglets_by_farrow_date(self, farrow_date, location, quantity, gilts_quantity=0):
    	tour = Tour.objects.create_tour_from_farrow_date_string(farrow_date)
    	return self.init_piglets_with_metatour(tour, location, quantity, gilts_quantity)


class Piglets(CoreModel):
    location = models.ForeignKey('locations.Location', on_delete=models.SET_NULL,
        null=True, related_name='piglets')
    status = models.ForeignKey(PigletsStatus, on_delete=models.SET_NULL, null=True)

    start_quantity = models.IntegerField()
    quantity = models.IntegerField()
    gilts_quantity = models.IntegerField(default=0)

    merger_as_parent = models.ForeignKey('piglets_events.PigletsMerger', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='piglets_as_parents')

    split_as_child = models.ForeignKey('piglets_events.PigletsSplit', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='piglets_as_child')

    transfer_part_number = models.IntegerField(null=True, blank=True)

    active = models.BooleanField(default=True)  

    objects = PigletsManager()

    class Meta:
        ordering = ['pk',]

    def __str__(self):
        return 'Piglets {}'.format(self.pk)

    def deactivate(self):
        self.active = False
        self.save()

    def remove_piglets(self, quantity):
        self.quantity = self.quantity - quantity
        if self.quantity <= 0:
            self.active = False
        self.save()

    def remove_gilts(self, quantity):
        if self.gilts_quantity > 0:
            self.quantity -= quantity
            self.gilts_quantity -= quantity
            self.save()

    def remove_gilts_without_decrease_quantity(self, quantity):
        self.gilts_quantity -= quantity
        self.save()

    def add_gilts_without_increase_quantity(self, quantity):
        self.gilts_quantity += quantity
        self.save()

    def change_status_to(self, status_title):
        self.status = PigletsStatus.objects.get(title=status_title)
        self.save()

    def change_status_to_without_save(self, status_title):
        self.status = PigletsStatus.objects.get(title=status_title)

    def add_piglets(self, quantity):
        self.quantity = self.quantity + quantity
        self.save()

    @property
    def metatour_repr(self):
        return self.metatour.records_repr()

    # @property
    # def metatour_repr(self):
    #     return self.metatour.records_repr()

    def change_location(self, location):
        self.location = location
        self.save()

    def assign_transfer_part_number(self, number):
        self.transfer_part_number = number
        self.save()

    @property
    def is_it_gilts_group(self):
        if self.gilts_quantity > 0:
            return True
        return False

