# -*- coding: utf-8 -*-
from mixer.backend.django import mixer

from django.contrib.auth.models import User

from staff.models import WorkShopEmployee


def create_employee():
    user = mixer.blend('auth.user', username='test_user', password=123)
    WorkShopEmployee.objects.create(user=user)
    return user


def create_seminator()
    user = mixer.blend('auth.user', username='test_seminator', password=123)
    WorkShopEmployee.objects.create(user=user, is_seminator=True)
    return user