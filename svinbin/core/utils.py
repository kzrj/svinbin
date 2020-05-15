# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
from datetime import datetime

from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError

from rest_framework import status, exceptions
from rest_framework.views import exception_handler as drf_exception_handler

from django.utils.encoding import force_text
from django.core.mail import send_mail
from django.db.utils import IntegrityError as DjangoIntegrityError

from staff.serializers import WorkshopEmployeeSerializer
from locations.models import Location
from tours.models import MetaTourRecord
from piglets.models import Piglets


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

def set_piglets_culling_location(culling):
    if not culling.location:
        if culling.initiator and not culling.initiator.employee.is_officer:
            culling.location = Location.objects.get(workshop=culling.initiator.employee.workshop)
        else:
            culling.location = culling.piglets_group.location

        culling.save()


def set_piglets_age_not_mixed():
    
    piglets_qs = Piglets.objects.filter(metatour__records__percentage=100)
    for piglets in piglets_qs:
        tour = piglets.metatour.week_tour
        first_farrow = tour.sowfarrow_set.all().first()

        if first_farrow:
            piglets.birthday = first_farrow.date
        else:
            piglets.birthday = tour.start_date

        piglets.save()


def set_piglets_age_mixed():
    
    piglets_qs = Piglets.objects.filter(metatour__records__percentage__lt=100)

    for piglets in piglets_qs:
        avg_ts = 0

        for record in piglets.metatour.records.all():

            first_farrow = record.tour.sowfarrow_set.all().first()
            pre_birthday_ts = 0

            if first_farrow:
                pre_birthday_ts = datetime.timestamp(first_farrow.date)
            else:
                pre_birthday_ts = datetime.timestamp(record.tour.start_date)

            avg_ts += (pre_birthday_ts * record.quantity / piglets.quantity)
        
        piglets.birthday = datetime.fromtimestamp(avg_ts)
        piglets.save()
