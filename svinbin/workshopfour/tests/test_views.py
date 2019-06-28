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

from piglets.models import NewBornPigletsGroup, NomadPigletsGroup
from piglets_events.models import NewBornPigletsGroupRecount, NewBornPigletsMerger, CullingNewBornPiglets
from locations.models import WorkShop, SowAndPigletsCell, PigletsGroupCell, Location
from transactions.models import PigletsTransaction, SowTransaction


class WorkshopFourPigletsViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        locations_testing.create_workshops_sections_and_cells()
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

    def test_move_one_group_to_cell(self):
        nomad_piglets_group1 = piglets_testing.create_nomad_group_from_three_new_born()
        nomad_piglets_group1.location = Location.objects.create_location(WorkShop.objects.get(number=4))
        nomad_piglets_group1.save()
        nomad_piglets_group2 = piglets_testing.create_nomad_group_from_three_new_born()
        nomad_piglets_group2.location = Location.objects.create_location(WorkShop.objects.get(number=4))
        nomad_piglets_group2.save()

        cell = PigletsGroupCell.objects.all().first()
        self.assertEqual(cell.workshop.number, 4)

        # empty cell
        response = self.client.post('/api/workshopfour/piglets/%s/move_one_group_to_cell/' %
          nomad_piglets_group1.pk, {'cell': cell.pk })
        self.assertEqual(response.data['piglets_group']['id'], nomad_piglets_group1.pk)
        self.assertEqual(response.data['piglets_group']['status'], 'Кормятся')
        self.assertEqual(response.data['transaction']['piglets_group'], nomad_piglets_group1.pk)
        
        # not empty cell
        response = self.client.post('/api/workshopfour/piglets/%s/move_one_group_to_cell/' %
          nomad_piglets_group2.pk, {'cell': cell.pk })
        self.assertEqual(response.data['merged_group']['quantity'],
         nomad_piglets_group1.start_quantity + nomad_piglets_group2.start_quantity)

        nomad_piglets_group2.refresh_from_db()
        nomad_piglets_group1.refresh_from_db()
        self.assertEqual(nomad_piglets_group2.active, False)
        self.assertEqual(nomad_piglets_group2.status.title, 'Объединены с другой группой')
        self.assertEqual(nomad_piglets_group1.active, False)
        self.assertEqual(nomad_piglets_group1.status.title, 'Объединены с другой группой')
        
    def test_move_one_group_to_cell_moving_without_split_to_empty_cell(self):
        nomad_piglets_group1 = piglets_testing.create_nomad_group_from_three_new_born()
        nomad_piglets_group1.location = Location.objects.create_location(WorkShop.objects.get(number=4))
        nomad_piglets_group1.save()

        from_cell = PigletsGroupCell.objects.all().first()
        self.assertEqual(from_cell.workshop.number, 4)

        to_cell = PigletsGroupCell.objects.all()[1]
        self.assertEqual(to_cell.workshop.number, 4)

        response = self.client.post('/api/workshopfour/piglets/%s/move_one_group_to_cell/' %
          nomad_piglets_group1.pk, {'cell': from_cell.pk })

        response = self.client.post('/api/workshopfour/piglets/move_group_from_cell_to_cell/', 
          {'from_cell': from_cell.pk, 'to_cell': to_cell.pk, 'quantity': nomad_piglets_group1.quantity })
        self.assertEqual(response.data['moving_group']['id'], nomad_piglets_group1.pk)
        self.assertEqual(response.data['transaction']['piglets_group'], nomad_piglets_group1.pk)
        self.assertEqual(response.data['from_cell']['locations'], ['No group'])
        self.assertEqual(response.data['to_cell']['locations'][0]['id'], nomad_piglets_group1.pk)

    def test_move_one_group_to_cell_moving_without_split_to_not_empty_cell(self):
        from_cell = PigletsGroupCell.objects.all().first()
        nomad_piglets_group1 = piglets_testing.create_nomad_group_from_three_new_born()
        nomad_piglets_group1.location = Location.objects.create_location(from_cell)
        nomad_piglets_group1.save()

        to_cell = PigletsGroupCell.objects.all()[1]
        nomad_piglets_group2 = piglets_testing.create_nomad_group_from_three_new_born()
        nomad_piglets_group2.location = Location.objects.create_location(to_cell)
        nomad_piglets_group2.save()

        response = self.client.post('/api/workshopfour/piglets/move_group_from_cell_to_cell/', 
          {'from_cell': from_cell.pk, 'to_cell': to_cell.pk, 'quantity': nomad_piglets_group1.quantity })

        self.assertEqual(response.data['moving_group']['id'], nomad_piglets_group1.pk)
        self.assertEqual(response.data['merged_group']['quantity'],
         nomad_piglets_group1.quantity + nomad_piglets_group2.quantity)

        nomad_piglets_group1.refresh_from_db()
        nomad_piglets_group2.refresh_from_db()
        self.assertEqual(nomad_piglets_group1.active, False)
        self.assertEqual(nomad_piglets_group2.active, False)
        self.assertEqual(nomad_piglets_group2.quantity, 0)
        self.assertEqual(nomad_piglets_group1.status.title, 'Объединены с другой группой')
        
    def test_move_one_group_to_cell_moving_with_split_to_empty_cell(self):
        from_cell = PigletsGroupCell.objects.all().first()
        nomad_piglets_group1 = piglets_testing.create_nomad_group_from_three_new_born()
        nomad_piglets_group1.location = Location.objects.create_location(from_cell)
        nomad_piglets_group1.save()

        to_cell = PigletsGroupCell.objects.all()[1]

        response = self.client.post('/api/workshopfour/piglets/move_group_from_cell_to_cell/', 
          {'from_cell': from_cell.pk, 'to_cell': to_cell.pk, 'quantity': 10 })

        self.assertEqual(response.data['moving_group']['quantity'], 10)

        from_cell.refresh_from_db()
        from_cell_group = from_cell.get_list_of_residents()[0]
        self.assertEqual(from_cell_group.quantity, 27)

        to_cell.refresh_from_db()
        to_cell_group = to_cell.get_list_of_residents()[0]
        self.assertEqual(response.data['moving_group']['id'], to_cell_group.pk)

    def test_move_one_group_to_cell_moving_with_split_to_not_empty_cell(self):
        from_cell = PigletsGroupCell.objects.all().first()
        nomad_piglets_group1 = piglets_testing.create_nomad_group_from_three_new_born()
        nomad_piglets_group1.location = Location.objects.create_location(from_cell)
        nomad_piglets_group1.save()

        to_cell = PigletsGroupCell.objects.all()[1]
        nomad_piglets_group2 = piglets_testing.create_nomad_group_from_three_new_born()
        nomad_piglets_group2.location = Location.objects.create_location(to_cell)
        nomad_piglets_group2.save()

        response = self.client.post('/api/workshopfour/piglets/move_group_from_cell_to_cell/', 
          {'from_cell': from_cell.pk, 'to_cell': to_cell.pk, 'quantity': 10 })

        print(response.data)



