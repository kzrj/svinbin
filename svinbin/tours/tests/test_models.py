# -*- coding: utf-8 -*-
import datetime

from django.test import TestCase
from django.utils import timezone
from django.db import models
from django.db.models import Q

from tours.models import Tour, MetaTour, MetaTourRecord
from sows.models import Sow, Gilt
from sows_events.models import Semination, Ultrasound, SowFarrow, AbortionSow
from locations.models import Location
from piglets.models import Piglets
from piglets_events.models import PigletsMerger, WeighingPiglets, CullingPiglets
from transactions.models import PigletsTransaction

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
        self.assertEqual(Tour.objects.all().first().year, datetime.datetime.now().year)

        tour = Tour.objects.get_or_create_by_week_in_current_year(1)
        self.assertEqual(Tour.objects.all().count(), 4)
        self.assertEqual(tour.week_number, 1)


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
        self.assertEqual(t1_t_2[0].week_number in [1,2], True)
        self.assertEqual(t1_t_2[1].week_number in [1,2], True)

        all_piglets_tours = Piglets.objects.all()
        self.assertEqual(Tour.objects.get_tours_by_piglets(all_piglets_tours).count(), 4)

    def test_get_week_tours_by_piglets(self):
        # piglets in ws5
        piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws4, 100)
        piglets2 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour2,
            self.loc_cell_ws4_3, 100)
        piglets3 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour3,
            self.loc_ws5, 100)
        piglets4 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour4,
            self.loc_ws5, 100)

        piglets_t1_t2 = Piglets.objects.filter(pk__in=[piglets1.pk, piglets2.pk])
        t1_t_2 = Tour.objects.get_week_tours_by_piglets(piglets=piglets_t1_t2)
        self.assertEqual(t1_t_2.count(), 2)
        self.assertEqual(t1_t_2[0].week_number in [1,2], True)
        self.assertEqual(t1_t_2[1].week_number in [1,2], True)

        all_piglets_tours = Piglets.objects.all()
        self.assertEqual(Tour.objects.get_week_tours_by_piglets(all_piglets_tours).count(), 4)

    
class TourModelTest(TestCase):
    def setUp(self):
        locations_testing.create_workshops_sections_and_cells()
        pigs_testings.create_statuses()
        sows_events_testing.create_types()
        piglets_testing.create_piglets_statuses()

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

        self.tour51 = Tour.objects.get_or_create_by_week_in_current_year(51)
        self.tour52 = Tour.objects.get_or_create_by_week_in_current_year(52)

        self.loc_cells = Location.objects.filter(pigletsGroupCell__isnull=False)

    def test_create_record_without_percentage(self):
        tour = Tour.objects.get_or_create_by_week_in_current_year(1)
        location = Location.objects.get(section__number=1, section__workshop__number=3)
        piglets = Piglets.objects.create(location=location, quantity=10, start_quantity=10, status=None)
        meta_tour = MetaTour.objects.create(piglets=piglets)

        record = meta_tour.records.create_record(metatour=meta_tour, tour=tour,
         quantity=piglets.quantity, total_quantity=piglets.quantity)
        self.assertEqual(record.quantity, 10)
        self.assertEqual(record.tour, tour)
        self.assertEqual(record.percentage, 100.0)

    def test_create_record_with_percentage(self):
        tour = Tour.objects.get_or_create_by_week_in_current_year(1)
        tour2 = Tour.objects.get_or_create_by_week_in_current_year(2)
        location = Location.objects.get(section__number=1, section__workshop__number=3)
        piglets = Piglets.objects.create(location=location, quantity=10, start_quantity=10, status=None)
        meta_tour = MetaTour.objects.create(piglets=piglets)

        record = meta_tour.records.create_record(metatour=meta_tour, tour=tour,
         quantity=8, total_quantity=piglets.quantity, percentage=80)
        self.assertEqual(record.quantity, 8)
        self.assertEqual(record.tour, tour)
        self.assertEqual(record.percentage, 80)

        record2 = meta_tour.records.create_record(metatour=meta_tour, tour=tour2,
         quantity=2, total_quantity=piglets.quantity, percentage=20)
        self.assertEqual(record2.quantity, 2)
        self.assertEqual(record2.tour, tour2)
        self.assertEqual(record2.percentage, 20)

    def test_recount_records_by_total_quantity_v1(self):
        tour = Tour.objects.get_or_create_by_week_in_current_year(1)
        tour2 = Tour.objects.get_or_create_by_week_in_current_year(2)
        location = Location.objects.get(section__number=1, section__workshop__number=3)
        piglets = Piglets.objects.create(location=location, quantity=100, start_quantity=100, status=None)
        meta_tour = MetaTour.objects.create(piglets=piglets)

        record1 = meta_tour.records.create_record(metatour=meta_tour, tour=tour, 
            quantity=60, total_quantity=piglets.quantity, percentage=60)
        record2 = meta_tour.records.create_record(metatour=meta_tour,  tour=tour2,
         quantity=40, total_quantity=piglets.quantity, percentage=40)

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
        self.assertEqual(record1.quantity, 60.6)
        self.assertEqual(record2.quantity, 40.4)

    def test_days_left(self):
        tour1 = Tour.objects.create_tour_from_farrow_date_string('2020-01-01')
        tour2 = Tour.objects.create_tour_from_farrow_date_string('2020-01-26')

        sow = pigs_testings.create_sow_and_put_in_workshop_three()
        sow.tour = tour1
        sow.save()
        farrow_date = datetime.datetime.strptime('2020-01-02', '%Y-%m-%d')
        SowFarrow.objects.create_sow_farrow(sow=sow, alive_quantity=10, date=farrow_date)
        
        location = Location.objects.filter(pigletsGroupCell__isnull=False).first()
        piglets = Piglets.objects.create(location=location, quantity=100, start_quantity=100, status=None)
        meta_tour = MetaTour.objects.create(piglets=piglets)

        record1 = meta_tour.records.create_record(meta_tour, tour1, 60, piglets.quantity)
        record2 = meta_tour.records.create_record(meta_tour, tour2, 40, piglets.quantity)

        self.assertEqual(
            isinstance(meta_tour.records_repr()[0]['days_left_from_farrow_approx'], str), True)

        self.assertEqual(isinstance(meta_tour.records_repr()[0]['days_left_from_farrow'], str), True)

        self.assertEqual(
            isinstance(meta_tour.records_repr()[1]['days_left_from_farrow_approx'], str), True)

        self.assertEqual(isinstance(meta_tour.records_repr()[1]['days_left_from_farrow'], str), False)

    # def test_create_record_v2_cal_qnty(self):
    #     piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(
    #         tour=self.tour51,
    #         location=self.loc_cells[0],
    #         quantity=100,
    #         birthday=(datetime.datetime.now() - datetime.timedelta(days=100))
    #         )
    #     metatour1 = piglets1.metatour
    #     mtr_main = piglets1.metatour.records.all().first()

    #     qnty = 90

    #     mtr1 = MetaTourRecord.objects.create_record(
    #         metatour=metatour1,
    #         tour=self.tour51,
    #         quantity=42 * qnty / 100,
    #         total_quantity=qnty,
    #         percentage=41.66
    #         )
    #     print(mtr1.quantity)

    #     mtr2 = MetaTourRecord.objects.create_record(
    #         metatour=metatour1,
    #         tour=self.tour51,
    #         quantity=8 * qnty / 100,
    #         total_quantity=qnty,
    #         percentage=8.33
    #         )
    #     print(mtr2.quantity)

    #     mtr3 = MetaTourRecord.objects.create_record(
    #         metatour=metatour1,
    #         tour=self.tour51,
    #         quantity=50 * qnty / 100,
    #         total_quantity=qnty,
    #         percentage=50
    #         )
    #     print(mtr3.quantity)


