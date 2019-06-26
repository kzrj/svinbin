# -*- coding: utf-8 -*-
import random

from workshops.models import SowSingleCell, SowGroupCell, Section, WorkShop, SowAndPigletsCell, PigletsGroupCell
from transactions.models import Location, PigletsTransaction
from sows.models import Sow, SowStatus
from piglets.models import NewBornPigletsGroup
from sows_events.models import Semination, SowFarrow
from piglets_events.models import NewBornPigletsMerger


def create_statuses():
    if SowStatus.objects.all().count() < 1:
        SowStatus.objects.bulk_create([
            SowStatus(title='just seminated'),
            SowStatus(title='waiting ultrasound'),
            SowStatus(title='pregnant in workshop one'),
            SowStatus(title='proholost'),
            SowStatus(title='pregnant in workshop two'),
            SowStatus(title='has slaughtered special'),
            SowStatus(title='waiting delivery in workshop three'),
            SowStatus(title='Опоросилась, кормит'),
            ])


def create_sow_and_put_in_workshop_one(section_number=None, cell_number=None):
    if section_number:
        section = Section.objects.get(workshop=WorkShop.objects.get(number=1), number=section_number)
        if cell_number:
            cell = SowSingleCell.objects.get(section=section, number=cell_number)
            location = Location.objects.create(sowSingleCell=cell)
            sow = Sow.objects.create(farm_id=random.randint(1, 1000), location=location)
            cell.sow = sow
            cell.save()
        else:
            location = Location.objects.create(section=section)
            sow = Sow.objects.create(farm_id=random.randint(1, 1000), location=location)
    else:
        location = Location.objects.create(workshop=WorkShop.objects.get(number=1))
        sow = Sow.objects.create(farm_id=random.randint(1, 1000), location=location)
    return sow

def create_sow_and_put_in_workshop_two(section_number, cell_number):
    section = Section.objects.get(workshop=WorkShop.objects.get(number=2), number=section_number)
    cell = SowGroupCell.objects.get(section=section, number=cell_number)
    location = Location.objects.create(sowGroupCell=cell)
    sow = Sow.objects.create(farm_id=random.randint(1, 1000), location=location)
    cell.sows.add(sow)
    return sow

def create_sow_and_put_in_workshop_three(section_number=1, cell_number=1):
    section = Section.objects.get(workshop=WorkShop.objects.get(number=3), number=section_number)
    cell = SowAndPigletsCell.objects.get(section=section, number=cell_number)
    location = Location.objects.create(sowAndPigletsCell=cell)
    sow = Sow.objects.create(farm_id=random.randint(1, 1000), location=location)
    return sow

def create_sow_with_semination_and_put_in_workshop_three(week=1, section_number=1, cell_number=1):
    sow = create_sow_and_put_in_workshop_three(section_number, cell_number)
    Semination.objects.create_semination(sow_farm_id=sow.farm_id, week=week,
     initiator=None, semination_employee=None)
    return sow
    
def create_sow_with_location(location):
    sow = Sow.objects.create(farm_id=random.randint(1, 1000), location=location)
    return sow

def create_sow_with_semination(location, week=1):
    sow = create_sow_with_location(location)
    Semination.objects.create_semination_object(sow=sow, week=week)
    return sow