# -*- coding: utf-8 -*-
import datetime
import random

from django.contrib.auth.models import User

from rest_framework.test import APIClient
from rest_framework.test import APITestCase

import locations.testing_utils as locations_testing
import sows.testing_utils as sows_testing
import piglets.testing_utils as piglets_testing

from piglets.models import NewBornPigletsGroup, NomadPigletsGroup
from piglets_events.models import NewBornPigletsGroupRecount, NewBornPigletsMerger, CullingNewBornPiglets
from locations.models import WorkShop, SowAndPigletsCell, Location
from transactions.models import PigletsTransaction, SowTransaction


class WorkshopThreePigletsViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        locations_testing.create_workshops_sections_and_cells()
        sows_testing.create_statuses()
        piglets_testing.create_piglets_statuses()

    def test_mark_to_transfer_mark_size_and_recount_without_recount(self):
        newBornPigletsGroup = piglets_testing.create_new_born_group()
        self.assertEqual(newBornPigletsGroup.location.sowAndPigletsCell.number, '4')

        response = self.client.post('/api/workshopthree/piglets/%s/mark_to_transfer_mark_size_and_recount/' %
          newBornPigletsGroup.pk, {'size_label': 'l'})
        
        newBornPigletsGroup.refresh_from_db()
        self.assertEqual(newBornPigletsGroup.transfer_label, True)
        self.assertEqual(newBornPigletsGroup.size_label, 'l')

    def test_mark_to_transfer_mark_size_and_recount(self):
        newBornPigletsGroup = piglets_testing.create_new_born_group()
        self.assertEqual(newBornPigletsGroup.location.sowAndPigletsCell.number, '4')

        response = self.client.post('/api/workshopthree/piglets/%s/mark_to_transfer_mark_size_and_recount/' %
          newBornPigletsGroup.pk, {'size_label': 'l', 'new_amount': 7})
        
        newBornPigletsGroup.refresh_from_db()
        self.assertEqual(newBornPigletsGroup.transfer_label, True)
        self.assertEqual(newBornPigletsGroup.size_label, 'l')
        self.assertEqual(newBornPigletsGroup.quantity, 7)
        self.assertEqual(newBornPigletsGroup.recounts.all().first().quantity_before, 10)
        self.assertEqual(newBornPigletsGroup.recounts.all().first().quantity_after, 7)

    def test_create_nomad_group_from_merge_and_transfer_to_weight(self):
        newBornPigletsGroup1 = piglets_testing.create_new_born_group()
        newBornPigletsGroup2 = piglets_testing.create_new_born_group(section_number=1, cell_number=3)
        self.assertEqual(newBornPigletsGroup2.location.sowAndPigletsCell.number, '3')

        response = self.client.post('/api/workshopthree/piglets/create_nomad_group_from_merge_and_transfer_to_weight/',
         {'piglets_groups': [newBornPigletsGroup1.pk, newBornPigletsGroup2.pk]})

        nomad_group = NomadPigletsGroup.objects.filter(pk=response.data['nomad_group']['id']).first()
        self.assertNotEqual(nomad_group, None)
        self.assertEqual(nomad_group.location.get_location, WorkShop.objects.get(number=4))

        new_born_merger = NewBornPigletsMerger.objects.filter(nomad_group=nomad_group).first()
        self.assertNotEqual(new_born_merger, None)
        # self.assertEqual(new_born_merger.piglets_groups.all()[0], newBornPigletsGroup1)
        # self.assertEqual(new_born_merger.piglets_groups.all()[1], newBornPigletsGroup2)
        # print(new_born_merger.piglets_groups.all())

        transaction = nomad_group.transactions.all().first()
        self.assertNotEqual(transaction, None)
        self.assertEqual(transaction.from_location.get_location, WorkShop.objects.get(number=3))
        self.assertEqual(transaction.to_location.get_location, WorkShop.objects.get(number=4))


    def test_culling_piglets(self):
        newBornPigletsGroup = piglets_testing.create_new_born_group()
        response = self.client.post('/api/workshopthree/piglets/%s/culling_piglets/' %
          newBornPigletsGroup.pk, {'culling_type': 'padej', 'reason': 'xz'})
        
        culling = CullingNewBornPiglets.objects.filter(piglets_group=newBornPigletsGroup).first()
        self.assertNotEqual(culling, None)
        self.assertEqual(culling.reason, 'xz')
        self.assertEqual(culling.culling_type, 'padej')


class WorkshopThreeSowsViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        locations_testing.create_workshops_sections_and_cells()
        sows_testing.create_statuses()

    def test_sow_farrow(self):
        sow = sows_testing.create_sow_with_semination_and_put_in_workshop_three(section_number=1,
         cell_number=1, week=7)
        response = self.client.post('/api/workshopthree/sows/%s/sow_farrow/' %
          sow.pk, {'alive_quantity': 10, 'dead_quantity': 1, 'mummy_quantity': 2, 'week': 7 })

        self.assertEqual(response.data['sow']['id'], sow.pk)
        self.assertEqual(response.data['sow']['farm_id'], sow.farm_id)
        self.assertEqual(response.data['sow']['tour'], 'Tour #7')
        self.assertEqual(response.data['sow']['status'], 'Опоросилась, кормит')
        self.assertEqual(response.data['farrow']['alive_quantity'], 10)
        self.assertEqual(response.data['farrow']['dead_quantity'], 1)
        self.assertEqual(response.data['farrow']['mummy_quantity'], 2)

    def test_occupy_sow_to_cell(self):
        sow = sows_testing.create_sow_with_location(Location.objects.create_workshop_location(3))
        self.assertEqual(sow.location.get_location, WorkShop.objects.get(number=3))

        cell = SowAndPigletsCell.objects.all().first()
        response = self.client.post('/api/workshopthree/sows/%s/occupy_sow_to_cell/' %
          sow.pk, {'cell_number': cell.pk })

        self.assertEqual(response.data['sow']['id'], sow.pk)
        
        transaction = SowTransaction.objects.get(pk=response.data['transaction']['id'])
        self.assertEqual(transaction.sow, sow)
        self.assertEqual(transaction.to_location.get_location, cell)

    def test_move_sow_to_workshop_one(self):
        sow = sows_testing.create_sow_and_put_in_workshop_three()
        response = self.client.post('/api/workshopthree/sows/%s/move_sow_to_workshop_one/' %
          sow.pk)

        self.assertEqual(response.data['sow']['id'], sow.pk)

        transaction = SowTransaction.objects.get(pk=response.data['transaction']['id'])
        self.assertEqual(transaction.sow, sow)
        self.assertEqual(transaction.to_location.get_location, WorkShop.objects.get(number=1))

    def test_move_many_sows_to_workshop_one(self):
        sow1 = sows_testing.create_sow_and_put_in_workshop_three(1, 1)
        sow2 = sows_testing.create_sow_and_put_in_workshop_three(1, 2)
        sow3 = sows_testing.create_sow_and_put_in_workshop_three(1, 3)

        self.assertEqual(SowTransaction.objects.all().count(), 0)
        response = self.client.post('/api/workshopthree/sows/move_many_sows_to_workshop_one/',
            {'sows': [sow1.pk, sow2.pk, sow3.pk]})
        
        self.assertEqual(SowTransaction.objects.all().count(), 3)

    def test_culling_sow(self):
        sow = sows_testing.create_sow_and_put_in_workshop_three(1, 1)
        response = self.client.post('/api/workshopthree/sows/%s/culling_sow/' %
          sow.pk, {'culling_type': 'padej', 'reason': 'xz'})

        self.assertEqual(response.data['sow']['id'], sow.pk)
        self.assertEqual(response.data['sow']['alive'], False)
        self.assertEqual(response.data['culling']['id'], 1)
        self.assertEqual(response.data['culling']['culling_type'], 'padej')
        self.assertEqual(response.data['culling']['reason'], 'xz')
