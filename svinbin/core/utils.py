# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
import xlsxwriter
from datetime import datetime, timedelta

from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError

from rest_framework import status, exceptions
from rest_framework.views import exception_handler as drf_exception_handler

from django.utils.encoding import force_text
from django.utils import timezone
from django.core.mail import send_mail
from django.db.utils import IntegrityError as DjangoIntegrityError

from staff.serializers import WorkshopEmployeeSerializer
from locations.models import Location
from tours.models import MetaTourRecord
from piglets.models import Piglets
from sows_events.models import ( SowFarrow, Semination, Ultrasound, CullingSow, WeaningSow, AbortionSow,
    MarkAsNurse)
from sows.models import SowStatus, Sow, SowStatusRecord
from transactions.models import SowTransaction


class CustomValidation(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Error'

    def __init__(self, detail, field, status_code):
        if status_code is not None:
            self.status_code = status_code
        if detail is not None:
            self.detail = {field: force_text(detail)}
        else: self.detail = {'detail': force_text(self.default_detail)}


def custom_exception_handler(exc, context):
    
    if isinstance(exc, CustomValidation):
        field = list(exc.detail.keys())[0]
        exc = DRFValidationError(detail={'message': field + ' ' + exc.detail[field]})

    if isinstance(exc, DjangoValidationError):
        if hasattr(exc, 'message_dict'):
            # TODO: handle many fields
            field = list(exc.detail.keys())[0]
            
            exc = DRFValidationError(detail={'message': field + ' ' + exc.detail[field]})
        else:
            exc = DRFValidationError(detail={'message': exc.message})

    if isinstance(exc, DjangoIntegrityError):
        exc = DRFValidationError(detail={'message': str(exc)})

    return drf_exception_handler(exc, context)


def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'user': WorkshopEmployeeSerializer(user.employee).data
    }


def export_to_excel_ws3(filename, data):
    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet()

    worksheet.write('A7', 'Дата') 
    worksheet.write('B7', 'Подсосные') 
    worksheet.write('C7', 'Супоросные') 
    worksheet.write('D7', 'Поросята сосуны') 
    worksheet.write('E7', 'всего начало дня') 
    worksheet.write('F7', 'приход подсосные') 
    worksheet.write('G7', 'приход супоросные из ц1') 
    worksheet.write('H7', 'приход супоросные из ц2') 
    worksheet.write('I7', 'Опоросилось') 
    worksheet.write('J7', 'Оприходовано') 
    worksheet.write('K7', 'расход подсосные') 
    worksheet.write('L7', 'расход супоросные') 
    worksheet.write('M7', 'падеж подсосные гол') 
    worksheet.write('N7', 'падеж подсосные вес') 
    worksheet.write('O7', 'падеж супоросные гол') 
    worksheet.write('P7', 'падеж супоросные вес') 
    worksheet.write('Q7', 'забой подсосные гол') 
    worksheet.write('R7', 'забой подсосные вес') 
    worksheet.write('S7', 'забой супоросные гол') 
    worksheet.write('T7', 'забой супоросные вес') 

    worksheet.write('U7', 'поросята перевод колво') 
    worksheet.write('V7', 'поросята перевод общий вес') 
    worksheet.write('W7', 'поросята перевод средний вес') 
    worksheet.write('X7', 'поросята падеж колво') 
    worksheet.write('Y7', 'поросята падеж вес') 
    worksheet.write('Z7', 'поросята забой колво') 
    worksheet.write('AA7', 'поросята забой вес') 
    worksheet.write('AB7', 'поросята ревизия колво') 
    worksheet.write('AC7', 'поросята ревизия вес') 
    worksheet.write('AD7', 'Подсосные') 
    worksheet.write('AE7', 'Супоросные') 
    worksheet.write('AF7', 'Поросята сосуны') 
    worksheet.write('AG7', 'Всего конец дня') 

    row = 7
    col = 0

    for record in data:
        worksheet.write(row, col,     record['date'])
        worksheet.write(row, col + 1, record['count_sows_ws3_start_date']['podsos'])
        worksheet.write(row, col + 2, record['count_sows_ws3_start_date']['suporos'])
        worksheet.write(row, col + 3, record['count_piglets_at_start'])
        worksheet.write(row, col + 4, int(record['count_sows_ws3_start_date']['suporos']) \
            + int(record['count_sows_ws3_start_date']['podsos']) \
            + int(record['count_piglets_at_start']))
        worksheet.write(row, col + 5, record['tr_in_podsos_count'])
        worksheet.write(row, col + 6, record['tr_in_from_1_sup_count'])
        worksheet.write(row, col + 7, record['tr_in_from_2_sup_count'])
        worksheet.write(row, col + 8, record['count_oporos'])
        worksheet.write(row, col + 9, record['count_alive'])
        worksheet.write(row, col + 10, record['tr_out_podsos_count'])
        worksheet.write(row, col + 11, record['tr_out_sup_count'])
        worksheet.write(row, col + 12, record['padej_podsos_count'])
        worksheet.write(row, col + 13, record['padej_podsos_weight'])
        worksheet.write(row, col + 14, record['padej_sup_count'])
        worksheet.write(row, col + 15, record['padej_sup_weight'])
        worksheet.write(row, col + 16, record['vinuzhd_podsos_count'])
        worksheet.write(row, col + 17, record['vinuzhd_podsos_weight'])
        worksheet.write(row, col + 18, record['vinuzhd_sup_count'])
        worksheet.write(row, col + 19, record['vinuzhd_sup_weight'])

        worksheet.write(row, col + 20, record['tr_out_aka_weight_qnty'])
        worksheet.write(row, col + 21, record['tr_out_aka_weight_total'])
        worksheet.write(row, col + 22, record['tr_out_aka_weight_avg'])

        worksheet.write(row, col + 23, record['piglets_padej_qnty'])
        worksheet.write(row, col + 24, record['piglets_padej_weight'])

        worksheet.write(row, col + 25, record['piglets_vinuzhd_qnty'])
        worksheet.write(row, col + 26, record['piglets_vinuzhd_weight'])

        worksheet.write(row, col + 27, '')
        worksheet.write(row, col + 28, '')

        worksheet.write(row, col + 29, record['count_sows_ws3_start_date']['suporos'])
        worksheet.write(row, col + 30, record['count_sows_ws3_start_date']['podsos'])
        worksheet.write(row, col + 31, record['count_piglets_at_start'])
        worksheet.write(row, col + 32, int(record['count_sows_ws3_start_date']['suporos']) \
            + int(record['count_sows_ws3_start_date']['podsos']) \
            + int(record['count_piglets_at_start']))
        row += 1

    workbook.close()