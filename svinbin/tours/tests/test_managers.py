from mixer.backend.django import mixer
# from freezegun import freeze_time

from django.test import TestCase


from tours.models import Tour


class TourModelManagerTest(TestCase):
    # def setUp(self):
    #     workshop_testing.create_workshops_sections_and_cells()

    def test_get_or_create_by_week_in_current_year(self):
        Tour.objects.get_or_create_by_week_in_current_year(1)
        self.assertEqual(Tour.objects.all().count(), 1)
        self.assertEqual(Tour.objects.all().first().week_number, 1)
        self.assertEqual(Tour.objects.all().first().year, 2019)

        tour = Tour.objects.get_or_create_by_week_in_current_year(1)
        self.assertEqual(Tour.objects.all().count(), 1)
        self.assertEqual(tour.week_number, 1)

        # add @freeze_time('2032-11-01') test year

