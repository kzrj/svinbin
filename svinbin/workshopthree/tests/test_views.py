# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
import random

from django.contrib.auth.models import User

from rest_framework.test import APIClient
from rest_framework.test import APITestCase

import workshops.testing_utils as workshops_testing
import pigs.testing_utils as pigs_testing

from pigs.models import NewBornPigletsGroup
from events.models import NewBornPigletsGroupRecount


class WorkshopThreeViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        workshops_testing.create_workshops_sections_and_cells()
        pigs_testing.create_statuses()

    def test_mark_to_transfer_mark_size_and_recount_without_recount(self):
        newBornPigletsGroup = pigs_testing.create_new_born_group()
        self.assertEqual(newBornPigletsGroup.location.sowAndPigletsCell.number, '4')

        response = self.client.post('/api/workshopthree/piglets/%s/mark_to_transfer_mark_size_and_recount/' %
          newBornPigletsGroup.pk, {'size_label': 'l'})
        
        newBornPigletsGroup.refresh_from_db()
        self.assertEqual(newBornPigletsGroup.transfer_label, True)
        self.assertEqual(newBornPigletsGroup.size_label, 'l')

    def test_mark_to_transfer_mark_size_and_recount(self):
        newBornPigletsGroup = pigs_testing.create_new_born_group()
        self.assertEqual(newBornPigletsGroup.location.sowAndPigletsCell.number, '4')

        response = self.client.post('/api/workshopthree/piglets/%s/mark_to_transfer_mark_size_and_recount/' %
          newBornPigletsGroup.pk, {'size_label': 'l', 'new_amount': 7})
        
        newBornPigletsGroup.refresh_from_db()
        self.assertEqual(newBornPigletsGroup.transfer_label, True)
        self.assertEqual(newBornPigletsGroup.size_label, 'l')
        self.assertEqual(newBornPigletsGroup.quantity, 7)
        self.assertEqual(newBornPigletsGroup.recounts.all().first().quantity_before, 10)
        self.assertEqual(newBornPigletsGroup.recounts.all().first().quantity_after, 7)

    def test_mark_to_transfer_mark_size_and_recount_without_recount(self):
        newBornPigletsGroup1 = pigs_testing.create_new_born_group()
        newBornPigletsGroup2 = pigs_testing.create_new_born_group(section_number=1, cell_number=3)
        self.assertEqual(newBornPigletsGroup2.location.sowAndPigletsCell.number, '3')

        response = self.client.post('/api/workshopthree/piglets/create_nomad_group_from_merge_and_transfer_to_weight/',
         {'piglets_groups': [newBornPigletsGroup1.pk, newBornPigletsGroup2.pk]})
        print(response.data)
        
        # newBornPigletsGroup.refresh_from_db()
        # self.assertEqual(newBornPigletsGroup.transfer_label, True)
        # self.assertEqual(newBornPigletsGroup.size_label, 'l')