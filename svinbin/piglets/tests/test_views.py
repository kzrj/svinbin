# -*- coding: utf-8 -*-
import datetime
import random

from django.contrib.auth.models import User
from django.db import connection

from rest_framework.test import APIClient
from rest_framework.test import APITestCase

import locations.testing_utils as locations_testing
import sows.testing_utils as sows_testing
import sows_events.utils as sows_events_testings
import piglets.testing_utils as piglets_testing
import staff.testing_utils as staff_testing

from piglets.models import Piglets
from locations.models import Location
from tours.models import Tour, MetaTour
from piglets_events.models import WeighingPiglets
from sows.models import Sow
from sows_events.models import SowFarrow
from transactions.models import PigletsTransaction, SowTransaction
from veterinary.models import PigletsVetEvent, Recipe


class PigletsViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        locations_testing.create_workshops_sections_and_cells()
        sows_testing.create_statuses()
        piglets_testing.create_piglets_statuses()
        sows_events_testings.create_types()
        staff_testing.create_svinbin_users()

        self.tour1 = Tour.objects.get_or_create_by_week_in_current_year(week_number=1)
        self.tour2 = Tour.objects.get_or_create_by_week_in_current_year(week_number=2)
        self.tour3 = Tour.objects.get_or_create_by_week_in_current_year(week_number=3)
        self.tour4 = Tour.objects.get_or_create_by_week_in_current_year(week_number=4)

        self.loc_ws1 = Location.objects.get(workshop__number=1)
        self.loc_ws2 = Location.objects.get(workshop__number=2)

        self.loc_ws3 = Location.objects.get(workshop__number=3)
        self.loc_ws3_sec1 = Location.objects.get(section__workshop__number=3, section__number=1)
        self.loc_ws3_sec2 = Location.objects.get(section__workshop__number=3, section__number=2)

        self.loc_ws4 = Location.objects.get(workshop__number=4)
        self.loc_ws4_cell1 = Location.objects.filter(pigletsGroupCell__isnull=False)[0]
        self.loc_ws4_cell2 = Location.objects.filter(pigletsGroupCell__isnull=False)[1]

        self.loc_ws8 = Location.objects.get(workshop__number=8)

        self.loc_ws5 = Location.objects.get(workshop__number=5)
        self.loc_ws6 = Location.objects.get(workshop__number=6)
        self.loc_ws7 = Location.objects.get(workshop__number=7)

        # self.user = staff_testing.create_employee()
        # self.client.force_authenticate(user=self.user)

        self.brig1 = User.objects.get(username='brigadir1')
        self.brig2 = User.objects.get(username='brigadir2')
        self.brig3 = User.objects.get(username='brigadir3')
        self.brig4 = User.objects.get(username='brigadir4')
        self.brig5 = User.objects.get(username='brigadir5')
        self.brig6 = User.objects.get(username='brigadir6')
        self.brig7 = User.objects.get(username='brigadir7')
        self.brig8 = User.objects.get(username='brigadir8')

        self.admin = User.objects.get(username='test_admin1')
        self.shmigina = User.objects.get(username='shmigina')
        self.veterinar = User.objects.get(username='veterinar')

    def test_create_from_merging_list(self):
        self.client.force_authenticate(user=self.brig3)
        piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws3_sec1, 10)
        piglets2 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws3_sec1, 10)
        piglets3 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws3_sec1, 10)

        response = self.client.post('/api/piglets/create_from_merging_list_and_move_to_ws4/', \
            {'records': [
                {'piglets_id': piglets1.pk, 'quantity': piglets1.quantity, 'changed': False },
                {'piglets_id': piglets2.pk, 'quantity': piglets2.quantity, 'changed': False }
                ],
            },
            format='json')
        self.assertEqual(response.data['message'], 'Партия создана и перемещена в Цех4.')
        self.client.logout()

    def test_create_from_merging_list_v2(self):
        # with gilts
        self.client.force_authenticate(user=self.brig3)
        piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws3_sec1, 10)
        piglets2 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws3_sec1, 10)
        piglets3 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws3_sec1, 10)

        response = self.client.post('/api/piglets/create_from_merging_list_and_move_to_ws4/', \
            {'records': [
                {'piglets_id': piglets1.pk, 'quantity': 8, 'changed': True },
                {'piglets_id': piglets2.pk, 'quantity': piglets2.quantity, 'changed': False }
                ],
            },
            format='json')
        self.assertEqual(response.data['message'], 'Партия создана и перемещена в Цех4.')
        self.client.logout()

    def test_create_from_merging_list_permissions(self):
        self.client.force_authenticate(user=self.brig1)
        piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws3_sec1, 10)
        piglets2 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws3_sec1, 10)
        piglets3 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws3_sec1, 10)

        response = self.client.post('/api/piglets/create_from_merging_list_and_move_to_ws4/', \
            {'records': [
                {'piglets_id': piglets1.pk, 'quantity': piglets1.quantity, 'changed': False },
                {'piglets_id': piglets2.pk, 'quantity': piglets2.quantity, 'changed': False }
                ],
            },
            format='json')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data['message'], 'Ошибка доступа. У вас нет прав.')
        self.client.logout()

        response = self.client.post(
            '/api/piglets/create_from_merging_list_and_move_to_ws4/', format='json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['message'], 'Ошибка доступа. Вы не авторизованы')

        self.client.force_authenticate(self.admin)
        response = self.client.post('/api/piglets/create_from_merging_list_and_move_to_ws4/', \
            {'records': [
                {'piglets_id': piglets1.pk, 'quantity': piglets1.quantity, 'changed': False },
                {'piglets_id': piglets2.pk, 'quantity': piglets2.quantity, 'changed': False }
                ],
            },
            format='json')

        self.assertEqual(response.status_code, 200)
        self.client.logout()

    def test_create_from_merging_list_transfer_part_number(self):
        self.client.force_authenticate(user=self.brig3)
        piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws3_sec1, 10)
        piglets2 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws3_sec1, 10)

        response = self.client.post('/api/piglets/create_from_merging_list_and_move_to_ws4/', \
            {'records': [
                {'piglets_id': piglets1.pk, 'quantity': piglets1.quantity, 'changed': False },
                {'piglets_id': piglets2.pk, 'quantity': piglets2.quantity, 'changed': False }
                ],
             'transfer_part_number': 1
            },
            format='json')

        self.assertNotEqual(Piglets.objects.filter(transfer_part_number=1).first(), None)
        self.client.logout()

    def test_culling(self):
        self.client.force_authenticate(user=self.brig3)
        piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws3_sec1, 10)

        response = self.client.post('/api/piglets/%s/culling/' % piglets1.pk, \
            {'culling_type': 'padej', 'reason': 'xz', 'quantity': 2, 'total_weight': 20})

        self.assertEqual(response.data['message'], 'Выбраковка прошла успешно.')
        self.client.logout()

    def test_culling_permissions(self):
        piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws3_sec1, 10)

        self.client.force_authenticate(user=self.brig4)
        response = self.client.post('/api/piglets/%s/culling/' % piglets1.pk, \
            {'culling_type': 'padej', 'reason': 'xz', 'quantity': 2, 'total_weight': 20})

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data['message'], 'Ошибка доступа. У вас нет прав.')
        self.client.logout()

        response = self.client.post('/api/piglets/%s/culling/' % piglets1.pk, \
            {'culling_type': 'padej', 'reason': 'xz', 'quantity': 2, 'total_weight': 20})

        self.assertEqual(response.status_code, 401)

        self.client.force_authenticate(user=self.admin)
        response = self.client.post('/api/piglets/%s/culling/' % piglets1.pk, \
            {'culling_type': 'padej', 'reason': 'xz', 'quantity': 2, 'total_weight': 20})

        self.assertEqual(response.status_code, 200)
        self.client.logout()

    def test_culling_permissions2(self):
        piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws4_cell1, 10)

        self.client.force_authenticate(user=self.brig4)
        response = self.client.post('/api/piglets/%s/culling/' % piglets1.pk, \
            {'culling_type': 'padej', 'reason': 'xz', 'quantity': 2, 'total_weight': 20})

        self.assertEqual(response.status_code, 200)
        self.client.logout()

    def test_weighing_piglets(self):
        piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws4_cell1, 10)

        self.client.force_authenticate(user=self.brig4)
        response = self.client.post('/api/piglets/%s/weighing_piglets/' %
          piglets1.pk, {'total_weight': 670, 'place': '3/4'})
        self.assertEqual(response.data['weighing_record']['piglets_group'], piglets1.pk)
        self.assertEqual(response.data['weighing_record']['total_weight'], 670)
        self.assertEqual(response.data['weighing_record']['place'], '3/4')

        piglets1.refresh_from_db()
        self.assertEqual(piglets1.status.title, 'Взвешены, готовы к заселению')
        self.client.logout()

    def test_weighing_piglets_permissions(self):
        piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws4_cell1, 10)

        self.client.force_authenticate(user=self.brig3)
        response = self.client.post('/api/piglets/%s/weighing_piglets/' %
          piglets1.pk, {'total_weight': 670, 'place': '3/4'})
        self.assertEqual(response.status_code, 403)      
        self.client.logout()

    def test_move_piglets_v1(self):
        # simple move
        self.client.force_authenticate(user=self.brig3)
        piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws3_sec1, 10)

        response = self.client.post('/api/piglets/%s/move_piglets/' %
          piglets1.pk, {'to_location': self.loc_ws4.pk })

        self.assertEqual(response.data['message'], 'Перевод прошел успешно.')
        self.client.logout()

    def test_move_piglets_permissions(self):
        # simple move
        self.client.force_authenticate(user=self.brig5)
        piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws3_sec1, 10)

        response = self.client.post('/api/piglets/%s/move_piglets/' %
          piglets1.pk, {'to_location': self.loc_ws4.pk })

        self.assertEqual(response.status_code, 403) 
        self.client.logout()

    def test_move_piglets_v2(self):
        # transaction with split
        self.client.force_authenticate(user=self.brig3)
        piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws3_sec1, 10)

        response = self.client.post('/api/piglets/%s/move_piglets/' %
          piglets1.pk, {'to_location': self.loc_ws4.pk, 'new_amount': 3 })

        self.assertEqual(response.data['message'], 'Перевод прошел успешно.')
        self.client.logout()

    def test_move_piglets_v3(self):
        # transaction with merge
        self.client.force_authenticate(user=self.brig3)
        piglets = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws3, 10)

        piglets_in_cell = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws4_cell1, 10)

        response = self.client.post('/api/piglets/%s/move_piglets/' %
          piglets.pk, {'to_location': self.loc_ws4.pk, 'merge': True })

        self.assertEqual(response.data['message'], 'Перевод прошел успешно.')
        self.client.logout()

    def test_move_piglets_v4(self):
        # transaction with merge and spli
        self.client.force_authenticate(user=self.brig3)
        piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws3, 10)

        piglets_in_cell = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws4_cell1, 10)

        response = self.client.post('/api/piglets/%s/move_piglets/' %
          piglets1.pk, {'to_location': self.loc_ws4.pk, 'merge': True, 'new_amount': 3 })

        self.assertEqual(response.data['message'], 'Перевод прошел успешно.')
        self.client.logout()

    def test_weighing_piglets_split_return(self):
        piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws3, 10)

        piglets2 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws4, 10)

        self.client.force_authenticate(user=self.brig4)
        response = self.client.post('/api/piglets/%s/weighing_piglets_split_return/' %
          piglets2.pk, {'to_location': self.loc_ws3.pk, 'new_amount': 8, 'total_weight': 80,
           'place': '3/4' })

        self.assertEqual(response.data['message'],
             'Взвешивание прошло успешно. Возврат поросят прошел успешно.')
        self.client.logout()

    def test_weighing_piglets_split_return_permissions(self):
        piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws3, 10)

        piglets2 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws4, 10)

        self.client.force_authenticate(user=self.brig3)
        response = self.client.post('/api/piglets/%s/weighing_piglets_split_return/' %
          piglets2.pk, {'to_location': self.loc_ws3.pk, 'new_amount': 8, 'total_weight': 80,
           'place': '3/4' })

        self.assertEqual(response.status_code, 403)
        self.client.logout()

    def test_recount_and_weighing_piglets(self):
        tour = Tour.objects.get_or_create_by_week_in_current_year(1)
        tour2 = Tour.objects.get_or_create_by_week_in_current_year(2)
        piglets = Piglets.objects.create(location=self.loc_ws4_cell1, quantity=100, start_quantity=100,
            status=None, birthday=datetime.datetime.now())
        meta_tour = MetaTour.objects.create(piglets=piglets)

        record1 = meta_tour.records.create_record(meta_tour, tour, 60, piglets.quantity)
        record2 = meta_tour.records.create_record(meta_tour, tour2, 40, piglets.quantity)

        self.client.force_authenticate(user=self.brig4)
        response = self.client.post('/api/piglets/%s/recount_and_weighing_piglets/' % piglets.pk, 
            {'new_quantity': 110, 'total_weight': 500, 'place': '3/4'})
        self.assertEqual(response.data['message'], 'Взвешивание прошло успешно.')
        
        piglets.refresh_from_db()
        self.assertEqual(piglets.quantity, 110)

        response = self.client.post('/api/piglets/%s/recount_and_weighing_piglets/' % piglets.pk, 
            {'total_weight': 580, 'place': '3/4'})
        self.assertEqual(response.data['message'], 'Взвешивание прошло успешно.')
        self.client.logout()

    def test_recount_piglets(self):
        tour = Tour.objects.get_or_create_by_week_in_current_year(1)
        tour2 = Tour.objects.get_or_create_by_week_in_current_year(2)
        location = Location.objects.get(section__number=1, section__workshop__number=3)
        piglets = Piglets.objects.create(location=location, quantity=100, start_quantity=100,
            status=None, birthday=datetime.datetime.now())
        meta_tour = MetaTour.objects.create(piglets=piglets)

        record1 = meta_tour.records.create_record(meta_tour, tour, 60, piglets.quantity)
        record2 = meta_tour.records.create_record(meta_tour, tour2, 40, piglets.quantity)

        self.client.force_authenticate(user=self.admin)
        response = self.client.post('/api/piglets/%s/recount_piglets/' % piglets.pk, 
            {'new_quantity': 105, 'comment': 'xz'})
        self.assertEqual(response.data['message'], 'Пересчет прошел успешно.')

        response = self.client.post('/api/piglets/%s/recount_piglets/' % piglets.pk, 
            {'new_quantity': 106,})
        self.assertEqual(response.data['message'], 'Пересчет прошел успешно.')
        self.client.logout()

    def test_recount_piglets_permissions(self):
        tour = Tour.objects.get_or_create_by_week_in_current_year(1)
        tour2 = Tour.objects.get_or_create_by_week_in_current_year(2)
        location = Location.objects.get(section__number=1, section__workshop__number=3)
        piglets = Piglets.objects.create(location=location, quantity=100, start_quantity=100,
            status=None, birthday=datetime.datetime.now())
        meta_tour = MetaTour.objects.create(piglets=piglets)

        record1 = meta_tour.records.create_record(meta_tour, tour, 60, piglets.quantity)
        record2 = meta_tour.records.create_record(meta_tour, tour2, 40, piglets.quantity)

        self.client.force_authenticate(user=self.brig2)
        response = self.client.post('/api/piglets/%s/recount_piglets/' % piglets.pk, 
            {'new_quantity': 105, 'comment': 'xz'})
        self.assertEqual(response.status_code, 403)
        self.client.logout()

        self.client.force_authenticate(user=self.shmigina)
        response = self.client.post('/api/piglets/%s/recount_piglets/' % piglets.pk, 
            {'new_quantity': 105, 'comment': 'xz'})
        self.assertEqual(response.status_code, 200)
        self.client.logout()

    def test_create_gilt(self):
        location = Location.objects.filter(sowAndPigletsCell__number=1).first()
        sow = sows_testing.create_sow_with_semination_usound(location, 1)
        farrow = SowFarrow.objects.create_sow_farrow(sow=sow, alive_quantity=10)
        piglets = farrow.piglets_group

        self.client.force_authenticate(user=self.brig3)
        response = self.client.post('/api/piglets/%s/create_gilt/' % piglets.pk,
            {'mother_sow_farm_id': sow.farm_id, 'birth_id': '1s'})
        self.assertEqual(response.data['message'], 'Ремонтная свинка создана успешно.')
        self.client.logout()

    def test_create_gilt_permissions(self):
        location = Location.objects.filter(sowAndPigletsCell__number=1).first()
        sow = sows_testing.create_sow_with_semination_usound(location, 1)
        farrow = SowFarrow.objects.create_sow_farrow(sow=sow, alive_quantity=10)
        piglets = farrow.piglets_group

        self.client.force_authenticate(user=self.brig4)
        response = self.client.post('/api/piglets/%s/create_gilt/' % piglets.pk,
            {'mother_sow_farm_id': sow.farm_id, 'birth_id': '1s'})
        self.assertEqual(response.status_code, 403)
        self.client.logout()

    def test_move_gilts_to_12(self):
        tour = Tour.objects.get_or_create_by_week_in_current_year(week_number=10)
        location = Location.objects.filter(pigletsGroupCell__isnull=False,
            pigletsGroupCell__workshop__number=5 ).first()
        piglets = piglets_testing.create_new_group_with_metatour_by_one_tour(
            tour=tour, location=location, quantity=50)

        self.client.force_authenticate(user=self.brig5)
        response = self.client.post('/api/piglets/%s/move_gilts_to_12/' % piglets.pk,
            {'new_amount': 25, 'total_weight': 750 })

        wp = WeighingPiglets.objects.all().first()
        self.assertEqual(wp.total_weight, 750)
        self.assertEqual(response.data['message'], 'Ремонтные свинки переведены успешно.')
        self.client.logout()

    def test_move_gilts_to_12_permissions(self):
        tour = Tour.objects.get_or_create_by_week_in_current_year(week_number=10)
        location = Location.objects.filter(pigletsGroupCell__isnull=False,
            pigletsGroupCell__workshop__number=5 ).first()
        piglets = piglets_testing.create_new_group_with_metatour_by_one_tour(
            tour=tour, location=location, quantity=50)

        self.client.force_authenticate(user=self.brig6)
        response = self.client.post('/api/piglets/%s/move_gilts_to_12/' % piglets.pk,
            {'total_weight': 100})
        self.assertEqual(response.status_code, 403)
        self.client.logout()

    def test_vet_event(self):
        piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws4, 10)

        self.client.force_authenticate(user=self.veterinar)
        response = self.client.post(f'/api/piglets/{piglets1.pk}/vet_event/', 
            data={'recipe': ''})
        self.assertEqual(response.data['message'], 'Мед. событие записано.')

        pve = PigletsVetEvent.objects.all().first()
        self.assertEqual(pve.week_tour, self.tour1)
        self.assertEqual(pve.target_piglets, piglets1)
        self.assertEqual(pve.piglets_quantity, 10)
        self.assertEqual(pve.recipe, None)

        self.client.logout()

    def test_access_workshop_permissions(self):
        ws5_cells = Location.objects.filter(pigletsGroupCell__isnull=False,
            pigletsGroupCell__workshop__number=5)
        piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            ws5_cells[0], 100)

        self.client.force_authenticate(user=self.brig5)
        response = self.client.post('/api/piglets/%s/move_piglets/' %
          piglets1.pk, {'to_location': ws5_cells[2].pk })
        self.assertEqual(response.status_code, 200) 
        self.client.logout()

        self.client.force_authenticate(user=self.brig7)
        response = self.client.post('/api/piglets/%s/move_piglets/' %
          piglets1.pk, {'to_location': ws5_cells[3].pk })
        self.assertEqual(response.status_code, 200) 
        self.client.logout()

        self.client.force_authenticate(user=self.brig6)
        response = self.client.post('/api/piglets/%s/move_piglets/' %
          piglets1.pk, {'to_location': ws5_cells[4].pk })
        self.assertEqual(response.status_code, 403) 
        self.client.logout()


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
