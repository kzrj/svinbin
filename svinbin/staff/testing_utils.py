# -*- coding: utf-8 -*-
from mixer.backend.django import mixer

from django.contrib.auth.models import User

from staff.models import WorkShopEmployee
from locations.models import WorkShop


def create_employee(farm_name='', workshop=None):
    user = mixer.blend('auth.user')
    WorkShopEmployee.objects.create(user=user, is_seminator=True, farm_name=farm_name, workshop=workshop)
    return user

def create_user(username, farm_name, workshop=None):
    user = User.objects.create_user(username, 't@t.ru', 'svinbin123')
    WorkShopEmployee.objects.create(user=user, is_seminator=True, is_officer=False, farm_name=farm_name,
        workshop=workshop)
    return user

def create_workshop_user(username, password, ws_number, farm_name, is_seminator=False, is_officer=False,
        is_staff=False, is_veterinar=False):
    workshop = WorkShop.objects.filter(number=ws_number).first()
    user = User.objects.create_user(username=username, email='t@t.ru', password=password, is_staff=is_staff)
    WorkShopEmployee.objects.create(user=user, workshop=workshop, farm_name=farm_name, \
        is_seminator=is_seminator, is_officer=is_officer, is_veterinar=is_veterinar)
    return user


def create_svinbin_users():
    User.objects.create_superuser(username='kaizerj',email='kzrster@gmail.com', password='jikozfree')
    User.objects.create_superuser(username='smileman',email='r@gmail.com', password='bulatbulat')
    create_workshop_user(username='test_admin1', password='svinbin123', ws_number=1, 
        farm_name='АДМ', is_seminator=True, is_officer=True, is_staff=True)
    create_workshop_user(username='test_admin2', password='svinbin123', ws_number=1, 
        farm_name='АДМ', is_seminator=True, is_officer=True, is_staff=True)
    create_workshop_user(username='test_officer', password='svinbin123', ws_number=1, farm_name='ОФИЦЕР',
        is_seminator=True, is_officer=True)

    create_workshop_user(username='mitkinov', password='qwerty', ws_number=1, farm_name='ОФИЦЕР',
     is_seminator=True, is_officer=True)

    create_workshop_user(username='shmigina', password='123', ws_number=1, farm_name='ШМЫГИ',
     is_seminator=True, is_officer=True)
    create_workshop_user(username='borisov', password='123', ws_number=1, farm_name='БОРИС', 
        is_seminator=True)
    create_workshop_user(username='semenova', password='123', ws_number=1, farm_name='СЕМЕН', 
        is_seminator=True)
    create_workshop_user(username='gary', password='123', ws_number=1, farm_name='ГАРИ', 
        is_seminator=True, is_officer=True)
    create_workshop_user(username='ivanov', password='123', ws_number=1, farm_name='ИВАНО', 
        is_seminator=True)
    create_workshop_user(username='stude', password='123', ws_number=1, farm_name='СТУДЕ', 
        is_seminator=True)
    create_workshop_user(username='veterinar', password='123', ws_number=1, farm_name='СТУДЕ', 
        is_seminator=True, is_veterinar=True)

    create_workshop_user(username='brigadir1', password='123', ws_number=1, farm_name='ИВАНО')
    create_workshop_user(username='brigadir2', password='123', ws_number=2, farm_name='ИВАНО')
    create_workshop_user(username='brigadir3', password='123', ws_number=3, farm_name='ИВАНО')
    create_workshop_user(username='brigadir4', password='123', ws_number=4, farm_name='ИВАНО')
    create_workshop_user(username='brigadir5', password='123', ws_number=5, farm_name='ИВАНО')
    create_workshop_user(username='brigadir6', password='123', ws_number=6, farm_name='ИВАНО')
    create_workshop_user(username='brigadir7', password='123', ws_number=7, farm_name='ИВАНО')
    create_workshop_user(username='brigadir8', password='123', ws_number=8, farm_name='ИВАНО')