class TourQuerysetAddPigletsDataTest(TestCase):
    def setUp(self):
        locations_testing.create_workshops_sections_and_cells()
        pigs_testings.create_statuses()
        sows_events_testing.create_types()
        piglets_testing.create_piglets_statuses()

        self.tour1 = Tour.objects.get_or_create_by_week_in_current_year(week_number=1)
        self.tour2 = Tour.objects.get_or_create_by_week_in_current_year(week_number=2)

        location1 = Location.objects.filter(sowAndPigletsCell__number=1).first()
        self.sow1 = pigs_testings.create_sow_with_semination_usound(location=location1, week=1)
        self.farrow1 = SowFarrow.objects.create_sow_farrow(
            sow=self.sow1,
            alive_quantity=10,
            dead_quantity=0,
            mummy_quantity=0
            )
        Gilt.objects.create_gilt('1a', self.sow1.farm_id, self.farrow1.piglets_group)
        Gilt.objects.create_gilt('1b', self.sow1.farm_id, self.farrow1.piglets_group)

        location2 = Location.objects.filter(sowAndPigletsCell__isnull=False)[1]
        self.sow2 = pigs_testings.create_sow_with_semination_usound(location=location2, week=1)
        self.farrow2 = SowFarrow.objects.create_sow_farrow(
            sow=self.sow2,
            alive_quantity=12,
            dead_quantity=5,
            mummy_quantity=1
            )

        location3 = Location.objects.filter(sowAndPigletsCell__isnull=False)[2]
        self.sow3 = pigs_testings.create_sow_with_semination_usound(location=location3, week=1)
        self.farrow3 = SowFarrow.objects.create_sow_farrow(
            sow=self.sow3,
            alive_quantity=13,
            dead_quantity=3,
            mummy_quantity=2
            )

        location4 = Location.objects.filter(sowAndPigletsCell__isnull=False)[3]
        self.sow4 = pigs_testings.create_sow_with_semination_usound(location=location4, week=2)
        self.farrow4 = SowFarrow.objects.create_sow_farrow(
            sow=self.sow4,
            alive_quantity=19,
            dead_quantity=3,
            mummy_quantity=2
            )

        location5 = Location.objects.filter(sowAndPigletsCell__isnull=False)[4]
        self.sow5 = pigs_testings.create_sow_with_semination_usound(location=location5, week=2)
        self.farrow5 = SowFarrow.objects.create_sow_farrow(
            sow=self.sow5,
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
            tours = Tour.objects.all() \
                .add_farrow_data() \
                .add_sow_data() \
                .add_farrow_percentage() \
                .add_week_weight() \
                .add_week_weight_ws8_v2() \
                .add_culling_data_by_week_tour() \
                .add_culling_percentage()
            bool(tours)
            self.assertEqual(tours[0].farrow_percentage, 100)
            self.assertEqual(tours[0].count_farrows, 3)
            self.assertEqual(tours[0].total_born_alive, 35)
            self.assertEqual(tours[0].total_born_dead, 8)
            self.assertEqual(tours[0].total_born_mummy, 3)
            self.assertEqual(tours[0].gilt_count, 2)

            self.assertEqual(tours[1].farrow_percentage, 100)
            self.assertEqual(tours[1].count_farrows, 2)
            self.assertEqual(tours[1].total_born_alive, 33)
            self.assertEqual(tours[1].total_born_dead, 3)
            self.assertEqual(tours[1].total_born_mummy, 2)

    def test_add_week_weight(self):
        piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws5, 100)
        WeighingPiglets.objects.create_weighing(piglets_group=piglets1, total_weight=1100,
         place='3/4')

        piglets3 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws5, 100)
        WeighingPiglets.objects.create_weighing(piglets_group=piglets3, total_weight=2600,
         place='4/8')

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
            self.loc_ws5, 50)
        piglets7 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour2,
            self.loc_ws5, 50)
        loc_cell_ws5_4 = Location.objects.filter(pigletsGroupCell__workshop__number=5)[3]
        merged_piglets2 = PigletsMerger.objects.create_merger_return_group(
            parent_piglets=[piglets6, piglets7], new_location=loc_cell_ws5_4)
        w2 = WeighingPiglets.objects.create_weighing(piglets_group=merged_piglets2,
         total_weight=1000,
         place='3/4', date=datetime.datetime.now() + datetime.timedelta(days=21))

        merged_piglets1.deactivate()

        with self.assertNumQueries(1):
            tours = Tour.objects.all().add_week_weight()
            bool(tours)
            self.assertEqual(tours[0].week_weight_3_4, 2100)
            self.assertEqual(tours[0].week_weight_avg_3_4, 10.5)
            self.assertEqual(tours[0].week_weight_qnty_3_4, 200)

    def test_add_week_weight_ws8_v2(self):
        piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws5, 100)
        WeighingPiglets.objects.create_weighing(piglets_group=piglets1, total_weight=1100, 
            place='8/5')

        piglets3 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws5, 100)
        WeighingPiglets.objects.create_weighing(piglets_group=piglets3, total_weight=2600, 
            place='8/6')

        # mixed tour piglets
        piglets4 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws5, 30)
        piglets5 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour2,
            self.loc_ws5, 70)
        loc_cell_ws5_3 = Location.objects.filter(pigletsGroupCell__workshop__number=5)[2]
        merged_piglets1 = PigletsMerger.objects.create_merger_return_group(
            parent_piglets=[piglets4, piglets5], new_location=loc_cell_ws5_3)
        WeighingPiglets.objects.create_weighing(piglets_group=merged_piglets1, total_weight=1000,
         place='8/7')

        piglets6 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws5, 50)
        piglets7 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour2,
            self.loc_ws5, 50)
        loc_cell_ws5_4 = Location.objects.filter(pigletsGroupCell__workshop__number=5)[3]
        merged_piglets2 = PigletsMerger.objects.create_merger_return_group(
            parent_piglets=[piglets6, piglets7], new_location=loc_cell_ws5_4)
        w2 = WeighingPiglets.objects.create_weighing(piglets_group=merged_piglets2, 
            total_weight=1000,  place='8/7',
            date=datetime.datetime.now() + datetime.timedelta(days=21))

        merged_piglets1.deactivate()

        with self.assertNumQueries(1):
            tours = Tour.objects.all() \
                .add_week_weight() \
                .add_week_weight_ws8_v2()
            bool(tours)
            self.assertEqual(tours[0].week_weight_qnty_ws8, 300)
            self.assertEqual(round(tours[0].week_weight_avg_ws8, 2), 15.67)

    def test_add_culling_data_by_ws_week_tour(self):
        piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws5, 100)
        CullingPiglets.objects.create_culling_piglets(piglets_group=piglets1, culling_type='padej',
         quantity=1, total_weight=19)

        piglets3 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws5, 100)
        CullingPiglets.objects.create_culling_piglets(piglets_group=piglets3, culling_type='padej',
         quantity=5, total_weight=51)

        loc2 = Location.objects.get(workshop__number=6)
        piglets2 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            loc2, 100)
        CullingPiglets.objects.create_culling_piglets(piglets_group=piglets2, culling_type='prirezka',
         quantity=4, total_weight=42)

         # less tour1 30/70
        piglets4 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws5, 30)
        piglets5 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour2,
            self.loc_ws5, 70)
        loc_cell_ws5_3 = Location.objects.filter(pigletsGroupCell__workshop__number=5)[2]
        merged_piglets1 = PigletsMerger.objects.create_merger_return_group(
            parent_piglets=[piglets4, piglets5], new_location=loc_cell_ws5_3)
        CullingPiglets.objects.create_culling_piglets(piglets_group=merged_piglets1,
         culling_type='spec', quantity=10, total_weight=190)

        CullingPiglets.objects.create_culling_piglets(piglets_group=merged_piglets1,
         culling_type='spec', quantity=5, total_weight=50)

        # more tour 1 80/20
        piglets8 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws5, 80)
        piglets9 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour2,
            self.loc_ws5, 20)
        loc_cell_ws5_5 = Location.objects.filter(pigletsGroupCell__workshop__number=5)[4]
        merged_piglets3 = PigletsMerger.objects.create_merger_return_group(
            parent_piglets=[piglets8, piglets9], new_location=loc_cell_ws5_5)
        CullingPiglets.objects.create_culling_piglets(piglets_group=merged_piglets3,
         culling_type='padej', quantity=20, total_weight=400)

        with self.assertNumQueries(1):
            tours = Tour.objects.all().add_culling_data_by_week_tour()
            bool(tours)
            self.assertEqual(tours[0].ws5_padej_quantity, 26)
            self.assertEqual(tours[1].ws5_spec_avg_weight, 14.5)


# class TourQuerysetAddPigletsData2Test(TestCase):
#     def setUp(self):
#         locations_testing.create_workshops_sections_and_cells()
#         pigs_testings.create_statuses()
#         sows_events_testing.create_types()
#         piglets_testing.create_piglets_statuses()

#         self.tour1 = Tour.objects.get_or_create_by_week_in_current_year(week_number=1)
#         self.tour2 = Tour.objects.get_or_create_by_week_in_current_year(week_number=2)

#         self.loc_ws5 = Location.objects.get(workshop__number=5)

#     def test_week_culling(self):
#         piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
#             self.loc_ws5, 100)

#         piglets3 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour2,
#             self.loc_ws5, 100)

