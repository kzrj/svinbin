from mixer.backend.django import mixer

from django.test import TestCase

import workshops.testing_utils as workshop_testing
import sows.testing_utils as sows_testings
import piglets.testing_utils as piglets_testing

from workshops.models import WorkShop, Section, SowSingleCell, PigletsGroupCell, SowGroupCell, \
SowAndPigletsCell
from sows.models import Sow, Gilt
from sows_events.models import SowFarrow
from transactions.models import Location


class SowModelManagerTest(TestCase):
    def setUp(self):
        workshop_testing.create_workshops_sections_and_cells()
        sows_testings.create_statuses()

    # def test_create_new_from_gilt_and_put_in_workshop_one(self):
    #     # add test
    #     pass

    def test_get_or_create_by_farm_id(self):
        for count_sow in range(1, 100):
            location = Location.objects.create_location(pre_location=WorkShop.objects.get(number=1))
            Sow.objects.create(farm_id=count_sow, location=location)
        for count_sow in range(1, 100):
            location = Location.objects.create_location(pre_location=WorkShop.objects.get(number=1))
            Sow.objects.create(location=location)

        Sow.objects.get_or_create_by_farm_id(1)
        self.assertEqual(Sow.objects.all().count(), 198)

        Sow.objects.get_or_create_by_farm_id(120)
        self.assertEqual(Sow.objects.all().count(), 199)        
        self.assertEqual(Sow.objects.filter(farm_id=120).count(), 1)

        # pass

    def test_move_to(self):
        sow = Sow.objects.get_or_create_by_farm_id(1)
        workshop1 = WorkShop.objects.get(number=1)
        workshop2 = WorkShop.objects.get(number=2)
        self.assertEqual(sow.location.get_location, workshop1)

        Sow.objects.move_to(sow, workshop2)
        sow.refresh_from_db()
        self.assertEqual(sow.location.get_location, workshop2)

        Sow.objects.move_to_by_farm_id(1, workshop1)
        sow.refresh_from_db()
        self.assertEqual(sow.location.get_location, workshop1)   

    def test_move_many(self):
        sow1 = Sow.objects.get_or_create_by_farm_id(1)
        sow2 = Sow.objects.get_or_create_by_farm_id(2)
        sow3 = Sow.objects.get_or_create_by_farm_id(3)

        sows = Sow.objects.filter(farm_id__in=[1,2,3])

        Sow.objects.move_many(sows, WorkShop.objects.get(number=2))

        sow1.refresh_from_db()
        sow2.refresh_from_db()
        sow3.refresh_from_db()

        self.assertEqual(sow1.location.get_location, WorkShop.objects.get(number=2))
        self.assertEqual(sow2.location.get_location, WorkShop.objects.get(number=2))
        self.assertEqual(sow3.location.get_location, WorkShop.objects.get(number=2))

    # def test_get_last_farrow(self):
    #     location = Location.objects.create_workshop_location(workshop_number=3)
    #     sow = sows_testings.create_sow_with_semination(location)
    #     farrow1 = SowFarrow.objects.create_sow_farrow_by_sow_object(sow=sow, week=1,
    #         alive_quantity=10, dead_quantity=1, mummy_quantity=1)
    #     farrow2 = SowFarrow.objects.create_sow_farrow_by_sow_object(sow=sow, week=1,
    #         alive_quantity=3, dead_quantity=1, mummy_quantity=1)
    #     farrow3 = SowFarrow.objects.create_sow_farrow_by_sow_object(sow=sow, week=1,
    #         alive_quantity=20, dead_quantity=1, mummy_quantity=5)
    #     print(sow.get_last_farrow())


class GiltModelManagerTest(TestCase):
    def setUp(self):
        workshop_testing.create_workshops_sections_and_cells()
        sows_testings.create_statuses()

    def test_create_gilt(self):
        new_born_group = piglets_testing.create_new_born_group()
        sow = new_born_group.farrows.all().first().sow
        gilt = Gilt.objects.create_gilt(birth_id=1, mother_sow=sow)

        new_born_group.refresh_from_db()
        self.assertEqual(new_born_group.gilts_quantity, 1)
        self.assertEqual(gilt.new_born_group, new_born_group)
        self.assertEqual(gilt.mother_sow, sow)
        self.assertEqual(gilt.location.get_location, sow.location.get_location)
