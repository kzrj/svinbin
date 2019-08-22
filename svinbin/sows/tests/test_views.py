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
from sows_events.models import Ultrasound, UltrasoundV2, Semination, SowFarrow


class WorkshopOneTwoSowViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        locations_testing.create_workshops_sections_and_cells()
        sows_testing.create_statuses()
        self.user = staff_testing.create_employee()
        
    def test_get_sow(self):
        self.client.force_authenticate(user=self.user)
        sow = sows_testing.create_sow_and_put_in_workshop_one()

        response = self.client.get('/api/sows/%s/' % sow.pk)

        Semination.objects.create_semination(sow=sow, week=1,
         initiator=self.user, semination_employee=self.user)
        response = self.client.get('/api/sows/%s/' % sow.pk)
        self.assertEqual(response.data['tours_info'][0]['seminations'][0]['semination_employee'],
            self.user.pk)

        Semination.objects.create_semination(sow=sow, week=1,
         initiator=self.user, semination_employee=self.user)
        response = self.client.get('/api/sows/%s/' % sow.pk)
        self.assertEqual(len(response.data['tours_info'][0]['seminations']), 2)

        Ultrasound.objects.create_ultrasound(sow, self.user, True)
        response = self.client.get('/api/sows/%s/' % sow.pk)
        self.assertEqual(response.data['tours_info'][0]['ultrasounds'][0]['result'], True)

        UltrasoundV2.objects.create_ultrasoundV2(sow, self.user, True)
        response = self.client.get('/api/sows/%s/' % sow.pk)
        self.assertEqual(response.data['tours_info'][0]['ultrasoundsV2'][0]['result'], True)

        SowFarrow.objects.create_sow_farrow(sow=sow, alive_quantity=7, mummy_quantity=1)
        response = self.client.get('/api/sows/%s/' % sow.pk)
        self.assertEqual(response.data['tours_info'][0]['farrows'][0]['alive_quantity'], 7)

        SowFarrow.objects.create_sow_farrow(sow=sow, alive_quantity=10, mummy_quantity=1)
        response = self.client.get('/api/sows/%s/' % sow.pk)
        self.assertEqual(response.data['tours_info'][0]['farrows'][1]['alive_quantity'], 10)
        
        Semination.objects.create_semination(sow=sow, week=2,
         initiator=self.user, semination_employee=self.user)
        response = self.client.get('/api/sows/%s/' % sow.pk)
        self.assertEqual(response.data['tours_info'][1]['seminations'][0]['semination_employee'],
            self.user.pk)

        Ultrasound.objects.create_ultrasound(sow, self.user, False)
        response = self.client.get('/api/sows/%s/' % sow.pk)
        self.assertEqual(response.data['tours_info'][1]['ultrasounds'][0]['result'], False)