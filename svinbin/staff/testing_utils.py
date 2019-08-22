# -*- coding: utf-8 -*-
from mixer.backend.django import mixer

from django.contrib.auth.models import User

from staff.models import WorkShopEmployee


def create_employee():
    user = mixer.blend('auth.user')
    WorkShopEmployee.objects.create(user=user, is_seminator=True)
    return user


def create_test_users():
    try:
        user = User.objects.create_user('test_seminator', 't@t.ru', 'qwerty123')
        WorkShopEmployee.objects.create(user=user, is_seminator=True)
        return user
    except:
        pass