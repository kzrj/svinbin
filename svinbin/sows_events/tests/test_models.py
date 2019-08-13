# -*- coding: utf-8 -*-
from django.test import TestCase

from sows_events.models import Semination, Ultrasound, SowFarrow, CullingSow, UltrasoundV2
from sows.models import Sow
from piglets.models import NewBornPigletsGroup

import locations.testing_utils as locations_testing
import sows.testing_utils as sows_testing


class SeminationModelManagerTest(TestCase):
    def setUp(self):
        locations_testing.create_workshops_sections_and_cells()
        sows_testing.create_statuses()

    def test_create_semination(self):
        sow = Sow.objects.create_new_from_gilt_and_put_in_workshop_one(1)
        semination = Semination.objects.create_semination(sow=sow, week=1,
         initiator=None, semination_employee=None)

        self.assertEqual(Semination.objects.all().count(), 1)
        self.assertEqual(semination.tour.week_number, 1)
        sow.refresh_from_db()
        self.assertEqual(sow.tour.week_number, 1)
        self.assertEqual(sow.status.title, 'Осеменена')


class UltrasoundModelManagerTest(TestCase):
    def setUp(self):
        locations_testing.create_workshops_sections_and_cells()
        sows_testing.create_statuses()

    def test_create_ultrasound(self):
        sow = Sow.objects.create_new_from_gilt_and_put_in_workshop_one(1)
        semination = Semination.objects.create_semination(sow=sow, week=1,
         initiator=None, semination_employee=None)

        ultrasound = Ultrasound.objects.create_ultrasound(sow=sow,
         initiator=None, result=False)

        self.assertEqual(Ultrasound.objects.all().count(), 1)
        self.assertEqual(ultrasound.tour.week_number, 1)
        sow.refresh_from_db()
        self.assertEqual(sow.status.title, 'Прохолост')

        Ultrasound.objects.create_ultrasound(sow=sow, 
         initiator=None, result=True)
        sow.refresh_from_db()
        self.assertEqual(sow.status.title, 'Беременна')

    def test_create_ultrasoundV2(self):
        sow = Sow.objects.create_new_from_gilt_and_put_in_workshop_one(1)
        semination = Semination.objects.create_semination(sow=sow, week=1,
         initiator=None, semination_employee=None)

        ultrasound = UltrasoundV2.objects.create_ultrasoundV2(sow=sow, 
         initiator=None, result=False)

        self.assertEqual(UltrasoundV2.objects.all().count(), 1)
        self.assertEqual(ultrasound.tour.week_number, 1)
        sow.refresh_from_db()
        self.assertEqual(sow.status.title, 'Прохолост')

        UltrasoundV2.objects.create_ultrasoundV2(sow=sow,
         initiator=None, result=True)
        sow.refresh_from_db()
        self.assertEqual(sow.status.title, 'Беременна')


class SowFarrowModelManagerTest(TestCase):
    def setUp(self):
        locations_testing.create_workshops_sections_and_cells()
        sows_testing.create_statuses()

    def test_create_farrow(self):
        sow = sows_testing.create_sow_and_put_in_workshop_three(1, 1)
        Semination.objects.create_semination(sow=sow, week=1,
         initiator=None, semination_employee=None)

        # first sow farrow in tour
        farrow1 = SowFarrow.objects.create_sow_farrow(
            sow=sow,
            alive_quantity=10,
            dead_quantity=1
            )
        
        self.assertEqual(NewBornPigletsGroup.objects.all().count(), 1)
        sow.refresh_from_db()
        self.assertEqual(sow.status.title, 'Опоросилась, кормит')
        self.assertEqual(sow.tour.week_number, 1)

        piglets_group1 = farrow1.new_born_piglets_group
        self.assertEqual(sow.tour, piglets_group1.tour)
        self.assertEqual(sow.location, piglets_group1.location)
        self.assertEqual(piglets_group1.quantity, farrow1.alive_quantity)
        self.assertEqual(piglets_group1.start_quantity, farrow1.alive_quantity)

        # second sow farrow in tour
        farrow2 = SowFarrow.objects.create_sow_farrow(
            sow=sow,
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


class CullingSowManagerTest(TestCase):
    def setUp(self):
        locations_testing.create_workshops_sections_and_cells()
        sows_testing.create_statuses()

    def test_create_farrow(self):
        sow = sows_testing.create_sow_and_put_in_workshop_three(1, 1)
        culling = CullingSow.objects.create_culling(sow, 'spec', 'prichina')
        sow.refresh_from_db()
        self.assertEqual(sow.alive, False)
        self.assertEqual(culling.sow, sow)
        self.assertEqual(culling.culling_type, 'spec')
        self.assertEqual(culling.reason, 'prichina')