# -*- coding: utf-8 -*-

from django.test import TestCase

from tours.models import Tour
from sows.models import Sow
from sows_events.models import Semination, Ultrasound
from locations.models import Location
from piglets.models import NewBornPigletsGroup
from piglets_events.models import NewBornPigletsGroupRecount

import locations.testing_utils as locations_testing
import sows.testing_utils as pigs_testings
import sows_events.utils as sows_events_testing
import piglets.testing_utils as piglets_testing


class TourModelManagerTest(TestCase):
    def setUp(self):
        locations_testing.create_workshops_sections_and_cells()
        pigs_testings.create_statuses()
        sows_events_testing.create_types()

    def test_get_or_create_by_week_in_current_year(self):
        Tour.objects.get_or_create_by_week_in_current_year(1)
        self.assertEqual(Tour.objects.all().count(), 1)
        self.assertEqual(Tour.objects.all().first().week_number, 1)
        self.assertEqual(Tour.objects.all().first().year, 2019)

        tour = Tour.objects.get_or_create_by_week_in_current_year(1)
        self.assertEqual(Tour.objects.all().count(), 1)
        self.assertEqual(tour.week_number, 1)

    def test_get_tours_in_workshop_by_sows(self):
        sow1 = pigs_testings.create_sow_and_put_in_workshop_one()
        sow2 = pigs_testings.create_sow_and_put_in_workshop_one()
        seminated_sow1 = pigs_testings.create_sow_with_semination(sow1.location)

        location2 = Location.objects.get(workshop__number=2)
        seminated_sow2 = pigs_testings.create_sow_with_semination(location2, 1)
        seminated_sow3 = pigs_testings.create_sow_with_semination(location2, 2)
        seminated_sow3 = pigs_testings.create_sow_with_semination(location2, 2)
        sow3 = pigs_testings.create_sow_and_put_in_workshop_one()
        sow3.location = location2
        sow3.save()

        self.assertEqual(Tour.objects.get_tours_in_workshop_by_sows(location2.workshop).count(), 2)

    def test_create_or_return_by_raw(self):
        tour = Tour.objects.create_or_return_by_raw('1940')
        self.assertEqual(tour.week_number, 40)
        self.assertEqual(tour.year, 2019)

    def test_qs_get_recounts_balance_data(self):
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

        tour = Tour.objects.filter(week_number=1).first()

        output_data = Tour.objects.all().get_recounts_balance_data()
        self.assertEqual('Тур 1 2019г' in output_data.keys(), True)
        self.assertEqual('positive' in output_data['Тур 1 2019г'].keys(), True)

    def test_get_tours_in_workshop_by_sows_and_piglets(self):
        for cell_number in range(1, 11):
            piglets_testing.create_new_born_group(section_number=1, cell_number=cell_number,
                week=1, quantity=10)

        location3 = Location.objects.get(workshop__number=3)
        seminated_sow2 = pigs_testings.create_sow_with_semination(location3, 2)

        location2 = Location.objects.get(workshop__number=2)
        seminated_sow2 = pigs_testings.create_sow_with_semination(location2, 2)
        seminated_sow3 = pigs_testings.create_sow_with_semination(location2, 3)

        tours = Tour.objects.get_tours_in_workshop_by_sows_and_piglets(location3.workshop)
        self.assertEqual(tours.count(), 2)
        self.assertEqual(tours[0].week_number in [1,2], True)
        self.assertEqual(tours[1].week_number in [1,2], True)

    
class TourModelTest(TestCase):
    def setUp(self):
        locations_testing.create_workshops_sections_and_cells()
        pigs_testings.create_statuses()
        sows_events_testing.create_types()

    def test_get_inseminated_sows(self):
        tour = Tour.objects.get_or_create_by_week_in_current_year(1)
        sow1 = Sow.objects.get_or_create_by_farm_id(101)
        sow2 = Sow.objects.get_or_create_by_farm_id(102)
        Semination.objects.create_semination(sow1, 1)
        Semination.objects.create_semination(sow2, 1)

        inseminated_sows_in_tour = tour.get_inseminated_sows
        self.assertEqual(sow1 in inseminated_sows_in_tour, True)
        self.assertEqual(sow2 in inseminated_sows_in_tour, True)

    def test_get_ultrasounded_sows(self):
        tour = Tour.objects.get_or_create_by_week_in_current_year(1)
        sow1 = Sow.objects.get_or_create_by_farm_id(201)
        sow2 = Sow.objects.get_or_create_by_farm_id(202)
        Semination.objects.create_semination(sow1, 1)
        Semination.objects.create_semination(sow2, 1)
        Ultrasound.objects.create_ultrasound(sow1, None, False, 30)
        Ultrasound.objects.create_ultrasound(sow2, None, True, 30)

        ultrasounded_sows_in_tour = tour.get_ultrasounded_sows
        self.assertEqual(ultrasounded_sows_in_tour[0], sow1)
        self.assertEqual(ultrasounded_sows_in_tour[1], sow2)

        ultrasounded_sows_in_tour_success = tour.get_ultrasounded_sows_success
        self.assertEqual(ultrasounded_sows_in_tour_success[0], sow2)

        ultrasounded_sows_in_tour_fail = tour.get_ultrasounded_sows_fail
        self.assertEqual(ultrasounded_sows_in_tour_fail[0], sow1)

    def test_get_recounts_balances(self):
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

        tour = Tour.objects.filter(week_number=1).first()
        
        self.assertEqual(tour.get_positive_recounts_balance, 10)
        self.assertEqual(tour.get_negative_recounts_balance, -10)

        self.assertEqual(tour.get_recount_balance_info,
            {'negative': -10, 'positive': 10, 'balance': 0, 'count_newborn_piglets': 100}) 

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

        tour.refresh_from_db()
        self.assertEqual(tour.get_recount_balance_info,
            {'negative': -10, 'positive': 10, 'balance': 0, 'count_newborn_piglets': 100})


    def test_test_get_recounts_balances_inactive_groups(self):
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

        nbgroup = NewBornPigletsGroup.objects.filter(tour__week_number=1).first()
        nbgroup.active = False
        nbgroup.save()

        tour = Tour.objects.filter(week_number=1).first()
        self.assertEqual(tour.get_positive_recounts_balance, 10)
        self.assertEqual(tour.get_negative_recounts_balance, -10)

        self.assertEqual(tour.get_recount_balance_info,
            {'negative': -10, 'positive': 10, 'balance': 0, 'count_newborn_piglets': 100}) 