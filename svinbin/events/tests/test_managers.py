from mixer.backend.django import mixer
# from freezegun import freeze_time

from django.test import TestCase

from events.models import Semination, Ultrasound
from pigs.models import Sow
import workshops.testing_utils as workshop_testing
import pigs.testing_utils as pigs_testing


class SeminationModelManagerTest(TestCase):
    def setUp(self):
        workshop_testing.create_workshops_sections_and_cells()
        pigs_testing.create_statuses()

    def test_create_semination(self):
        Sow.objects.create_new_from_gilt_and_put_in_workshop_one(1)
        semination = Semination.objects.create_semination(sow_farm_id=1, week=1,
         initiator=None, semination_employee=None)

        self.assertEqual(Semination.objects.all().count(), 1)
        self.assertEqual(semination.tour.week_number, 1)


class UltrasoundModelManagerTest(TestCase):
    def setUp(self):
        workshop_testing.create_workshops_sections_and_cells()
        pigs_testing.create_statuses()

    def test_create_ultrasound(self):
        sow = Sow.objects.create_new_from_gilt_and_put_in_workshop_one(1)
        semination = Semination.objects.create_semination(sow_farm_id=1, week=1,
         initiator=None, semination_employee=None)

        ultrasound = Ultrasound.objects.create_ultrasound(sow_farm_id=1, week=1,
         initiator=None, result=False)

        self.assertEqual(Ultrasound.objects.all().count(), 1)
        self.assertEqual(ultrasound.tour.week_number, 1)
        sow.refresh_from_db()
        self.assertEqual(sow.status.title, 'proholost')

        Ultrasound.objects.create_ultrasound(sow_farm_id=1, week=1,
         initiator=None, result=True)
        sow.refresh_from_db()
        self.assertEqual(sow.status.title, 'pregnant in workshop one')