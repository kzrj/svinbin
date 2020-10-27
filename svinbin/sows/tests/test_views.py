# -*- coding: utf-8 -*-
from datetime import timedelta, date
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

from locations.models import Location
from tours.models import Tour
from transactions.models import SowTransaction
from sows_events.models import Ultrasound, Semination, SowFarrow, UltrasoundType, WeaningSow
from sows.models import Boar, Sow, BoarBreed


class SowViewSetTest(APITestCase):
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
        
    def test_get_sow(self):
        self.client.force_authenticate(user=self.brig5)
        sow = sows_testing.create_sow_and_put_in_workshop_one()
        boar = Boar.objects.all().first()

        response = self.client.get('/api/sows/%s/' % sow.pk)

        Semination.objects.create_semination(sow=sow, week=1,
         initiator=self.user, semination_employee=self.user, boar=boar)
        response = self.client.get('/api/sows/%s/' % sow.pk)
        self.assertEqual(response.data['tours_info'][0]['seminations'][0]['semination_employee'],
            self.user.pk)

        Semination.objects.create_semination(sow=sow, week=1,
         initiator=self.user, semination_employee=self.user, boar=boar)
        response = self.client.get('/api/sows/%s/' % sow.pk)
        self.assertEqual(len(response.data['tours_info'][0]['seminations']), 2)

        Ultrasound.objects.create_ultrasound(sow, self.user, True)
        response = self.client.get('/api/sows/%s/' % sow.pk)
        self.assertEqual(response.data['tours_info'][0]['ultrasounds'][0]['result'], True)

        location = Location.objects.filter(sowAndPigletsCell__isnull=False).first()
        sow.change_sow_current_location(location)
        SowFarrow.objects.create_sow_farrow(sow=sow, alive_quantity=7, mummy_quantity=1)
        response = self.client.get('/api/sows/%s/' % sow.pk)
        self.assertEqual(response.data['tours_info'][0]['farrows'][0]['alive_quantity'], 7)
        
        Semination.objects.create_semination(sow=sow, week=2,
         initiator=self.user, semination_employee=self.user, boar=boar)
        response = self.client.get('/api/sows/%s/' % sow.pk)
        self.assertEqual(response.data['tours_info'][1]['seminations'][0]['semination_employee'],
            self.user.pk)

        Ultrasound.objects.create_ultrasound(sow, self.user, False)
        response = self.client.get('/api/sows/%s/' % sow.pk)
        self.assertEqual(response.data['tours_info'][1]['ultrasounds'][0]['result'], False)
        self.client.logout()

    def test_status_title_in_not_in(self):
        self.client.force_authenticate(user=self.brig1)

        # not seminated sow
        sow1 = sows_testing.create_sow_and_put_in_workshop_one()

        # sow one time seminated
        seminated_sow1 = sows_testing.create_sow_with_semination(sow1.location)
        
        # sow two times seminated
        seminated_sow3 = sows_testing.create_sow_with_semination(sow1.location)
        Semination.objects.create_semination(sow=seminated_sow3, week=1, initiator=None,
         semination_employee=None)

        # sow have usound 30
        seminated_sow2 = sows_testing.create_sow_with_semination(sow1.location)
        Semination.objects.create_semination(sow=seminated_sow2, week=1, initiator=None,
         semination_employee=None)
        Ultrasound.objects.create_ultrasound(sow=seminated_sow2,
         initiator=None, result=True, days=30)

        # sow have usound 60
        seminated_sow4 = sows_testing.create_sow_with_semination(sow1.location)
        Semination.objects.create_semination(sow=seminated_sow4, week=1, initiator=None,
         semination_employee=None)
        Ultrasound.objects.create_ultrasound(sow=seminated_sow4,
         initiator=None, result=True, days=30)
        Ultrasound.objects.create_ultrasound(sow=seminated_sow4,
         initiator=None, result=True, days=60)

        # sow have usound 30
        seminated_sow5 = sows_testing.create_sow_with_semination(sow1.location)
        Semination.objects.create_semination(sow=seminated_sow5, week=1, initiator=None,
         semination_employee=None)
        Ultrasound.objects.create_ultrasound(sow=seminated_sow5,
         initiator=None, result=False, days=30)

        # status in
        response = self.client.get('/api/sows/?status_title_in=Осеменена 1&status_title_in=Осеменена 2&')
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(response.data['results'][0]['id'] in [seminated_sow1.pk, seminated_sow3.pk], True)
        self.assertEqual(response.data['results'][1]['id'] in [seminated_sow1.pk, seminated_sow3.pk], True)

        response = self.client.get('/api/sows/?status_title_in=Осеменена 1&status_title_in=Супорос 28')
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(response.data['results'][0]['id'] in [seminated_sow1.pk, seminated_sow2.pk], True)
        self.assertEqual(response.data['results'][1]['id'] in [seminated_sow1.pk, seminated_sow2.pk], True)

        response = self.client.get('/api/sows/?status_title_in=Супорос 28&status_title_in=Супорос 35')
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(response.data['results'][0]['id'] in [seminated_sow2.pk, seminated_sow4.pk], True)
        self.assertEqual(response.data['results'][1]['id'] in [seminated_sow2.pk, seminated_sow4.pk], True)

        # status not in
        response = self.client.get('/api/sows/?status_title_not_in=Супорос 28&status_title_not_in=Супорос 35')
        self.assertEqual(response.data['count'], 4)
        for result_sow in response.data['results']:
            self.assertEqual(
                result_sow['id'] in [sow1.pk, seminated_sow1.pk, seminated_sow3.pk, seminated_sow5.pk],
                True)

        response = self.client.get('/api/sows/?status_title_not_in=Осеменена 1&status_title_not_in=Супорос 35')
        self.assertEqual(response.data['count'], 4)
        for result_sow in response.data['results']:
            self.assertEqual(
                result_sow['id'] in [sow1.pk, seminated_sow2.pk, seminated_sow3.pk, seminated_sow5.pk],
                True)

        self.client.logout()

    def test_to_seminate(self):
        self.client.force_authenticate(user=self.brig1)

        # not seminated sow
        sow1 = sows_testing.create_sow_and_put_in_workshop_one()

        # sow one time seminated
        seminated_sow1 = sows_testing.create_sow_with_semination(sow1.location)
        
        # sow two times seminated
        seminated_sow3 = sows_testing.create_sow_with_semination(sow1.location)
        Semination.objects.create_semination(sow=seminated_sow3, week=1, initiator=None,
         semination_employee=None)

        # sow have usound 30
        seminated_sow2 = sows_testing.create_sow_with_semination(sow1.location)
        Semination.objects.create_semination(sow=seminated_sow2, week=1, initiator=None,
         semination_employee=None)
        Ultrasound.objects.create_ultrasound(sow=seminated_sow2,
         initiator=None, result=True, days=30)

        # sow have usound 60
        seminated_sow4 = sows_testing.create_sow_with_semination(sow1.location)
        Semination.objects.create_semination(sow=seminated_sow4, week=1, initiator=None,
         semination_employee=None)
        Ultrasound.objects.create_ultrasound(sow=seminated_sow4,
         initiator=None, result=True, days=30)
        Ultrasound.objects.create_ultrasound(sow=seminated_sow4,
         initiator=None, result=True, days=60)

        # sow have usound 30
        seminated_sow5 = sows_testing.create_sow_with_semination(sow1.location)
        Semination.objects.create_semination(sow=seminated_sow5, week=1, initiator=None,
         semination_employee=None)
        Ultrasound.objects.create_ultrasound(sow=seminated_sow5,
         initiator=None, result=False, days=30)

        response =self.client.get('/api/sows/?to_seminate=True')
        self.assertEqual(response.data['count'], 2)
        for result_sow in response.data['results']:
            self.assertEqual(
                result_sow['id'] in [sow1.pk, seminated_sow5.pk],
                True)
        self.client.logout()

    def test_retrieve_by_farm_id_cycles(self):
        self.client.force_authenticate(user=self.brig1)
        sow1 = sows_testing.create_sow_with_semination(self.loc_ws1)
        Semination.objects.create_semination(sow=sow1, week=1, initiator=None,
         semination_employee=None)
        Ultrasound.objects.create_ultrasound(sow=sow1,
         initiator=None, result=True, days=30)
        Ultrasound.objects.create_ultrasound(sow=sow1,
         initiator=None, result=True, days=60)

        Semination.objects.create_semination(sow=sow1, week=2, initiator=None,
         semination_employee=None)
        Ultrasound.objects.create_ultrasound(sow=sow1,
         initiator=None, result=True, days=30)
        Ultrasound.objects.create_ultrasound(sow=sow1,
         initiator=None, result=True, days=60)
        sow1.change_sow_current_location(
            Location.objects.filter(sowAndPigletsCell__isnull=False).first())
        farrow = SowFarrow.objects.create_sow_farrow(sow=sow1, alive_quantity=7, mummy_quantity=1)
        WeaningSow.objects.create_weaning(sow=sow1, piglets=farrow.piglets_group)

        response = self.client.get(f'/api/sows/retrieve_by_farm_id/?farm_id={sow1.farm_id}')
        self.assertEqual(response.data['sow']['farm_id'], sow1.farm_id)
        self.assertEqual(response.data['cycles'][0]['week_number'], 2)
        self.assertEqual(len(response.data['cycles'][0]['sow_semination']), 1)
        self.assertEqual(len(response.data['cycles'][0]['sow_ultrasound']), 2)
        self.assertEqual(response.data['cycles'][0]['sow_farrow'][0]['alive_quantity'], 7)

        self.client.logout()

    # def test_retrieve_by_farm_id_ops(self):
    #     pass


class BoarViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        locations_testing.create_workshops_sections_and_cells()
        sows_testing.create_statuses()
        sows_testing.create_boars()
        staff_testing.create_svinbin_users()
        self.tour1 = Tour.objects.get_or_create_by_week_in_current_year(week_number=1)

        self.loc_ws1 = Location.objects.get(workshop__number=1)
        self.loc_ws2 = Location.objects.get(workshop__number=2)

        self.brig1 = User.objects.get(username='brigadir1')
        self.brig2 = User.objects.get(username='brigadir2')
        self.brig3 = User.objects.get(username='brigadir3')
        
    def test_get_boars(self):
        self.client.force_authenticate(user=self.brig1)
        response = self.client.get('/api/boars/')
        self.assertEqual(response.data['count'], 2)
        self.client.logout()

    def test_culling_boars(self):
        self.client.force_authenticate(user=self.brig1)
        boar = Boar.objects.all().first()
        response = self.client.post('/api/boars/%s/culling/' % boar.pk, 
            {'culling_type': 'padej', 'reason': 'test reason', 'weight': 100})
        self.assertEqual(response.data['message'], f"Выбраковка прошла успешно. Хряк №{boar.birth_id}.")
        boar.refresh_from_db()
        self.assertEqual(boar.active, False)
        self.client.logout()

    def test_culling_boars_401(self):
        boar = Boar.objects.all().first()
        response = self.client.post('/api/boars/%s/culling/' % boar.pk, 
            {'culling_type': 'padej', 'reason': 'test reason', 'weight': 100})
        self.assertEqual(response.status_code, 401)

    def test_culling_boars_403(self):
        self.client.force_authenticate(user=self.brig3)
        boar = Boar.objects.all().first()
        response = self.client.post('/api/boars/%s/culling/' % boar.pk, 
            {'culling_type': 'padej', 'reason': 'test reason', 'weight': 100})
        self.assertEqual(response.status_code, 403)
        self.client.logout()

    def test_create_boars(self):
        self.client.force_authenticate(user=self.brig1)
        breed = BoarBreed.objects.all().first()
        response = self.client.post('/api/boars/', {'birth_id': 123, 'breed': breed.pk})
        self.assertEqual(response.data['message'], f"Хряк №123 создан.")

        boar = Boar.objects.filter(birth_id='123').first()
        self.assertEqual(boar.birth_id, '123')
        self.assertEqual(boar.breed.title, 'first breed')
        self.client.logout()

    def test_create_boars_401(self):
        breed = BoarBreed.objects.all().first()
        response = self.client.post('/api/boars/', {'birth_id': 123, 'breed': breed.pk})
        self.assertEqual(response.status_code, 401)

    def test_create_boars_403(self):
        self.client.force_authenticate(user=self.brig3)
        breed = BoarBreed.objects.all().first()
        response = self.client.post('/api/boars/', {'birth_id': 123, 'breed': breed.pk})
        self.assertEqual(response.status_code, 403)
        self.client.logout()

    def test_semen_boar(self):
        self.client.force_authenticate(user=self.brig1)
        boar = Boar.objects.all().first()
        response = self.client.post('/api/boars/%s/semen_boar/' % boar.pk,
         {'a': 1000, 'b': 1, 'd': 50, 'morphology_score': 1, 'final_motility_score': 50,
            'date': date(2020, 7, 1)})

        self.assertEqual(response.data['message'], f"Запись создана. Хряк №{boar.birth_id}.")
        self.client.logout()

    def test_semen_boar_401(self):
        boar = Boar.objects.all().first()
        response = self.client.post('/api/boars/%s/semen_boar/' % boar.pk,
         {'a': 1000, 'b': 1, 'd': 50, 'morphology_score': 1, 'final_motility_score': 50,
            'date': date(2020, 7, 1)})
        self.assertEqual(response.status_code, 401)

    def test_semen_boar_403(self):
        self.client.force_authenticate(user=self.brig3)
        boar = Boar.objects.all().first()
        response = self.client.post('/api/boars/%s/semen_boar/' % boar.pk,
         {'a': 1000, 'b': 1, 'd': 50, 'morphology_score': 1, 'final_motility_score': 50,
            'date': date(2020, 7, 1)})
        self.assertEqual(response.status_code, 403)
        self.client.logout()
        