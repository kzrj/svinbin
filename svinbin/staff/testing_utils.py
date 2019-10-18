# -*- coding: utf-8 -*-
from mixer.backend.django import mixer

from django.contrib.auth.models import User

from staff.models import WorkShopEmployee
from locations.models import WorkShop


def create_employee():
    user = mixer.blend('auth.user')
    WorkShopEmployee.objects.create(user=user, is_seminator=True)
    return user


def create_test_users():
    try:
        user = User.objects.create_user('test_seminator', 't@t.ru', 'qwerty123')
        WorkShopEmployee.objects.create(user=user, is_seminator=True, is_officer=True)
        return user
    except:
        pass


def create_workshop_user(username, password, ws_number, is_seminator=False, is_officer=False):
    workshop = WorkShop.objects.filter(number=ws_number).first()
    user = User.objects.create_user(username, 't@t.ru', password)
    WorkShopEmployee.objects.create(user=user, workshop=workshop, \
        is_seminator=is_seminator, is_officer=is_officer)
    return user