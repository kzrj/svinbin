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


class WorkShopNomadPigletsViewsTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        locations_testing.create_workshops_sections_and_cells()
        sows_testing.create_statuses()
        piglets_testing.create_piglets_statuses()
        self.user = staff_testing.create_employee()
        self.client.force_authenticate(user=self.user)

    # def test_weighing_piglets(self):
    #     nomad_piglets_group = piglets_testing.create_nomad_group_from_three_new_born()

    #     response = self.client.post('/api/nomadpiglets/%s/weighing_piglets/' %
    #       nomad_piglets_group.pk, {'total_weight': 670, 'place': '3/4'})
    #     self.assertEqual(response.data['piglets_group']['id'], nomad_piglets_group.pk)
    #     self.assertEqual(response.data['piglets_group']['status'], 'Взвешены, готовы к заселению')
    #     self.assertEqual(response.data['weighing_record']['piglets_group'], nomad_piglets_group.pk)
    #     self.assertEqual(response.data['weighing_record']['total_weight'], 670)
    #     self.assertEqual(response.data['weighing_record']['place'], '3/4')

    # def test_get_weighted_piglets_outside_cells(self):
    #     nomad_piglets_group1 = piglets_testing.create_nomad_group_from_three_new_born()
    #     nomad_piglets_group2 = piglets_testing.create_nomad_group_from_three_new_born()
    #     nomad_piglets_group2.location = Location.objects.get(workshop__number=4)
    #     nomad_piglets_group2.save()
    #     nomad_piglets_group3 = piglets_testing.create_nomad_group_from_three_new_born()
    #     nomad_piglets_group3.location = Location.objects.get(workshop__number=4)
    #     nomad_piglets_group3.save()

    #     response = self.client.post('/api/nomadpiglets/%s/weighing_piglets/' %
    #       nomad_piglets_group2.pk, {'total_weight': 670, 'place': '3/4'})
        
    #     response = self.client.get('/api/nomadpiglets/get_weighted_piglets_outside_cells/')
    #     self.assertEqual(response.data['piglets_groups'][0]['id'], nomad_piglets_group2.pk)
    #     self.assertEqual(len(response.data['piglets_groups']), 1)

    # def test_waiting_for_weighing_piglets_outside_cells(self):
    #     nomad_piglets_group1 = piglets_testing.create_nomad_group_from_three_new_born()
    #     nomad_piglets_group1.location = Location.objects.get(workshop__number=4)
    #     nomad_piglets_group1.save()
    #     nomad_piglets_group2 = piglets_testing.create_nomad_group_from_three_new_born()
    #     nomad_piglets_group2.location = Location.objects.get(workshop__number=4)
    #     nomad_piglets_group2.save()
    #     nomad_piglets_group3 = piglets_testing.create_nomad_group_from_three_new_born()
    #     nomad_piglets_group3.location = Location.objects.get(workshop__number=4)
    #     nomad_piglets_group3.reset_status()

    #     response = self.client.post('/api/nomadpiglets/%s/weighing_piglets/' %
    #       nomad_piglets_group2.pk, {'total_weight': 670, 'place': '3/4'})
        
    #     response = self.client.get('/api/nomadpiglets/waiting_for_weighing_piglets_outside_cells/')
    #     self.assertEqual(len(response.data['piglets_groups']), 1)
    #     self.assertEqual(response.data['piglets_groups'][0]['id'], nomad_piglets_group1.pk)

    # def test_move_one_group_to_cell(self):
    #     nomad_piglets_group1 = piglets_testing.create_nomad_group_from_three_new_born()
    #     nomad_piglets_group1.location = Location.objects.get(workshop__number=4)
    #     nomad_piglets_group1.save()
    #     nomad_piglets_group2 = piglets_testing.create_nomad_group_from_three_new_born()
    #     nomad_piglets_group2.location = Location.objects.get(workshop__number=4)
    #     nomad_piglets_group2.save()

    #     cell = PigletsGroupCell.objects.all().first()
    #     location = Location.objects.get(pigletsGroupCell=cell)
    #     self.assertEqual(cell.workshop.number, 4)

    #     # empty cell
    #     response = self.client.post('/api/nomadpiglets/%s/move_one_group_to_cell/' %
    #       nomad_piglets_group1.pk, {'location': location.pk })
    #     self.assertEqual(response.data['piglets_group']['id'], nomad_piglets_group1.pk)
    #     self.assertEqual(response.data['piglets_group']['status'], 'Кормятся')
    #     self.assertEqual(response.data['transaction']['piglets_group'], nomad_piglets_group1.pk)
        
    #     # not empty cell
    #     response = self.client.post('/api/nomadpiglets/%s/move_one_group_to_cell/' %
    #       nomad_piglets_group2.pk, {'location': location.pk })
    #     self.assertEqual(response.data['merged_group']['quantity'],
    #      nomad_piglets_group1.start_quantity + nomad_piglets_group2.start_quantity)

    #     nomad_piglets_group2.refresh_from_db()
    #     nomad_piglets_group1.refresh_from_db()
    #     self.assertEqual(nomad_piglets_group2.active, False)
    #     self.assertEqual(nomad_piglets_group2.status.title, 'Объединены с другой группой')
    #     self.assertEqual(nomad_piglets_group1.active, False)
    #     self.assertEqual(nomad_piglets_group1.status.title, 'Объединены с другой группой')
        
    # def test_move_one_group_to_cell_moving_without_split_to_empty_cell(self):
    #     nomad_piglets_group1 = piglets_testing.create_nomad_group_from_three_new_born()
    #     nomad_piglets_group1.location = Location.objects.get(workshop__number=4)
    #     nomad_piglets_group1.save()

    #     from_cell = PigletsGroupCell.objects.all().first()
    #     from_location = Location.objects.get(pigletsGroupCell=from_cell)
    #     self.assertEqual(from_cell.workshop.number, 4)

    #     to_cell = PigletsGroupCell.objects.all()[1]
    #     to_location = Location.objects.get(pigletsGroupCell=to_cell)
    #     self.assertEqual(to_cell.workshop.number, 4)

    #     response = self.client.post('/api/nomadpiglets/%s/move_one_group_to_cell/' %
    #       nomad_piglets_group1.pk, {'location': from_location.pk })

    #     response = self.client.post('/api/nomadpiglets/move_group_from_cell_to_cell/', 
    #       {'from_location': from_location.pk, 'to_location': to_location.pk, 'quantity': nomad_piglets_group1.quantity })
    #     self.assertEqual(response.data['moving_group']['id'], nomad_piglets_group1.pk)
    #     self.assertEqual(response.data['transaction']['piglets_group'], nomad_piglets_group1.pk)
        
    #     self.assertEqual(response.data['from_location']['id'], from_location.pk)
    #     self.assertEqual(response.data['to_location']['id'], to_location.pk)

    # def test_move_one_group_to_cell_moving_without_split_to_not_empty_cell(self):
    #     from_cell = PigletsGroupCell.objects.all().first()
    #     from_location = Location.objects.get(pigletsGroupCell=from_cell)
    #     nomad_piglets_group1 = piglets_testing.create_nomad_group_from_three_new_born()
    #     nomad_piglets_group1.location = from_location
    #     nomad_piglets_group1.save()

    #     to_cell = PigletsGroupCell.objects.all()[1]
    #     to_location = Location.objects.get(pigletsGroupCell=to_cell)
    #     nomad_piglets_group2 = piglets_testing.create_nomad_group_from_three_new_born()
    #     nomad_piglets_group2.location = to_location
    #     nomad_piglets_group2.save()

    #     response = self.client.post('/api/nomadpiglets/move_group_from_cell_to_cell/', 
    #       {'from_location': from_location.pk, 'to_location': to_location.pk, 'quantity': nomad_piglets_group1.quantity })

    #     self.assertEqual(response.data['moving_group']['id'], nomad_piglets_group1.pk)
    #     self.assertEqual(response.data['merged_group']['quantity'],
    #      nomad_piglets_group1.quantity + nomad_piglets_group2.quantity)

    #     nomad_piglets_group1.refresh_from_db()
    #     nomad_piglets_group2.refresh_from_db()
    #     self.assertEqual(nomad_piglets_group1.active, False)
    #     self.assertEqual(nomad_piglets_group2.active, False)
    #     self.assertEqual(nomad_piglets_group2.quantity, 0)
    #     self.assertEqual(nomad_piglets_group1.status.title, 'Объединены с другой группой')
        
    # def test_move_one_group_to_cell_moving_with_split_to_empty_cell(self):
    #     from_cell = PigletsGroupCell.objects.all().first()
    #     from_location = Location.objects.get(pigletsGroupCell=from_cell)
    #     nomad_piglets_group1 = piglets_testing.create_nomad_group_from_three_new_born()
    #     nomad_piglets_group1.location = from_location
    #     nomad_piglets_group1.save()

    #     to_cell = PigletsGroupCell.objects.all()[1]
    #     to_location = Location.objects.get(pigletsGroupCell=to_cell)

    #     response = self.client.post('/api/nomadpiglets/move_group_from_cell_to_cell/', 
    #       {'from_location': from_location.pk, 'to_location': to_location.pk, 'quantity': 10 })

    #     self.assertEqual(response.data['moving_group']['quantity'], 10)

    #     from_location.refresh_from_db()
    #     from_cell_group = from_location.get_located_active_nomad_groups()[0]
    #     self.assertEqual(from_cell_group.quantity, 27)

    #     to_location.refresh_from_db()
    #     to_cell_group = to_location.get_located_active_nomad_groups()[0]
    #     self.assertEqual(response.data['moving_group']['id'], to_cell_group.pk)

    # def test_move_one_group_to_cell_moving_with_split_to_not_empty_cell(self):
    #     from_cell = PigletsGroupCell.objects.all().first()
    #     from_location = Location.objects.get(pigletsGroupCell=from_cell)
    #     nomad_piglets_group1 = piglets_testing.create_nomad_group_from_three_new_born()
    #     nomad_piglets_group1.location = from_location
    #     nomad_piglets_group1.save()

    #     to_cell = PigletsGroupCell.objects.all()[1]
    #     to_location = Location.objects.get(pigletsGroupCell=to_cell)
    #     nomad_piglets_group2 = piglets_testing.create_nomad_group_from_three_new_born()
    #     nomad_piglets_group2.location = to_location
    #     nomad_piglets_group2.save()

    #     response = self.client.post('/api/nomadpiglets/move_group_from_cell_to_cell/', 
    #       {'from_location': from_location.pk, 'to_location': to_location.pk, 'quantity': 10 })

    #     self.assertEqual(response.data['merged_group']['quantity'], 47)

    # def test_culling_piglets(self):
    #     from_cell = PigletsGroupCell.objects.all().first()
    #     from_location = Location.objects.get(pigletsGroupCell=from_cell)
    #     nomad_piglets_group1 = piglets_testing.create_nomad_group_from_three_new_born()
    #     nomad_piglets_group1.location = from_location
    #     nomad_piglets_group1.save()

    #     response = self.client.post('/api/nomadpiglets/%s/culling_piglets/' %
    #       nomad_piglets_group1.pk, {'culling_type': 'padej', 'reason': 'test reason' })

    #     self.assertEqual(response.data['culling']['culling_type'], 'padej')
    #     self.assertEqual(response.data['culling']['reason'], 'test reason')

    # def test_culling_gilts(self):
    #     from_cell = PigletsGroupCell.objects.all().first()
    #     from_location = Location.objects.get(pigletsGroupCell=from_cell)
    #     nomad_piglets_group1 = piglets_testing.create_nomad_group_from_three_new_born()
    #     nomad_piglets_group1.location = from_location
    #     nomad_piglets_group1.gilts_quantity = 10
    #     nomad_piglets_group1.save()

    #     response = self.client.post('/api/nomadpiglets/%s/culling_gilts/' %
    #       nomad_piglets_group1.pk, {'culling_type': 'padej', 'reason': 'test reason' })

    #     self.assertEqual(response.data['culling']['culling_type'], 'padej')
    #     self.assertEqual(response.data['culling']['reason'], 'test reason')
    #     nomad_piglets_group1.refresh_from_db()
    #     self.assertEqual(nomad_piglets_group1.gilts_quantity, 9)

    # def test_move_to(self):
    #     from_cell = PigletsGroupCell.objects.all().first()
    #     from_location = Location.objects.get(pigletsGroupCell=from_cell)
    #     nomad_piglets_group1 = piglets_testing.create_nomad_group_from_three_new_born()
    #     nomad_piglets_group1.location = from_location
    #     nomad_piglets_group1.save()

    #     to_location = Location.objects.get(workshop__number=8)
    #     response = self.client.post('/api/nomadpiglets/%s/move_to/' %
    #       nomad_piglets_group1.pk, {'to_location': to_location.pk, 'quantity': 10 })
    #     self.assertEqual(response.data['piglets_group']['quantity'], 10)

    def test_serilalizers_fields(self):
        piglets_group1 = piglets_testing.create_new_born_group(1, 10, 1, 10)
        piglets_group2 = piglets_testing.create_new_born_group(1, 11, 1, 12)
        nomad_piglets_group1 = piglets_testing.create_nomad_group_from_three_new_born()

        response = self.client.get('/api/nomadpiglets/%s/' % nomad_piglets_group1.pk)
        # response = self.client.get('/api/nomadpiglets/')
        print(response.data)
        self.assertEqual(len(response.data['cells_numbers_from_merger']), 3)