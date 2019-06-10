# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone

from pigs.models import Sow, NewBornPigletsGroup
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
        sow.change_status_to('just seminated')
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
            sow.change_status_to('pregnant in workshop one')
        else:
            sow.change_status_to('proholost')
        return ultrasound


class Ultrasound(SowEvent):
    result = models.BooleanField()

    objects = UltrasoundManager()


class SowFarrowManager(models.Manager):
    def create_sow_farrow(self, sow_farm_id, week, initiator=None,
        alive_quantity=0, dead_quantity=0, mummy_quantity=0):
        sow = Sow.objects.get_by_farm_id(sow_farm_id)
        tour = Tour.objects.get_tour_by_week_in_current_year(week)

        # check is it first sow_farrow in courrent tour
        farrow = SowFarrow.objects.filter(sow=sow, tour=tour).first()
        if farrow:
            farrow.new_born_piglets_group.add_piglets(alive_quantity)
        else:
            new_born_piglets_group = NewBornPigletsGroup.objects.create(
                location=sow.location,
                start_quantity=alive_quantity,
                quantity=alive_quantity,
                tour=tour
                )
            farrow = self.create(sow=sow, tour=tour, initiator=initiator,
                date=timezone.now(), alive_quantity=alive_quantity,
                dead_quantity=dead_quantity, mummy_quantity=mummy_quantity,
                new_born_piglets_group=new_born_piglets_group
                )

        return farrow


class SowFarrow(SowEvent):
    new_born_piglets_group = models.ForeignKey('pigs.NewBornPigletsGroup', on_delete=models.SET_NULL, null=True)
    alive_quantity = models.IntegerField(default=0)
    dead_quantity = models.IntegerField(default=0)
    mummy_quantity = models.IntegerField(default=0)

    objects = SowFarrowManager()


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


class PigletsMerger(Event):
    pass


class NewBornPigletsMerger(PigletsMerger):

    @property
    def is_single_tour_merge(self):
        self.piglets_groups.all()
        
    

