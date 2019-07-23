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
import piglets.testing_utils as piglets_testing

from tours.models import Tour


class WorkshopOneTwoSowViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        locations_testing.create_workshops_sections_and_cells()
        sows_testing.create_statuses()
        self.user = staff_testing.create_employee()
        
    def test_assing_farm_id(self):
        piglets1 = piglets_testing.create_new_born_group(week=1)
        piglets2 = piglets_testing.create_new_born_group(week=2)
        piglets3 = piglets_testing.create_new_born_group(week=3)

        response = self.client.get('/api/tours/')
        print(response.data)
