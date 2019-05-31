from mixer.backend.django import mixer
# from freezegun import freeze_time

from django.test import TestCase

import workshops.testing_utils as workshop_testing
import pigs.testing_utils as pigs_testings
from tours.models import Tour
from pigs.models import Sow
from events.models import Semination, Ultrasound


class TourModelManagerTest(TestCase):
    def setUp(self):
        workshop_testing.create_workshops_sections_and_cells()
        pigs_testings.create_statuses()

    def test_get_or_create_by_week_in_current_year(self):
        Tour.objects.get_or_create_by_week_in_current_year(1)
        self.assertEqual(Tour.objects.all().count(), 1)
        self.assertEqual(Tour.objects.all().first().week_number, 1)
        self.assertEqual(Tour.objects.all().first().year, 2019)

        tour = Tour.objects.get_or_create_by_week_in_current_year(1)
        self.assertEqual(Tour.objects.all().count(), 1)
        self.assertEqual(tour.week_number, 1)

        # add @freeze_time('2032-11-01') test year

    # def test_get_tour_by_week_in_current_year(self):
        # pass
    
class TourModelTest(TestCase):
    def setUp(self):
        workshop_testing.create_workshops_sections_and_cells()
        pigs_testings.create_statuses()

    def test_get_inseminated_sows(self):
        tour = Tour.objects.get_or_create_by_week_in_current_year(1)
        sow1 = Sow.objects.get_or_create_by_farm_id(101)
        sow2 = Sow.objects.get_or_create_by_farm_id(102)
        semination101 = Semination.objects.create_semination(101, 1)
        semination102 = Semination.objects.create_semination(102, 1)

        inseminated_sows_in_tour = tour.get_inseminated_sows
        self.assertEqual(inseminated_sows_in_tour[0], sow1)
        self.assertEqual(inseminated_sows_in_tour[1], sow2)

    def test_get_ultrasounded_sows(self):
        tour = Tour.objects.get_or_create_by_week_in_current_year(1)
        sow1 = Sow.objects.get_or_create_by_farm_id(201)
        sow2 = Sow.objects.get_or_create_by_farm_id(202)
        ultrasound201 = Ultrasound.objects.create_ultrasound(201, 1, None, False)
        ultrasound201 = Ultrasound.objects.create_ultrasound(202, 1, None, True)

        ultrasounded_sows_in_tour = tour.get_ultrasounded_sows
        self.assertEqual(ultrasounded_sows_in_tour[0], sow1)
        self.assertEqual(ultrasounded_sows_in_tour[1], sow2)

        ultrasounded_sows_in_tour_success = tour.get_ultrasounded_sows_success
        self.assertEqual(ultrasounded_sows_in_tour_success[0], sow2)

        ultrasounded_sows_in_tour_fail = tour.get_ultrasounded_sows_fail
        self.assertEqual(ultrasounded_sows_in_tour_fail[0], sow1)


