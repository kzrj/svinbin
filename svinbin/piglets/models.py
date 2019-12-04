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

    def active_and_inactive(self):
        return self.filter(Q(active=False) | Q(active=True))


class PigletsManager(CoreModelManager):
    def get_queryset(self):
        return PigletsQuerySet(self.model, using=self._db).select_related('metatour')

    def get_active(self):
        return self.get_queryset().active()

    def get_inactive(self):
        return self.get_queryset().inactive()

    def get_active_and_inactive(self):
        return self.get_queryset().active_and_inactive()


class Piglets(CoreModel):
    location = models.ForeignKey('locations.Location', on_delete=models.SET_NULL,
        null=True, related_name='piglets')
    status = models.ForeignKey(PigletsStatus, on_delete=models.SET_NULL, null=True)

    start_quantity = models.IntegerField()
    quantity = models.IntegerField()
    gilts_quantity = models.IntegerField(default=0)

    merger_as_parent = models.ForeignKey('piglets_events.PigletsMerger', on_delete=models.SET_NULL,
        null=True, related_name='piglets_as_parents')

    split_as_child = models.ForeignKey('piglets_events.PigletsSplit', on_delete=models.SET_NULL,
        null=True, related_name='piglets_as_child')

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

    # def add_gilts(self, quantity):
    #     self.gilts_quantity += quantity
    #     self.save()

    # def add_gilts_increase_quantity(self, quantity):
    #     self.quantity += quantity
    #     self.gilts_quantity += quantity
    #     self.save()

    @property
    def metatour_repr(self):
        return self.metatour.records_repr()

    def change_location(self, location):
        self.location = location
        self.save()