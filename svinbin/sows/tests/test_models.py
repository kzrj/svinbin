# -*- coding: utf-8 -*-
from mixer.backend.django import mixer

from django.test import TestCase
from django.db import models

import locations.testing_utils as locaions_testing
import sows.testing_utils as sows_testings
import piglets.testing_utils as piglets_testing

from locations.models import Location
from sows.models import Sow, Gilt
from sows_events.models import SowFarrow


class SowModelManagerTest(TestCase):
    def setUp(self):
        locaions_testing.create_workshops_sections_and_cells()
        sows_testings.create_statuses()

    def test_get_or_create_by_farm_id(self):
        location = Location.objects.get(workshop__number=1)
        for count_sow in range(1, 100):
            Sow.objects.create(farm_id=count_sow, location=location)
        
        Sow.objects.get_or_create_by_farm_id(1)
        self.assertEqual(Sow.objects.all().count(), 99)

        Sow.objects.get_or_create_by_farm_id(120)
        self.assertEqual(Sow.objects.all().count(), 100)        
        self.assertEqual(Sow.objects.filter(farm_id=120).count(), 1)

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

    def test_get_all_sows_in_workshop(self):
        sow1 = sows_testings.create_sow_and_put_in_workshop_one()
        sow2 = sows_testings.create_sow_and_put_in_workshop_one()
        seminated_sow1 = sows_testings.create_sow_with_semination(sow1.location)

        location2 = Location.objects.get(workshop__number=2)
        seminated_sow2 = sows_testings.create_sow_with_semination(location2)
        seminated_sow3 = sows_testings.create_sow_with_semination(location2, 2)

        self.assertEqual(Sow.objects.all().count(), 5)
        self.assertEqual(Sow.objects.get_all_sows_in_workshop(sow1.location.workshop).count(), 3)

        self.assertEqual(Sow.objects.get_all_sows_in_workshop(sow1.location.workshop)
            .filter(tour=seminated_sow1.tour).get().pk, seminated_sow1.pk)

        # print(Sow.objects.all().values_list('tour', flat=True))
        # print(type(Sow.objects.all().values_list('tour', flat=True)))
        # print(list(Sow.objects.all().values_list('tour', flat=True)))


class GiltModelManagerTest(TestCase):
    def setUp(self):
        locaions_testing.create_workshops_sections_and_cells()
        sows_testings.create_statuses()

    def test_create_gilt(self):
        new_born_group = piglets_testing.create_new_born_group()
        sow = new_born_group.farrows.all().first().sow
        gilt = Gilt.objects.create_gilt(birth_id=1, mother_sow=sow)

        new_born_group.refresh_from_db()
        self.assertEqual(new_born_group.gilts_quantity, 1)
        self.assertEqual(gilt.new_born_group, new_born_group)
        self.assertEqual(gilt.mother_sow, sow)
        self.assertEqual(gilt.location, sow.location)
