# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from django.db import models
from core.models import CoreModel, CoreModelManager, Event


class VetEvent(Event):
    sow = models.ForeignKey('sows.Sow', on_delete=models.SET_NULL, null=True, blank=True)
    piglets = models.ForeignKey('piglets.Piglets', on_delete=models.SET_NULL, null=True, blank=True)

    VET_METHODS = [('feed', 'feed'), ('water', 'water'), ('inj', 'inj') ]
    med_method = models.CharField(max_length=10, choices=MED_METHODS, null=True, blank=True)

    comment = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        abstract = True


class VetItem(CoreModel):
    VET_GROUPS = [('sows', 'sows'), ('gilts', 'gilts'), ('piglets', 'piglets') ]
    vet_group = models.CharField(max_length=10, choices=VET_GROUPS, default='piglets')   
    name = models.CharField(max_length=100)

    class Meta:
        abstract = True
    

class Vaccine(VetItem):
    def __str__(self):
        return f'vac {self.name}'


class VaccinationEvent(VetEvent):
    vaccine = models.ForeignKey(Vaccine, on_delete=models.CASCADE)

    def __str__(self):
        return f'vac event {self.pk}'


class Drug(VetItem):
    def __str__(self):
        return f'drug {self.name}'


class DrugEvent(VetEvent):
    HEAL_TYPES = [('heal', 'heal'), ('prof', 'prof')]
    heal_type = models.CharField(max_length=20, choices=HEAL_TYPES, default='heal')

    drug = models.ForeignKey(Drug, on_delete=models.CASCADE, related_name='drugs')
    doze = models.CharField(max_length=100)

    def __str__(self):
        return f'drug event {self.pk}'