#         # less tour1 30/70
#         piglets4 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
#             self.loc_ws5, 30)
#         piglets5 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour2,
#             self.loc_ws5, 70)
#         loc_cell_ws5_3 = Location.objects.filter(pigletsGroupCell__workshop__number=5)[2]
#         merged_piglets1 = PigletsMerger.objects.create_merger_return_group(
#             parent_piglets=[piglets4, piglets5], new_location=loc_cell_ws5_3)

#         # 50/50
#         piglets6 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
#             self.loc_ws5, 50)
#         piglets7 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour2,
#             self.loc_ws5, 50)
#         loc_cell_ws5_4 = Location.objects.filter(pigletsGroupCell__workshop__number=5)[3]
#         merged_piglets2 = PigletsMerger.objects.create_merger_return_group(
#             parent_piglets=[piglets6, piglets7], new_location=loc_cell_ws5_4)

#         # more tour 1 80/20
#         piglets8 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
#             self.loc_ws5, 80)
#         piglets9 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour2,
#             self.loc_ws5, 20)
#         loc_cell_ws5_5 = Location.objects.filter(pigletsGroupCell__workshop__number=5)[4]
#         merged_piglets3 = PigletsMerger.objects.create_merger_return_group(
#             parent_piglets=[piglets8, piglets9], new_location=loc_cell_ws5_5)

#         piglets = Piglets.objects.filter(metatour__records__tour=self.tour1,
#              metatour__records__percentage__lt=100)
        # print(piglets)

        # print(piglets.values('metatour__records'))
        # print(piglets.values('metatour__records').values('metatour__records__tour'))


class TourQuerysetAddSowsDataTest(TestCase):
    def setUp(self):
        locations_testing.create_workshops_sections_and_cells()
        pigs_testings.create_statuses()
        sows_events_testing.create_types()
        piglets_testing.create_piglets_statuses()

    def test_add_sow_data_seminated(self):
        loc_ws1 = Location.objects.get(workshop__number=1)

        sow3 = pigs_testings.create_sow_with_location(loc_ws1)
        Semination.objects.create_semination(sow=sow3, week=1)
        Semination.objects.create_semination(sow=sow3, week=1)

        sow4 = pigs_testings.create_sow_with_location(loc_ws1)
        Semination.objects.create_semination(sow=sow4, week=1)
        Semination.objects.create_semination(sow=sow4, week=1)

        sow7 = pigs_testings.create_sow_with_location(loc_ws1)
        Semination.objects.create_semination(sow=sow7, week=1)

        sow8 = pigs_testings.create_sow_with_location(loc_ws1)
        Semination.objects.create_semination(sow=sow8, week=2)
        Semination.objects.create_semination(sow=sow8, week=2)

        sow9 = pigs_testings.create_sow_with_location(loc_ws1)
        
        sows_seminated = Semination.objects.filter(tour__week_number=1).values_list('sow')
        count_seminated = Sow.objects.filter(pk__in=sows_seminated).distinct().count()
        bool(count_seminated)

        with self.assertNumQueries(1):
            tours = Tour.objects.all().add_farrow_data().add_sow_data()
            bool(tours)
            self.assertEqual(tours[0].count_seminated, count_seminated)
            
    def test_add_sow_data_usound_abort(self):
        loc_ws1 = Location.objects.get(workshop__number=1)

        sow3 = pigs_testings.create_sow_with_location(loc_ws1)
        Semination.objects.create_semination(sow=sow3, week=1)
        Semination.objects.create_semination(sow=sow3, week=1)

        sow4 = pigs_testings.create_sow_with_location(loc_ws1)
        Semination.objects.create_semination(sow=sow4, week=1)
        Semination.objects.create_semination(sow=sow4, week=1)
        Ultrasound.objects.create_ultrasound(sow=sow4, result=True, days=30)
        Ultrasound.objects.create_ultrasound(sow=sow4, result=True, days=60)

        sow5 = pigs_testings.create_sow_with_location(loc_ws1)
        Semination.objects.create_semination(sow=sow5, week=1)
        Semination.objects.create_semination(sow=sow5, week=1)
        Ultrasound.objects.create_ultrasound(sow=sow5, result=False, days=30)

        sow6 = pigs_testings.create_sow_with_location(loc_ws1)
        Semination.objects.create_semination(sow=sow6, week=1)
        Semination.objects.create_semination(sow=sow6, week=1)
        Ultrasound.objects.create_ultrasound(sow=sow6, result=True, days=30)
        Ultrasound.objects.create_ultrasound(sow=sow6, result=False, days=60)

        sow12 = pigs_testings.create_sow_with_location(loc_ws1)
        Semination.objects.create_semination(sow=sow12, week=1)
        Semination.objects.create_semination(sow=sow12, week=1)
        Ultrasound.objects.create_ultrasound(sow=sow12, result=True, days=30)
        Ultrasound.objects.create_ultrasound(sow=sow12, result=True, days=60)

        sow13 = pigs_testings.create_sow_with_location(loc_ws1)
        Semination.objects.create_semination(sow=sow13, week=2)
        Semination.objects.create_semination(sow=sow13, week=2)
        Ultrasound.objects.create_ultrasound(sow=sow13, result=True, days=30)
        Ultrasound.objects.create_ultrasound(sow=sow13, result=True, days=60)

        AbortionSow.objects.create_abortion(sow=sow13)

        sow7 = pigs_testings.create_sow_with_location(loc_ws1)
        Semination.objects.create_semination(sow=sow7, week=1)

        sow8 = pigs_testings.create_sow_with_location(loc_ws1)
        Semination.objects.create_semination(sow=sow8, week=2)
        Semination.objects.create_semination(sow=sow8, week=2)

        sow9 = pigs_testings.create_sow_with_location(loc_ws1)

        sow10 = pigs_testings.create_sow_with_location(loc_ws1)
        Semination.objects.create_semination(sow=sow10, week=1)
        Semination.objects.create_semination(sow=sow10, week=1)
        Ultrasound.objects.create_ultrasound(sow=sow10, result=False, days=30)

        sow11 = pigs_testings.create_sow_with_location(loc_ws1)
        Semination.objects.create_semination(sow=sow11, week=2)
        Semination.objects.create_semination(sow=sow11, week=2)
        Ultrasound.objects.create_ultrasound(sow=sow11, result=True, days=30)
        Ultrasound.objects.create_ultrasound(sow=sow11, result=False, days=60)

        sow14 = pigs_testings.create_sow_with_location(loc_ws1)
        Semination.objects.create_semination(sow=sow13, week=2)
        Semination.objects.create_semination(sow=sow13, week=2)
        Ultrasound.objects.create_ultrasound(sow=sow13, result=True, days=30)
        Ultrasound.objects.create_ultrasound(sow=sow13, result=True, days=60)
        
        with self.assertNumQueries(1):
            tours = Tour.objects.all().add_sow_data()
            bool(tours)
            self.assertEqual(tours[0].count_usound28_suporos, 3)
            self.assertEqual(tours[0].count_usound28_proholost, 2)
            self.assertEqual(tours[0].count_usound35_suporos, 2)
            self.assertEqual(tours[0].count_usound35_proholost, 1)
            self.assertEqual(tours[1].count_abort, 1)

    def test_count_tour_sow(self):
        loc_ws1 = Location.objects.get(workshop__number=1)
        loc_ws2 = Location.objects.get(workshop__number=2)
        loc_ws3 = Location.objects.get(workshop__number=3)

        sow1 = pigs_testings.create_sow_with_location(loc_ws1)
        Semination.objects.create_semination(sow=sow1, week=1)

        sow2 = pigs_testings.create_sow_with_location(loc_ws1)
        Semination.objects.create_semination(sow=sow2, week=1)

        sow3 = pigs_testings.create_sow_with_location(loc_ws2)
        Semination.objects.create_semination(sow=sow3, week=1)

        sow4 = pigs_testings.create_sow_with_location(loc_ws3)
        Semination.objects.create_semination(sow=sow4, week=1)

        sow5 = pigs_testings.create_sow_with_location(loc_ws3)
        Semination.objects.create_semination(sow=sow5, week=2)
        sow6 = pigs_testings.create_sow_with_location(loc_ws3)
        Semination.objects.create_semination(sow=sow6, week=2)

        with self.assertNumQueries(1):
            tours = Tour.objects.all().add_count_tour_sow()
            bool(tours)
            self.assertEqual(tours[0].ws1_count_tour_sow,2)
            self.assertEqual(tours[0].ws3_count_tour_sow,1)

    def test_add_sow_events(self):
        loc_ws1 = Location.objects.get(workshop__number=1)
        sow1 = pigs_testings.create_sow_with_location(loc_ws1)
        Semination.objects.create_semination(sow=sow1, week=2)
        Semination.objects.create_semination(sow=sow1, week=2)
        Ultrasound.objects.create_ultrasound(sow=sow1, result=True, days=30)
        Ultrasound.objects.create_ultrasound(sow=sow1, result=False, days=60)

        Semination.objects.create_semination(sow=sow1, week=3)
        Semination.objects.create_semination(sow=sow1, week=3)
        Ultrasound.objects.create_ultrasound(sow=sow1, result=True, days=30)
        Ultrasound.objects.create_ultrasound(sow=sow1, result=True, days=60)

        sow3 = pigs_testings.create_sow_with_location(loc_ws1)
        Semination.objects.create_semination(sow=sow3, week=3)
        Semination.objects.create_semination(sow=sow3, week=3)
        Ultrasound.objects.create_ultrasound(sow=sow3, result=True, days=30)
        Ultrasound.objects.create_ultrasound(sow=sow3, result=False, days=60)

        sow1_tours = Tour.objects.filter(pk__in=sow1.get_tours_pk()).add_sow_events(sow=sow1)

        self.assertEqual(len(sow1_tours), 2)
        self.assertEqual(sow1_tours[0].sow_semination[0].sow, sow1)
        self.assertEqual(sow1_tours[0].sow_semination[1].tour.week_number, 2)
        self.assertEqual(sow1_tours[0].sow_ultrasound[0].tour.week_number, 2)
        self.assertEqual(sow1_tours[1].sow_semination[0].sow, sow1)
        self.assertEqual(sow1_tours[1].sow_semination[1].tour.week_number, 3)


