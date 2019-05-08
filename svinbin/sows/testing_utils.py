# -*- coding: utf-8 -*-
import random

from workshops.models import SowSingleCell, SowGroupCell
from transactions.models import Location
from sows.models import Sow


def create_sow_and_put_in_workshop_one(section_number, cell_number):
    cell = SowSingleCell.objects.get(section=section_number, number=cell_number)
    location = Location.objects.create(sowSingleCell=cell)
    sow = Sow.objects.create(birth_id=random.randint(1, 1000), location=location)
    return sow

def create_sow_and_put_in_workshop_two(section_number, cell_number):
    cell = SowGroupCell.objects.get(section=section_number, number=cell_number)
    location = Location.objects.create(sowGroupCell=cell)
    sow = Sow.objects.create(birth_id=random.randint(1, 1000), location=location)
    return sow

def create_sow_and_put_in_workshop_three(section_number, cell_number):
    cell = SowAndPigletsCell.objects.get(section=section_number, number=cell_number)
    location = Location.objects.create(sowAndPigletsCell=cell)
    sow = Sow.objects.create(birth_id=random.randint(1, 1000), location=location)
    return sow
    