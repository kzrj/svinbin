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
import staff.testing_utils as staff_testings

from sows.models import Boar, Sow
from locations.models import Location
from transactions.models import SowTransaction
from sows_events.models import Ultrasound, Semination


class WorkshopOneTwoSowViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        locations_testing.create_workshops_sections_and_cells()
        sows_testing.create_statuses()
        sows_testing.create_boars()
        sows_events_testing.create_types()
        self.boar = Boar.objects.all().first()
        self.user = staff_testings.create_employee() # is_seminator = True

    # def test_put_in_semination_row(self):
    #     self.client.force_authenticate(user=self.user)
    #     sow = sows_testing.create_sow_and_put_in_workshop_one()

    #     response = self.client.post('/api/workshoponetwo/sows/%s/put_in_semination_row/' %
    #       sow.pk)
    #     self.assertEqual(response.data['sow']['id'], sow.pk)
    #     self.assertEqual(response.data['transaction']['to_location'], 'Ряд осеменения, Цех 1 Осеменение')

    def test_semination(self):
        self.client.force_authenticate(user=self.user)
        sow = sows_testing.create_sow_and_put_in_workshop_one()
        boar = Boar.objects.all().first()
        semination_employee = staff_testings.create_employee()

        response = self.client.post('/api/workshoponetwo/sows/%s/semination/' %
          sow.pk, {'week': 7, 'semination_employee': semination_employee.pk, 'boar': boar.pk})

        self.assertNotEqual(response.data['semination']['id'], None)
        self.assertEqual(response.data['sow']['status'], 'Осеменена 1')
        self.assertEqual(response.data['semination']['boar'], boar.pk)

    def test_ultrasound(self):
        self.client.force_authenticate(user=self.user)
        sow = sows_testing.create_sow_and_put_in_workshop_one()
        semination_employee = staff_testings.create_employee()
        boar = Boar.objects.all().first()
        response = self.client.post('/api/workshoponetwo/sows/%s/semination/' %
          sow.pk, {'week': 7, 'semination_employee': semination_employee.pk, 'boar': boar.pk})

        response = self.client.post('/api/workshoponetwo/sows/%s/ultrasound/' %
          sow.pk, {'result': True, 'days': 30})

        # self.assertEqual(response.data['ultrasound']['id'], 2)
        self.assertEqual(response.data['sow']['status'], 'Супорос 28')

    def test_culling(self):
        self.client.force_authenticate(user=self.user)
        sow = sows_testing.create_sow_and_put_in_workshop_one()
        semination_employee = staff_testings.create_employee()

        response = self.client.post('/api/workshoponetwo/sows/%s/culling/' %
          sow.pk, {'culling_type': 'padej', 'reason': 'test reason', 'weight': 150})

        self.assertEqual(response.data['culling']['reason'], 'test reason')
        self.assertEqual(response.data['sow']['status'], 'Брак')

    def test_get_one(self):
        self.client.force_authenticate(user=self.user)
        sow = sows_testing.create_sow_and_put_in_workshop_one()
        response = self.client.get('/api/workshoponetwo/sows/%s/' % sow.pk)

        self.assertEqual(response.data['sow']['id'], sow.pk)

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
        self.assertEqual(response.data['message'], 'Нет ремонтных свиноматок. Создайте свиноматку без номера.')

    def test_mass_semination(self):
        sow1 = sows_testing.create_sow_and_put_in_workshop_one()
        sow2 = sows_testing.create_sow_and_put_in_workshop_one()
        sow3 = sows_testing.create_sow_and_put_in_workshop_one()

        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/workshoponetwo/sows/mass_semination/',
            { 'sows': [sow1.pk, sow2.pk, sow3.pk], 'week': 1, 
              'semination_employee': self.user.pk, 'boar': self.boar.pk
            })
        sow1.refresh_from_db()
        sow2.refresh_from_db()
        sow3.refresh_from_db()
        self.assertEqual(sow1.tour.week_number, 1)
        self.assertEqual(sow2.tour.week_number, 1)
        self.assertEqual(sow3.tour.week_number, 1)

        self.assertEqual(sow1.status.title, 'Осеменена 1')
        self.assertEqual(sow2.status.title, 'Осеменена 1')
        self.assertEqual(sow3.status.title, 'Осеменена 1')


    def test_mass_ultrasound(self):
        sow1 = sows_testing.create_sow_and_put_in_workshop_one()
        sow2 = sows_testing.create_sow_and_put_in_workshop_one()
        sow3 = sows_testing.create_sow_and_put_in_workshop_one()

        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/workshoponetwo/sows/mass_semination/',
            { 'sows': [sow1.pk, sow2.pk, sow3.pk], 'week': 1, 
              'semination_employee': self.user.pk, 'boar': self.boar.pk
            })

        response = self.client.post('/api/workshoponetwo/sows/mass_ultrasound/',
            { 'sows': [sow1.pk, sow2.pk, sow3.pk], 'days': 30, 
              'result': True
            })

        sow1.refresh_from_db()
        sow2.refresh_from_db()
        sow3.refresh_from_db()
        self.assertEqual(sow1.tour.week_number, 1)
        self.assertEqual(sow2.tour.week_number, 1)
        self.assertEqual(sow3.tour.week_number, 1)

        self.assertEqual(sow1.status.title, 'Супорос 28')
        self.assertEqual(sow2.status.title, 'Супорос 28')
        self.assertEqual(sow3.status.title, 'Супорос 28')

    def test_abortion(self):
        self.client.force_authenticate(user=self.user)        
        sow1 = sows_testing.create_sow_and_put_in_workshop_one()        
        Semination.objects.create_semination(sow=sow1, week=1, initiator=None,
         semination_employee=None)
        Ultrasound.objects.create_ultrasound(sow=sow1,
         initiator=None, result=True, days=30)

        response = self.client.post('/api/workshoponetwo/sows/%s/abortion/' % sow1.pk)
        self.assertEqual(response.data['sow']['status'], 'Аборт')

    def test_double_semination(self):
        sow1 = sows_testing.create_sow_and_put_in_workshop_one()
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/workshoponetwo/sows/%s/double_semination/' % sow1.pk, 
            {'week': 55, 'semination_employee': self.user.pk, 'boar1': self.boar.pk,
             'boar2': Boar.objects.all()[1].pk})
        self.assertEqual(response.data['semination1']['tour'], 'Тур 55 2020г')
        self.assertEqual(response.data['semination2']['tour'], 'Тур 55 2020г')
        self.assertEqual(response.data['semination1']['boar'], self.boar.pk)
        self.assertEqual(response.data['semination2']['boar'], Boar.objects.all()[1].pk)
        self.assertEqual(response.data['semination1']['semination_employee'], self.user.pk)
        self.assertEqual(response.data['semination2']['semination_employee'], self.user.pk)