class MetaTourTest(TestCase):
    def setUp(self):
        locations_testing.create_workshops_sections_and_cells()
        pigs_testings.create_statuses()
        sows_events_testing.create_types()
        piglets_testing.create_piglets_statuses()

        self.tour1 = Tour.objects.get_or_create_by_week_in_current_year(week_number=1)
        self.tour2 = Tour.objects.get_or_create_by_week_in_current_year(week_number=2)
        self.tour3 = Tour.objects.get_or_create_by_week_in_current_year(week_number=3)
        self.tour4 = Tour.objects.get_or_create_by_week_in_current_year(week_number=4)
        self.tour52 = Tour.objects.get_or_create_by_week(week_number=52, year=2019)
        self.tour51 = Tour.objects.get_or_create_by_week(week_number=51, year=2019)
        self.loc_ws5 = Location.objects.get(workshop__number=5)

    def test_set_week_tour1(self):
        # one metarecord
        piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws5, 100)

        piglets1.metatour.set_week_tour()
        self.assertEqual(piglets1.metatour.week_tour, self.tour1)

    def test_set_week_tour2(self):
        # two metarecord
        # less tour1 30/70
        piglets4 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws5, 30)
        piglets5 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour2,
            self.loc_ws5, 70)
        loc_cell_ws5_3 = Location.objects.filter(pigletsGroupCell__workshop__number=5)[2]
        merged_piglets1 = PigletsMerger.objects.create_merger_return_group(
            parent_piglets=[piglets4, piglets5], new_location=loc_cell_ws5_3)

        merged_piglets1.metatour.set_week_tour()
        self.assertEqual(merged_piglets1.metatour.week_tour, self.tour2)

    def test_set_week_tour3(self):
        # two metarecord
        # equal 50/50
        piglets4 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws5, 50)
        piglets5 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour2,
            self.loc_ws5, 50)
        loc_cell_ws5_3 = Location.objects.filter(pigletsGroupCell__workshop__number=5)[2]
        merged_piglets1 = PigletsMerger.objects.create_merger_return_group(
            parent_piglets=[piglets4, piglets5], new_location=loc_cell_ws5_3)

        merged_piglets1.metatour.set_week_tour()
        self.assertEqual(merged_piglets1.metatour.week_tour, self.tour1)

    def test_set_week_tour4(self):
        # four metarecord
        # equal, same year 
        piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws5, 50)
        piglets2 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour2,
            self.loc_ws5, 50)
        piglets3 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour3,
            self.loc_ws5, 50)
        piglets4 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour4,
            self.loc_ws5, 50)
        loc_cell_ws5_3 = Location.objects.filter(pigletsGroupCell__workshop__number=5)[2]
        merged_piglets1 = PigletsMerger.objects.create_merger_return_group(
            parent_piglets=[piglets1, piglets2, piglets3, piglets4], new_location=loc_cell_ws5_3)

        merged_piglets1.metatour.set_week_tour()
        self.assertEqual(merged_piglets1.metatour.week_tour, self.tour1)

    def test_set_week_tour5(self):
        # four metarecord
        # one less, same year 
        piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws5, 45)
        piglets2 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour2,
            self.loc_ws5, 50)
        piglets3 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour3,
            self.loc_ws5, 50)
        piglets4 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour4,
            self.loc_ws5, 50)
        loc_cell_ws5_3 = Location.objects.filter(pigletsGroupCell__workshop__number=5)[2]
        merged_piglets1 = PigletsMerger.objects.create_merger_return_group(
            parent_piglets=[piglets1, piglets2, piglets3, piglets4], new_location=loc_cell_ws5_3)

        merged_piglets1.metatour.set_week_tour()
        self.assertEqual(merged_piglets1.metatour.week_tour, self.tour2)

    def test_set_week_tour6(self):
        # four metarecord
        # equal, not same year 
        piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws5, 50)
        piglets2 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour2,
            self.loc_ws5, 50)
        piglets3 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour3,
            self.loc_ws5, 50)
        piglets4 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour52,
            self.loc_ws5, 50)
        loc_cell_ws5_3 = Location.objects.filter(pigletsGroupCell__workshop__number=5)[2]
        merged_piglets1 = PigletsMerger.objects.create_merger_return_group(
            parent_piglets=[piglets1, piglets2, piglets3, piglets4], new_location=loc_cell_ws5_3)

        merged_piglets1.metatour.set_week_tour()
        self.assertEqual(merged_piglets1.metatour.week_tour, self.tour52)

    def test_set_week_tour7(self):
        # four metarecord
        # equal, not same year 
        piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws5, 50)
        piglets2 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour2,
            self.loc_ws5, 50)
        piglets3 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour51,
            self.loc_ws5, 50)
        piglets4 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour52,
            self.loc_ws5, 50)
        loc_cell_ws5_3 = Location.objects.filter(pigletsGroupCell__workshop__number=5)[2]
        merged_piglets1 = PigletsMerger.objects.create_merger_return_group(
            parent_piglets=[piglets1, piglets2, piglets3, piglets4], new_location=loc_cell_ws5_3)

        merged_piglets1.metatour.set_week_tour()
        self.assertEqual(merged_piglets1.metatour.week_tour, self.tour51)


class TourQuerysetAddWeighingData(TestCase):
    def setUp(self):
        locations_testing.create_workshops_sections_and_cells()
        pigs_testings.create_statuses()
        sows_events_testing.create_types()
        piglets_testing.create_piglets_statuses()

        self.tour1 = Tour.objects.get_or_create_by_week_in_current_year(week_number=1)
        self.tour2 = Tour.objects.get_or_create_by_week_in_current_year(week_number=2)

        self.loc_ws4 = Location.objects.get(workshop__number=4)

    def test_add_weighing_first_dates(self):
        piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(
            tour=self.tour1,
            location=self.loc_ws4,
            quantity=100,
            birthday=datetime.datetime(2020,5,5,0,0)
            )
        piglets2 = piglets_testing.create_new_group_with_metatour_by_one_tour(
            tour=self.tour1,
            location=self.loc_ws4,
            quantity=100,
            birthday=datetime.datetime(2020,5,8,0,0)
            )

        WeighingPiglets.objects.create_weighing(piglets_group=piglets1, total_weight=120,
            place='3/4', date=datetime.datetime.today())

        WeighingPiglets.objects.create_weighing(piglets_group=piglets2, total_weight=360,
            place='4/8', date=datetime.datetime(2020,9,15,0,0))

        with self.assertNumQueries(1):
            tours = Tour.objects.all().add_weighing_first_dates()
            bool(tours)
            self.assertEqual(tours[0].first_date_3_4, datetime.date.today())
            self.assertEqual(tours[0].first_date_4_8, datetime.date(2020,9,15))
            # self.assertEqual(tours[0].ws1_count_tour_sow,2)


