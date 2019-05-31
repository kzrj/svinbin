from mixer.backend.django import mixer
# from freezegun import freeze_time

from django.test import TestCase

from events.models import Semination
from pigs.models import Sow
import workshops.testing_utils as workshop_testing



# class EventModelTest(TestCase):




class SeminationModelManagerTest(TestCase):
    def setUp(self):
        workshop_testing.create_workshops_sections_and_cells()

    def test_create_semination(self):
        Sow.objects.create_new_from_gilt_and_put_in_workshop_one(1)
        semination = Semination.objects.create_semination(sow_farm_id=1, week=1,
         initiator=None, semination_employee=None)

        self.assertEqual(Semination.objects.all().count(), 1)
        self.assertEqual(semination.tour.week_number, 1)
