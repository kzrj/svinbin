# -*- coding: utf-8 -*-

from workshops.models import WorkShop, WorkShopEmployee, Section, SowSingleCell, \
    PigletsGroupCell, SowAndPigletsCell, SowGroupCell


def create_workshops():
    WorkShop.objects.bulk_create([
        WorkShop(number=1, title='Осеменение'),
        WorkShop(number=2, title='Ожидание родов'),
        WorkShop(number=3, title='Маточник'),
        WorkShop(number=4, title='Доращивание 4'),
        WorkShop(number=8, title='Доращивание 8'),
        WorkShop(number=5, title='Откорм 5'),
        WorkShop(number=6, title='Откорм 6'),
        WorkShop(number=7, title='Откорм 7'),
        WorkShop(number=9, title='Убойный цех'),
        WorkShop(number=10, title='Крематорий')])

def create_sections_and_cell_for_workshop_one():
    workshop_one = WorkShop.objects.get(number=1)

    Section.objects.bulk_create([Section(workshop=workshop_one, name='Змейка', number=1),
     Section(workshop=workshop_one, name='Ряд осеменения', number=2)])

    workshop_one_section_1 = Section.objects.get(name='Змейка')
    SowSingleCell.objects.bulk_create([
        SowSingleCell(section=workshop_one_section_1, number=cellNumber) for cellNumber in range(1, 481)
        ])

def create_sections_and_cell_for_workshop_two():
    workshop_two = WorkShop.objects.get(number=2)

    Section.objects.bulk_create([Section(workshop=workshop_two, name='Секция 2-1', number=1),
     Section(workshop=workshop_two, name='Секция 2-2', number=2)])

    for section in Section.objects.filter(workshop=workshop_two):
        SowGroupCell.objects.bulk_create([
            SowGroupCell(section=section, number=cellNumber) for cellNumber in range(1, 7)]
            )

def create_sections_and_cell_for_workshop_three():
    workshop_three = WorkShop.objects.get(number=3)

    Section.objects.bulk_create([Section(workshop=workshop_three, name='Секция 3-1', number=1),
     Section(workshop=workshop_three, name='Секция 3-2', number=2)])

    for section in Section.objects.filter(workshop=workshop_three):
        SowAndPigletsCell.objects.bulk_create([
            SowAndPigletsCell(section=section, number=cellNumber) for cellNumber in range(1, 7)
            ])

def create_sections_and_cell_for_workshop_with_group_cells(number):
    workshop = WorkShop.objects.get(number=number)

    Section.objects.bulk_create([Section(workshop=workshop, name='Секция %s-1' % number, number=1),
     Section(workshop=workshop, name='Секция %s-2' % number, number=2),
     Section(workshop=workshop, name='Секция %s-3' % number, number=3),
     Section(workshop=workshop, name='Секция %s-4' % number, number=4),
     Section(workshop=workshop, name='Секция %s-5' % number, number=5),
     ])

    for section in Section.objects.filter(workshop=workshop):
        PigletsGroupCell.objects.bulk_create([
            PigletsGroupCell(section=section, number=cellNumber) for cellNumber in range(1, 7)
            ])

def create_workshops_sections_and_cells():
    create_workshops()
    create_sections_and_cell_for_workshop_one()
    create_sections_and_cell_for_workshop_two()
    create_sections_and_cell_for_workshop_three()
    
    for workshop_number in range(4, 9):
        create_sections_and_cell_for_workshop_with_group_cells(workshop_number)
