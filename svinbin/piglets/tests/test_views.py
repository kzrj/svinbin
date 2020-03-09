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

from piglets.models import Piglets
from locations.models import Location
from tours.models import Tour, MetaTour
from piglets_events.models import WeighingPiglets
from sows.models import Sow
from transactions.models import PigletsTransaction, SowTransaction


class PigletsViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        locations_testing.create_workshops_sections_and_cells()
        sows_testing.create_statuses()
        piglets_testing.create_piglets_statuses()
        self.user = staff_testing.create_employee()
        self.client.force_authenticate(user=self.user)

        self.tour1 = Tour.objects.get_or_create_by_week_in_current_year(week_number=1)
        self.tour2 = Tour.objects.get_or_create_by_week_in_current_year(week_number=2)
        self.tour3 = Tour.objects.get_or_create_by_week_in_current_year(week_number=3)
        self.tour4 = Tour.objects.get_or_create_by_week_in_current_year(week_number=4)
        self.loc_ws3 = Location.objects.get(workshop__number=3)
        self.loc_ws3_sec1 = Location.objects.get(section__workshop__number=3, section__number=1)
        self.loc_ws3_sec2 = Location.objects.get(section__workshop__number=3, section__number=2)

        self.loc_ws4 = Location.objects.get(workshop__number=4)
        self.loc_ws4_cell1 = Location.objects.filter(pigletsGroupCell__isnull=False)[0]
        self.loc_ws4_cell2 = Location.objects.filter(pigletsGroupCell__isnull=False)[1]

    def test_create_from_merging_list(self):
        piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws3_sec1, 10)
        piglets2 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws3_sec1, 10)
        piglets3 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws3_sec1, 10)

        response = self.client.post('/api/piglets/create_from_merging_list_and_move_to_ws4/', \
            {'records': [
                {'piglets_id': piglets1.pk, 'quantity': piglets1.quantity, 'changed': False, 
                    'gilts_contains': False},
                {'piglets_id': piglets2.pk, 'quantity': piglets2.quantity, 'changed': False, 
                    'gilts_contains': False}
                ],
            },
            format='json')
        self.assertEqual(response.data['message'], 'Партия создана и перемещена в Цех4.')

    def test_create_from_merging_list_v2(self):
        # with gilts
        piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws3_sec1, 10)
        piglets1.add_gilts_without_increase_quantity(2)
        piglets2 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws3_sec1, 10)
        piglets2.add_gilts_without_increase_quantity(2)
        piglets3 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws3_sec1, 10)
        piglets3.add_gilts_without_increase_quantity(2)

        response = self.client.post('/api/piglets/create_from_merging_list_and_move_to_ws4/', \
            {'records': [
                {'piglets_id': piglets1.pk, 'quantity': 8, 'changed': True, 
                    'gilts_contains': True},
                {'piglets_id': piglets2.pk, 'quantity': piglets2.quantity, 'changed': False, 
                    'gilts_contains': False}
                ],
            },
            format='json')
        self.assertEqual(response.data['message'], 'Партия создана и перемещена в Цех4.')

    def test_create_from_merging_list_transfer_part_number(self):
        piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws3_sec1, 10)
        piglets2 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws3_sec1, 10)

        response = self.client.post('/api/piglets/create_from_merging_list_and_move_to_ws4/', \
            {'records': [
                {'piglets_id': piglets1.pk, 'quantity': piglets1.quantity, 'changed': False, 
                    'gilts_contains': False},
                {'piglets_id': piglets2.pk, 'quantity': piglets2.quantity, 'changed': False, 
                    'gilts_contains': False}
                ],
             'transfer_part_number': 1
            },
            format='json')

        self.assertNotEqual(Piglets.objects.filter(transfer_part_number=1).first(), None)

    def test_culling(self):
        piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws3_sec1, 10)

        response = self.client.post('/api/piglets/%s/culling/' % piglets1.pk, \
            {'culling_type': 'padej', 'reason': 'xz', 'quantity': 2, 'total_weight': 20})

        self.assertEqual(response.data['message'], 'Выбраковка прошла успешно.')


    def test_weighing_piglets(self):
        piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws3_sec1, 10)

        response = self.client.post('/api/piglets/%s/weighing_piglets/' %
          piglets1.pk, {'total_weight': 670, 'place': '3/4'})
        self.assertEqual(response.data['weighing_record']['piglets_group'], piglets1.pk)
        self.assertEqual(response.data['weighing_record']['total_weight'], 670)
        self.assertEqual(response.data['weighing_record']['place'], '3/4')

        piglets1.refresh_from_db()
        self.assertEqual(piglets1.status.title, 'Взвешены, готовы к заселению')

    def test_move_piglets_v1(self):
        # simple move
        piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws3_sec1, 10)

        response = self.client.post('/api/piglets/%s/move_piglets/' %
          piglets1.pk, {'to_location': self.loc_ws4.pk })

        self.assertEqual(response.data['message'], 'Перевод прошел успешно.')

    def test_move_piglets_v2(self):
        # transaction with split
        piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws3_sec1, 10)

        response = self.client.post('/api/piglets/%s/move_piglets/' %
          piglets1.pk, {'to_location': self.loc_ws4.pk, 'new_amount': 3 })

        self.assertEqual(response.data['message'], 'Перевод прошел успешно.')

    def test_move_piglets_v3(self):
        # transaction with merge
        piglets = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws3, 10)

        piglets_in_cell = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws4_cell1, 10)

        response = self.client.post('/api/piglets/%s/move_piglets/' %
          piglets.pk, {'to_location': self.loc_ws4.pk, 'merge': True })

        self.assertEqual(response.data['message'], 'Перевод прошел успешно.')

    def test_move_piglets_v4(self):
        # transaction with merge and spli
        piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws3, 10)

        piglets_in_cell = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws4_cell1, 10)

        response = self.client.post('/api/piglets/%s/move_piglets/' %
          piglets1.pk, {'to_location': self.loc_ws4.pk, 'merge': True, 'new_amount': 3 })

        self.assertEqual(response.data['message'], 'Перевод прошел успешно.')

    def test_move_piglets_v5(self):
        # transaction with  split + gilts
        piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws3, 10)
        piglets1.add_gilts_without_increase_quantity(2)

        # piglets_in_cell = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
        #     self.loc_ws4_cell1, 10)
        # piglets2.add_gilts_without_increase_quantity(2)

        response = self.client.post('/api/piglets/%s/move_piglets/' %
          piglets1.pk, {'to_location': self.loc_ws4.pk, 'merge': True, 'new_amount': 3,
           'gilts_contains': True })

        piglets1.refresh_from_db()
        self.assertEqual(piglets1.active, False)
        piglets1.split_as_parent

        self.assertEqual(response.data['message'], 'Перевод прошел успешно.')

    def test_weighing_piglets_split_return(self):
        piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws3, 10)

        piglets2 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws4, 10)

        response = self.client.post('/api/piglets/%s/weighing_piglets_split_return/' %
          piglets2.pk, {'to_location': self.loc_ws3.pk, 'new_amount': 8, 'total_weight': 80,
           'place': '3/4' })

        self.assertEqual(response.data['message'],
             'Взвешивание прошло успешно. Возврат поросят прошел успешно.')

    def test_move_gilts_to_ws1(self):
        gilts_piglets = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws4, 10)
        loc1 = Location.objects.get(workshop__number=1)

        response = self.client.post('/api/piglets/%s/move_gilts_to_ws1/' % gilts_piglets.pk, 
            {'to_location': loc1.pk})

        gilts_piglets.refresh_from_db()
        self.assertEqual(gilts_piglets.active, False)
        self.assertEqual(Sow.objects.filter(farm_id__isnull=True).count(), 10)

        gilts_piglets2 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws4, 10)
        response = self.client.post('/api/piglets/%s/move_gilts_to_ws1/' % gilts_piglets2.pk, 
            {'to_location': loc1.pk, 'new_amount': 5})

        gilts_piglets2.refresh_from_db()
        self.assertEqual(gilts_piglets2.active, False)
        self.assertEqual(Sow.objects.filter(farm_id__isnull=True).count(), 15)

    def test_merge_init_list_and_move_merged_to_ws4(self):
        response = self.client.post('/api/piglets/merge_init_list_and_move_merged_to_ws4/', \
            {'records': [
                {'week': 9, 'quantity': 60 },
                {'week': 8, 'quantity': 40 },
                ],
             'transfer_part_number': 1
            },
            format='json')
        self.assertEqual(response.data['message'], 'Партия создана и перемещена в Цех4.')

    def test_recount_and_weighing_piglets(self):
        tour = Tour.objects.get_or_create_by_week_in_current_year(1)
        tour2 = Tour.objects.get_or_create_by_week_in_current_year(2)
        location = Location.objects.get(section__number=1, section__workshop__number=3)
        piglets = Piglets.objects.create(location=location, quantity=100, start_quantity=100,
            gilts_quantity=0, status=None)
        meta_tour = MetaTour.objects.create(piglets=piglets)

        record1 = meta_tour.records.create_record(meta_tour, tour, 60, piglets.quantity)
        record2 = meta_tour.records.create_record(meta_tour, tour2, 40, piglets.quantity)

        response = self.client.post('/api/piglets/%s/recount_and_weighing_piglets/' % piglets.pk, 
            {'new_quantity': 110, 'total_weight': 500, 'place': '3/4'})
        self.assertEqual(response.data['message'], 'Взвешивание прошло успешно.')
        
        piglets.refresh_from_db()
        self.assertEqual(piglets.quantity, 110)

        response = self.client.post('/api/piglets/%s/recount_and_weighing_piglets/' % piglets.pk, 
            {'total_weight': 580, 'place': '3/4'})
        self.assertEqual(response.data['message'], 'Взвешивание прошло успешно.')

    def test_init_piglets_from_farrow(self):
        location = Location.objects.get(workshop__number=4)
        from_location = Location.objects.get(workshop__number=3)
        response = self.client.post('/api/piglets/init_piglets_from_farrow/', 
            {
                'farrow_date': '1-03-2020', 'location': location.pk, 'quantity': 102,
                'from_location': from_location.pk, 'transaction_date': '9-03-2020',
            })
        self.assertEqual(response.data['message'], 'Свиньи успешно созданы.')
        self.assertEqual(Piglets.objects.filter(quantity=102, location=location).count(), 1)
        transaction = PigletsTransaction.objects.all().first()

        self.assertEqual(transaction.piglets_group.quantity, 102)
        self.assertEqual(transaction.from_location, from_location)
        self.assertEqual(transaction.to_location, location)

    def test_recount_piglets(self):
        tour = Tour.objects.get_or_create_by_week_in_current_year(1)
        tour2 = Tour.objects.get_or_create_by_week_in_current_year(2)
        location = Location.objects.get(section__number=1, section__workshop__number=3)
        piglets = Piglets.objects.create(location=location, quantity=100, start_quantity=100,
            gilts_quantity=0, status=None)
        meta_tour = MetaTour.objects.create(piglets=piglets)

        record1 = meta_tour.records.create_record(meta_tour, tour, 60, piglets.quantity)
        record2 = meta_tour.records.create_record(meta_tour, tour2, 40, piglets.quantity)

        response = self.client.post('/api/piglets/%s/recount_piglets/' % piglets.pk, 
            {'new_quantity': 105, 'comment': 'xz'})
        self.assertEqual(response.data['message'], 'Пересчет прошел успешно.')

        response = self.client.post('/api/piglets/%s/recount_piglets/' % piglets.pk, 
            {'new_quantity': 106,})
        self.assertEqual(response.data['message'], 'Пересчет прошел успешно.')


class PigletsFilterTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        locations_testing.create_workshops_sections_and_cells()
        sows_testing.create_statuses()
        piglets_testing.create_piglets_statuses()
        self.user = staff_testing.create_employee()
        self.client.force_authenticate(user=self.user)

        self.tour1 = Tour.objects.get_or_create_by_week_in_current_year(week_number=1)
        self.tour2 = Tour.objects.get_or_create_by_week_in_current_year(week_number=2)
        self.tour3 = Tour.objects.get_or_create_by_week_in_current_year(week_number=3)
        self.tour4 = Tour.objects.get_or_create_by_week_in_current_year(week_number=4)
        self.loc_ws3 = Location.objects.get(workshop__number=3)
        self.loc_ws3_sec1 = Location.objects.get(section__workshop__number=3, section__number=1)
        self.loc_ws3_sec2 = Location.objects.get(section__workshop__number=3, section__number=2)

        self.loc_ws4 = Location.objects.get(workshop__number=4)
        self.loc_ws4_cell1 = Location.objects.filter(pigletsGroupCell__isnull=False)[0]
        self.loc_ws4_cell2 = Location.objects.filter(pigletsGroupCell__isnull=False)[1]

    def test_filter_piglets_without_weighing_record(self):
        piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws4, 10)

        piglets2 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws4, 10)

        WeighingPiglets.objects.create_weighing(piglets1, 240, '3/4')

        response = self.client.get('/api/piglets/?piglets_without_weighing_record=3/4')
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['id'], piglets2.pk)

        response = self.client.get('/api/piglets/?piglets_with_weighing_record=3/4')
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['id'], piglets1.pk)
