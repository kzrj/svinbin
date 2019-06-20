# -*- coding: utf-8 -*-
import datetime
import random

from django.contrib.auth.models import User
from django.db import connection

from rest_framework.test import APIClient
from rest_framework.test import APITestCase

import workshops.testing_utils as workshops_testing
import sows.testing_utils as sows_testing
import piglets.testing_utils as piglets_testing

from piglets.models import NewBornPigletsGroup, NomadPigletsGroup
from piglets_events.models import NewBornPigletsGroupRecount, NewBornPigletsMerger, CullingNewBornPiglets
from workshops.models import WorkShop, SowAndPigletsCell
from transactions.models import PigletsTransaction, Location, SowTransaction


class WorkshopFourPigletsViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        workshops_testing.create_workshops_sections_and_cells()
        sows_testing.create_statuses()
        piglets_testing.create_piglets_statuses()

    def test_weighing_piglets(self):
        nomad_piglets_group = piglets_testing.create_nomad_group_from_three_new_born()

        response = self.client.post('/api/workshopfour/piglets/%s/weighing_piglets/' %
          nomad_piglets_group.pk, {'total_weight': 670, 'place': '3/4'})
        self.assertEqual(response.data['piglets_group']['id'], nomad_piglets_group.pk)
        self.assertEqual(response.data['piglets_group']['status'], 'Взвешены, готовы к заселению')
        self.assertEqual(response.data['weighing_record']['piglets_group'], nomad_piglets_group.pk)
        self.assertEqual(response.data['weighing_record']['total_weight'], 670)
        self.assertEqual(response.data['weighing_record']['place'], '3/4')

    def test_get_weighted_piglets_outside_cells(self):
        nomad_piglets_group1 = piglets_testing.create_nomad_group_from_three_new_born()
        nomad_piglets_group2 = piglets_testing.create_nomad_group_from_three_new_born()
        nomad_piglets_group2.location = Location.objects.create_location(WorkShop.objects.get(number=4))
        nomad_piglets_group2.save()
        nomad_piglets_group3 = piglets_testing.create_nomad_group_from_three_new_born()
        nomad_piglets_group3.location = Location.objects.create_location(WorkShop.objects.get(number=4))
        nomad_piglets_group3.save()

        response = self.client.post('/api/workshopfour/piglets/%s/weighing_piglets/' %
          nomad_piglets_group2.pk, {'total_weight': 670, 'place': '3/4'})
        
        response = self.client.get('/api/workshopfour/piglets/get_weighted_piglets_outside_cells/')
        print(response.data)
        self.assertEqual(response.data['piglets_groups'][0]['id'], nomad_piglets_group2.pk)
        self.assertEqual(len(response.data['piglets_groups']), 1)

    def test_waiting_for_weighing_piglets_outside_cells(self):
        nomad_piglets_group1 = piglets_testing.create_nomad_group_from_three_new_born()
        nomad_piglets_group1.location = Location.objects.create_location(WorkShop.objects.get(number=4))
        nomad_piglets_group1.save()
        nomad_piglets_group2 = piglets_testing.create_nomad_group_from_three_new_born()
        nomad_piglets_group2.location = Location.objects.create_location(WorkShop.objects.get(number=4))
        nomad_piglets_group2.save()
        nomad_piglets_group3 = piglets_testing.create_nomad_group_from_three_new_born()
        nomad_piglets_group3.location = Location.objects.create_location(WorkShop.objects.get(number=4))
        nomad_piglets_group3.reset_status()

        response = self.client.post('/api/workshopfour/piglets/%s/weighing_piglets/' %
          nomad_piglets_group2.pk, {'total_weight': 670, 'place': '3/4'})
        
        response = self.client.get('/api/workshopfour/piglets/waiting_for_weighing_piglets_outside_cells/')
        self.assertEqual(len(response.data['piglets_groups']), 1)
        self.assertEqual(response.data['piglets_groups'][0]['id'], nomad_piglets_group1.pk)