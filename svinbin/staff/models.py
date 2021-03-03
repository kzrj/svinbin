# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError as DjangoValidationError

from core.models import CoreModel, CoreModelManager


class WorkShopEmployeeModelManager(CoreModelManager):
	def get_seminator_by_farm_name(self, farm_name):
		ws_employee = self.get_queryset().filter(farm_name=farm_name).first()
		if ws_employee:
			return ws_employee.user
		raise DjangoValidationError(message='Нет сотрудника с фарм_именем {}'.format(farm_name))


class WorkShopEmployee(CoreModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="employee")
    farm_name = models.CharField(max_length=20, default='')
    workshop = models.ForeignKey('locations.WorkShop', on_delete=models.CASCADE, null=True, blank=True)
    access_workshops = models.ManyToManyField('locations.WorkShop', related_name='access_employees') 

    is_officer = models.BooleanField(default=False)
    is_operator = models.BooleanField(default=False)
    is_seminator = models.BooleanField(default=False)
    is_veterinar = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = WorkShopEmployeeModelManager()

    def __str__(self):
        return self.farm_name