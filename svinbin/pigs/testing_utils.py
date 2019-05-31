# -*- coding: utf-8 -*-
import random

from workshops.models import SowSingleCell, SowGroupCell, Section, WorkShop
from transactions.models import Location
from pigs.models import Sow, SowStatus


def create_statuses():
    SowStatus.objects.bulk_create([
        SowStatus(title='waiting ultrasound'),
        SowStatus(title='pregnant in workshop one'),
        SowStatus(title='proholost'),
        SowStatus(title='pregnant in workshop two'),
        ])


def create_sow_and_put_in_workshop_one(section_number=None, cell_number=None):
    if section_number:
        section = Section.objects.get(workshop=WorkShop.objects.get(number=1), number=section_number)
        if cell_number:
            cell = SowSingleCell.objects.get(section=section, number=cell_number)
            location = Location.objects.create(sowSingleCell=cell)
            sow = Sow.objects.create(birth_id=random.randint(1, 1000), location=location)
            cell.sow = sow
            cell.save()
        else:
            location = Location.objects.create(section=section)
            sow = Sow.objects.create(birth_id=random.randint(1, 1000), location=location)
    else:
        location = Location.objects.create(workshop=WorkShop.objects.get(number=1))
        sow = Sow.objects.create(birth_id=random.randint(1, 1000), location=location)
    return sow

def create_sow_and_put_in_workshop_two(section_number, cell_number):
    section = Section.objects.get(workshop=WorkShop.objects.get(number=2), number=section_number)
    cell = SowGroupCell.objects.get(section=section, number=cell_number)
    location = Location.objects.create(sowGroupCell=cell)
    sow = Sow.objects.create(birth_id=random.randint(1, 1000), location=location)
    cell.sows.add(sow)
    return sow

def create_sow_and_put_in_workshop_three(section_number, cell_number):
    section = Section.objects.get(workshop=WorkShop.objects.get(number=3), number=section_number)
    cell = SowAndPigletsCell.objects.get(section=section, number=cell_number)
    location = Location.objects.create(sowAndPigletsCell=cell)
    sow = Sow.objects.create(birth_id=random.randint(1, 1000), location=location)
    return sow
    
def create_sow_with_farm_id(location, farm_id):
    sow = Sow.objects.create(farm_id=random.randint(1, 1000), location=location)
    return sow

def create_sow_without_farm_id(location):
    sow = Sow.objects.create(birth_id=random.randint(1, 1000), location=location)
    return sow