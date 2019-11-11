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

from sows.models import Gilt
from piglets.models import NewBornPigletsGroup, NomadPigletsGroup
from piglets_events.models import NewBornPigletsGroupRecount, NewBornPigletsMerger, CullingNewBornPiglets
from locations.models import WorkShop, SowAndPigletsCell, Location
from transactions.models import PigletsTransaction, SowTransaction
from tours.models import Tour


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

    def test_create_gilt(self):
        newBornPigletsGroup1 = piglets_testing.create_new_born_group(section_number=1, cell_number=3)
        response = self.client.post('/api/workshopthree/newbornpiglets/%s/create_gilt/'
             % newBornPigletsGroup1.pk, {'birth_id': 1})
        gilt = Gilt.objects.filter(birth_id=1).first()
        self.assertEqual(response.data['gilt']['id'], gilt.pk)

        # response = self.client.post('/api/workshopthree/newbornpiglets/%s/create_gilt/'
        #      % newBornPigletsGroup1.pk, {'birth_id': 1})
        # self.assertEqual(response.status_code, 400)

        # response = self.client.post('/api/workshopthree/newbornpiglets/%s/create_gilt/'
        #      % newBornPigletsGroup1.pk, {'birth_id': gilt.mother_sow.pk})
        # self.assertEqual(response.status_code, 400)

    def test_recount(self):
        newBornPigletsGroup1 = piglets_testing.create_new_born_group(section_number=1,
            cell_number=3, quantity=10)
        response = self.client.post('/api/workshopthree/newbornpiglets/%s/recount/'
             % newBornPigletsGroup1.pk, {'quantity': 11})
        self.assertEqual(response.data['recount']['balance'], 1)
        

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
        self.assertEqual(response.data['sow']['tour'], 'Тур 7 2019г')
        self.assertEqual(response.data['sow']['status'], 'Опоросилась')
        self.assertEqual(response.data['farrow']['alive_quantity'], 10)
        self.assertEqual(response.data['farrow']['dead_quantity'], 1)
        self.assertEqual(response.data['farrow']['mummy_quantity'], 2)

    def test_mark_as_nurse_without_creating_piglets(self):
        sow = sows_testing.create_sow_and_put_in_workshop_three(section_number=1, cell_number=1)
        response = self.client.post('/api/workshopthree/sows/%s/mark_as_nurse/' % sow.pk)
        sow.refresh_from_db()
        self.assertEqual(sow.status.title, 'Кормилица')
        self.assertEqual(response.data['message'], 'Свинья почемена как кормилица.')

    def test_mark_as_nurse_creating_piglets(self):
        sow = sows_testing.create_sow_and_put_in_workshop_three(section_number=1, cell_number=1)
        tour = Tour.objects.get_or_create_by_week_in_current_year(45)
        response = self.client.post('/api/workshopthree/sows/%s/mark_as_nurse/' % sow.pk,
            {'piglets_tour': tour.pk})
        self.assertEqual(response.data['message'], 'Свинья почемена как кормилица. Создана группа поросят.')


class WorkshopThreeInfoViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        locations_testing.create_workshops_sections_and_cells()
        sows_testing.create_statuses()
        self.user = staff_testing.create_employee()
        self.client.force_authenticate(user=self.user)

    def test_info(self):
        sow1 = sows_testing.create_sow_with_semination_and_put_in_workshop_three(section_number=1,
         cell_number=1, week=7)
        sow2 = sows_testing.create_sow_with_semination_and_put_in_workshop_three(section_number=1,
         cell_number=2, week=7)
        sow3 = sows_testing.create_sow_with_semination_and_put_in_workshop_three(section_number=1,
         cell_number=3, week=7)

        response = self.client.post('/api/workshopthree/sows/%s/sow_farrow/' %
          sow1.pk, {'alive_quantity': 10, 'dead_quantity': 1, 'mummy_quantity': 2, 'week': 7 })
        response = self.client.post('/api/workshopthree/sows/%s/sow_farrow/' %
          sow2.pk, {'alive_quantity': 15, 'dead_quantity': 1, 'mummy_quantity': 2, 'week': 7 })

        response = self.client.get('/api/workshopthree/wsinfo/info/')
        self.assertEqual('Цех' in response.data.keys(), True)
        self.assertEqual('1' in response.data.keys(), True)
        self.assertEqual('2' in response.data.keys(), True)
        self.assertEqual('3' in response.data.keys(), True)
        self.assertEqual('4' in response.data.keys(), True)
        self.assertEqual('5' in response.data.keys(), True)
        self.assertEqual('6' in response.data.keys(), True)

    def test_balances_by_tours(self):
        # create newborngroups tour=1, qnty=10
        for cell_number in range(1, 11):
            piglets_testing.create_new_born_group(section_number=1, cell_number=cell_number,
                week=1, quantity=10)
        piglets_group_qs = NewBornPigletsGroup.objects.all()

        # get 1 piglet from every group. recount -1. negative recount
        for nbgroup in piglets_group_qs:
            NewBornPigletsGroupRecount.objects.create_recount(nbgroup, 9)

        # add 1 piglet to every group. recount +1. positive recount
        for nbgroup in piglets_group_qs:
            NewBornPigletsGroupRecount.objects.create_recount(nbgroup, 10)

        # add another tour
        # create newborngroups tour=1, qnty=10
        for cell_number in range(1, 11):
            piglets_testing.create_new_born_group(section_number=2, cell_number=cell_number,
                week=2, quantity=10)
        piglets_group_qs = NewBornPigletsGroup.objects.filter(tour__week_number=2)

        # get 1 piglet from every group. recount -1. negative recount
        for nbgroup in piglets_group_qs:
            NewBornPigletsGroupRecount.objects.create_recount(nbgroup, 8)

        # add 1 piglet to every group. recount +1. positive recount
        for nbgroup in piglets_group_qs:
            NewBornPigletsGroupRecount.objects.create_recount(nbgroup, 12)

        response = self.client.get('/api/workshopthree/wsinfo/balances_by_tours/')
        self.assertEqual('Тур 1 2019г' in response.data.keys(), True)
        self.assertEqual('Тур 2 2019г' in response.data.keys(), True)