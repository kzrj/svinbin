# -*- coding: utf-8 -*-
import datetime
import random

from django.contrib.auth.models import User
from django.db import connection

from rest_framework.test import APIClient
from rest_framework.test import APITestCase

import locations.testing_utils as locations_testing
import sows.testing_utils as sows_testing
import piglets.testing_utils as piglets_testing
import staff.testing_utils as staff_testing

from piglets.models import NewBornPigletsGroup, NomadPigletsGroup
from piglets_events.models import NewBornPigletsGroupRecount, NewBornPigletsMerger, CullingNewBornPiglets
from locations.models import WorkShop, SowAndPigletsCell, PigletsGroupCell, Location
from transactions.models import PigletsTransaction, SowTransaction


class LocationsViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        locations_testing.create_workshops_sections_and_cells()
        sows_testing.create_statuses()
        piglets_testing.create_piglets_statuses()
        self.user = staff_testing.create_employee()
        self.client.force_authenticate(user=self.user)

    def test_weighing_piglets(self):
        nomad_piglets_group = piglets_testing.create_nomad_group_from_three_new_born()

        response = self.client.get('/api/locations/')
        print(response.data)
        