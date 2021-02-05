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
import piglets.testing_utils as piglets_testing

from sows.models import Boar, Sow
from tours.models import Tour
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
        staff_testing.create_svinbin_users()
        self.boar = Boar.objects.all().first()
        self.user = staff_testing.create_employee() # is_seminator = True

        self.brig1 = User.objects.get(username='brigadir1')
        self.brig2 = User.objects.get(username='brigadir2')
        self.brig3 = User.objects.get(username='brigadir3')
        self.brig4 = User.objects.get(username='brigadir4')
        self.brig5 = User.objects.get(username='brigadir5')

    def test_culling(self):
        self.client.force_authenticate(user=self.brig1)
        sow = sows_testing.create_sow_and_put_in_workshop_one()
        semination_employee = staff_testing.create_employee()

        response = self.client.post('/api/workshoponetwo/sows/%s/culling/' %
          sow.pk, {'culling_type': 'padej', 'reason': 'test reason', 'weight': 150})

        self.assertEqual(response.data['culling']['reason'], 'test reason')
        self.assertEqual(response.data['sow']['status'], 'Брак')
        self.client.logout()

    def test_culling_brig2(self):
        self.client.force_authenticate(user=self.brig2)
        sow = sows_testing.create_sow_and_put_in_workshop_one()
        semination_employee = staff_testing.create_employee()

        response = self.client.post('/api/workshoponetwo/sows/%s/culling/' %
          sow.pk, {'culling_type': 'padej', 'reason': 'test reason', 'weight': 150})

        self.assertEqual(response.data['culling']['reason'], 'test reason')
        self.assertEqual(response.data['sow']['status'], 'Брак')
        self.client.logout()

    def test_mass_semination(self):
        sow1 = sows_testing.create_sow_and_put_in_workshop_one()
        sow2 = sows_testing.create_sow_and_put_in_workshop_one()
        sow3 = sows_testing.create_sow_and_put_in_workshop_one()

        self.client.force_authenticate(user=self.brig1)
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
        self.client.logout()

    def test_mass_ultrasound(self):
        sow1 = sows_testing.create_sow_and_put_in_workshop_one()
        sow2 = sows_testing.create_sow_and_put_in_workshop_one()
        sow3 = sows_testing.create_sow_and_put_in_workshop_one()

        self.client.force_authenticate(user=self.brig1)
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
        self.client.logout()

    def test_mass_culling(self):
        sow1 = sows_testing.create_sow_and_put_in_workshop_one()
        sow2 = sows_testing.create_sow_and_put_in_workshop_one()
        sow3 = sows_testing.create_sow_and_put_in_workshop_one()

        self.client.force_authenticate(user=self.brig1)
        response = self.client.post('/api/workshoponetwo/sows/mass_culling/',
            { 
              'sows': [sow1.pk, sow2.pk, sow3.pk], 'culling_type': 'padej', 
              'reason': 'test_reason', 'weight': 0
            })

        sow1.refresh_from_db()
        sow2.refresh_from_db()
        sow3.refresh_from_db()

        self.assertEqual(sow1.alive, False)
        self.assertEqual(sow2.alive, False)
        self.assertEqual(sow3.alive, False)

        self.assertEqual(sow1.status.title, 'Брак')
        self.assertEqual(sow2.status.title, 'Брак')
        self.assertEqual(sow3.status.title, 'Брак')
        self.client.logout()

    def test_abortion(self):
        self.client.force_authenticate(user=self.brig1)        
        sow1 = sows_testing.create_sow_and_put_in_workshop_one()        
        Semination.objects.create_semination(sow=sow1, week=1, initiator=None,
         semination_employee=None)
        Ultrasound.objects.create_ultrasound(sow=sow1,
         initiator=None, result=True, days=30)

        response = self.client.post('/api/workshoponetwo/sows/%s/abortion/' % sow1.pk)
        self.assertEqual(response.data['sow']['status'], 'Аборт')
        self.client.logout()

    def test_abortion_brig2(self):
        self.client.force_authenticate(user=self.brig2)        
        sow1 = sows_testing.create_sow_and_put_in_workshop_one()        
        Semination.objects.create_semination(sow=sow1, week=1, initiator=None,
         semination_employee=None)
        Ultrasound.objects.create_ultrasound(sow=sow1,
         initiator=None, result=True, days=30)

        response = self.client.post('/api/workshoponetwo/sows/%s/abortion/' % sow1.pk)
        self.assertEqual(response.data['sow']['status'], 'Аборт')
        self.client.logout()

    def test_double_semination(self):
        sow1 = sows_testing.create_sow_and_put_in_workshop_one()
        self.client.force_authenticate(user=self.brig1)
        response = self.client.post('/api/workshoponetwo/sows/double_semination/', 
            {'week': 55, 'seminator1': self.user.pk, 'seminator2': self.user.pk,
             'boar1': self.boar.pk, 'date': '2020-09-09T00:00',
             'boar2': Boar.objects.all()[1].pk, 'farm_id': sow1.farm_id})

        self.assertEqual('Тур 55' in response.data['semination1']['tour'], True)
        self.assertEqual('Тур 55' in response.data['semination2']['tour'], True)
        self.assertEqual(response.data['semination1']['boar'], self.boar.pk)
        self.assertEqual(response.data['semination2']['boar'], Boar.objects.all()[1].pk)
        self.assertEqual(response.data['semination1']['semination_employee'], self.user.pk)
        self.assertEqual(response.data['semination2']['semination_employee'], self.user.pk)
        self.client.logout()


