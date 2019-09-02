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
        sows_events_testing.create_types()
        self.user = staff_testing.create_employee()
        
    def test_get_sow(self):
        self.client.force_authenticate(user=self.user)
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

        SowFarrow.objects.create_sow_farrow(sow=sow, alive_quantity=7, mummy_quantity=1)
        response = self.client.get('/api/sows/%s/' % sow.pk)
        self.assertEqual(response.data['tours_info'][0]['farrows'][0]['alive_quantity'], 7)

        SowFarrow.objects.create_sow_farrow(sow=sow, alive_quantity=10, mummy_quantity=1)
        response = self.client.get('/api/sows/%s/' % sow.pk)
        self.assertEqual(response.data['tours_info'][0]['farrows'][1]['alive_quantity'], 10)
        
        Semination.objects.create_semination(sow=sow, week=2,
         initiator=self.user, semination_employee=self.user, boar=boar)
        response = self.client.get('/api/sows/%s/' % sow.pk)
        self.assertEqual(response.data['tours_info'][1]['seminations'][0]['semination_employee'],
            self.user.pk)

        Ultrasound.objects.create_ultrasound(sow, self.user, False)
        response = self.client.get('/api/sows/%s/' % sow.pk)
        self.assertEqual(response.data['tours_info'][1]['ultrasounds'][0]['result'], False)

    # init only tests
    def test_add_new_seminated_to_ws1(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/sows/add_new_seminated_to_ws1/',
         {'farm_id': 100, 'boar': 100, 'week': 10})
        self.assertEqual(response.data['sow']['farm_id'], 100)
        self.assertEqual(response.data['sow']['tour'], 'Tour #10')
        self.assertEqual(response.data['semination']['boar'], Boar.objects.get(birth_id=100).pk)
        self.assertEqual(Sow.objects.get(farm_id=100).location.workshop.number, 1)

    def test_add_new_ultrasounded_to_ws12(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/sows/add_new_ultrasounded_to_ws12/',
         {'farm_id': 101, 'boar': 100, 'week': 11, 'workshop_number': 2, 'days': 60,
          'result': True})
        self.assertEqual(response.data['sow']['farm_id'], 101)
        self.assertEqual(response.data['sow']['tour'], 'Tour #11')
        self.assertEqual(response.data['semination']['boar'], Boar.objects.get(birth_id=100).pk)
        self.assertEqual(response.data['ultrasound']['u_type'], UltrasoundType.objects.get(days=60).pk)
        self.assertEqual(Sow.objects.get(farm_id=101).location.workshop.number, 2)

    def test_add_new_suporos_to_ws3(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/sows/add_new_suporos_to_ws3/',
         {'farm_id': 102, 'boar': 100, 'week': 12, 'section': 1, 'cell': 5})
        self.assertEqual(response.data['sow']['farm_id'], 102)
        self.assertEqual(response.data['sow']['tour'], 'Tour #12')
        self.assertEqual(response.data['semination']['boar'], Boar.objects.get(birth_id=100).pk)
        sow = Sow.objects.get(farm_id=102)
        self.assertEqual(sow.location.sowAndPigletsCell.number, '5')
        self.assertEqual(sow.location.sowAndPigletsCell.section.number, 1)

    def test_add_new_oporos_to_ws3(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/sows/add_new_oporos_to_ws3/',
         {'farm_id': 103, 'boar': 100, 'week': 12, 'section': 6, 'cell': 45,
          'alive_quantity': 5, 'dead_quantity': 4, 'mummy_quantity': 3})
        self.assertEqual(response.data['sow']['farm_id'], 103)
        self.assertEqual(response.data['sow']['tour'], 'Tour #12')
        self.assertEqual(response.data['semination']['boar'], Boar.objects.get(birth_id=100).pk)
        sow = Sow.objects.get(farm_id=103)
        self.assertEqual(sow.location.sowAndPigletsCell.number, '45')
        self.assertEqual(sow.location.sowAndPigletsCell.section.number, 6)
        self.assertEqual(response.data['farrow']['alive_quantity'], 5)

    def test_filter_suporos(self):
        self.client.force_authenticate(user=self.user)
        sow1 = sows_testing.create_sow_and_put_in_workshop_one()
        seminated_sow1 = sows_testing.create_sow_with_semination(sow1.location)
        seminated_sow3 = sows_testing.create_sow_with_semination(sow1.location)
        seminated_sow2 = sows_testing.create_sow_with_semination(sow1.location)
        seminated_sow5 = sows_testing.create_sow_with_semination(sow1.location)
        seminated_sow6 = sows_testing.create_sow_with_semination(sow1.location)

        # in tour, without usound
        seminated_sow4 = sows_testing.create_sow_with_semination(sow1.location)

        # sow have usound 30 and 60, both true. In tour true. In qs 60
        Ultrasound.objects.create_ultrasound(sow=seminated_sow1,
         initiator=None, result=True, days=30)
        Ultrasound.objects.create_ultrasound(sow=seminated_sow1,
         initiator=None, result=True, days=60)

        # sow have usound 30 and 60, both true. Not in tour true. Should not be in qs
        Ultrasound.objects.create_ultrasound(sow=seminated_sow6,
         initiator=None, result=True, days=30)
        Ultrasound.objects.create_ultrasound(sow=seminated_sow6,
         initiator=None, result=False, days=60)

        # have usound 30 false. Should not be in qs
        Ultrasound.objects.create_ultrasound(sow=seminated_sow3,
         initiator=None, result=False, days=30)

        # have usound 30 True, In tour. Should not be in qs
        Ultrasound.objects.create_ultrasound(sow=seminated_sow2,
         initiator=None, result=True, days=30)

        # have u30, u60, tour and farrow. Should not be in qs
        Ultrasound.objects.create_ultrasound(sow=seminated_sow5,
         initiator=None, result=True, days=30)
        Ultrasound.objects.create_ultrasound(sow=seminated_sow5,
         initiator=None, result=True, days=60)
        SowFarrow.objects.create_sow_farrow(sow=seminated_sow5, alive_quantity=10,
         dead_quantity=1, mummy_quantity=2)

        response = self.client.get('/api/sows/?suporos=30')
        self.assertEqual(response.data['results'][0]['id'], seminated_sow2.pk)

        response = self.client.get('/api/sows/?suporos=60')
        self.assertEqual(response.data['results'][0]['id'], seminated_sow1.pk)

    def test_filter_seminated(self):
        self.client.force_authenticate(user=self.user)
        
        # not seminated sow
        sow1 = sows_testing.create_sow_and_put_in_workshop_one()

        # sow one time seminated
        seminated_sow1 = sows_testing.create_sow_with_semination(sow1.location)
        
        # sow two times seminated. not in 1
        seminated_sow3 = sows_testing.create_sow_with_semination(sow1.location)
        Semination.objects.create_semination(sow=seminated_sow3, week=1, initiator=None,
         semination_employee=None)

        # sow have usound
        seminated_sow2 = sows_testing.create_sow_with_semination(sow1.location)
        Ultrasound.objects.create_ultrasound(sow=seminated_sow2,
         initiator=None, result=True, days=30)

        response = self.client.get('/api/sows/?seminated=1')
        print(response.data)
        print(response.data['results'][0]['seminations_current_tour'])
        print(type(response.data['results'][0]['seminations_current_tour']))
        self.assertEqual(response.data['results'][0]['id'], seminated_sow1.pk)
        self.assertEqual(response.data['count'], 1)

        response = self.client.get('/api/sows/?seminated=2')
        self.assertEqual(response.data['results'][0]['id'], seminated_sow3.pk)
        self.assertEqual(response.data['count'], 1)




class BoarViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        locations_testing.create_workshops_sections_and_cells()
        sows_testing.create_statuses()
        sows_testing.create_boars()
        self.user = staff_testing.create_employee()
        
    def test_get_boars(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/boars/')
        self.assertEqual(response.data['count'], 2)