# -*- coding: utf-8 -*-
from xlrd import open_workbook, xldate_as_tuple
import re
import datetime

from sows.models import Sow, Boar
from tours.models import Tour
from staff.models import WorkShopEmployee
from sows_events.models import Semination, Ultrasound, AbortionSow


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

    return row

def define_match_row_and_convert_datetime(row_values): # to test
    if len(row_values) > 3 and \
        re.match(r'^[0-9]+$', str(row_values[0])) and \
        re.match(r'^[0-9A-ZА-Я]+$', str(row_values[1])) and \
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
                # if ro
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
        tour = Tour.objects.create_or_return_by_raw(row[3], row[4])
        sow, created = Sow.objects.create_or_return(row[0])

        if sow.alive == False:
            continue

        try:
            semination_employee1 = WorkShopEmployee.objects.get_seminator_by_farm_name(row[6])
            semination_employee2 = WorkShopEmployee.objects.get_seminator_by_farm_name(row[8])
        except:
            semination_employee1, semination_employee2 = None, None

        if sow.tour and sow.tour != tour:
            # if we meet sow with tour but row_tour is earlier.
            if sow.tour.week_number < tour.week_number:
                # do proholost
                Ultrasound.objects.create_ultrasound(sow, semination_employee1, False, 30, row[4])
            else:
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