class TourQuerysetAddDataByWs(TestCase):
    def setUp(self):
        locations_testing.create_workshops_sections_and_cells()
        pigs_testings.create_statuses()
        sows_events_testing.create_types()
        piglets_testing.create_piglets_statuses()

        self.tour1 = Tour.objects.get_or_create_by_week_in_current_year(week_number=1)
        self.tour2 = Tour.objects.get_or_create_by_week_in_current_year(week_number=2)

        self.loc_ws4 = Location.objects.get(workshop__number=4)
        self.loc_ws4_cells = Location.objects.filter(pigletsGroupCell__workshop__number=4)
        self.loc_ws5_cells = Location.objects.filter(pigletsGroupCell__workshop__number=5)
        self.loc_ws6_cells = Location.objects.filter(pigletsGroupCell__workshop__number=6)

    def test_add_weight_data_by_place(self):
        piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(
            tour=self.tour1,
            location=self.loc_ws4,
            quantity=100,
            birthday=datetime.datetime(2020,5,5,0,0)
            )
        piglets2 = piglets_testing.create_new_group_with_metatour_by_one_tour(
            tour=self.tour1,
            location=self.loc_ws4,
            quantity=100,
            birthday=datetime.datetime(2020,5,8,0,0)
            )

        WeighingPiglets.objects.create_weighing(piglets_group=piglets1, total_weight=120,
            place='8/5', date=datetime.datetime.today())

        WeighingPiglets.objects.create_weighing(piglets_group=piglets2, total_weight=360,
            place='8/5', date=datetime.datetime(2020,9,15,0,0))

        WeighingPiglets.objects.create_weighing(piglets_group=piglets2, total_weight=360,
            place='8/6', date=datetime.datetime(2020,9,15,0,0))
        
        tours = Tour.objects.all().add_weight_data_by_place(place='8/5')
        self.assertEqual(tours[0].weight_quantity, 200)
        self.assertEqual(tours[0].weight_avg, 2.4)
        self.assertEqual(tours[0].weight_total, 480)
        self.assertEqual(tours[1].weight_quantity, None)

    def test_add_culling_data_by_ws(self):
        piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(
            tour=self.tour1,
            location=self.loc_ws5_cells[0],
            quantity=100,
            birthday=datetime.datetime(2020,5,5,0,0)
            )
        piglets2 = piglets_testing.create_new_group_with_metatour_by_one_tour(
            tour=self.tour2,
            location=self.loc_ws5_cells[1],
            quantity=100,
            birthday=datetime.datetime(2020,5,8,0,0)
            )


        CullingPiglets.objects.create_culling_piglets(piglets_group=piglets1,
         culling_type='spec', quantity=20, total_weight=400)

        CullingPiglets.objects.create_culling_piglets(piglets_group=piglets1,
         culling_type='spec', quantity=12, total_weight=250)

        CullingPiglets.objects.create_culling_piglets(piglets_group=piglets2,
         culling_type='spec', quantity=10, total_weight=230)
        
        tours = Tour.objects.all().add_culling_data_by_ws(ws_number=5, culling_type='spec')
        self.assertEqual(tours[0].spec_quantity, 32)
        self.assertEqual(tours[0].spec_total, 650)
        self.assertEqual(round(tours[0].spec_avg, 2), 20.42)
        self.assertEqual(tours[1].spec_quantity, 10)
        self.assertEqual(tours[1].spec_total, 230)

        tours = Tour.objects.all().add_culling_data_by_ws(ws_number=5, culling_type='padej')
        CullingPiglets.objects.create_culling_piglets(piglets_group=piglets2,
         culling_type='padej', quantity=5, total_weight=120)
        self.assertEqual(tours[0].padej_quantity, None)
        self.assertEqual(tours[1].padej_quantity, 5)
        self.assertEqual(tours[1].padej_total, 120)
        self.assertEqual(tours[1].padej_avg, 24)

    def test_culling_percentage(self):
        piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(
            tour=self.tour1,
            location=self.loc_ws5_cells[0],
            quantity=100,
            birthday=datetime.datetime(2020,5,5,0,0)
            )
        piglets2 = piglets_testing.create_new_group_with_metatour_by_one_tour(
            tour=self.tour2,
            location=self.loc_ws5_cells[1],
            quantity=100,
            birthday=datetime.datetime(2020,5,8,0,0)
            )

        WeighingPiglets.objects.create_weighing(piglets_group=piglets1, total_weight=120,
            place='8/5', )

        WeighingPiglets.objects.create_weighing(piglets_group=piglets2, total_weight=360,
            place='8/5', )

        CullingPiglets.objects.create_culling_piglets(piglets_group=piglets1,
         culling_type='padej', quantity=20, total_weight=400)

        CullingPiglets.objects.create_culling_piglets(piglets_group=piglets1,
         culling_type='vinuzhd', quantity=12, total_weight=250)

        CullingPiglets.objects.create_culling_piglets(piglets_group=piglets2,
         culling_type='padej', quantity=5, total_weight=120)

        CullingPiglets.objects.create_culling_piglets(piglets_group=piglets2,
         culling_type='vinuzhd', quantity=16, total_weight=250)

        piglets3 = piglets_testing.create_new_group_with_metatour_by_one_tour(
            tour=self.tour1,
            location=self.loc_ws6_cells[0],
            quantity=200,
            birthday=datetime.datetime(2020,5,5,0,0)
            )
        piglets4 = piglets_testing.create_new_group_with_metatour_by_one_tour(
            tour=self.tour2,
            location=self.loc_ws6_cells[1],
            quantity=200,
            birthday=datetime.datetime(2020,5,8,0,0)
            )

        WeighingPiglets.objects.create_weighing(piglets_group=piglets3, total_weight=120,
            place='8/6', )

        WeighingPiglets.objects.create_weighing(piglets_group=piglets4, total_weight=360,
            place='8/6', )

        CullingPiglets.objects.create_culling_piglets(piglets_group=piglets3,
         culling_type='padej', quantity=20, total_weight=400)

        CullingPiglets.objects.create_culling_piglets(piglets_group=piglets3,
         culling_type='vinuzhd', quantity=12, total_weight=250)

        CullingPiglets.objects.create_culling_piglets(piglets_group=piglets4,
         culling_type='padej', quantity=5, total_weight=120)

        CullingPiglets.objects.create_culling_piglets(piglets_group=piglets4,
         culling_type='vinuzhd', quantity=16, total_weight=250)

        piglets5 = piglets_testing.create_new_group_with_metatour_by_one_tour(
            tour=self.tour1,
            location=self.loc_ws4_cells[0],
            quantity=200,
            birthday=datetime.datetime(2020,5,5,0,0)
            )
        piglets6 = piglets_testing.create_new_group_with_metatour_by_one_tour(
            tour=self.tour2,
            location=self.loc_ws4_cells[1],
            quantity=200,
            birthday=datetime.datetime(2020,5,8,0,0)
            )

        WeighingPiglets.objects.create_weighing(piglets_group=piglets5, total_weight=120,
            place='3/4', )

        WeighingPiglets.objects.create_weighing(piglets_group=piglets6, total_weight=360,
            place='3/4', )

        CullingPiglets.objects.create_culling_piglets(piglets_group=piglets5,
         culling_type='padej', quantity=20, total_weight=400)

        CullingPiglets.objects.create_culling_piglets(piglets_group=piglets5,
         culling_type='vinuzhd', quantity=12, total_weight=250)

        CullingPiglets.objects.create_culling_piglets(piglets_group=piglets6,
         culling_type='padej', quantity=5, total_weight=120)

        CullingPiglets.objects.create_culling_piglets(piglets_group=piglets6,
         culling_type='vinuzhd', quantity=16, total_weight=250)

        tours = Tour.objects.all() \
            .add_week_weight(places=['3/4', '4/8','8/5', '8/6', '8/7']) \
            .add_week_weight_ws8_v2() \
            .add_culling_data_by_week_tour(ws_numbers=[4, 8, 5, 6, 7]) \
            .add_culling_percentage(ws_numbers=[4, 8, 5, 6, 7])

        self.assertEqual(tours[0].ws5_padej_percentage, 20)
        self.assertEqual(tours[0].ws5_vinuzhd_percentage, 12)
        self.assertEqual(tours[1].ws5_padej_percentage, 5)
        self.assertEqual(tours[1].ws5_vinuzhd_percentage, 16)

        self.assertEqual(tours[0].ws6_padej_percentage, 10)
        self.assertEqual(tours[0].ws6_vinuzhd_percentage, 6)
        self.assertEqual(tours[1].ws6_padej_percentage, 2.5)
        self.assertEqual(tours[1].ws6_vinuzhd_percentage, 8)

        self.assertEqual(tours[0].ws4_padej_percentage, 10)
        self.assertEqual(tours[0].ws4_vinuzhd_percentage, 6)
        self.assertEqual(tours[1].ws4_padej_percentage, 2.5)
        self.assertEqual(tours[1].ws4_vinuzhd_percentage, 8)

    def test_add_culling_percentage_by_ws_exclude_ws3(self):
        piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(
            tour=self.tour1,
            location=self.loc_ws5_cells[0],
            quantity=100,
            birthday=datetime.datetime(2020,5,5,0,0)
            )
        piglets2 = piglets_testing.create_new_group_with_metatour_by_one_tour(
            tour=self.tour2,
            location=self.loc_ws5_cells[1],
            quantity=100,
            birthday=datetime.datetime(2020,5,8,0,0)
            )

        WeighingPiglets.objects.create_weighing(piglets_group=piglets1, total_weight=120,
            place='8/5', )

        WeighingPiglets.objects.create_weighing(piglets_group=piglets2, total_weight=360,
            place='8/5', )

        CullingPiglets.objects.create_culling_piglets(piglets_group=piglets1,
         culling_type='padej', quantity=20, total_weight=400)

        CullingPiglets.objects.create_culling_piglets(piglets_group=piglets1,
         culling_type='vinuzhd', quantity=12, total_weight=250)

        CullingPiglets.objects.create_culling_piglets(piglets_group=piglets2,
         culling_type='padej', quantity=5, total_weight=120)

        CullingPiglets.objects.create_culling_piglets(piglets_group=piglets2,
         culling_type='vinuzhd', quantity=16, total_weight=250)

        piglets3 = piglets_testing.create_new_group_with_metatour_by_one_tour(
            tour=self.tour1,
            location=self.loc_ws6_cells[0],
            quantity=200,
            birthday=datetime.datetime(2020,5,5,0,0)
            )
        piglets4 = piglets_testing.create_new_group_with_metatour_by_one_tour(
            tour=self.tour2,
            location=self.loc_ws6_cells[1],
            quantity=200,
            birthday=datetime.datetime(2020,5,8,0,0)
            )

        WeighingPiglets.objects.create_weighing(piglets_group=piglets3, total_weight=120,
            place='8/6', )

        WeighingPiglets.objects.create_weighing(piglets_group=piglets4, total_weight=360,
            place='8/6', )

        CullingPiglets.objects.create_culling_piglets(piglets_group=piglets3,
         culling_type='padej', quantity=20, total_weight=400)

        CullingPiglets.objects.create_culling_piglets(piglets_group=piglets3,
         culling_type='vinuzhd', quantity=12, total_weight=250)

        CullingPiglets.objects.create_culling_piglets(piglets_group=piglets4,
         culling_type='padej', quantity=5, total_weight=120)

        CullingPiglets.objects.create_culling_piglets(piglets_group=piglets4,
         culling_type='vinuzhd', quantity=16, total_weight=250)

        piglets5 = piglets_testing.create_new_group_with_metatour_by_one_tour(
            tour=self.tour1,
            location=self.loc_ws4_cells[0],
            quantity=200,
            birthday=datetime.datetime(2020,5,5,0,0)
            )
        piglets6 = piglets_testing.create_new_group_with_metatour_by_one_tour(
            tour=self.tour2,
            location=self.loc_ws4_cells[1],
            quantity=200,
            birthday=datetime.datetime(2020,5,8,0,0)
            )

        WeighingPiglets.objects.create_weighing(piglets_group=piglets5, total_weight=120,
            place='3/4', )

        WeighingPiglets.objects.create_weighing(piglets_group=piglets6, total_weight=360,
            place='3/4', )

        CullingPiglets.objects.create_culling_piglets(piglets_group=piglets5,
         culling_type='padej', quantity=20, total_weight=400)

        CullingPiglets.objects.create_culling_piglets(piglets_group=piglets5,
         culling_type='vinuzhd', quantity=12, total_weight=250)

        CullingPiglets.objects.create_culling_piglets(piglets_group=piglets6,
         culling_type='padej', quantity=5, total_weight=120)

        CullingPiglets.objects.create_culling_piglets(piglets_group=piglets6,
         culling_type='vinuzhd', quantity=16, total_weight=250)

        tours = Tour.objects.all() \
            .add_week_weight(places=['3/4','8/5', '8/6', '8/7']) \
            .add_week_weight_ws8_v2() \
            .add_culling_data_by_week_tour(ws_numbers=[4, 5, 6, 7]) \
            .add_culling_percentage_by_ws_exclude_ws3(ws_number=4, place_number='3_4') \
            .add_culling_percentage_by_ws_exclude_ws3(ws_number=5, place_number='8_5') \
            .add_culling_percentage_by_ws_exclude_ws3(ws_number=6, place_number='8_6') \
            .add_culling_percentage_by_ws_exclude_ws3(ws_number=7, place_number='8_7') \

        self.assertEqual(tours[0].ws5_padej_percentage, 20)
        self.assertEqual(tours[0].ws5_vinuzhd_percentage, 12)
        self.assertEqual(tours[1].ws5_padej_percentage, 5)
        self.assertEqual(tours[1].ws5_vinuzhd_percentage, 16)

        self.assertEqual(tours[0].ws6_padej_percentage, 10)
        self.assertEqual(tours[0].ws6_vinuzhd_percentage, 6)
        self.assertEqual(tours[1].ws6_padej_percentage, 2.5)
        self.assertEqual(tours[1].ws6_vinuzhd_percentage, 8)

        self.assertEqual(tours[0].ws4_padej_percentage, 10)
        self.assertEqual(tours[0].ws4_vinuzhd_percentage, 6)
        self.assertEqual(tours[1].ws4_padej_percentage, 2.5)
        self.assertEqual(tours[1].ws4_vinuzhd_percentage, 8)

    def test_add_culling_percentage_otkorm(self):
        piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(
            tour=self.tour1,
            location=self.loc_ws5_cells[0],
            quantity=100,
            birthday=datetime.datetime(2020,5,5,0,0)
            )
        piglets2 = piglets_testing.create_new_group_with_metatour_by_one_tour(
            tour=self.tour2,
            location=self.loc_ws5_cells[1],
            quantity=100,
            birthday=datetime.datetime(2020,5,8,0,0)
            )

        WeighingPiglets.objects.create_weighing(piglets_group=piglets1, total_weight=120,
            place='8/5', )

        WeighingPiglets.objects.create_weighing(piglets_group=piglets2, total_weight=360,
            place='8/5', )

        CullingPiglets.objects.create_culling_piglets(piglets_group=piglets1,
         culling_type='padej', quantity=20, total_weight=400)

        CullingPiglets.objects.create_culling_piglets(piglets_group=piglets1,
         culling_type='vinuzhd', quantity=12, total_weight=250)

        CullingPiglets.objects.create_culling_piglets(piglets_group=piglets2,
         culling_type='padej', quantity=5, total_weight=120)

        CullingPiglets.objects.create_culling_piglets(piglets_group=piglets2,
         culling_type='vinuzhd', quantity=16, total_weight=250)

        piglets3 = piglets_testing.create_new_group_with_metatour_by_one_tour(
            tour=self.tour1,
            location=self.loc_ws6_cells[0],
            quantity=200,
            birthday=datetime.datetime(2020,5,5,0,0)
            )
        piglets4 = piglets_testing.create_new_group_with_metatour_by_one_tour(
            tour=self.tour2,
            location=self.loc_ws6_cells[1],
            quantity=200,
            birthday=datetime.datetime(2020,5,8,0,0)
            )

        WeighingPiglets.objects.create_weighing(piglets_group=piglets3, total_weight=120,
            place='8/6', )

        WeighingPiglets.objects.create_weighing(piglets_group=piglets4, total_weight=360,
            place='8/6', )

        CullingPiglets.objects.create_culling_piglets(piglets_group=piglets3,
         culling_type='padej', quantity=20, total_weight=400)

        CullingPiglets.objects.create_culling_piglets(piglets_group=piglets3,
         culling_type='vinuzhd', quantity=12, total_weight=250)

        CullingPiglets.objects.create_culling_piglets(piglets_group=piglets4,
         culling_type='padej', quantity=5, total_weight=120)

        CullingPiglets.objects.create_culling_piglets(piglets_group=piglets4,
         culling_type='vinuzhd', quantity=16, total_weight=250)

        piglets5 = piglets_testing.create_new_group_with_metatour_by_one_tour(
            tour=self.tour1,
            location=self.loc_ws4_cells[0],
            quantity=200,
            birthday=datetime.datetime(2020,5,5,0,0)
            )
        piglets6 = piglets_testing.create_new_group_with_metatour_by_one_tour(
            tour=self.tour2,
            location=self.loc_ws4_cells[1],
            quantity=200,
            birthday=datetime.datetime(2020,5,8,0,0)
            )

        WeighingPiglets.objects.create_weighing(piglets_group=piglets5, total_weight=120,
            place='3/4', )

        WeighingPiglets.objects.create_weighing(piglets_group=piglets6, total_weight=360,
            place='3/4', )

        CullingPiglets.objects.create_culling_piglets(piglets_group=piglets5,
         culling_type='padej', quantity=20, total_weight=400)

        CullingPiglets.objects.create_culling_piglets(piglets_group=piglets5,
         culling_type='vinuzhd', quantity=12, total_weight=250)

        CullingPiglets.objects.create_culling_piglets(piglets_group=piglets6,
         culling_type='padej', quantity=5, total_weight=120)

        CullingPiglets.objects.create_culling_piglets(piglets_group=piglets6,
         culling_type='vinuzhd', quantity=16, total_weight=250)

        tours = Tour.objects.all() \
            .add_week_weight(places=['3/4','8/5', '8/6', '8/7']) \
            .add_week_weight_ws8_v2() \
            .add_culling_data_by_week_tour(ws_numbers=[4, 5, 6, 7]) \
            .add_culling_percentage_by_ws_exclude_ws3(ws_number=4, place_number='3_4') \
            .add_culling_percentage_by_ws_exclude_ws3(ws_number=5, place_number='8_5') \
            .add_culling_percentage_by_ws_exclude_ws3(ws_number=6, place_number='8_6') \
            .add_culling_percentage_by_ws_exclude_ws3(ws_number=7, place_number='8_7') \
            .add_culling_percentage_otkorm()

        self.assertEqual(tours[0].week_weight_qnty_ws8, 300)

        self.assertEqual(tours[0].otkorm_padej_qnty, 40)
        self.assertEqual(round(tours[0].otkorm_padej_percentage, 2), 13.33)
        self.assertEqual(tours[0].otkorm_vinuzhd_qnty, 24)
        self.assertEqual(round(tours[0].otkorm_vinuzhd_percentage, 2), 8.0)

        self.assertEqual(tours[1].otkorm_padej_qnty, 10)
        self.assertEqual(round(tours[1].otkorm_padej_percentage, 2), 3.33)
        self.assertEqual(tours[1].otkorm_vinuzhd_qnty, 32)
        self.assertEqual(round(tours[1].otkorm_vinuzhd_percentage, 2), 10.67)

       
