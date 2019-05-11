# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
import random

from django.contrib.auth.models import User

from rest_framework.test import APIClient
from rest_framework.test import APITestCase

import workshops.testing_utils as workshops_testing
import sows.testing_utils as sows_testing
from transactions.views import WorkShopSowTransactionViewSet
from workshops.models import WorkShop, Section, SowSingleCell, PigletsGroupCell, SowGroupCell, \
SowAndPigletsCell
from sows.models import Sow
from transactions.models import Location, SowTransaction


class WorkshopOneSowTransactionTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        workshops_testing.create_workshops_sections_and_cells()

    def test_move_to_workshop_one(self):
        sow = sows_testing.create_sow_and_put_in_workshop_two(2, '2')
        self.assertEqual(sow.location.sowGroupCell.number, '2')

        response = self.client.post('/api/workshopone/sowtransactions/move_to_workshop_one/',
         {'sow': sow.pk})

        sowTransaction = SowTransaction.objects.get(sow=sow)
        self.assertEqual(sowTransaction.from_location.sowGroupCell.number, '2')
        self.assertEqual(sowTransaction.to_location.workshop.number, 1)

        sow.refresh_from_db()
        self.assertEqual(sow.location.workshop.number, 1)

    def test_put_sow_in_cell(self):
        sow = sows_testing.create_sow_and_put_in_workshop_two(2, '2')
        response = self.client.post('/api/workshopone/sowtransactions/move_to_workshop_one/',
         {'sow': sow.pk})

        response = self.client.post('/api/workshopone/sowtransactions/put_sow_in_cell/',
         {'sow': sow.pk, 'cell_number': '5'})

        sow.refresh_from_db()
        self.assertEqual(sow.location.sowSingleCell.number, '5')
        self.assertEqual(sow.location.workshop, None)
        self.assertEqual(sow.location.section, None)
        self.assertNotEqual(sow.location.sowSingleCell, None)
        self.assertEqual(sow.location.pigletsGroupCell, None)
        self.assertEqual(sow.location.sowAndPigletsCell, None)
        self.assertEqual(sow.location.sowGroupCell, None)

    def test_return_sow(self):
        sow = sows_testing.create_sow_and_put_in_workshop_two(2, '2')
        response = self.client.post('/api/workshopone/sowtransactions/move_to_workshop_one/',
         {'sow': sow.pk})

        response = self.client.post('/api/workshopone/sowtransactions/return_sow/',
         {'sow': sow.pk})
        sow.refresh_from_db()
        
        self.assertEqual(sow.location.workshop.number, 2)
        self.assertEqual(sow.location.section, None)
        self.assertEqual(sow.location.sowSingleCell, None)
        self.assertEqual(sow.location.pigletsGroupCell, None)
        self.assertEqual(sow.location.sowAndPigletsCell, None)
        self.assertEqual(sow.location.sowGroupCell, None)

    def test_move_to(self):
        sow = sows_testing.create_sow_and_put_in_workshop_two(2, '2')
        test_view = WorkShopSowTransactionViewSet()
        test_view._move_to(sow, Section.objects.get(workshop__number=1, number=1))
        # test_view._move_to(sow, 'HUo')

        sow.refresh_from_db()
        self.assertEqual(sow.location.section.number, 1)

