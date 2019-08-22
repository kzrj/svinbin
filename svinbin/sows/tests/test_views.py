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
import staff.testing_utils as staff_testing

from locations.models import Location
from transactions.models import SowTransaction
from sows_events.models import Ultrasound, UltrasoundV2, Semination


class WorkshopOneTwoSowViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        locations_testing.create_workshops_sections_and_cells()
        sows_testing.create_statuses()
        self.user = staff_testing.create_employee()
        
    def test_get_sow(self):
        self.client.force_authenticate(user=self.user)
        sow = sows_testing.create_sow_and_put_in_workshop_one()

        print(len(connection.queries))
        response = self.client.get('/api/sows/%s/' % sow.pk)
        print(response.data)
        print(len(connection.queries))

        Semination.objects.create_semination(sow=sow, week=1,
         initiator=self.user, semination_employee=self.user)
        response = self.client.get('/api/sows/%s/' % sow.pk)
        print(response.data)
        