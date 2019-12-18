# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import Q
from django.core.exceptions import ValidationError as DjangoValidationError

from core.models import CoreModel, CoreModelManager


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


class PigletsManager(CoreModelManager):
    def get_queryset(self):
        return PigletsQuerySet(self.model, using=self._db).select_related('metatour').active()

    def get_all(self):
        return PigletsQuerySet(self.model, using=self._db)


class Piglets(CoreModel):
    location = models.ForeignKey('locations.Location', on_delete=models.SET_NULL,
        null=True, related_name='piglets')
    status = models.ForeignKey(PigletsStatus, on_delete=models.SET_NULL, null=True)

    start_quantity = models.IntegerField()
    quantity = models.IntegerField()
    gilts_quantity = models.IntegerField(default=0)
    is_it_gilts_group = models.BooleanField(default=False)

    merger_as_parent = models.ForeignKey('piglets_events.PigletsMerger', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='piglets_as_parents')

    split_as_child = models.ForeignKey('piglets_events.PigletsSplit', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='piglets_as_child')

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

    def change_status_to(self, status_title):
        self.status = PigletsStatus.objects.get(title=status_title)
        self.save()

    def add_piglets(self, quantity):
        self.quantity = self.quantity + quantity
        self.save()

    @property
    def metatour_repr(self):
        return self.metatour.records_repr()

    def change_location(self, location):
        self.location = location
        self.save()

    @property
    def mark_as_gilts(self):
        self.is_it_gilts_group = True
        self.save()