# -*- coding: utf-8 -*-
import datetime

from django.test import TestCase
from django.utils import timezone

from tours.models import Tour, MetaTour, MetaTourRecord
from sows.models import Sow
from sows_events.models import Semination, Ultrasound, SowFarrow
from locations.models import Location
from piglets.models import Piglets

import locations.testing_utils as locations_testing
import sows.testing_utils as pigs_testings
import sows_events.utils as sows_events_testing
import piglets.testing_utils as piglets_testing


class TourModelManagerTest(TestCase):
    def setUp(self):
        locations_testing.create_workshops_sections_and_cells()
        pigs_testings.create_statuses()
        sows_events_testing.create_types()

        self.tour1 = Tour.objects.get_or_create_by_week_in_current_year(week_number=1)
        self.tour2 = Tour.objects.get_or_create_by_week_in_current_year(week_number=2)
        self.tour3 = Tour.objects.get_or_create_by_week_in_current_year(week_number=3)
        self.tour4 = Tour.objects.get_or_create_by_week_in_current_year(week_number=4)

        self.loc_ws4 = Location.objects.get(workshop__number=4)
        self.loc_cell_ws4_1 = Location.objects.filter(pigletsGroupCell__workshop__number=4)[0]
        self.loc_cell_ws4_2 = Location.objects.filter(pigletsGroupCell__workshop__number=4)[1]
        self.loc_cell_ws4_3 = Location.objects.filter(pigletsGroupCell__workshop__number=4)[2]
        self.loc_cell_ws4_4 = Location.objects.filter(pigletsGroupCell__workshop__number=4)[3]
        self.loc_section_ws4_1 = Location.objects.filter(section__workshop__number=4)[0]
        self.loc_ws5 = Location.objects.get(workshop__number=5)

    def test_get_or_create_by_week_in_current_year(self):
        Tour.objects.get_or_create_by_week_in_current_year(1)
        self.assertEqual(Tour.objects.all().count(), 4)
        self.assertEqual(Tour.objects.all().first().week_number, 1)
        self.assertEqual(Tour.objects.all().first().year, 2020)

        tour = Tour.objects.get_or_create_by_week_in_current_year(1)
        self.assertEqual(Tour.objects.all().count(), 4)
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

    def test_create_tour_from_farrow_date_string(self):
        tour = Tour.objects.create_tour_from_farrow_date_string(farrow_date='2020-03-5', days=4)
        self.assertEqual(tour.week_number, 9)
        self.assertEqual(tour.start_date.day, 1)

    def test_get_monday_date_by_week_number(self):
        monday = Tour.objects.get_monday_date_by_week_number(week_number=1, year=2020)
        self.assertEqual(monday.day, 6)
        
        monday2 = Tour.objects.get_monday_date_by_week_number(week_number=2, year=2020)
        self.assertEqual(monday2.day, 13)

    def test_get_tours_by_piglets(self):
        # piglets in ws 4
        piglets4 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws4, 100)
        piglets5 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour2,
            self.loc_ws4, 100)

        #  piglets in pigletsCell in ws
        piglets6 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour2,
            self.loc_cell_ws4_1, 100)
        piglets7 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour2,
            self.loc_cell_ws4_2, 100)

        # inactive piglets
        piglets8 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour2,
            self.loc_cell_ws4_3, 100)
        piglets8.deactivate()
        piglets9 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour2,
            self.loc_cell_ws4_4, 100)
        piglets9.deactivate()

        # piglets in section
        piglets10 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour2,
            self.loc_section_ws4_1, 100)

        # piglets in ws5
        piglets11 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws5, 100)
        piglets12 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour2,
            self.loc_ws5, 100)
        piglets13 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour3,
            self.loc_ws5, 100)
        piglets14 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour4,
            self.loc_ws5, 100)

        piglets_t1_t2 = Piglets.objects.filter(pk__in=[piglets4.pk, piglets5.pk])
        t1_t_2 = Tour.objects.get_tours_by_piglets(piglets=piglets_t1_t2)
        self.assertEqual(t1_t_2.count(), 2)
        self.assertEqual(t1_t_2[0].week_number, 1)
        self.assertEqual(t1_t_2[1].week_number, 2)

        all_piglets_tours = Piglets.objects.all()
        self.assertEqual(Tour.objects.get_tours_by_piglets(all_piglets_tours).count(), 4)

    
