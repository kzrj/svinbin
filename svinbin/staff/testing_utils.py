# -*- coding: utf-8 -*-
from mixer.backend.django import mixer

from django.contrib.auth.models import User

from staff.models import WorkShopEmployee
from locations.models import WorkShop


def create_employee(farm_name=''):
    user = mixer.blend('auth.user')
    WorkShopEmployee.objects.create(user=user, is_seminator=True, farm_name=farm_name)
    return user


def create_test_users():
    try:
        user = User.objects.create_user('test_seminator', 't@t.ru', 'svinbin123')
        WorkShopEmployee.objects.create(user=user, is_seminator=True, is_officer=True)
        return user
    except:
        pass

def create_user(username, farm_name):
    user = User.objects.create_user(username, 't@t.ru', 'svinbin123')
    WorkShopEmployee.objects.create(user=user, is_seminator=True, is_officer=False, farm_name=farm_name)
    return user


def create_workshop_user(username, password, ws_number, farm_name, is_seminator=False, is_officer=False):
    workshop = WorkShop.objects.filter(number=ws_number).first()
    user = User.objects.create_user(username, 't@t.ru', password)
    WorkShopEmployee.objects.create(user=user, workshop=workshop, farm_name=farm_name, \
        is_seminator=is_seminator, is_officer=is_officer)
    return user


def create_svinbin_users():
    User.objects.create_superuser(username='kaizerj',email='kzrster@gmail.com', password='jikozfree')
    User.objects.create_superuser(username='smileman',email='r@gmail.com', password='bulatbulat')
    create_workshop_user('test_admin', 'svinbin123', 1, 'АДМ', True, True)
    create_workshop_user('test_officer', 'svinbin123', 1, 'ОФИЦЕР', True, True)

    create_workshop_user('shmigina', '123', 1, 'ШМЫГИ', True)
    create_workshop_user('borisov', '123', 1, 'БОРИС', True)
    create_workshop_user('semenova', '123', 1, 'СЕМЕН', True)
    create_workshop_user('gary', '123', 1, 'ГАРИ', True, True)
    create_workshop_user('ivanov', '123', 1, 'ИВАНО', True)
    create_workshop_user('stude', '123', 1, 'СТУДЕ', True)

    create_workshop_user('brigadir1', '123', 1, 'ИВАНО')
    create_workshop_user('brigadir2', '123', 2, 'ИВАНО')
    create_workshop_user('brigadir3', '123', 3, 'ИВАНО')
    create_workshop_user('brigadir4', '123', 4, 'ИВАНО')
    create_workshop_user('brigadir5', '123', 5, 'ИВАНО')
    create_workshop_user('brigadir6', '123', 6, 'ИВАНО')
    create_workshop_user('brigadir7', '123', 7, 'ИВАНО')
