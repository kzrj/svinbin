# -*- coding: utf-8 -*-
from mixer.backend.django import mixer

from django.test import TestCase
from django.db import models
from django.db.models import Q
from django.db import connection

import locations.testing_utils as locaions_testing
import sows.testing_utils as sows_testings
import sows_events.utils as sows_events_testings
import piglets.testing_utils as piglets_testing

from locations.models import Location
from sows.models import Sow, Gilt, Boar
from sows_events.models import SowFarrow, Ultrasound, Semination
from tours.models import Tour


class SowModelManagerTest(TestCase):
    def setUp(self):
        locaions_testing.create_workshops_sections_and_cells()
        sows_testings.create_statuses()
        sows_events_testings.create_types()

    def test_get_or_create_by_farm_id(self):
        location = Location.objects.get(workshop__number=1)
        for count_sow in range(1, 100):
            Sow.objects.create(farm_id=count_sow, location=location)
        
        Sow.objects.get_or_create_by_farm_id(1)
        self.assertEqual(Sow.objects.all().count(), 99)

        Sow.objects.get_or_create_by_farm_id(120)
        self.assertEqual(Sow.objects.all().count(), 100)        
        self.assertEqual(Sow.objects.filter(farm_id=120).count(), 1)

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

    def test_create_new_from_gilt_without_farm_id(self):
        sow_noname = Sow.objects.create_new_from_gilt_without_farm_id()
        self.assertEqual(sow_noname.farm_id, None)

    def test_get_without_farm_id_in_workshop(self):
        sow1 = sows_testings.create_sow_and_put_in_workshop_one()
        seminated_sow1 = sows_testings.create_sow_with_semination(sow1.location)
        seminated_sow3 = sows_testings.create_sow_with_semination(sow1.location)
        sow_noname = Sow.objects.create_new_from_gilt_without_farm_id()

        Ultrasound.objects.create_ultrasound(sow=seminated_sow1,
         initiator=None, result=True)
        Ultrasound.objects.create_ultrasound(sow=seminated_sow3,
         initiator=None, result=False)
        qs = Sow.objects.get_without_farm_id_in_workshop(workshop=sow1.location.workshop)        
        self.assertEqual(list(qs.values_list(flat=True)), [sow_noname.pk])

    def test_create_new_from_noname(self):
        noname_sow1 = Sow.objects.create_new_from_gilt_without_farm_id()

        named_sow1 = Sow.objects.create_new_from_noname(900, noname_sow1.location.workshop)
        self.assertEqual(named_sow1.farm_id, 900)
        self.assertEqual(named_sow1.location.workshop.number, 1)

        named_sow2 = Sow.objects.create_new_from_noname(901, named_sow1.location.workshop)
        self.assertEqual(named_sow2, None)

    def test_get_by_tour(self):
        sow = sows_testings.create_sow_and_put_in_workshop_one()
        Semination.objects.create_semination(sow=sow, week=1, initiator=None,
         semination_employee=None)
        Semination.objects.create_semination(sow=sow, week=1, initiator=None,
         semination_employee=None)
        tour = Tour.objects.filter(week_number=1).first()
        self.assertEqual(sow.get_seminations_by_tour(tour).count(), 2)
        Ultrasound.objects.create_ultrasound(sow, None, True)
        self.assertEqual(sow.get_ultrasounds1_by_tour(tour).count(), 1)
        SowFarrow.objects.create_sow_farrow(sow=sow, alive_quantity=7, mummy_quantity=1)
        self.assertEqual(sow.get_farrows_by_tour(tour).count(), 1)

    def test_get_tours_pk(self):
        sow = sows_testings.create_sow_and_put_in_workshop_one()

        # tour 1
        Semination.objects.create_semination(sow=sow, week=1, initiator=None,
         semination_employee=None)
        Semination.objects.create_semination(sow=sow, week=1, initiator=None,
         semination_employee=None)
        Ultrasound.objects.create_ultrasound(sow, None, True)
        SowFarrow.objects.create_sow_farrow(sow=sow, alive_quantity=7, mummy_quantity=1)

        # tour 2
        Semination.objects.create_semination(sow=sow, week=2, initiator=None,
         semination_employee=None)
        Semination.objects.create_semination(sow=sow, week=2, initiator=None,
         semination_employee=None)
        Ultrasound.objects.create_ultrasound(sow, None, True)
        SowFarrow.objects.create_sow_farrow(sow=sow, alive_quantity=7, mummy_quantity=1)

        # tour 3
        Semination.objects.create_semination(sow=sow, week=3, initiator=None,
         semination_employee=None)
        Ultrasound.objects.create_ultrasound(sow, None, False)

        self.assertEqual(sow.get_tours_pk().first(), 
            Tour.objects.filter(week_number=1).first().pk)

    def test_is_farrow_in_current_tour(self):
        sow = sows_testings.create_sow_and_put_in_workshop_one()
        Semination.objects.create_semination(sow=sow, week=1, initiator=None,
         semination_employee=None)
        Semination.objects.create_semination(sow=sow, week=1, initiator=None,
         semination_employee=None)
        Ultrasound.objects.create_ultrasound(sow, None, True)
        SowFarrow.objects.create_sow_farrow(sow=sow, alive_quantity=7, mummy_quantity=1)
        
        self.assertEqual(sow.is_farrow_in_current_tour, True)

        sow2 = sows_testings.create_sow_and_put_in_workshop_one()
        Semination.objects.create_semination(sow=sow2, week=1, initiator=None,
         semination_employee=None)
        Semination.objects.create_semination(sow=sow2, week=1, initiator=None,
         semination_employee=None)
        Ultrasound.objects.create_ultrasound(sow2, None, True)
        self.assertEqual(sow2.is_farrow_in_current_tour, False)

    def test_does_once_seminate_in_tour(self):
        sow = sows_testings.create_sow_and_put_in_workshop_one()
        
        # 1 semination
        Semination.objects.create_semination(sow=sow, week=1, initiator=None,
         semination_employee=None)
        self.assertEqual(sow.does_once_seminate_in_tour, True)

        # 2 seminations
        Semination.objects.create_semination(sow=sow, week=1, initiator=None,
         semination_employee=None)
        sow.refresh_from_db()
        self.assertEqual(sow.does_once_seminate_in_tour, False)

        Ultrasound.objects.create_ultrasound(sow=sow, result=False, days=30)
        sow.refresh_from_db()
        self.assertEqual(sow.tour, None)

        # not seminated
        sow.refresh_from_db()
        self.assertEqual(sow.does_once_seminate_in_tour, False)

        # 1 semination in another tour
        Semination.objects.create_semination(sow=sow, week=2, initiator=None,
         semination_employee=None)
        self.assertEqual(sow.does_once_seminate_in_tour, True)

        # 2 semination in anopther tour
        Semination.objects.create_semination(sow=sow, week=2, initiator=None,
         semination_employee=None)
        self.assertEqual(sow.does_once_seminate_in_tour, False)

    def test_get_with_seminations_in_tour(self):
        sow = sows_testings.create_sow_and_put_in_workshop_one()
        
        # 1 semination
        Semination.objects.create_semination(sow=sow, week=1, initiator=None,
         semination_employee=None)

        sows_qs = Sow.objects.all().get_with_seminations_in_tour(
                tour=Tour.objects.get(week_number=1))
        self.assertEqual(len(sows_qs.first().seminations_by_tour), 1)

        # not seminated
        sow.refresh_from_db()
        tour = Tour.objects.get_or_create_by_week_in_current_year(2)
        sows_qs = Sow.objects.all().get_with_seminations_in_tour(
                tour=tour)
        self.assertEqual(len(sows_qs.first().seminations_by_tour), 0)

        # 2 semination in another tour
        Semination.objects.create_semination(sow=sow, week=2, initiator=None,
         semination_employee=None)
        Semination.objects.create_semination(sow=sow, week=2, initiator=None,
         semination_employee=None)

        sows_qs = Sow.objects.all().get_with_seminations_in_tour(
                tour=tour)
        self.assertEqual(len(sows_qs.first().seminations_by_tour), 2)

    def test_get_list_of_qs_by_seminations_in_tour(self):
        sow1 = sows_testings.create_sow_and_put_in_workshop_one()
        sow2 = sows_testings.create_sow_and_put_in_workshop_one()
        
        # 1 semination sow1, 2 semination sow2
        Semination.objects.create_semination(sow=sow1, week=1, initiator=None,
         semination_employee=None)
        Semination.objects.create_semination(sow=sow2, week=1, initiator=None,
         semination_employee=None)
        Semination.objects.create_semination(sow=sow2, week=1, initiator=None,
         semination_employee=None)

        sows_once_seminated_qs, sows_two_seminated_qs = Sow.objects.all().get_list_of_qs_by_seminations_in_tour(
                tour=Tour.objects.get(week_number=1))
        self.assertEqual(sows_once_seminated_qs.count(), 1)
        self.assertEqual(sows_once_seminated_qs.first(), sow1)
        self.assertEqual(sows_two_seminated_qs.count(), 1)
        self.assertEqual(sows_two_seminated_qs.first(), sow2)

        # lets seminate sow1 by tour 2. sow1 have 2 seminations with different tours
        Semination.objects.create_semination(sow=sow1, week=2, initiator=None,
         semination_employee=None)
        sows_once_seminated_qs, sows_two_seminated_qs = Sow.objects.all().get_list_of_qs_by_seminations_in_tour(
                tour=Tour.objects.get(week_number=1))
        self.assertEqual(sows_once_seminated_qs.count(), 1)
        self.assertEqual(sows_once_seminated_qs.first(), sow1)
        self.assertEqual(sows_two_seminated_qs.count(), 1)
        self.assertEqual(sows_two_seminated_qs.first(), sow2)

        sows_once_seminated_qs, sows_two_seminated_qs = Sow.objects.all().get_list_of_qs_by_seminations_in_tour(
                tour=Tour.objects.get(week_number=2))
        self.assertEqual(sows_once_seminated_qs.count(), 1)
        self.assertEqual(sows_once_seminated_qs.first(), sow1)
        self.assertEqual(sows_two_seminated_qs.count(), 0)
        self.assertEqual(sows_two_seminated_qs.first(), None)

    def test_split_free_and_exist_farm_ids(self):
        location = Location.objects.all()[1]
        sow1 = sows_testings.create_sow_with_location(location=location, farm_id=1)
        sow2 = sows_testings.create_sow_with_location(location=location, farm_id=2)
        free_farm_ids, exist_farm_ids = Sow.objects.split_free_and_exist_farm_ids([1, 2, 3, 4])
        self.assertEqual(free_farm_ids, [3, 4])
        self.assertEqual(exist_farm_ids, [1, 2])

    def test_create_bulk_at_ws(self):
        location = Location.objects.all()[1]
        sow1 = sows_testings.create_sow_with_location(location=location, farm_id=1)
        sow2 = sows_testings.create_sow_with_location(location=location, farm_id=2)

        created, existed = Sow.objects.create_bulk_at_ws([1, 2, 3, 4], location)
        self.assertEqual(created, [3, 4])
        self.assertEqual(existed, [1, 2])
        self.assertEqual(Sow.objects.filter(farm_id__in=[3, 4]).count(), 2)


class GiltModelManagerTest(TestCase):
    def setUp(self):
        locaions_testing.create_workshops_sections_and_cells()
        sows_testings.create_statuses()

    def test_create_gilt(self):
        new_born_group = piglets_testing.create_new_born_group()
        farrow = new_born_group.farrows.all().first()
        gilt = Gilt.objects.create_gilt(birth_id=1, new_born_group=new_born_group)

        new_born_group.refresh_from_db()
        self.assertEqual(new_born_group.gilts_quantity, 1)
        self.assertEqual(gilt.new_born_group, new_born_group)
        self.assertEqual(gilt.mother_sow, farrow.sow)
        self.assertEqual(gilt.location, new_born_group.location)