class WS12SowViewSetPermissionsTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        locations_testing.create_workshops_sections_and_cells()
        sows_testing.create_statuses()
        sows_testing.create_boars()
        sows_events_testing.create_types()
        piglets_testing.create_piglets_statuses()
        staff_testing.create_svinbin_users()
        self.user = staff_testing.create_employee()
        self.boar = Boar.objects.all().first()

        self.tour1 = Tour.objects.get_or_create_by_week_in_current_year(week_number=1)
        self.tour2 = Tour.objects.get_or_create_by_week_in_current_year(week_number=2)
        self.tour3 = Tour.objects.get_or_create_by_week_in_current_year(week_number=3)
        self.tour4 = Tour.objects.get_or_create_by_week_in_current_year(week_number=4)

        self.loc_ws1 = Location.objects.get(workshop__number=1)
        self.loc_ws2 = Location.objects.get(workshop__number=2)

        self.loc_ws3 = Location.objects.get(workshop__number=3)
        self.loc_ws3_sec1 = Location.objects.get(section__workshop__number=3, section__number=1)
        self.loc_ws3_sec2 = Location.objects.get(section__workshop__number=3, section__number=2)

        self.loc_ws4 = Location.objects.get(workshop__number=4)
        self.loc_ws4_cell1 = Location.objects.filter(pigletsGroupCell__isnull=False)[0]
        self.loc_ws4_cell2 = Location.objects.filter(pigletsGroupCell__isnull=False)[1]

        self.loc_ws8 = Location.objects.get(workshop__number=8)

        self.loc_ws5 = Location.objects.get(workshop__number=5)
        self.loc_ws6 = Location.objects.get(workshop__number=6)
        self.loc_ws7 = Location.objects.get(workshop__number=7)

        self.brig1 = User.objects.get(username='brigadir1')
        self.brig2 = User.objects.get(username='brigadir2')
        self.brig3 = User.objects.get(username='brigadir3')
        self.brig4 = User.objects.get(username='brigadir4')
        self.brig5 = User.objects.get(username='brigadir5')

    def test_move_to_permissions_200(self):
        self.client.force_authenticate(user=self.brig1)
        sow1 = sows_testing.create_sow_and_put_in_workshop_one()
        response = self.client.post('/api/workshoponetwo/sows/%s/move_to/' % sow1.pk,
         {'location': self.loc_ws2})
        self.assertEqual(response.status_code, 200)
        self.client.logout()

    def test_move_to_permissions_200_br2(self):
        self.client.force_authenticate(user=self.brig2)
        sow1 = sows_testing.create_sow_and_put_in_workshop_one()
        response = self.client.post('/api/workshoponetwo/sows/%s/move_to/' % sow1.pk,
         {'location': self.loc_ws2})
        self.assertEqual(response.status_code, 200)
        self.client.logout()

    def test_move_to_permissions_401(self):
        sow1 = sows_testing.create_sow_and_put_in_workshop_one()
        response = self.client.post('/api/workshoponetwo/sows/%s/move_to/' % sow1.pk,
         {'location': self.loc_ws2})
        self.assertEqual(response.status_code, 401)

    def test_move_to_permissions_403(self):
        self.client.force_authenticate(user=self.brig3)
        sow1 = sows_testing.create_sow_and_put_in_workshop_one()
        response = self.client.post('/api/workshoponetwo/sows/%s/move_to/' % sow1.pk,
         {'location': self.loc_ws2})
        self.assertEqual(response.status_code, 403)
        self.client.logout()

    def test_move_many_permissions_200(self):
        self.client.force_authenticate(user=self.brig1)
        sow1 = sows_testing.create_sow_and_put_in_workshop_one()
        sow2 = sows_testing.create_sow_and_put_in_workshop_one()
        sow3 = sows_testing.create_sow_and_put_in_workshop_one()

        response = self.client.post('/api/workshoponetwo/sows/move_many/',
         {'to_location': self.loc_ws2, 'sows': [sow1.pk, sow2.pk, sow3.pk]})
        self.assertEqual(response.status_code, 200)
        self.client.logout()

    def test_move_many_permissions_401(self):
        sow1 = sows_testing.create_sow_and_put_in_workshop_one()
        sow2 = sows_testing.create_sow_and_put_in_workshop_one()
        sow3 = sows_testing.create_sow_and_put_in_workshop_one()

        response = self.client.post('/api/workshoponetwo/sows/move_many/',
         {'to_location': self.loc_ws2, 'sows': [sow1.pk, sow2.pk, sow3.pk]})
        self.assertEqual(response.status_code, 401)

    def test_move_many_permissions_403(self):
        self.client.force_authenticate(user=self.brig3)
        sow1 = sows_testing.create_sow_and_put_in_workshop_one()
        sow2 = sows_testing.create_sow_and_put_in_workshop_one()
        sow3 = sows_testing.create_sow_and_put_in_workshop_one()

        response = self.client.post('/api/workshoponetwo/sows/move_many/',
         {'to_location': self.loc_ws2, 'sows': [sow1.pk, sow2.pk, sow3.pk]})
        self.assertEqual(response.status_code, 403)
        self.client.logout()

    def test_culling_permissions_200(self):
        self.client.force_authenticate(user=self.brig1)
        sow1 = sows_testing.create_sow_and_put_in_workshop_one()
        response = self.client.post('/api/workshoponetwo/sows/%s/culling/' % sow1.pk,
         {'culling_type': 'padej', 'reason': 'test', 'weight': 150})
        self.assertEqual(response.status_code, 200)
        self.client.logout()

    def test_culling_permissions_401(self):
        sow1 = sows_testing.create_sow_and_put_in_workshop_one()
        response = self.client.post('/api/workshoponetwo/sows/%s/culling/' % sow1.pk,
         {'culling_type': 'padej', 'reason': 'test', 'weight': 150})
        self.assertEqual(response.status_code, 401)

    def test_culling_permissions_403(self):
        self.client.force_authenticate(user=self.brig5)
        sow1 = sows_testing.create_sow_and_put_in_workshop_one()
        response = self.client.post('/api/workshoponetwo/sows/%s/culling/' % sow1.pk,
         {'culling_type': 'padej', 'reason': 'test', 'weight': 150})
        self.assertEqual(response.status_code, 403)
        self.client.logout()

    def test_abortion_permissions_200(self):
        self.client.force_authenticate(user=self.brig1)
        sow1 = sows_testing.create_sow_and_put_in_workshop_one()
        response = self.client.post('/api/workshoponetwo/sows/%s/abortion/' % sow1.pk)
        self.assertEqual(response.status_code, 200)
        self.client.logout()

    def test_abortion_permissions_401(self):
        sow1 = sows_testing.create_sow_and_put_in_workshop_one()
        response = self.client.post('/api/workshoponetwo/sows/%s/abortion/' % sow1.pk)
        self.assertEqual(response.status_code, 401)

    def test_abortion_permissions_403(self):
        self.client.force_authenticate(user=self.brig3)
        sow1 = sows_testing.create_sow_and_put_in_workshop_one()
        response = self.client.post('/api/workshoponetwo/sows/%s/abortion/' % sow1.pk)
        self.assertEqual(response.status_code, 403)
        self.client.logout()

    def test_assing_farm_id_permissions_200(self):
        self.client.force_authenticate(user=self.brig1)
        sow1 = sows_testing.create_sow_and_put_in_workshop_one()
        sow1.farm_id = None
        sow1.save()
        response = self.client.post('/api/workshoponetwo/sows/%s/assing_farm_id/' \
            % sow1.pk, {'farm_id': '123'})
        self.assertEqual(response.status_code, 200)
        self.client.logout()

    def test_assing_farm_id_permissions_401(self):
        sow1 = sows_testing.create_sow_and_put_in_workshop_one()
        sow1.farm_id = None
        sow1.save()
        response = self.client.post('/api/workshoponetwo/sows/%s/assing_farm_id/' \
            % sow1.pk, {'farm_id': '123'})
        self.assertEqual(response.status_code, 401)

    def test_assing_farm_id_permissions_403(self):
        self.client.force_authenticate(user=self.brig3)
        sow1 = sows_testing.create_sow_and_put_in_workshop_one()
        sow1.farm_id = None
        sow1.save()
        response = self.client.post('/api/workshoponetwo/sows/%s/assing_farm_id/' \
            % sow1.pk, {'farm_id': '123'})
        self.assertEqual(response.status_code, 403)
        self.client.logout()

    def test_mass_semination_permissions_200(self):
        self.client.force_authenticate(user=self.brig1)
        sow1 = sows_testing.create_sow_and_put_in_workshop_one()
        sow2 = sows_testing.create_sow_and_put_in_workshop_one()
        sow3 = sows_testing.create_sow_and_put_in_workshop_one()

        response = self.client.post('/api/workshoponetwo/sows/mass_semination/',
         {'week': 5, 'sows': [sow1.pk, sow2.pk, sow3.pk], 
         'semination_employee': self.brig1.pk, 'boar': self.boar.pk})
        print(response.data)
        self.assertEqual(response.status_code, 200)
        self.client.logout()

    def test_mass_semination_permissions_401(self):
        sow1 = sows_testing.create_sow_and_put_in_workshop_one()
        sow2 = sows_testing.create_sow_and_put_in_workshop_one()
        sow3 = sows_testing.create_sow_and_put_in_workshop_one()

        response = self.client.post('/api/workshoponetwo/sows/mass_semination/',
         {'week': 5, 'sows': [sow1.pk, sow2.pk, sow3.pk], 
         'semination_employee': self.brig1.pk, 'boar': self.boar.pk})
        self.assertEqual(response.status_code, 401)

    def test_mass_semination_permissions_403(self):
        self.client.force_authenticate(user=self.brig3)
        sow1 = sows_testing.create_sow_and_put_in_workshop_one()
        sow2 = sows_testing.create_sow_and_put_in_workshop_one()
        sow3 = sows_testing.create_sow_and_put_in_workshop_one()

        response = self.client.post('/api/workshoponetwo/sows/mass_semination/',
         {'week': 5, 'sows': [sow1.pk, sow2.pk, sow3.pk], 
         'semination_employee': self.brig1.pk, 'boar': self.boar.pk})
        self.assertEqual(response.status_code, 403)
        self.client.logout()

    def test_import_seminations_from_farm_permissions_401(self):
        response = self.client.post('/api/workshoponetwo/sows/import_seminations_from_farm/')
        self.assertEqual(response.status_code, 401)

    def test_import_seminations_from_farm_permissions_403(self):
        self.client.force_authenticate(user=self.brig3)
        response = self.client.post('/api/workshoponetwo/sows/import_seminations_from_farm/')
        self.assertEqual(response.status_code, 403)
        self.client.logout()