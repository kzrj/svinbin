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

from sows.models import Boar
from locations.models import Location
from transactions.models import SowTransaction
from sows_events.models import Ultrasound, UltrasoundV2


class WorkshopOneTwoSowViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        locations_testing.create_workshops_sections_and_cells()
        sows_testing.create_statuses()
        sows_testing.create_boars()
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
        boar = Boar.objects.all().first()
        semination_employee = staff_testing.create_employee()

        response = self.client.post('/api/workshoponetwo/sows/%s/semination/' %
          sow.pk, {'week': 7, 'semination_employee': semination_employee.pk, 'boar': boar.pk})

        self.assertEqual(response.data['semination']['id'], 1)
        self.assertEqual(response.data['sow']['status'], 'Осеменена')
        self.assertEqual(response.data['semination']['boar'], boar.pk)

    def test_ultrasound(self):
        self.client.force_authenticate(user=self.user)
        sow = sows_testing.create_sow_and_put_in_workshop_one()
        semination_employee = staff_testing.create_employee()

        response = self.client.post('/api/workshoponetwo/sows/%s/ultrasound/' %
          sow.pk, {'result': True})

        # self.assertEqual(response.data['ultrasound']['id'], 2)
        self.assertEqual(response.data['sow']['status'], 'Прошла УЗИ1, супорос')

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

        self.assertEqual(response.data['sow']['id'], sow.pk)

    def test_sows_by_tours(self):
        self.client.force_authenticate(user=self.user)
        sow1 = sows_testing.create_sow_and_put_in_workshop_one()
        sow2 = sows_testing.create_sow_and_put_in_workshop_one()
        seminated_sow1 = sows_testing.create_sow_with_semination(sow1.location)
        Ultrasound.objects.create_ultrasound(sow=seminated_sow1,
         initiator=None, result=True)

        location2 = Location.objects.get(workshop__number=2)
        seminated_sow2 = sows_testing.create_sow_with_semination(location2)
        seminated_sow3 = sows_testing.create_sow_with_semination(location2, 2)
        seminated_sow3 = sows_testing.create_sow_with_semination(location2, 2)
        sow3 = sows_testing.create_sow_and_put_in_workshop_one()
        sow3.location = location2
        sow3.save()
        seminated_sow4 = sows_testing.create_sow_with_semination(location2, 3)

        response = self.client.get('/api/workshoponetwo/sows/sows_by_tours/')
        self.assertEqual(response.data[0]['tour']['id'], seminated_sow1.tour.pk)
        self.assertEqual(response.data[0]['sows'][0]['id'], seminated_sow1.pk)

    def test_sows_by_tours_ws2(self):
        self.client.force_authenticate(user=self.user)
        sow1 = sows_testing.create_sow_and_put_in_workshop_one()
        sow2 = sows_testing.create_sow_and_put_in_workshop_one()
        seminated_sow1 = sows_testing.create_sow_with_semination(sow1.location)
        Ultrasound.objects.create_ultrasound(sow=seminated_sow1,
         initiator=None, result=True)

        location2 = Location.objects.get(workshop__number=2)
        seminated_sow2 = sows_testing.create_sow_with_semination(location2)
        seminated_sow3 = sows_testing.create_sow_with_semination(location2, 2)
        seminated_sow3 = sows_testing.create_sow_with_semination(location2, 2)
        Ultrasound.objects.create_ultrasound(sow=seminated_sow3,
         initiator=None, result=True)
        sow3 = sows_testing.create_sow_and_put_in_workshop_one()
        sow3.location = location2
        sow3.save()
        seminated_sow4 = sows_testing.create_sow_with_semination(location2, 3)

        response = self.client.get('/api/workshoponetwo/sows/sows_by_tours_ws2/')
        self.assertEqual(response.data[0]['count'], 1)
        self.assertEqual(response.data[1]['tour']['id'], "Не супорос")
        self.assertEqual(response.data[1]['count'], 4)

    def test_sows_move_many(self):
        self.client.force_authenticate(user=self.user)
        sow1 = sows_testing.create_sow_and_put_in_workshop_one()
        sow2 = sows_testing.create_sow_and_put_in_workshop_one()
        seminated_sow1 = sows_testing.create_sow_with_semination(sow1.location)
        location2 = Location.objects.get(workshop__number=2)

        response = self.client.post('/api/workshoponetwo/sows/move_many/', 
            {'sows': [sow1.pk, sow2.pk, seminated_sow1.pk], 'to_location': location2.pk})
        self.assertEqual(type(response.data['transaction_ids']), list)
        self.assertEqual(len(response.data['transaction_ids']), 3)

    def test_create_new_without_farm_id(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/workshoponetwo/sows/create_new_without_farm_id/')
        self.assertEqual(response.data['sow']['farm_id'], None)
        self.assertEqual(response.data['noname_sows_count'], 1)

        response = self.client.post('/api/workshoponetwo/sows/create_new_without_farm_id/')
        self.assertEqual(response.data['noname_sows_count'], 2)

    def test_create_new(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/workshoponetwo/sows/create_new_without_farm_id/')

        response = self.client.post('/api/workshoponetwo/sows/create_new/', 
            {'farm_id': 99999})
        self.assertEqual(response.data['sow']['farm_id'], 99999)

        response = self.client.post('/api/workshoponetwo/sows/create_new/', 
            {'farm_id': 99998})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['message'], 'Net remontok')

