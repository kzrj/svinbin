# -*- coding: utf-8 -*-

from workshops.models import WorkShop, WorkShopEmployee, Section, SowSingleCell, \
    PigletsGroupCell, SowAndPigletsCell, SowGroupCell


def create_workshops():
    WorkShop.objects.bulk_create([
        WorkShop(number=1, title='Цех 1 Осеменение'),
        WorkShop(number=2, title='Цех 2 Ожидание родов'),
        WorkShop(number=3, title='Цех 3 Маточник'),
        WorkShop(number=4, title='Цех 4 Доращивание 4'),
        WorkShop(number=8, title='Цех 8 Доращивание 8'),
        WorkShop(number=5, title='Цех 5 Откорм 5'),
        WorkShop(number=6, title='Цех 6 Откорм 6'),
        WorkShop(number=7, title='Цех 7 Откорм 7'),
        WorkShop(number=9, title='Цех 9 Убойный цех'),
        WorkShop(number=10, title='Цех 10 Крематорий'),
        WorkShop(number=11, title='Цех Взвешивание 3/4'),
        ])

def create_sections_and_cell_for_workshop_one():
    workshop_one = WorkShop.objects.get(number=1)

    Section.objects.bulk_create([Section(workshop=workshop_one, name='Змейка', number=1),
     Section(workshop=workshop_one, name='Ряд осеменения', number=2),
     Section(workshop=workshop_one, name='Групповые клетки', number=3)])

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

def create_sections_and_cell_for_workshop_with_group_cells(workshop_number):
    workshop = WorkShop.objects.get(number=workshop_number)

    Section.objects.bulk_create([Section(workshop=workshop, name='Секция %s-1' % workshop_number, number=1),
     Section(workshop=workshop, name='Секция %s-2' % workshop_number, number=2),
     Section(workshop=workshop, name='Секция %s-3' % workshop_number, number=3),
     Section(workshop=workshop, name='Секция %s-4' % workshop_number, number=4),
     Section(workshop=workshop, name='Секция %s-5' % workshop_number, number=5),
     ])

    for section in Section.objects.filter(workshop=workshop):
        PigletsGroupCell.objects.bulk_create([
            PigletsGroupCell(section=section, number=cellNumber) for cellNumber in range(1, 7)
            ])

# def create_sections_and_cell_for_workshop_eleven():
#     workshop = WorkShop.objects.get(number=11)
#     section = Section.objects.create(workshop=workshop, number=1, name='Секция взвешивания')
#     WeighingCell.objects.create(section=section, number=1)


def create_workshops_sections_and_cells():
    if WorkShop.objects.all().count() < 1:
        create_workshops()
        create_sections_and_cell_for_workshop_one()
        create_sections_and_cell_for_workshop_two()
        create_sections_and_cell_for_workshop_three()
        
        for workshop_number in range(4, 9):
            create_sections_and_cell_for_workshop_with_group_cells(workshop_number)
