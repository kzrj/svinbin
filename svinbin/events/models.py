# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone

from pigs.models import Sow
from tours.models import Tour


class Event(models.Model):
    date = models.DateTimeField(null=True)
    initiator = models.ForeignKey('workshops.WorkShopEmployee',
     on_delete=models.SET_NULL, null=True)
    
    class Meta:
        abstract = True


class SowEvent(Event):
    sow = models.ForeignKey('pigs.Sow', on_delete=models.CASCADE)
    tour = models.ForeignKey('tours.Tour', null=True, on_delete=models.CASCADE)

    class Meta:
        abstract = True

    
class SeminationManager(models.Manager):
    def create_semination(self, sow_farm_id, week, initiator=None, semination_employee=None):
        sow = Sow.objects.get_by_farm_id(sow_farm_id)
        tour = Tour.objects.get_or_create_by_week_in_current_year(week)
        semination = self.create(sow=sow, tour=tour, initiator=initiator,
         semination_employee=semination_employee, date=timezone.now())
        sow.tour = tour
        sow.save()
        return semination


class Semination(SowEvent):
    semination_employee = models.ForeignKey('workshops.WorkShopEmployee',
     on_delete=models.SET_NULL, null=True, related_name="semination_employee")
    # boar 

    objects = SeminationManager()


class UltrasoundManager(models.Manager):
    def create_ultrasound(self, sow_farm_id, week, initiator=None, result=False):
        sow = Sow.objects.get_by_farm_id(sow_farm_id)
        tour = Tour.objects.get_tour_by_week_in_current_year(week)
        ultrasound = self.create(sow=sow, tour=tour, initiator=initiator,
         date=timezone.now(), result=result)
        if result:
            sow.change_status_to_pregnant_in_workshop_one
        else:
            sow.change_status_to_proholost
        return ultrasound


class Ultrasound(SowEvent):
    result = models.BooleanField()

    objects = UltrasoundManager()


class SlaughterSowManager(models.Manager):
    def create_slaughter(self, sow_farm_id, slaughter_type, initiator=None, result=False):
        sow = Sow.objects.get_by_farm_id(sow_farm_id)
        slaughter = self.create(sow=sow, initiator=initiator,
         date=timezone.now(), slaughter_type=slaughter_type)
        sow.change_status_to(status_title='has slaughtered special', alive=False)

        return slaughter


class SlaughterSow(SowEvent):
    SLAUGHTER_TYPES = [('spec', 'spec uboi'), ('padej', 'padej'), ('prirezka', 'prirezka')]
    slaughter_type = models.CharField(max_length=50, choices=SLAUGHTER_TYPES)

    objects = SlaughterSowManager()
