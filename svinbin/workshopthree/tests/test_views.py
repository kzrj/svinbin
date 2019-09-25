# -*- coding: utf-8 -*-
import datetime
import random

from django.contrib.auth.models import User

from rest_framework.test import APIClient
from rest_framework.test import APITestCase

import locations.testing_utils as locations_testing
import sows.testing_utils as sows_testing
import piglets.testing_utils as piglets_testing
import staff.testing_utils as staff_testing

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
        self.user = staff_testing.create_employee()
        self.client.force_authenticate(user=self.user)

    def test_culling_piglets(self):
        newBornPigletsGroup = piglets_testing.create_new_born_group()
        response = self.client.post('/api/workshopthree/newbornpiglets/%s/culling_piglets/' %
          newBornPigletsGroup.pk, {'culling_type': 'padej', 'reason': 'xz'})
        
        culling = CullingNewBornPiglets.objects.filter(piglets_group=newBornPigletsGroup).first()
        self.assertNotEqual(culling, None)
        self.assertEqual(culling.reason, 'xz')
        self.assertEqual(culling.culling_type, 'padej')

    def test_culling_piglets_gilt(self):
        newBornPigletsGroup = piglets_testing.create_new_born_group()        
        newBornPigletsGroup.add_gilts_increase_quantity(2)
        self.assertEqual(newBornPigletsGroup.quantity, 12)
        self.assertEqual(newBornPigletsGroup.gilts_quantity, 2)
        qty = newBornPigletsGroup.quantity
        gilts_qty = newBornPigletsGroup.quantity
        response = self.client.post('/api/workshopthree/newbornpiglets/%s/culling_gilts/' %
          newBornPigletsGroup.pk, {'culling_type': 'padej', 'reason': 'xz'})
        
        culling = CullingNewBornPiglets.objects.filter(piglets_group=newBornPigletsGroup).first()
        self.assertNotEqual(culling, None)
        self.assertEqual(culling.reason, 'xz')
        self.assertEqual(culling.culling_type, 'padej')
        newBornPigletsGroup.refresh_from_db()
        self.assertEqual(newBornPigletsGroup.quantity, 11)
        self.assertEqual(newBornPigletsGroup.gilts_quantity, 1)

    def test_create_nomad_group_from_merge(self):
        newBornPigletsGroup1 = piglets_testing.create_new_born_group()
        newBornPigletsGroup2 = piglets_testing.create_new_born_group(section_number=1, cell_number=3)
        self.assertEqual(newBornPigletsGroup2.location.sowAndPigletsCell.number, '3')

        response = self.client.post('/api/workshopthree/newbornpiglets/create_nomad_group_from_merge/',
         {'piglets_groups': [newBornPigletsGroup1.pk, newBornPigletsGroup2.pk], 'part_number': 1})

        nomad_group = NomadPigletsGroup.objects.filter(pk=response.data['nomad_group']['id']).first()
        self.assertNotEqual(nomad_group, None)
        self.assertEqual(nomad_group.location.get_location, WorkShop.objects.get(number=3))

        new_born_merger = NewBornPigletsMerger.objects.filter(nomad_group=nomad_group).first()
        self.assertNotEqual(new_born_merger, None)
        self.assertEqual(new_born_merger.part_number, 1)


class WorkshopThreeSowsViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        locations_testing.create_workshops_sections_and_cells()
        sows_testing.create_statuses()
        self.user = staff_testing.create_employee()
        self.client.force_authenticate(user=self.user)

    def test_sow_farrow(self):
        sow = sows_testing.create_sow_with_semination_and_put_in_workshop_three(section_number=1,
         cell_number=1, week=7)
        response = self.client.post('/api/workshopthree/sows/%s/sow_farrow/' %
          sow.pk, {'alive_quantity': 10, 'dead_quantity': 1, 'mummy_quantity': 2, 'week': 7 })

        self.assertEqual(response.data['sow']['id'], sow.pk)
        self.assertEqual(response.data['sow']['farm_id'], sow.farm_id)
        self.assertEqual(response.data['sow']['tour'], 'Tour #7')
        self.assertEqual(response.data['sow']['status'], 'Опоросилась')
        self.assertEqual(response.data['farrow']['alive_quantity'], 10)
        self.assertEqual(response.data['farrow']['dead_quantity'], 1)
        self.assertEqual(response.data['farrow']['mummy_quantity'], 2)