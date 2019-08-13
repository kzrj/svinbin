# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
from django.conf import settings

from core.models import Event, CoreModel, CoreModelManager
from sows.models import Sow
from piglets.models import NewBornPigletsGroup, NomadPigletsGroup
from tours.models import Tour
from locations.models import WorkShop, Location


class SowEvent(Event):
    sow = models.ForeignKey('sows.Sow', on_delete=models.CASCADE)
    tour = models.ForeignKey('tours.Tour', null=True, on_delete=models.CASCADE)

    class Meta:
        abstract = True

    
class SeminationManager(CoreModelManager):
    def create_semination(self, sow, week, initiator=None, semination_employee=None):
        tour = Tour.objects.get_or_create_by_week_in_current_year(week)
        semination = self.create(sow=sow, tour=tour, initiator=initiator,
         semination_employee=semination_employee, date=timezone.now())
        sow.tour = tour
        sow.change_status_to('Осеменена')
        return semination


class Semination(SowEvent):
    semination_employee = models.ForeignKey(settings.AUTH_USER_MODEL,
     on_delete=models.SET_NULL, null=True, related_name="semination_employee")
    # boar 

    objects = SeminationManager()


class UltrasoundManager(CoreModelManager):
    def create_ultrasound(self, sow, initiator=None, result=False):
        ultrasound = self.create(sow=sow, tour=sow.tour, initiator=initiator,
         date=timezone.now(), result=result)
        if result:
            sow.change_status_to('Беременна')
        else:
            sow.tour = None
            sow.change_status_to('Прохолост')
        return ultrasound


class Ultrasound(SowEvent):
    result = models.BooleanField()

    objects = UltrasoundManager()


class UltrasoundV2Manager(CoreModelManager):
    def create_ultrasoundV2(self, sow, initiator=None, result=False):
        ultrasoundV2 = self.create(sow=sow, tour=sow.tour, initiator=initiator,
         date=timezone.now(), result=result)
        if result:
            sow.change_status_to('Беременна')
        else:
            sow.tour = None
            sow.change_status_to('Прохолост')
        return ultrasoundV2


class UltrasoundV2(SowEvent):
    result = models.BooleanField()

    objects = UltrasoundV2Manager()


class SowFarrowManager(CoreModelManager):
    def create_sow_farrow(self, sow, initiator=None,
        alive_quantity=0, dead_quantity=0, mummy_quantity=0):
        # tour = Tour.objects.get_tour_by_week_in_current_year(week)
        tour = sow.tour
        sow.change_status_to('Опоросилась, кормит')

        # check is it first sow_farrow in current tour
        previous_farrow_in_tour = SowFarrow.objects.filter(sow=sow, tour=tour).first()
        if previous_farrow_in_tour:
            new_born_piglets_group = previous_farrow_in_tour.new_born_piglets_group
            new_born_piglets_group.add_piglets(alive_quantity)
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
    new_born_piglets_group = models.ForeignKey(NewBornPigletsGroup, on_delete=models.SET_NULL,
     null=True, related_name='farrows')
    alive_quantity = models.IntegerField(default=0)
    dead_quantity = models.IntegerField(default=0)
    mummy_quantity = models.IntegerField(default=0)

    objects = SowFarrowManager()


class CullingSowManager(CoreModelManager):
    def create_culling(self, sow, culling_type, reason, initiator=None):
        culling = self.create(sow=sow, initiator=initiator, tour=sow.tour, reason=reason,
         date=timezone.now(), culling_type=culling_type)
        sow.change_status_to(status_title='Брак', alive=False)
        return culling

    def create_culling_from_farm_id(self, sow_farm_id, culling_type, reason, initiator=None):
        sow = Sow.objects.get_by_farm_id(sow_farm_id)
        return self.create_culling(sow, culling_type, reason, initiator)


class CullingSow(SowEvent):
    CULLING_TYPES = [('spec', 'spec uboi'), ('padej', 'padej'), ('prirezka', 'prirezka')]
    culling_type = models.CharField(max_length=50, choices=CULLING_TYPES)
    reason = models.CharField(max_length=300, null=True)

    objects = CullingSowManager()