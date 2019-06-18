# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re

from rest_framework import status, exceptions
from rest_framework.views import exception_handler

from django.utils.encoding import force_text
from django.core.mail import send_mail


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
    response = exception_handler(exc, context)
    if response is not None:
        response.data['status_code'] = response.status_code
    else:
        return response

    if isinstance(exc, CustomValidation):
        field = list(exc.detail.keys())[0]
        response.data['errMessage'] = field + ' ' + exc.detail[field]
        
    elif isinstance(exc, exceptions.ValidationError):
        try:
            key = next(iter(exc.detail))
            value = exc.detail.get(key, '0')[0]
            response.data['errMessage'] = key + ' ' + value
        except:
            response.data['errMessage'] = 'ValidationError.'

    elif isinstance(exc, exceptions.AuthenticationFailed):
        response.data['errMessage'] = 'Ошибка авторизации.'

    elif isinstance(exc, exceptions.NotAuthenticated):
        response.data['errMessage'] = 'Пользователь не авторизован.'

    elif isinstance(exc, exceptions.PermissionDenied):
        response.data['errMessage'] = 'Пользователь не имеет достаточно прав.'

    elif isinstance(exc, exceptions.NotFound):
        response.data['errMessage'] = 'Не найдено.'

    else:
        print('Exception!!')
        print(exc)

        response.data['errMessage'] = 'Непредвиденная ошибка.'
        # print('StandartException!!!')
        # print(exc.get_full_details())
        # print(exc.detail)
        # print(type(str(exc.detail)))
        # print(exc.get_full_details()['message'])
        # print(exc.get_full_details()['code'])
        # print(exc.detail.keys())

    return response