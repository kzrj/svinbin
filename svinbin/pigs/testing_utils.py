# -*- coding: utf-8 -*-
import random

from workshops.models import SowSingleCell, SowGroupCell, Section, WorkShop, SowAndPigletsCell, PigletsGroupCell
from transactions.models import Location, PigletsTransaction
from pigs.models import Sow, SowStatus, NewBornPigletsGroup
from events.models import Semination, SowFarrow, NewBornPigletsMerger


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
            SowStatus(title='farrow, feed'),
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

def create_sow_and_put_in_workshop_three(section_number, cell_number):
    section = Section.objects.get(workshop=WorkShop.objects.get(number=3), number=section_number)
    cell = SowAndPigletsCell.objects.get(section=section, number=cell_number)
    location = Location.objects.create(sowAndPigletsCell=cell)
    sow = Sow.objects.create(farm_id=random.randint(1, 1000), location=location)
    return sow
    
def create_sow_with_farm_id(location, farm_id):
    sow = Sow.objects.create(farm_id=random.randint(1, 1000), location=location)
    return sow

def create_sow_without_farm_id(location):
    sow = Sow.objects.create(birth_id=random.randint(1, 1000), location=location)
    return sow


def create_nomad_group_from_three_new_born():
    sow1 = create_sow_and_put_in_workshop_three(1, 1)
    Semination.objects.create_semination(sow_farm_id=sow1.farm_id, week=1,
     initiator=None, semination_employee=None)

    farrow1 = SowFarrow.objects.create_sow_farrow(sow_farm_id=sow1.farm_id, week=1,
     alive_quantity=10)

    sow2 = create_sow_and_put_in_workshop_three(1, 2)
    Semination.objects.create_semination(sow_farm_id=sow2.farm_id, week=1,
     initiator=None, semination_employee=None)
    farrow2 = SowFarrow.objects.create_sow_farrow(sow_farm_id=sow2.farm_id, week=1,
        alive_quantity=12)

    sow3 = create_sow_and_put_in_workshop_three(1, 3)
    Semination.objects.create_semination(sow_farm_id=sow3.farm_id, week=2,
     initiator=None, semination_employee=None)
    farrow3 = SowFarrow.objects.create_sow_farrow(sow_farm_id=sow3.farm_id, week=2,
        alive_quantity=15)

    piglets_group1 = farrow1.new_born_piglets_group
    piglets_group2 = farrow2.new_born_piglets_group
    piglets_group3 = farrow3.new_born_piglets_group

    piglets_groups_two_tours = NewBornPigletsGroup.objects.filter(pk__in=
        [piglets_group1.pk, piglets_group2.pk, piglets_group3.pk])

    new_born_merger_two_tours = NewBornPigletsMerger.objects.create_merger(piglets_groups_two_tours)

    new_born_merger_two_tours.create_records()

    nomad_group = new_born_merger_two_tours.create_nomad_group()

    return nomad_group

def create_nomad_group_from_three_new_born2():
    sow1 = create_sow_and_put_in_workshop_three(1, 4)
    Semination.objects.create_semination(sow_farm_id=sow1.farm_id, week=2,
     initiator=None, semination_employee=None)

    farrow1 = SowFarrow.objects.create_sow_farrow(sow_farm_id=sow1.farm_id, week=2,
     alive_quantity=10)

    sow2 = create_sow_and_put_in_workshop_three(1, 5)
    Semination.objects.create_semination(sow_farm_id=sow2.farm_id, week=2,
     initiator=None, semination_employee=None)
    farrow2 = SowFarrow.objects.create_sow_farrow(sow_farm_id=sow2.farm_id, week=2,
        alive_quantity=10)

    sow3 = create_sow_and_put_in_workshop_three(1, 6)
    Semination.objects.create_semination(sow_farm_id=sow3.farm_id, week=3,
     initiator=None, semination_employee=None)
    farrow3 = SowFarrow.objects.create_sow_farrow(sow_farm_id=sow3.farm_id, week=3,
        alive_quantity=10)

    piglets_group1 = farrow1.new_born_piglets_group
    piglets_group2 = farrow2.new_born_piglets_group
    piglets_group3 = farrow3.new_born_piglets_group

    piglets_groups_two_tours = NewBornPigletsGroup.objects.filter(pk__in=
        [piglets_group1.pk, piglets_group2.pk, piglets_group3.pk])

    new_born_merger_two_tours = NewBornPigletsMerger.objects.create_merger(piglets_groups_two_tours)

    new_born_merger_two_tours.create_records()

    nomad_group = new_born_merger_two_tours.create_nomad_group()

    return nomad_group

def create_nomad_and_move_to_cell_in_workshop_four():
    nomad_group = create_nomad_group_from_three_new_born()

    section = Section.objects.get(workshop__number=4, number=1)
    piglet_group_cell = PigletsGroupCell.objects.get(section=section, number=1)
    to_location = Location.objects.create_location(piglet_group_cell)

    transaction = PigletsTransaction.objects.create_transaction_without_merge(to_location,
            nomad_group)

    return nomad_group

def create_new_born_group(section_number=1, cell_number=4, week_number=2, quantity=10):
    sow1 = create_sow_and_put_in_workshop_three(section_number, cell_number)
    Semination.objects.create_semination(sow_farm_id=sow1.farm_id, week=week_number,
     initiator=None, semination_employee=None)
    
    farrow1 = SowFarrow.objects.create_sow_farrow(sow_farm_id=sow1.farm_id, week=week_number,
     alive_quantity=quantity)

    return farrow1.new_born_piglets_group