class TourModelTest(TestCase):
    def setUp(self):
        locations_testing.create_workshops_sections_and_cells()
        pigs_testings.create_statuses()
        sows_events_testing.create_types()
        piglets_testing.create_piglets_statuses()

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

    def test_days_left_from_farrow(self):
        tour1 = Tour.objects.create_tour_from_farrow_date_string('2020-01-01')
        tour2 = Tour.objects.create_tour_from_farrow_date_string('2020-01-26')

        sow = pigs_testings.create_sow_and_put_in_workshop_three()
        sow.tour = tour1
        sow.save()
        farrow_date = datetime.datetime.strptime('2020-01-02', '%Y-%m-%d')
        SowFarrow.objects.create_sow_farrow(sow=sow, alive_quantity=10, date=farrow_date)

        t1_days_left_from_farrow_approx = timezone.now() - (tour1.start_date + datetime.timedelta(days=135))
        self.assertEqual(tour1.days_left_from_farrow_approx.days, t1_days_left_from_farrow_approx.days)

        t1_days_left_from_farrow = timezone.now() - (tour1.sowfarrow_set.all().first().date)
        self.assertEqual(tour1.days_left_from_farrow.days, t1_days_left_from_farrow.days)


class TestMetaTourRecordModel(TestCase):
    def setUp(self):
        locations_testing.create_workshops_sections_and_cells()
        pigs_testings.create_statuses()
        piglets_testing.create_piglets_statuses()

    def test_create_record(self):
        tour = Tour.objects.get_or_create_by_week_in_current_year(1)
        location = Location.objects.get(section__number=1, section__workshop__number=3)
        piglets = Piglets.objects.create(location=location, quantity=10, start_quantity=10,
        gilts_quantity=0, status=None)
        meta_tour = MetaTour.objects.create(piglets=piglets)

        record = meta_tour.records.create_record(meta_tour, tour, piglets.quantity, piglets.quantity)
        self.assertEqual(record.quantity, 10)
        self.assertEqual(record.tour, tour)
        self.assertEqual(record.percentage, 100.0)

    def test_recount_records_by_total_quantity_v1(self):
        tour = Tour.objects.get_or_create_by_week_in_current_year(1)
        tour2 = Tour.objects.get_or_create_by_week_in_current_year(2)
        location = Location.objects.get(section__number=1, section__workshop__number=3)
        piglets = Piglets.objects.create(location=location, quantity=100, start_quantity=100,
        gilts_quantity=0, status=None)
        meta_tour = MetaTour.objects.create(piglets=piglets)

        record1 = meta_tour.records.create_record(meta_tour, tour, 60, piglets.quantity)
        record2 = meta_tour.records.create_record(meta_tour, tour2, 40, piglets.quantity)

        self.assertEqual(record1.quantity, 60)
        self.assertEqual(record1.tour, tour)
        self.assertEqual(record1.percentage, 60)
        self.assertEqual(record2.quantity, 40)
        self.assertEqual(record2.tour, tour2)
        self.assertEqual(record2.percentage, 40)

        piglets.metatour.records.recount_records_by_total_quantity(110)
        record1.refresh_from_db()
        record2.refresh_from_db()

        self.assertEqual(record1.quantity, 66)
        self.assertEqual(record2.quantity, 44)
        self.assertEqual(record1.percentage, 60)
        self.assertEqual(record2.percentage, 40)

        piglets.metatour.records.recount_records_by_total_quantity(90)
        record1.refresh_from_db()
        record2.refresh_from_db()
        self.assertEqual(record1.quantity, 54)
        self.assertEqual(record2.quantity, 36)

        piglets.metatour.records.recount_records_by_total_quantity(100)
        record1.refresh_from_db()
        record2.refresh_from_db()
        self.assertEqual(record1.quantity, 60)
        self.assertEqual(record2.quantity, 40)

        piglets.metatour.records.recount_records_by_total_quantity(101)
        record1.refresh_from_db()
        record2.refresh_from_db()
        self.assertEqual(record1.quantity, 61)
        self.assertEqual(record2.quantity, 40)

    def test_days_left(self):
        tour1 = Tour.objects.create_tour_from_farrow_date_string('2020-01-01')
        tour2 = Tour.objects.create_tour_from_farrow_date_string('2020-01-26')

        sow = pigs_testings.create_sow_and_put_in_workshop_three()
        sow.tour = tour1
        sow.save()
        farrow_date = datetime.datetime.strptime('2020-01-02', '%Y-%m-%d')
        SowFarrow.objects.create_sow_farrow(sow=sow, alive_quantity=10, date=farrow_date)
        
        location = Location.objects.filter(pigletsGroupCell__isnull=False).first()
        piglets = Piglets.objects.create(location=location, quantity=100, start_quantity=100,
        gilts_quantity=0, status=None)
        meta_tour = MetaTour.objects.create(piglets=piglets)

        record1 = meta_tour.records.create_record(meta_tour, tour1, 60, piglets.quantity)
        record2 = meta_tour.records.create_record(meta_tour, tour2, 40, piglets.quantity)

        self.assertEqual(
            isinstance(meta_tour.records_repr()[0]['days_left_from_farrow_approx'], str), True)

        self.assertEqual(isinstance(meta_tour.records_repr()[0]['days_left_from_farrow'], str), True)

        self.assertEqual(
            isinstance(meta_tour.records_repr()[1]['days_left_from_farrow_approx'], str), True)

        self.assertEqual(isinstance(meta_tour.records_repr()[1]['days_left_from_farrow'], str), False)
