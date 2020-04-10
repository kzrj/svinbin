# -*- coding: utf-8 -*-
import datetime

from django.test import TestCase
from django.utils import timezone
from django.db import models

from tours.models import Tour, MetaTour, MetaTourRecord
from sows.models import Sow
from sows_events.models import Semination, Ultrasound, SowFarrow
from locations.models import Location
from piglets.models import Piglets
from piglets_events.models import PigletsMerger, WeighingPiglets

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


class TourQuerysetTest(TestCase):
    def setUp(self):
        locations_testing.create_workshops_sections_and_cells()
        pigs_testings.create_statuses()
        sows_events_testing.create_types()
        piglets_testing.create_piglets_statuses()

        self.tour1 = Tour.objects.get_or_create_by_week_in_current_year(week_number=1)
        self.tour2 = Tour.objects.get_or_create_by_week_in_current_year(week_number=2)

        location1 = Location.objects.filter(sowAndPigletsCell__number=1).first()
        sow1 = pigs_testings.create_sow_with_semination_usound(location=location1, week=1)
        farrow = SowFarrow.objects.create_sow_farrow(
            sow=sow1,
            alive_quantity=10,
            dead_quantity=0,
            mummy_quantity=0
            )

        location2 = Location.objects.filter(sowAndPigletsCell__isnull=False)[1]
        sow2 = pigs_testings.create_sow_with_semination_usound(location=location2, week=1)
        farrow = SowFarrow.objects.create_sow_farrow(
            sow=sow2,
            alive_quantity=12,
            dead_quantity=5,
            mummy_quantity=1
            )

        location3 = Location.objects.filter(sowAndPigletsCell__isnull=False)[2]
        sow3 = pigs_testings.create_sow_with_semination_usound(location=location3, week=1)
        farrow = SowFarrow.objects.create_sow_farrow(
            sow=sow3,
            alive_quantity=13,
            dead_quantity=3,
            mummy_quantity=2
            )

        location4 = Location.objects.filter(sowAndPigletsCell__isnull=False)[3]
        sow4 = pigs_testings.create_sow_with_semination_usound(location=location4, week=2)
        farrow = SowFarrow.objects.create_sow_farrow(
            sow=sow4,
            alive_quantity=19,
            dead_quantity=3,
            mummy_quantity=2
            )

        location5 = Location.objects.filter(sowAndPigletsCell__isnull=False)[4]
        sow5 = pigs_testings.create_sow_with_semination_usound(location=location5, week=2)
        farrow = SowFarrow.objects.create_sow_farrow(
            sow=sow5,
            alive_quantity=14,
            dead_quantity=0,
            mummy_quantity=0
            )

        # piglets without farrow
        self.loc_ws5 = Location.objects.get(workshop__number=5)
        piglets11 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws5, 100)
        piglets12 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour2,
            self.loc_ws5, 100)

         # merged piglets
        piglets13 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws5, 100)
        piglets14 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour2,
            self.loc_ws5, 50)

        self.loc_cell_ws5_1 = Location.objects.filter(pigletsGroupCell__workshop__number=5)[0]
        merged_piglets1 = PigletsMerger.objects.create_merger_return_group(
            parent_piglets=[piglets13, piglets14], new_location=self.loc_cell_ws5_1)

        piglets15 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws5, 30)
        piglets16 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour2,
            self.loc_ws5, 50)

        loc_cell_ws5_2 = Location.objects.filter(pigletsGroupCell__workshop__number=5)[1]
        merged_piglets2 = PigletsMerger.objects.create_merger_return_group(
            parent_piglets=[piglets15, piglets16], new_location=loc_cell_ws5_2)

    def test_add_farrow_data(self):
        with self.assertNumQueries(1):
            tours = Tour.objects.all().add_farrow_data()
            bool(tours)
            self.assertEqual(tours[0].total_born_alive, 35)
            self.assertEqual(tours[0].total_born_dead, 8)
            self.assertEqual(tours[0].total_born_mummy, 3)

            self.assertEqual(tours[1].total_born_alive, 33)
            self.assertEqual(tours[1].total_born_dead, 3)
            self.assertEqual(tours[1].total_born_mummy, 2)


    def test_add_current_not_mixed_piglets_quantity(self):
        with self.assertNumQueries(1):
            tours = Tour.objects.all().add_current_not_mixed_piglets_quantity()
            bool(tours)
            self.assertEqual(tours[0].total_not_mixed_piglets, 135)
            self.assertEqual(tours[1].total_not_mixed_piglets, 133)

    def test_add_current_mixed_piglets_quantity(self):
        with self.assertNumQueries(1):
            tours = Tour.objects.all().add_current_mixed_piglets_quantity()
            bool(tours)
            self.assertEqual(tours[0].total_mixed_piglets, 130)
            self.assertEqual(tours[1].total_mixed_piglets, 100)

    def test_add_weight_data_not_mixed(self):
        piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws5, 100)
        WeighingPiglets.objects.create_weighing(piglets_group=piglets1, total_weight=1100, place='3/4')

        piglets2 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws5, 100)
        WeighingPiglets.objects.create_weighing(piglets_group=piglets2, total_weight=1300, place='3/4')

        piglets4 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws5, 30)
        piglets5 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour2,
            self.loc_ws5, 50)

        loc_cell_ws5_2 = Location.objects.filter(pigletsGroupCell__workshop__number=5)[2]
        merged_piglets1 = PigletsMerger.objects.create_merger_return_group(
            parent_piglets=[piglets4, piglets5], new_location=loc_cell_ws5_2)
        WeighingPiglets.objects.create_weighing(piglets_group=merged_piglets1, total_weight=1200,
         place='3/4')

        piglets3 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws5, 100)
        WeighingPiglets.objects.create_weighing(piglets_group=piglets3, total_weight=2600, place='4/8')

        with self.assertNumQueries(1):
            tours = Tour.objects.all().add_weight_data_not_mixed()
            bool(tours)
            self.assertEqual(tours[0].total_weight_not_mixed_3_4, 2400)
            self.assertEqual(tours[0].total_weight_not_mixed_4_8, 2600)

    def test_add_weight_data_mixed(self):
        piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws5, 100)
        WeighingPiglets.objects.create_weighing(piglets_group=piglets1, total_weight=1100, place='3/4')

        piglets3 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws5, 100)
        WeighingPiglets.objects.create_weighing(piglets_group=piglets3, total_weight=2600, place='4/8')

        # mixed tour piglets
        piglets4 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws5, 30)
        piglets5 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour2,
            self.loc_ws5, 70)
        loc_cell_ws5_3 = Location.objects.filter(pigletsGroupCell__workshop__number=5)[2]
        merged_piglets1 = PigletsMerger.objects.create_merger_return_group(
            parent_piglets=[piglets4, piglets5], new_location=loc_cell_ws5_3)
        WeighingPiglets.objects.create_weighing(piglets_group=merged_piglets1, total_weight=1000,
         place='3/4')

        piglets6 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws5, 20)
        piglets7 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour2,
            self.loc_ws5, 80)
        loc_cell_ws5_4 = Location.objects.filter(pigletsGroupCell__workshop__number=5)[3]
        merged_piglets2 = PigletsMerger.objects.create_merger_return_group(
            parent_piglets=[piglets6, piglets7], new_location=loc_cell_ws5_4)
        WeighingPiglets.objects.create_weighing(piglets_group=merged_piglets2, total_weight=1000,
         place='3/4')

        WeighingPiglets.objects.create_weighing(piglets_group=merged_piglets2, total_weight=1000,
         place='4/8')

        WeighingPiglets.objects.create_weighing(piglets_group=merged_piglets2, total_weight=2000,
         place='8/5')

        WeighingPiglets.objects.create_weighing(piglets_group=merged_piglets1, total_weight=2000,
         place='8/5')
        merged_piglets1.deactivate()

        with self.assertNumQueries(1):
            tours = Tour.objects.all().add_weight_data_mixed()
            bool(tours)            
            self.assertEqual(tours[0].total_weight_mixed_3_4, 500)
            self.assertEqual(tours[0].total_weight_mixed_4_8, 200)
            self.assertEqual(tours[0].total_weight_mixed_8_5, 1000)

    def test_add_avg_weight_data(self):
        piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws5, 100)
        WeighingPiglets.objects.create_weighing(piglets_group=piglets1, total_weight=1100, place='3/4')

        piglets3 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws5, 100)
        WeighingPiglets.objects.create_weighing(piglets_group=piglets3, total_weight=2600, place='4/8')

        # mixed tour piglets
        piglets4 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws5, 30)
        piglets5 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour2,
            self.loc_ws5, 70)
        loc_cell_ws5_3 = Location.objects.filter(pigletsGroupCell__workshop__number=5)[2]
        merged_piglets1 = PigletsMerger.objects.create_merger_return_group(
            parent_piglets=[piglets4, piglets5], new_location=loc_cell_ws5_3)
        WeighingPiglets.objects.create_weighing(piglets_group=merged_piglets1, total_weight=1000,
         place='3/4')

        merged_piglets1.deactivate()

        with self.assertNumQueries(1):
            tours = Tour.objects.all().add_avg_weight_data()
            bool(tours)            
            self.assertEqual(tours[0].avg_weight_3_4, 10.5)
            
