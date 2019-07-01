# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models

from core.models import CoreModel, CoreModelManager


class WorkShopEmployee(CoreModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    workshop = models.ForeignKey('locations.WorkShop', on_delete=models.CASCADE, null=True)

    is_officer = models.BooleanField(default=False)
    is_seminator = models.BooleanField(default=False)

    def __str__(self):
        return 'Employee {} '.format(self.user.username)