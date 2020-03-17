# -*- coding: utf-8 -*-
from xlrd import open_workbook, xldate_as_tuple
import re
import datetime
import json
from pytz import timezone

from sows.models import Sow, Boar
from tours.models import Tour
from staff.models import WorkShopEmployee
from sows_events.models import Semination, Ultrasound, AbortionSow
from locations.models import Location


def init_wb(file_from_request): # to test
    with open('../data/seminations.xls', 'wb') as file:
        for chunk in file_from_request.chunks():
            file.write(chunk)
    wb = open_workbook('../data/seminations.xls')
    return wb

def normalize_row(row, workbook): # to test
    row[0] = int(row[0]) # farm_id to int
    row[4] = datetime.datetime(*xldate_as_tuple(row[4], workbook.datemode))
    if row[5] == '*' or row[5] == '**':
        del row[5] # delete *
    row[5] = int(row[5])
    row[7] = int(row[7])
    
    # try:
    #     print(row[10])
    # except:
    #     pass

    return row

def define_match_row_and_convert_datetime(row_values): # to test
    if len(row_values) > 3 and \
        re.match(r'^[0-9]+$', str(row_values[0])) and \
        re.match(r'^[0-9A-Z]+$', str(row_values[1])) and \
        re.match(r'^[0-9]{4}$', str(row_values[3])):        
        return True
        
    return False

def get_semenation_rows(workbook): # to test
    rows = list()
    for s in workbook.sheets():
        for row in range(s.nrows):
            row_values = list()
            for col in range(s.ncols):
                if len(str(s.cell(row,col).value).strip()) > 0:
                    row_values.append(s.cell(row, col).value)
            if define_match_row_and_convert_datetime(row_values):
                row_values = normalize_row(row_values, workbook)
                rows.append(row_values)
    return rows

def create_semination_lists(rows, request_user):
    seminated_list = list()
    already_seminated_in_tour = list()
    sows_in_another_tour = list()
    proholost_list = list()

    count = 0

    for row in rows:
        tour = Tour.objects.create_or_return_by_raw(row[3])
        sow, created = Sow.objects.create_or_return(row[0])

        try:
            semination_employee1 = WorkShopEmployee.objects.get_seminator_by_farm_name(row[6])
            semination_employee2 = WorkShopEmployee.objects.get_seminator_by_farm_name(row[8])
        except:
            semination_employee1, semination_employee2 = None, None

        if sow.tour and sow.tour != tour:
            sows_in_another_tour.append(sow)
            continue
            
        boar1 = Boar.objects.get_or_create_boar(row[5])
        boar2 = Boar.objects.get_or_create_boar(row[7])

            
        # if usouded by hand and then file updated. It is to avoid double usound, semination
        if 'Рег. Пов тор' in row or 'Не рег. пов тор' in row \
            and Ultrasound.objects.filter(sow=sow, tour=tour, result=False).first():
            proholost_list.append(sow)
            continue

        sow, seminated = Semination.objects.double_semination_or_not(
            sow=sow, tour=tour, date=row[4], initiator=request_user,
            boar1=boar1, semination_employee1=semination_employee1,
            boar2=boar2, semination_employee2=semination_employee2,                    
            )

        if 'Рег. Пов тор' in row or 'Не рег. пов тор' in row:
        # рег повтор не рег повтор. Прохолост
        # проверить была ли свинья уже осеменена в этом туре.
            Ultrasound.objects.create_ultrasound(sow, semination_employee1, False, 30, row[4])
            proholost_list.append(sow)
            continue

        # Аборт
        if 'Абортировали' in row:
            AbortionSow.objects.create_abortion(sow, semination_employee1, row[4])      
            proholost_list.append(sow)
            continue

        if seminated:
            seminated_list.append(sow)
        else:
            already_seminated_in_tour.append(sow)

    return seminated_list, already_seminated_in_tour, sows_in_another_tour, proholost_list

# берем только более позднее
# какие больше 35 с момента осеменения, делаем узи +35 дней осеменение
# отфильтровать по тур.