class TourQuerysetAddRemont(TestCase):
    def setUp(self):
        locations_testing.create_workshops_sections_and_cells()
        pigs_testings.create_statuses()
        sows_events_testing.create_types()
        piglets_testing.create_piglets_statuses()

        self.tour1 = Tour.objects.get_or_create_by_week_in_current_year(week_number=1)
        self.tour2 = Tour.objects.get_or_create_by_week_in_current_year(week_number=2)

        self.loc_ws4 = Location.objects.get(workshop__number=4)
        self.loc_ws2 = Location.objects.get(workshop__number=2)
        self.loc_ws5_cells = Location.objects.filter(pigletsGroupCell__workshop__number=5)
        self.loc_ws6_cells = Location.objects.filter(pigletsGroupCell__workshop__number=6)

    def test_add_remont_trs_out(self):
        piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(
            tour=self.tour1,
            location=self.loc_ws5_cells[0],
            quantity=100,
            birthday=datetime.datetime(2020,5,5,0,0)
            )
        piglets2 = piglets_testing.create_new_group_with_metatour_by_one_tour(
            tour=self.tour1,
            location=self.loc_ws6_cells[1],
            quantity=100,
            birthday=datetime.datetime(2020,5,8,0,0)
            )

        PigletsTransaction.objects.transaction_with_split_and_merge(
            piglets=piglets1,
            to_location=self.loc_ws2,
            new_amount=65
            )

        PigletsTransaction.objects.transaction_with_split_and_merge(
            piglets=piglets2,
            to_location=self.loc_ws2,
            new_amount=43
            )

        piglets3 = piglets_testing.create_new_group_with_metatour_by_one_tour(
            tour=self.tour2,
            location=self.loc_ws6_cells[1],
            quantity=100,
            birthday=datetime.datetime(2020,5,8,0,0)
            )

        PigletsTransaction.objects.transaction_with_split_and_merge(
            piglets=piglets3,
            to_location=self.loc_ws2,
            new_amount=29
            )

        tours = Tour.objects.all() \
                .add_farrow_data() \
                .add_sow_data() \
                .add_farrow_percentage() \
                .add_week_weight() \
                .add_week_weight_ws8_v2() \
                .add_culling_data_by_week_tour() \
                .add_culling_percentage() \
                .add_remont_trs_out() \
                
        self.assertEqual(tours[0].count_remont_total, 108)
        self.assertEqual(tours[0].ws5_remont, 65)
        self.assertEqual(tours[0].ws6_remont, 43)
        self.assertEqual(tours[0].ws7_remont, None)

        self.assertEqual(tours[1].count_remont_total, 29)
        self.assertEqual(tours[1].ws5_remont, None)
        self.assertEqual(tours[1].ws6_remont, 29)
        self.assertEqual(tours[1].ws7_remont, None)


