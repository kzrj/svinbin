# -*- coding: utf-8 -*-
from rest_framework.test import APIClient
from rest_framework.test import APITestCase

import locations.testing_utils as locations_testing
import sows.testing_utils as sows_testing
import sows_events.utils as sows_events_testings
import piglets.testing_utils as piglets_testing
import staff.testing_utils as staff_testing

from sows.models import Gilt
from sows_events.models import SowFarrow
from locations.models import WorkShop, SowAndPigletsCell, Location
from transactions.models import PigletsTransaction, SowTransaction
from tours.models import Tour


class WorkshopThreeSowsViewSetTest(APITestCase):
    def setUp(self):
        locations_testing.create_workshops_sections_and_cells()
        sows_testing.create_statuses()
        sows_events_testings.create_types()
        piglets_testing.create_piglets_statuses()
        self.client = APIClient()
        self.user = staff_testing.create_employee()
        self.client.force_authenticate(user=self.user)

    def test_sow_farrow(self):
        sow = sows_testing.create_sow_seminated_usouded_ws3_section(section_number=1, week=7)
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
        sow = sows_testing.create_sow_seminated_usouded_ws3_section(section_number=1, week=7)
        SowFarrow.objects.create_sow_farrow(sow=sow, alive_quantity=10)
        response = self.client.post('/api/workshopthree/sows/%s/mark_as_nurse/' % sow.pk)
        sow.refresh_from_db()
        self.assertEqual(sow.status.title, 'Кормилица')
        self.assertEqual(response.data['message'], 'Свинья помечена как кормилица.')

    def test_create_gilt(self):
        sow = sows_testing.create_sow_seminated_usouded_ws3_section(section_number=1, week=7)
        SowFarrow.objects.create_sow_farrow(sow=sow, alive_quantity=10)

        response = self.client.post('/api/workshopthree/sows/%s/create_gilt/' % sow.pk,
            {'birth_id': 1})
        self.assertEqual(response.data['message'], 'Ремонтная свинка успешно создана.')

    # def test_mark_as_nurse_creating_piglets(self):
    #     sow = sows_testing.create_sow_and_put_in_workshop_three(section_number=1, cell_number=1)
    #     tour = Tour.objects.get_or_create_by_week_in_current_year(45)
    #     response = self.client.post('/api/workshopthree/sows/%s/mark_as_nurse/' % sow.pk,
    #         {'piglets_tour': tour.pk})
    #     self.assertEqual(response.data['message'], 'Свинья почемена как кормилица. Создана группа поросят.')


# class WorkshopThreeInfoViewTest(APITestCase):
#     def setUp(self):
#         self.client = APIClient()
#         locations_testing.create_workshops_sections_and_cells()
#         sows_testing.create_statuses()
#         self.user = staff_testing.create_employee()
#         self.client.force_authenticate(user=self.user)

    # def test_info(self):
    #     sow1 = sows_testing.create_sow_with_semination_and_put_in_workshop_three(section_number=1,
    #      cell_number=1, week=7)
    #     sow2 = sows_testing.create_sow_with_semination_and_put_in_workshop_three(section_number=1,
    #      cell_number=2, week=7)
    #     sow3 = sows_testing.create_sow_with_semination_and_put_in_workshop_three(section_number=1,
    #      cell_number=3, week=7)

    #     response = self.client.post('/api/workshopthree/sows/%s/sow_farrow/' %
    #       sow1.pk, {'alive_quantity': 10, 'dead_quantity': 1, 'mummy_quantity': 2, 'week': 7 })
    #     response = self.client.post('/api/workshopthree/sows/%s/sow_farrow/' %
    #       sow2.pk, {'alive_quantity': 15, 'dead_quantity': 1, 'mummy_quantity': 2, 'week': 7 })

    #     response = self.client.get('/api/workshopthree/wsinfo/info/')
    #     self.assertEqual('Цех' in response.data.keys(), True)
    #     self.assertEqual('1' in response.data.keys(), True)
    #     self.assertEqual('2' in response.data.keys(), True)
    #     self.assertEqual('3' in response.data.keys(), True)
    #     self.assertEqual('4' in response.data.keys(), True)
    #     self.assertEqual('5' in response.data.keys(), True)
    #     self.assertEqual('6' in response.data.keys(), True)

    # def test_balances_by_tours(self):
    #     # create newborngroups tour=1, qnty=10
    #     for cell_number in range(1, 11):
    #         piglets_testing.create_new_born_group(section_number=1, cell_number=cell_number,
    #             week=1, quantity=10)
    #     piglets_group_qs = NewBornPigletsGroup.objects.all()

    #     # get 1 piglet from every group. recount -1. negative recount
    #     for nbgroup in piglets_group_qs:
    #         NewBornPigletsGroupRecount.objects.create_recount(nbgroup, 9)

    #     # add 1 piglet to every group. recount +1. positive recount
    #     for nbgroup in piglets_group_qs:
    #         NewBornPigletsGroupRecount.objects.create_recount(nbgroup, 10)

    #     # add another tour
    #     # create newborngroups tour=1, qnty=10
    #     for cell_number in range(1, 11):
    #         piglets_testing.create_new_born_group(section_number=2, cell_number=cell_number,
    #             week=2, quantity=10)
    #     piglets_group_qs = NewBornPigletsGroup.objects.filter(tour__week_number=2)

    #     # get 1 piglet from every group. recount -1. negative recount
    #     for nbgroup in piglets_group_qs:
    #         NewBornPigletsGroupRecount.objects.create_recount(nbgroup, 8)

    #     # add 1 piglet to every group. recount +1. positive recount
    #     for nbgroup in piglets_group_qs:
    #         NewBornPigletsGroupRecount.objects.create_recount(nbgroup, 12)

    #     location = Location.objects.get(workshop__number=3)
    #     tour = Tour.objects.get_or_create_by_week_in_current_year(40)
    #     NewBornPigletsGroup.objects.create_new_born_group(location, tour)

    #     location2 = Location.objects.get(sowAndPigletsCell__number=40,
    #      sowAndPigletsCell__section__number=1)
    #     tour2 = Tour.objects.get_or_create_by_week_in_current_year(41)
    #     NewBornPigletsGroup.objects.create_new_born_group(location2, tour2)

    #     response = self.client.get('/api/workshopthree/wsinfo/balances_by_tours/')
    #     self.assertEqual(response.data[0]['title'], 'Тур 1 2019г')
    #     self.assertEqual(response.data[1]['title'], 'Тур 2 2019г')
    #     self.assertEqual(response.data[2]['title'], 'Тур 40 2019г')
    #     self.assertEqual(len(response.data), 4)