def import_from_json_to_ws3(initiator=None):
    with open('../data/ceh03.json', 'r') as file:
        data = json.load(file)

    for key in data.keys():
        sow, created = Sow.objects.create_or_return(data[key]['farm_id'])
        
        if not created:
            continue

        cycle = data[key]['Cicles'][0]
        tour = Tour.objects.create_or_return_by_raw(cycle['week'])

        boar1 = Boar.objects.get_or_create_boar(cycle['boar1'])
        boar2 = Boar.objects.get_or_create_boar(cycle['boar2'])
        semination_employee1 = WorkShopEmployee.objects.get_seminator_by_farm_name(cycle['insr1'])
        semination_employee2 = WorkShopEmployee.objects.get_seminator_by_farm_name(cycle['insr2'])
        date = datetime.datetime.strptime(cycle['insemdate'], '%Y-%m-%d')

        sow, seminated = Semination.objects.double_semination_or_not(
            sow=sow, tour=tour, date=date, initiator=None,
            boar1=boar1, semination_employee1=semination_employee1,
            boar2=boar2, semination_employee2=semination_employee2,                    
            )

        # usound
        Ultrasound.objects.create_ultrasound(sow=sow, initiator=None, result=True,
         days=30, date=date + datetime.timedelta(days=28))
        Ultrasound.objects.create_ultrasound(sow=sow, initiator=None, result=True,
         days=60, date=date + datetime.timedelta(days=35))

        sow.location = Location.objects.filter(workshop__number=3).first()
        sow.save()


def import_from_json_to_ws2(initiator=None):
    with open('../data/ceh02.json', 'r') as file:
        data = json.load(file)

    for key in data.keys():
        sow, created = Sow.objects.create_or_return(data[key]['farm_id'])

        if not created:
            continue

        cycle = data[key]['Cicles'][0]
        tour = Tour.objects.create_or_return_by_raw(cycle['week'])

        boar1 = Boar.objects.get_or_create_boar(cycle['boar1'])
        boar2 = Boar.objects.get_or_create_boar(cycle['boar2'])
        semination_employee1 = WorkShopEmployee.objects.get_seminator_by_farm_name(cycle['insr1'])
        semination_employee2 = WorkShopEmployee.objects.get_seminator_by_farm_name(cycle['insr2'])
        date = datetime.datetime.strptime(cycle['insemdate'], '%Y-%m-%d')

        sow, seminated = Semination.objects.double_semination_or_not(
            sow=sow, tour=tour, date=date, initiator=None,
            boar1=boar1, semination_employee1=semination_employee1,
            boar2=boar2, semination_employee2=semination_employee2,                    
            )

        # usound
        Ultrasound.objects.create_ultrasound(sow=sow, initiator=None, result=True,
         days=30, date=date + datetime.timedelta(days=28))
        Ultrasound.objects.create_ultrasound(sow=sow, initiator=None, result=True,
         days=60, date=date + datetime.timedelta(days=35))

        sow.location = Location.objects.filter(workshop__number=2).first()
        sow.save()


def init_sow_cycle(sow, cycle, ws_number, initiator=None):
    tour = Tour.objects.create_or_return_by_raw(cycle['week'])

    boar1 = Boar.objects.get_or_create_boar(cycle['boar1'])
    boar2 = Boar.objects.get_or_create_boar(cycle['boar2'])
    semination_employee1 = WorkShopEmployee.objects.get_seminator_by_farm_name(cycle['insr1'])
    semination_employee2 = WorkShopEmployee.objects.get_seminator_by_farm_name(cycle['insr2'])
    date = datetime.datetime.strptime(cycle['insemdate'], '%Y-%m-%d')

    sow, seminated = Semination.objects.double_semination_or_not(
        sow=sow, tour=tour, date=date, initiator=None,
        boar1=boar1, semination_employee1=semination_employee1,
        boar2=boar2, semination_employee2=semination_employee2,                    
        )

    # usound
    Ultrasound.objects.create_ultrasound(sow=sow, initiator=None, result=True,
     days=30, date=date + datetime.timedelta(days=28))
    Ultrasound.objects.create_ultrasound(sow=sow, initiator=None, result=True,
     days=60, date=date + datetime.timedelta(days=35))

    sow.location = Location.objects.filter(workshop__number=ws_number).first()
    sow.save()

    return sow
    

def import_from_json_to_ws2_3(file, ws_number, initiator=None):
    data = json.load(file)
    sows_created = list()
    sows_passed = list()

    for key in data.keys():
        sow, created = Sow.objects.create_or_return(data[key]['farm_id'])

        if not created:
            sows_passed.append(sow)
            continue

        cycle = data[key]['Cicles'][0]
        sow = init_sow_cycle(sow, cycle, ws_number, initiator)
        sows_created.append(sow)

    return sows_created, sows_passed