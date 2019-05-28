# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone

from tours.models import Tour
from pigs.models import Sow


class Event(models.Model):
    date = models.DateTimeField(null=True)
    initiator = models.ForeignKey('workshops.WorkShopEmployee',
     on_delete=models.SET_NULL, null=True, related_name="initiator")
    
    class Meta:
        abstract = True


class SeminationManager(models.Manager):
	def create_semination(self, sow_farm_id, week, initiator=None, semination_employee=None):
		sow = Sow.objects.filter(farm_id=sow_farm_id).first()
		tour = Tour.objects.get_or_create_by_week_in_current_year(week)
		semination = self.create(sow=sow, tour=tour, initiator=initiator,
		 semination_employee=semination_employee, date=timezone.now())
		return semination


class Semination(Event):
	sow = models.ForeignKey('pigs.Sow', on_delete=models.CASCADE)
	semination_employee = models.ForeignKey('workshops.WorkShopEmployee',
	 on_delete=models.SET_NULL, null=True, related_name="semination_employee")
	# boar 
	tour = models.ForeignKey('tours.Tour', null=True, on_delete=models.CASCADE)

	objects = SeminationManager()
