# -*- coding: utf-8 -*-
import datetime
import random

from django.contrib.auth.models import User

from rest_framework.test import APIClient
from rest_framework.test import APITestCase

import workshops.testing_utils as workshops_testing
import sows.testing_utils as sows_testing
import piglets.testing_utils as piglets_testing

from piglets.models import NewBornPigletsGroup, NomadPigletsGroup
from piglets_events.models import NewBornPigletsGroupRecount, NewBornPigletsMerger, CullingNewBornPiglets
from workshops.models import WorkShop
from transactions.models import PigletsTransaction


class WorkshopThreeViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        workshops_testing.create_workshops_sections_and_cells()
        sows_testing.create_statuses()

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

    def test_mark_to_transfer_mark_size_and_recount_without_recount(self):
        newBornPigletsGroup1 = piglets_testing.create_new_born_group()
        newBornPigletsGroup2 = piglets_testing.create_new_born_group(section_number=1, cell_number=3)
        self.assertEqual(newBornPigletsGroup2.location.sowAndPigletsCell.number, '3')

        response = self.client.post('/api/workshopthree/piglets/create_nomad_group_from_merge_and_transfer_to_weight/',
         {'piglets_groups': [newBornPigletsGroup1.pk, newBornPigletsGroup2.pk]})

        nomad_group = NomadPigletsGroup.objects.filter(pk=response.data['nomad_group']['id']).first()
        self.assertNotEqual(nomad_group, None)
        self.assertEqual(nomad_group.location.get_location, WorkShop.objects.get(number=11))

        new_born_merger = NewBornPigletsMerger.objects.filter(nomad_group=nomad_group).first()
        self.assertNotEqual(new_born_merger, None)
        self.assertEqual(new_born_merger.piglets_groups.all()[0], newBornPigletsGroup1)
        self.assertEqual(new_born_merger.piglets_groups.all()[1], newBornPigletsGroup2)

        transaction = nomad_group.transactions.all().first()
        self.assertNotEqual(transaction, None)
        self.assertEqual(transaction.from_location.get_location, WorkShop.objects.get(number=3))
        self.assertEqual(transaction.to_location.get_location, WorkShop.objects.get(number=11))


    def test_culling_piglets(self):
        newBornPigletsGroup = piglets_testing.create_new_born_group()
        response = self.client.post('/api/workshopthree/piglets/%s/culling_piglets/' %
          newBornPigletsGroup.pk, {'culling_type': 'padej', 'reason': 'xz'})
        
        culling = CullingNewBornPiglets.objects.filter(piglets_group=newBornPigletsGroup).first()
        self.assertNotEqual(culling, None)
        self.assertEqual(culling.reason, 'xz')
        self.assertEqual(culling.culling_type, 'padej')

