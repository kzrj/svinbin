# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
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

def set_piglets_culling_location(culling):
    if not culling.location:
        if culling.initiator and not culling.initiator.employee.is_officer:
            culling.location = Location.objects.get(workshop=culling.initiator.employee.workshop)
        else:
            culling.location = culling.piglets_group.location

        culling.save()


def set_piglets_age_not_mixed(piglets_qs=None):
    if not piglets_qs:
        piglets_qs = Piglets.objects.get_all().filter(metatour__records__percentage=100)

    for piglets in piglets_qs:
        tour = piglets.metatour.week_tour
        first_farrow = tour.sowfarrow_set.all().first()

        if hasattr(piglets, 'farrow'):
            piglets.birthday = piglets.farrow.date

        else:
            if first_farrow:
                piglets.birthday = first_farrow.date
            else:
                piglets.birthday = tour.start_date + timedelta(135)

        piglets.save()


def set_piglets_age_mixed():
    
    piglets_qs = Piglets.objects.get_all().filter(metatour__records__percentage__lt=100)

    for piglets in piglets_qs:
        avg_ts = 0

        for record in piglets.metatour.records.all():

            first_farrow = record.tour.sowfarrow_set.all().first()
            pre_birthday_ts = 0

            if first_farrow:
                pre_birthday_ts = datetime.timestamp(first_farrow.date)
            else:
                pre_birthday_ts = datetime.timestamp(record.tour.start_date + timedelta(135))

            if piglets.quantity < 1:
                avg_ts = datetime.timestamp(piglets.metatour.week_tour.start_date + timedelta(135))
                break
            else:
                avg_ts += (pre_birthday_ts * record.quantity / piglets.quantity)
        
        piglets.birthday = datetime.fromtimestamp(avg_ts)
        piglets.save()


def fix_minus_age():
    now = timezone.now()
    piglets_qs = Piglets.objects.get_all().filter(birthday__gt=now)

    for piglets in piglets_qs:
        tour = piglets.metatour.week_tour
        first_farrow = tour.sowfarrow_set.all().first()

        if hasattr(piglets, 'farrow'):
            piglets.birthday = piglets.farrow.date

        else:
            correct_birthday = Piglets.objects.get_all().filter(metatour__week_tour=tour,
                birthday__lt=now).order_by('-birthday').first().birthday
            piglets.birthday = correct_birthday

        piglets.save()


def fix_plus_age():
    now = timezone.now()
    piglets_qs = Piglets.objects.get_all().filter(birthday__date__year__lt=2019)

    for piglets in piglets_qs:
        tour = piglets.metatour.week_tour
        first_farrow = tour.sowfarrow_set.all().first()

        if hasattr(piglets, 'farrow'):
            piglets.birthday = piglets.farrow.date

        else:
            correct_birthday = Piglets.objects.get_all().filter(metatour__week_tour=tour,
                birthday__lt=now).order_by('birthday').first().birthday
            piglets.birthday = correct_birthday

        piglets.save()


def create_sow_status_records(change_date=False):
    status_ozhidaet = SowStatus.objects.get(title='Ожидает осеменения')
    status_osem2 = SowStatus.objects.get(title='Осеменена 2')
    status_sup28 = SowStatus.objects.get(title='Супорос 28')
    status_sup35 = SowStatus.objects.get(title='Супорос 35')
    status_proh = SowStatus.objects.get(title='Прохолост')
    status_oporos = SowStatus.objects.get(title='Опоросилась')
    status_otiem = SowStatus.objects.get(title='Отъем')
    status_abort = SowStatus.objects.get(title='Аборт')
    status_brak = SowStatus.objects.get(title='Брак')
    status_korm = SowStatus.objects.get(title='Кормилица')

    for semination in Semination.objects.all().select_related('sow', 'sow__status'):
        semination.sow.status_records.create(sow=semination.sow, status_before=status_ozhidaet,
            status_after=status_osem2, date=semination.date)

    for usound in Ultrasound.objects.all().select_related('sow', 'sow__status', 'u_type'):
        if change_date:
            usound.date = usound.created_at
            usound.save()

        if usound.result:
            if usound.u_type.days == 30:
                usound.sow.status_records.create(sow=usound.sow, status_before=status_osem2,
                    status_after=status_sup28, date=usound.date)
            if usound.u_type.days == 60:
                usound.sow.status_records.create(sow=usound.sow, status_before=status_sup28,
                    status_after=status_sup35, date=usound.date)
        else:
            usound.sow.status_records.create(sow=usound.sow, status_before=status_sup28,
                status_after=status_proh, date=usound.date)

    for farrow in SowFarrow.objects.all().select_related('sow', 'sow__status'):
        if change_date:
            farrow.date = farrow.created_at
            farrow.save()

        farrow.sow.status_records.create(sow=farrow.sow, status_before=status_sup35,
            status_after=status_oporos, date=farrow.date)

    for weaning in WeaningSow.objects.all().select_related('sow', 'sow__status'):
        if change_date:
            weaning.date = weaning.created_at
            weaning.save()

        weaning.sow.status_records.create(sow=weaning.sow, status_before=status_oporos,
            status_after=status_otiem, date=weaning.date)

    for nurse in MarkAsNurse.objects.all().select_related('sow', 'sow__status'):
        if change_date:
            nurse.date = nurse.created_at
            nurse.save()

        nurse.sow.status_records.create(sow=nurse.sow, status_before=status_oporos,
            status_after=status_korm, date=nurse.date)

    for abort in AbortionSow.objects.all().select_related('sow', 'sow__status'):
        if change_date:
            abort.date = abort.created_at
            abort.save()

        abort.sow.status_records.create(sow=abort.sow, status_before=status_sup35,
            status_after=status_abort, date=abort.date)

    ws3_locs = Location.objects.all().get_workshop_location_by_number(workshop_number=3)
    for tr in SowTransaction.objects.filter(from_location__in=ws3_locs, to_location__workshop__number=1):
        if change_date:
            tr.date = tr.created_at
            tr.save()

        last_record = tr.sow.status_records.filter(date__lte=tr.date).order_by('-created_at').first()
        
        if last_record:
            tr.sow.status_records.create(sow=tr.sow, status_before=last_record.status_after,
                status_after=status_ozhidaet, date=tr.date)
        else:
            tr.sow.status_records.create(sow=tr.sow, status_before=last_record,
                status_after=status_ozhidaet, date=tr.date)

    for culling in CullingSow.objects.all().select_related('sow', 'sow__status'):
        if change_date:
            culling.date = culling.created_at
            culling.save()

        last_record = culling.sow.status_records.filter(date__lte=culling.date) \
            .order_by('-created_at').first()
        if last_record:
            culling.sow.status_records.create(sow=culling.sow, status_before=last_record.status_after,
                status_after=status_brak, date=culling.date)
        else:
            culling.sow.status_records.create(sow=culling.sow, status_before=last_record,
                status_after=status_brak, date=culling.date)


def add_sow_statuses_to_cullings():
    for culling in CullingSow.objects.all().select_related('sow', 'sow__status'):
        st_record = culling.sow.status_records.all().filter(date__date=culling.date,
         status_after__title='Брак').first()
        culling.sow_status = st_record.status_before
        culling.save()

def add_sow_statuses_to_trs():
    for tr in SowTransaction.objects.all():
        st_record = tr.sow.status_records.all().filter(date__lte=tr.date).first()
        tr.sow_status = st_record.status_after
        tr.save()