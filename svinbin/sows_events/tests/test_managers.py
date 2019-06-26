from mixer.backend.django import mixer
# from freezegun import freeze_time

from django.test import TestCase

from sows_events.models import Semination, Ultrasound, SowFarrow
from sows.models import Sow
from piglets.models import NewBornPigletsGroup
from tours.models import Tour

import workshops.testing_utils as workshop_testing
import sows.testing_utils as sows_testing


class SeminationModelManagerTest(TestCase):
    def setUp(self):
        workshop_testing.create_workshops_sections_and_cells()
        sows_testing.create_statuses()

    def test_create_semination(self):
        sow = Sow.objects.create_new_from_gilt_and_put_in_workshop_one(1)
        semination = Semination.objects.create_semination(sow_farm_id=1, week=1,
         initiator=None, semination_employee=None)

        self.assertEqual(Semination.objects.all().count(), 1)
        self.assertEqual(semination.tour.week_number, 1)
        sow.refresh_from_db()
        self.assertEqual(sow.tour.week_number, 1)


class UltrasoundModelManagerTest(TestCase):
    def setUp(self):
        workshop_testing.create_workshops_sections_and_cells()
        sows_testing.create_statuses()

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


class SowFarrowModelManagerTest(TestCase):
    def setUp(self):
        workshop_testing.create_workshops_sections_and_cells()
        sows_testing.create_statuses()

    def test_create_farrow(self):
        sow = sows_testing.create_sow_and_put_in_workshop_three(1, 1)
        Semination.objects.create_semination(sow_farm_id=sow.farm_id, week=1,
         initiator=None, semination_employee=None)

        # first sow farrow in tour
        farrow1 = SowFarrow.objects.create_sow_farrow(
            sow_farm_id=sow.farm_id,
            week=1,
            alive_quantity=10,
            dead_quantity=1
            )
        
        self.assertEqual(NewBornPigletsGroup.objects.all().count(), 1)
        sow.refresh_from_db()
        self.assertEqual(sow.status.title, 'Опоросилась, кормит')

        piglets_group1 = farrow1.new_born_piglets_group
        self.assertEqual(sow.tour, piglets_group1.tour)
        self.assertEqual(sow.location.get_location, piglets_group1.location.get_location)
        self.assertEqual(piglets_group1.quantity, farrow1.alive_quantity)
        self.assertEqual(piglets_group1.start_quantity, farrow1.alive_quantity)

        # second sow farrow in tour
        farrow2 = SowFarrow.objects.create_sow_farrow(
            sow_farm_id=sow.farm_id,
            week=1,
            alive_quantity=7,
            mummy_quantity=1
            )

        self.assertEqual(NewBornPigletsGroup.objects.all().count(), 1)

        piglets_group2 = farrow2.new_born_piglets_group
        self.assertEqual(piglets_group1, piglets_group2)
        self.assertEqual(piglets_group2.quantity, 17)
        self.assertEqual(piglets_group2.start_quantity, 10)

        self.assertEqual(SowFarrow.objects.all().count(), 2)
        self.assertEqual(farrow1.new_born_piglets_group, farrow2.new_born_piglets_group)
