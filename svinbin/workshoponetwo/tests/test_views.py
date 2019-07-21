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


class WorkshopOneTwoSowViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        locations_testing.create_workshops_sections_and_cells()
        sows_testing.create_statuses()
        self.user = staff_testing.create_employee()
        
    def test_assing_farm_id(self):
        sow_without_farm_id = sows_testing.create_sow_without_farm_id_with_birth_id(1)

        response = self.client.post('/api/workshoponetwo/sows/%s/assing_farm_id/' %
          sow_without_farm_id.pk, {'farm_id': 670 })
        self.assertEqual(response.data['sow']['id'], sow_without_farm_id.pk)
        self.assertEqual(response.data['sow']['farm_id'], 670)

    def test_put_in_semination_row(self):
        self.client.force_authenticate(user=self.user)
        sow = sows_testing.create_sow_and_put_in_workshop_one()

        response = self.client.post('/api/workshoponetwo/sows/%s/put_in_semination_row/' %
          sow.pk)
        self.assertEqual(response.data['sow']['id'], sow.pk)
        self.assertEqual(response.data['transaction']['to_location'], 'Ряд осеменения, Цех 1 Осеменение')

    def test_semination(self):
        self.client.force_authenticate(user=self.user)
        sow = sows_testing.create_sow_and_put_in_workshop_one()
        semination_employee = staff_testing.create_employee()

        response = self.client.post('/api/workshoponetwo/sows/%s/semination/' %
          sow.pk, {'week': 7, 'semination_employee': semination_employee.pk})

        self.assertEqual(response.data['semination']['id'], 1)
        self.assertEqual(response.data['sow']['status'], 'Осеменена')

    def test_ultrasound(self):
        self.client.force_authenticate(user=self.user)
        sow = sows_testing.create_sow_and_put_in_workshop_one()
        semination_employee = staff_testing.create_employee()

        response = self.client.post('/api/workshoponetwo/sows/%s/ultrasound/' %
          sow.pk, {'week': 7, 'result': True})

        self.assertEqual(response.data['ultrasound']['id'], 1)
        self.assertEqual(response.data['sow']['status'], 'Беременна')

    def test_culling(self):
        self.client.force_authenticate(user=self.user)
        sow = sows_testing.create_sow_and_put_in_workshop_one()
        semination_employee = staff_testing.create_employee()

        response = self.client.post('/api/workshoponetwo/sows/%s/culling/' %
          sow.pk, {'culling_type': 'padej', 'reason': 'test reason'})

        self.assertEqual(response.data['culling']['id'], 1)
        self.assertEqual(response.data['culling']['reason'], 'test reason')
        self.assertEqual(response.data['sow']['status'], 'Брак')

    def test_get_one(self):
        self.client.force_authenticate(user=self.user)
        sow = sows_testing.create_sow_and_put_in_workshop_one()
        response = self.client.get('/api/workshoponetwo/sows/%s/' % sow.pk)

        self.assertEqual(response.data['id'], sow.pk)