class TourPrivesTest(TestCase):
    def setUp(self):
        locations_testing.create_workshops_sections_and_cells()
        pigs_testings.create_statuses()
        sows_events_testing.create_types()
        piglets_testing.create_piglets_statuses()

        self.tour1 = Tour.objects.get_or_create_by_week_in_current_year(week_number=1)
        self.tour2 = Tour.objects.get_or_create_by_week_in_current_year(week_number=2)

        self.loc_ws4 = Location.objects.get(workshop__number=4)
        self.loc_ws2 = Location.objects.get(workshop__number=2)
        self.loc_ws5_cells = Location.objects.filter(pigletsGroupCell__workshop__number=5)
        self.loc_ws6_cells = Location.objects.filter(pigletsGroupCell__workshop__number=6)

        self.piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(
            tour=self.tour1,
            location=self.loc_ws5_cells[0],
            quantity=100,
            birthday=datetime.datetime(2020,5,1,0,0)
            )

        self.piglets2 = piglets_testing.create_new_group_with_metatour_by_one_tour(
            tour=self.tour1,
            location=self.loc_ws5_cells[1],
            quantity=100,
            birthday=datetime.datetime(2020,5,5,0,0)
            )

        self.piglets3 = piglets_testing.create_new_group_with_metatour_by_one_tour(
            tour=self.tour1,
            location=self.loc_ws5_cells[2],
            quantity=100,
            birthday=datetime.datetime(2020,5,5,0,0)
            )

        self.piglets4 = piglets_testing.create_new_group_with_metatour_by_one_tour(
            tour=self.tour1,
            location=self.loc_ws5_cells[3],
            quantity=100,
            birthday=datetime.datetime(2020,5,5,0,0)
            )

        self.piglets5 = piglets_testing.create_new_group_with_metatour_by_one_tour(
            tour=self.tour1,
            location=self.loc_ws5_cells[4],
            quantity=100,
            birthday=datetime.datetime(2020,5,5,0,0)
            )

        self.piglets6 = piglets_testing.create_new_group_with_metatour_by_one_tour(
            tour=self.tour1,
            location=self.loc_ws5_cells[5],
            quantity=100,
            birthday=datetime.datetime(2020,5,5,0,0)
            )

        # 3/4 взвешивания
        WeighingPiglets.objects.create_weighing(
            piglets_group=self.piglets1, total_weight=2400,
            place='3/4', date=self.piglets1.birthday + datetime.timedelta(days=60))
        WeighingPiglets.objects.create_weighing(
            piglets_group=self.piglets2, total_weight=2500,
            place='3/4', date=self.piglets2.birthday + datetime.timedelta(days=60))
        WeighingPiglets.objects.create_weighing(
            piglets_group=self.piglets3, total_weight=2700,
            place='3/4', date=self.piglets3.birthday + datetime.timedelta(days=64))
        WeighingPiglets.objects.create_weighing(
            piglets_group=self.piglets4, total_weight=2600,
            place='3/4', date=self.piglets4.birthday + datetime.timedelta(days=64))
        WeighingPiglets.objects.create_weighing(
            piglets_group=self.piglets5, total_weight=3000,
            place='3/4', date=self.piglets5.birthday + datetime.timedelta(days=70))
        WeighingPiglets.objects.create_weighing(
            piglets_group=self.piglets6, total_weight=3200,
            place='3/4', date=self.piglets6.birthday + datetime.timedelta(days=70))

        # 4/8 взвешивания
        WeighingPiglets.objects.create_weighing(
            piglets_group=self.piglets1, total_weight=5100,
            place='4/8', date=self.piglets2.birthday + datetime.timedelta(days=110))
        WeighingPiglets.objects.create_weighing(
            piglets_group=self.piglets2, total_weight=4900,
            place='4/8', date=self.piglets2.birthday + datetime.timedelta(days=110))
        WeighingPiglets.objects.create_weighing(
            piglets_group=self.piglets3, total_weight=5400,
            place='4/8', date=self.piglets3.birthday + datetime.timedelta(days=110))
        WeighingPiglets.objects.create_weighing(
            piglets_group=self.piglets4, total_weight=5200,
            place='4/8', date=self.piglets4.birthday + datetime.timedelta(days=110))
        WeighingPiglets.objects.create_weighing(
            piglets_group=self.piglets5, total_weight=5800,
            place='4/8', date=self.piglets5.birthday + datetime.timedelta(days=110))
        WeighingPiglets.objects.create_weighing(
            piglets_group=self.piglets6, total_weight=5700,
            place='4/8', date=self.piglets6.birthday + datetime.timedelta(days=110))

        # 8/5 взвешивания
        WeighingPiglets.objects.create_weighing(
            piglets_group=self.piglets1, total_weight=15100,
            place='8/5', date=self.piglets2.birthday + datetime.timedelta(days=150))
        WeighingPiglets.objects.create_weighing(
            piglets_group=self.piglets2, total_weight=14900,
            place='8/5', date=self.piglets2.birthday + datetime.timedelta(days=150))
        WeighingPiglets.objects.create_weighing(
            piglets_group=self.piglets3, total_weight=15400,
            place='8/5', date=self.piglets3.birthday + datetime.timedelta(days=150))
        WeighingPiglets.objects.create_weighing(
            piglets_group=self.piglets4, total_weight=15200,
            place='8/6', date=self.piglets4.birthday + datetime.timedelta(days=150))
        WeighingPiglets.objects.create_weighing(
            piglets_group=self.piglets5, total_weight=15800,
            place='8/6', date=self.piglets5.birthday + datetime.timedelta(days=150))
        WeighingPiglets.objects.create_weighing(
            piglets_group=self.piglets6, total_weight=15700,
            place='8/7', date=self.piglets6.birthday + datetime.timedelta(days=150))

        # simulate remont transfer
        transaction, self.moved_piglets1, self.stayed_piglets1, split_event, merge_event = \
            PigletsTransaction.objects.transaction_with_split_and_merge(piglets=self.piglets1,
                to_location=self.loc_ws2, date=self.piglets1.birthday + datetime.timedelta(days=175),
                new_amount=75)

        CullingPiglets.objects.create_culling_piglets(
            piglets_group=self.stayed_piglets1, culling_type='spec', quantity=25, total_weight=10000,
            date=self.stayed_piglets1.birthday + datetime.timedelta(days=200))

        CullingPiglets.objects.create_culling_piglets(
            piglets_group=self.piglets2, culling_type='spec', quantity=50, total_weight=20000,
            date=self.piglets2.birthday + datetime.timedelta(days=200))
        CullingPiglets.objects.create_culling_piglets(
            piglets_group=self.piglets3, culling_type='spec', quantity=50, total_weight=20000,
            date=self.piglets3.birthday + datetime.timedelta(days=200))
        CullingPiglets.objects.create_culling_piglets(
            piglets_group=self.piglets4, culling_type='spec', quantity=50, total_weight=20000,
            date=self.piglets4.birthday + datetime.timedelta(days=200))
        CullingPiglets.objects.create_culling_piglets(
            piglets_group=self.piglets5, culling_type='spec', quantity=50, total_weight=20000,
            date=self.piglets5.birthday + datetime.timedelta(days=200))

    def test_add_prives_prepare(self):
        tours = Tour.objects.all().add_prives_prepare()
        self.assertEqual(round(tours[0].sv_age_3_4, 2), 64.67)
        self.assertEqual(tours[0].total2_3_4, 16400)
        
        self.assertEqual(round(tours[0].sv_age_4_8, 2), 110.67)
        self.assertEqual(tours[0].total2_4_8, 32100)

        self.assertEqual(round(tours[0].sv_age_ws8, 2), 150.67)
        self.assertEqual(tours[0].total2_ws8, 92100)

    def test_add_prives_prepare_spec(self):
        tours = Tour.objects.all().add_prives_prepare_spec()

        self.assertEqual(tours[0].spec_weight_total_ws5, 90000)
        self.assertEqual(tours[0].spec_sv_avg_age_ws5, 200)

    def test_add_prives(self):
        tours = Tour.objects.all() \
            .add_remont_trs_out() \
            .add_culling_data_by_week_tour() \
            .add_week_weight() \
            .add_week_weight_ws8_v2() \
            .add_prives()
        bool(tours)

        self.assertEqual(round(tours[0].prives_4, 2),
            round(((tours[0].total2_4_8 - tours[0].total2_3_4) / 
                (tours[0].sv_age_4_8 - tours[0].sv_age_3_4)), 2))

        self.assertEqual(round(tours[0].prives_8, 2),
            round(((tours[0].total2_ws8 - tours[0].total2_4_8) / 
                (tours[0].sv_age_ws8 - tours[0].sv_age_4_8)), 2))

        self.assertEqual(round(tours[0].prives_5, 2),
            round(((tours[0].spec_weight_total_ws5 - tours[0].total2_8_5) / 
                (tours[0].spec_sv_avg_age_ws5 - tours[0].sv_age_8_5)), 2))

        self.assertEqual(round(tours[0].prives_without_remont_5, 2),
            round(((tours[0].spec_weight_total_ws5 - tours[0].total3_8_5) / 
                (tours[0].spec_sv_avg_age_ws5 - tours[0].sv_age_8_5)), 2))

    def test_add_prives_na_1g(self):
        tours = Tour.objects.all() \
            .add_remont_trs_out() \
            .add_culling_data_by_week_tour() \
            .add_week_weight() \
            .add_week_weight_ws8_v2() \
            .add_prives() \
            .add_prives_na_1g()
        bool(tours)

        self.assertEqual(round(tours[0].prives_1g_5, 2),
         round(tours[0].prives_5 * 1000 / tours[0].ws5_spec_quantity, 2))

        self.assertEqual(round(tours[0].prives_without_remont_1g_5, 2),
         round(tours[0].prives_without_remont_5 * 1000 / tours[0].ws5_spec_quantity, 2))

        self.assertEqual(round(tours[0].prives_1g_4, 2),
         round(tours[0].prives_4 * 1000 / tours[0].week_weight_qnty_4_8, 2))

        self.assertEqual(round(tours[0].prives_1g_8, 2),
         round(tours[0].prives_8 * 1000 / tours[0].week_weight_qnty_ws8, 2))

    def test_xz(self):
        tours = Tour.objects.all() \
                .add_remont_trs_out() \
                .add_farrow_data() \
                .add_sow_data() \
                .add_farrow_percentage() \
                .add_week_weight() \
                .add_week_weight_ws8_v2() \
                .add_culling_data_by_week_tour() \
                .add_culling_percentage() \
                .add_prives()

        bool(tours)
        self.assertEqual(round(tours[0].sv_age_3_4, 2), 64.67)
        self.assertEqual(tours[0].total2_3_4, 16400)
        
        self.assertEqual(round(tours[0].sv_age_4_8, 2), 110.67)
        self.assertEqual(tours[0].total2_4_8, 32100)

        self.assertEqual(round(tours[0].sv_age_ws8, 2), 150.67)
        self.assertEqual(tours[0].total2_ws8, 92100)

    def test_add_prives_prepare_otkorm_weight_data_without_remont(self):
        tours = Tour.objects.all() \
                .add_remont_trs_out() \
                .add_week_weight() \
                .add_prives_prepare_otkorm_weight_data_without_remont()

        bool(tours)
        self.assertEqual(round(tours[0].total3_8_5, 2), round(tours[0].week_weight_8_5 - \
            (tours[0].ws5_remont * tours[0].week_weight_avg_8_5), 2))

    def test_get_prives_data_only_by_one_ws(self):
        tours = Tour.objects.all() \
            .add_remont_trs_out(ws_numbers=[5, ]) \
            .add_culling_data_by_week_tour(ws_numbers=[5, ]) \
            .add_week_weight(places=['8/5', ]) \
            .add_prives(ws_numbers=[5, ])

        self.assertEqual(round(tours[0].prives_5,2),
         round(((tours[0].spec_weight_total_ws5 - tours[0].total2_8_5) / 
            (tours[0].spec_sv_avg_age_ws5 - tours[0].sv_age_8_5)), 2))