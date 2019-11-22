# -*- coding: utf-8 -*-
import datetime
import random
from mixer.backend.django import mixer

from django.contrib.auth.models import User
from django.db import connection

from rest_framework.test import APIClient
from rest_framework.test import APITestCase

import locations.testing_utils as locations_testing
import sows.testing_utils as sows_testing
import sows_events.utils as sows_events_testing
import staff.testing_utils as staff_testing

from locations.models import Location
from transactions.models import SowTransaction
from sows_events.models import Ultrasound, Semination, SowFarrow, UltrasoundType
from sows.models import Boar, Sow


class SowViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        locations_testing.create_workshops_sections_and_cells()
        sows_testing.create_statuses()
        sows_testing.create_boars()
        sows_events_testing.create_types()
        self.user = staff_testing.create_employee()
        self.boar = Boar.objects.all().first()
        
    def test_handler_django_model_exception(self):
        '''
            exception raises in model, raise django.core.exceptions.ValidationError.
        '''
        self.client.force_authenticate(user=self.user)
        sow = sows_testing.create_sow_and_put_in_workshop_one()
        boar = Boar.objects.all().first()

        response = self.client.get('/api/sows/%s/' % sow.pk)
