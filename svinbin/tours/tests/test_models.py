# -*- coding: utf-8 -*-

from django.test import TestCase

from tours.models import Tour, MetaTour, MetaTourRecord
from sows.models import Sow
from sows_events.models import Semination, Ultrasound
from locations.models import Location
from piglets.models import Piglets
# from piglets_events.models import NewBornPigletsGroupRecount

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
        self.assertEqual(Tour.objects.all().first().year, 2020)

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


class TestMetaTourRecordModel(TestCase):
    def setUp(self):
        locations_testing.create_workshops_sections_and_cells()
        pigs_testings.create_statuses()

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