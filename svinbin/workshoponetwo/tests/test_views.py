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
        self.assertEqual(response.data['sow']['status'], 'Супорос 30')

    def test_culling(self):
        self.client.force_authenticate(user=self.user)
        sow = sows_testing.create_sow_and_put_in_workshop_one()
        semination_employee = staff_testings.create_employee()

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

        self.assertEqual(sow1.status.title, 'Супорос 30')
        self.assertEqual(sow2.status.title, 'Супорос 30')
        self.assertEqual(sow3.status.title, 'Супорос 30')

    def test_abortion(self):
        self.client.force_authenticate(user=self.user)        
        sow1 = sows_testing.create_sow_and_put_in_workshop_one()        
        Semination.objects.create_semination(sow=sow1, week=1, initiator=None,
         semination_employee=None)
        Ultrasound.objects.create_ultrasound(sow=sow1,
         initiator=None, result=True, days=30)

        response = self.client.post('/api/workshoponetwo/sows/%s/abortion/' % sow1.pk)
        self.assertEqual(response.data['sow']['status'], 'Аборт')

    def test_mass_init_and_transfer(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/workshoponetwo/sows/mass_init_and_transfer/', 
            {'sows': [1, 2, 3, 4], 'week': 55})

        self.assertEqual(Semination.objects.filter(tour__week_number=55).count(), 8)
        self.assertEqual(Ultrasound.objects.filter(tour__week_number=55, u_type__days=30).count(), 4)
        self.assertEqual(Ultrasound.objects.filter(tour__week_number=55, u_type__days=60).count(), 4)
        self.assertEqual(SowTransaction.objects.all().count(), 4)

        response = self.client.post('/api/workshoponetwo/sows/mass_init_and_transfer/', 
            {'sows': [1, 2, 3, 4, 5, 6, 7], 'week': 55})
        self.assertEqual(response.data['created'], [5, 6, 7])
        self.assertEqual(response.data['not_created'], [1, 2, 3, 4])
        self.assertEqual(Semination.objects.filter(tour__week_number=55).count(), 14)
        self.assertEqual(Ultrasound.objects.filter(tour__week_number=55, u_type__days=30).count(), 7)
        self.assertEqual(Ultrasound.objects.filter(tour__week_number=55, u_type__days=60).count(), 7)
        self.assertEqual(SowTransaction.objects.all().count(), 7)

    def test_double_semination(self):
        sow1 = sows_testing.create_sow_and_put_in_workshop_one()
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/workshoponetwo/sows/%s/double_semination/' % sow1.pk, 
            {'week': 55, 'semination_employee': self.user.pk, 'boar1': self.boar.pk,
             'boar2': Boar.objects.all()[1].pk})
        self.assertEqual(response.data['semination1']['tour'], 'Tour #55')
        self.assertEqual(response.data['semination2']['tour'], 'Tour #55')
        self.assertEqual(response.data['semination1']['boar'], self.boar.pk)
        self.assertEqual(response.data['semination2']['boar'], Boar.objects.all()[1].pk)
        self.assertEqual(response.data['semination1']['semination_employee'], self.user.pk)
        self.assertEqual(response.data['semination2']['semination_employee'], self.user.pk)

    def test_import_seminations_from_farm(self):
        self.client.force_authenticate(user=self.user)
        shmigina = staff_testings.create_employee('ШМЫГИ')
        ivanov = staff_testings.create_employee('ИВАНО')
        semen = staff_testings.create_employee('СЕМЕН')
        boris = staff_testings.create_employee('БОРИС')
        gary = staff_testings.create_employee('ГАРИ')

        file_path ='../data/1.xls'
        with open(file_path, 'rb') as file:
            response = self.client.post('/api/workshoponetwo/sows/import_seminations_from_farm/', 
                {'file': file})
            self.assertEqual(response.status_code, 200)
            self.assertNotEqual(response.data.get('seminated_list_count'), None)
            self.assertNotEqual(response.data.get('already_seminated_in_tour_count'), None)
            self.assertNotEqual(response.data.get('sows_in_another_tour_count'), None)
            self.assertEqual(response.data.get('message'), "Файл загружен и обработан.")

        # # 19432 - last farm id from file
        # sow = Sow.objects.filter(farm_id=19432).first()
        # semination = Semination.objects.filter(sow=sow, tour=sow.tour).first()
        # print(semination)
        # print(semination.date)