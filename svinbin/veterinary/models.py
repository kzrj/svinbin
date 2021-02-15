# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from django.db import models
from core.models import CoreModel, CoreModelManager, Event


class Drug(CoreModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Recipe(CoreModel):
    MED_TYPES = [
        ('vac', 'Вакцинация'), ('heal', 'Лечение'),
        ('prev', 'Профилактика'),]
    MED_METHODS = [
        ('feed', 'Корм'), ('inj', 'Инъекция'),
        ('water', 'Вода'),]

    med_type = models.CharField(max_length=50, choices=MED_TYPES)
    med_method = models.CharField(max_length=30, choices=MED_METHODS)
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE, related_name='recipes')
    doze = models.CharField(max_length=50, null=True, blank=True)

    @property
    def get_med_type(self):
        for mt in self.MED_TYPES:
            if self.med_type == mt[0]:
                return mt[1]
        return None

    @property
    def get_med_method(self):
        for mm in self.MED_METHODS:
            if self.med_method == mm[0]:
                return mm[1]
        return None

    def __str__(self):
        return f'{self.get_med_type} {self.get_med_method} {self.drug} {self.doze}'


class PigletsVetEventManager(CoreModelManager):
    def create_vet_event(self, piglets, recipe, date=None, initiator=None):
        event = self.create(recipe=recipe, date=date, initiator=initiator, location=piglets.location,
            piglets_quantity=piglets.quantity, week_tour=piglets.metatour.week_tour,
            target_piglets=piglets)
        event.piglets.add(piglets)
        return event


class PigletsVetEvent(Event):
    location = models.ForeignKey('locations.Location', on_delete=models.SET_NULL, null=True, 
        related_name='piglets_vet_events')
    week_tour = models.ForeignKey('tours.Tour', on_delete=models.SET_NULL, null=True, 
        related_name='piglets_vet_events')
    piglets_quantity = models.IntegerField(null=True)

    target_piglets = models.ForeignKey('piglets.Piglets', on_delete=models.SET_NULL, null=True,
        related_name='piglets_vet_events_as_target')

    piglets = models.ManyToManyField('piglets.Piglets')
    recipe = models.ForeignKey(Recipe, on_delete=models.SET_NULL, null=True, 
        related_name='piglets_vet_events')

    objects = PigletsVetEventManager()

    def __str__(self):
        return f'{self.recipe}'

    class Meta:
        ordering = ['-date']
