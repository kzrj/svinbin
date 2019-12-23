# -*- coding: utf-8 -*-
import random

from locations.models import Location, SowSingleCell, SowGroupCell, Section, WorkShop, \
    SowAndPigletsCell, PigletsGroupCell
from sows.models import Sow, SowStatus, Gilt, Boar
from sows_events.models import Semination, SowFarrow, Ultrasound


FARM_ID_COUNT = 100000

def create_statuses():
    if SowStatus.objects.all().count() < 1:
        SowStatus.objects.bulk_create([
            SowStatus(title='Осеменена 1'),
            SowStatus(title='Осеменена 2'),
            SowStatus(title='Супорос 28'),
            SowStatus(title='Супорос 35'),
            SowStatus(title='Прохолост'),
            SowStatus(title='Аборт'),
            SowStatus(title='Отъем'),            
            SowStatus(title='Брак'),
            SowStatus(title='Опоросилась'),
            SowStatus(title='Кормилица'),
            SowStatus(title='Ожидает осеменения'),
            ])


def create_sow_and_put_in_workshop_one(section_number=None, cell_number=None):
    if section_number:
        section = Section.objects.get(workshop=WorkShop.objects.get(number=1), number=section_number)
        if cell_number:
            cell = SowSingleCell.objects.get(section=section, number=cell_number)
            location = Location.objects.get(sowSingleCell=cell)
            sow = Sow.objects.create(farm_id=random.randint(1, FARM_ID_COUNT), location=location)
            cell.sow = sow
            cell.save()
        else:
            location = Location.objects.get(section=section)
            sow = Sow.objects.create(farm_id=random.randint(1, FARM_ID_COUNT), location=location)
    else:
        location = Location.objects.get(workshop=WorkShop.objects.get(number=1))
        sow = Sow.objects.create(farm_id=random.randint(1, FARM_ID_COUNT), location=location)
    return sow

def create_sow_and_put_in_workshop_two(section_number, cell_number):
    section = Section.objects.get(workshop=WorkShop.objects.get(number=2), number=section_number)
    cell = SowGroupCell.objects.get(section=section, number=cell_number)
    location = Location.objects.get(sowGroupCell=cell)
    sow = Sow.objects.create(farm_id=random.randint(1, FARM_ID_COUNT), location=location)
    cell.sows.add(sow)
    return sow

def create_sow_and_put_in_workshop_three(section_number=1, cell_number=1):
    section = Section.objects.get(workshop=WorkShop.objects.get(number=3), number=section_number)
    cell = SowAndPigletsCell.objects.get(section=section, number=cell_number)
    location = Location.objects.get(sowAndPigletsCell=cell)
    sow = Sow.objects.create(farm_id=random.randint(1, FARM_ID_COUNT), location=location)
    return sow

def create_sow_and_put_in_workshop_three_section(section_number=1, cell_number=1):
    section = Section.objects.get(workshop__number=3, number=section_number)
    location = Location.objects.get(section=section)
    sow = Sow.objects.create(farm_id=random.randint(1, FARM_ID_COUNT), location=location)
    return sow

def create_sow_with_semination_and_put_in_workshop_three(week=1, section_number=1, cell_number=1):
    sow = create_sow_and_put_in_workshop_three(section_number, cell_number)
    Semination.objects.create_semination(sow=sow, week=week,
     initiator=None, semination_employee=None)
    return sow

def create_sow_seminated_usouded_ws3_section(week=1, section_number=1):
    sow = create_sow_and_put_in_workshop_three_section(section_number)
    Semination.objects.create_semination(sow=sow, week=week,
     initiator=None, semination_employee=None)
    Ultrasound.objects.create_ultrasound(sow=sow, days=30, result=True)
    Ultrasound.objects.create_ultrasound(sow=sow, days=60, result=True)
    return sow
    
def create_sow_with_location(location, farm_id=None):
    init_farm_id = random.randint(1, FARM_ID_COUNT)
    if farm_id:
        init_farm_id = farm_id
    sow = Sow.objects.create(farm_id=init_farm_id, location=location)
    return sow

def create_sow_with_semination(location, week=1):
    sow = create_sow_with_location(location)
    Semination.objects.create_semination(sow=sow, week=week)
    return sow

def create_sow_with_semination_usound(location, week=1):
    sow = create_sow_with_location(location)
    Semination.objects.create_semination(sow=sow, week=week)
    Ultrasound.objects.create_ultrasound(sow=sow, days=30, result=True)
    Ultrasound.objects.create_ultrasound(sow=sow, days=60, result=True)
    return sow

def create_gilt(birth_id):
    sow = create_sow_and_put_in_workshop_three(week=1)
    SowFarrow.objects.create_sow_farrow_by_sow_object(sow=sow, week=1, alive_quantity=10)
    gilt = Gilt.objects.create_gilt(birth_id, sow)
    return gilt

def create_sow_without_farm_id_with_birth_id(birth_id):
    sow = Sow.objects.create(birth_id=birth_id,
        location=Location.objects.get(section=Section.objects.get(workshop__number=1, number=3)))
    return sow

def create_some_sows_with_tours_put_in_ws_one():
    location = Location.objects.get(workshop__number=1)
    for tour_number in range(1, 4):
        for i in range(1, 4):
            create_sow_with_semination(location, tour_number)


def create_boars():
    if Boar.objects.all().count() < 1:
        Boar.objects.create_boar(1)
        Boar.objects.create_boar(2)
