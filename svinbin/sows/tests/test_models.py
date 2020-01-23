# -*- coding: utf-8 -*-
from mixer.backend.django import mixer

from django.test import TestCase, TransactionTestCase
from django.db import models
from django.db.models import Q, Prefetch, F
from django.db import connection
from django.core.exceptions import ValidationError

import locations.testing_utils as locations_testing
import sows.testing_utils as sows_testings
import sows_events.utils as sows_events_testings
import piglets.testing_utils as piglets_testing

from locations.models import Location, Section
from sows.models import Sow, Gilt, Boar
from sows_events.models import SowFarrow, Ultrasound, Semination
from tours.models import Tour

from sows.serializers import SowManySerializer


class SowModelManagerTest(TransactionTestCase):
    def setUp(self):
        locations_testing.create_workshops_sections_and_cells()
        sows_testings.create_statuses()
        sows_events_testings.create_types()
        piglets_testing.create_piglets_statuses()

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

        sow.location = Location.objects.filter(sowAndPigletsCell__number=1).first()
        sow.save()
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
        sow.location = Location.objects.filter(sowAndPigletsCell__number=1).first()
        sow.save()
        SowFarrow.objects.create_sow_farrow(sow=sow, alive_quantity=7, mummy_quantity=1)

        # tour 2
        Semination.objects.create_semination(sow=sow, week=2, initiator=None,
         semination_employee=None)
        Semination.objects.create_semination(sow=sow, week=2, initiator=None,
         semination_employee=None)
        Ultrasound.objects.create_ultrasound(sow, None, True)
        sow.location = Location.objects.filter(sowAndPigletsCell__number=2).first()
        sow.save()
        SowFarrow.objects.create_sow_farrow(sow=sow, alive_quantity=7, mummy_quantity=1)

        # tour 3
        Semination.objects.create_semination(sow=sow, week=3, initiator=None,
         semination_employee=None)
        Ultrasound.objects.create_ultrasound(sow, None, False)

        self.assertEqual(sow.get_tours_pk().first(), Tour.objects.filter(week_number=1).first().pk)
        self.assertEqual(sow.get_tours_pk()[1], Tour.objects.filter(week_number=2).first().pk)
        self.assertEqual(sow.get_tours_pk()[2], Tour.objects.filter(week_number=3).first().pk)
        self.assertEqual(sow.get_tours_pk().count(), 3)

    # def test_is_farrow_in_current_tour(self):
    #     sow = sows_testings.create_sow_and_put_in_workshop_one()
    #     Semination.objects.create_semination(sow=sow, week=1, initiator=None,
    #      semination_employee=None)
    #     Semination.objects.create_semination(sow=sow, week=1, initiator=None,
    #      semination_employee=None)
    #     Ultrasound.objects.create_ultrasound(sow, None, True)
    #     # first section ws3
    #     sow.location = Location.objects.get(section__number=1, section__workshop__number=3)
    #     sow.save()
    #     SowFarrow.objects.create_sow_farrow(sow=sow, alive_quantity=7, mummy_quantity=1)
        
    #     self.assertEqual(sow.is_farrow_in_current_tour, True)

    #     sow2 = sows_testings.create_sow_and_put_in_workshop_one()
    #     Semination.objects.create_semination(sow=sow2, week=1, initiator=None,
    #      semination_employee=None)
    #     Semination.objects.create_semination(sow=sow2, week=1, initiator=None,
    #      semination_employee=None)
    #     Ultrasound.objects.create_ultrasound(sow2, None, True)
    #     self.assertEqual(sow2.is_farrow_in_current_tour, False)

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

        sow.location = Location.objects.get(section__number=1, section__workshop__number=3)
        sow.save()

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

    def test_create_or_return(self):
        sow, created = Sow.objects.create_or_return(123)
        self.assertEqual(sow.farm_id, 123)
        self.assertEqual(created, True)

        sow, created = Sow.objects.create_or_return(123)
        self.assertEqual(sow.farm_id, 123)
        self.assertEqual(created, False)

    def test_create_from_gilts_group(self):
        tour = Tour.objects.get_or_create_by_week(3, 2020)
        location = Location.objects.get(sowAndPigletsCell__number=1, 
             sowAndPigletsCell__section__number=1)
        gilts_piglets = piglets_testing.create_from_sow_farrow(tour, location, 12)

        Sow.objects.create_from_gilts_group(gilts_piglets)

        self.assertEqual(Sow.objects.all().count(), 13)
        self.assertEqual(Sow.objects.filter(farm_id__isnull=True).count(), 12)


class SowQueryTest(TransactionTestCase):
    def setUp(self):
        locations_testing.create_workshops_sections_and_cells()
        sows_testings.create_statuses()
        sows_events_testings.create_types()
        piglets_testing.create_piglets_statuses()

    def test_get_count_by_tours(self):
        sows_testings.create_sow_seminated_usouded_ws3_section(1, 1)
        sows_testings.create_sow_seminated_usouded_ws3_section(1, 1)
        sows_testings.create_sow_seminated_usouded_ws3_section(1, 2)
        sows_testings.create_sow_seminated_usouded_ws3_section(2, 1)
        sows_testings.create_sow_seminated_usouded_ws3_section(2, 2)
        sows_testings.create_sow_seminated_usouded_ws3_section(3, 1)
        sows_testings.create_sow_seminated_usouded_ws3_section(3, 1)
        sows_testings.create_sow_seminated_usouded_ws3_section(3, 1)

        tour5 = Tour.objects.get_or_create_by_week_in_current_year(week_number=5)

        location = Location.objects.filter(section__number=1, section__workshop__number=3).first()
        data = Sow.objects.get_tours_with_count_sows_by_location(location)
        self.assertEqual(data[0]['count_sows'], 2)
        self.assertEqual(data[1]['count_sows'], 1)
        self.assertEqual(data[2]['count_sows'], 3)

        location = Location.objects.filter(section__number=2, section__workshop__number=3).first()
        data = Sow.objects.get_tours_with_count_sows_by_location(location)
        self.assertEqual(data[0]['count_sows'], 1)
        self.assertEqual(data[1]['count_sows'], 1)
        
        with self.assertNumQueries(1):
            data = Sow.objects.get_tours_with_count_sows_by_location(location)
            print(data)

    def test_queryset_serializer(self):
        location1 = Location.objects.filter(sowAndPigletsCell__number=1).first()
        sow1 = sows_testings.create_sow_with_semination_usound(location=location1, week=1)

        location2 = Location.objects.filter(sowAndPigletsCell__number=2).first()
        sow2 = sows_testings.create_sow_with_semination_usound(location=location2, week=1)

        location3 = Location.objects.filter(sowAndPigletsCell__number=3).first()
        sow3 = sows_testings.create_sow_with_semination_usound(location=location3, week=2)

        location4 = Location.objects.filter(sowAndPigletsCell__number=4).first()
        sow4 = sows_testings.create_sow_with_semination_usound(location=location4, week=2)

        location5 = Location.objects.filter(sowAndPigletsCell__number=5).first()
        sow5 = sows_testings.create_sow_with_semination_usound(location=location5, week=3)

        location6 = Location.objects.filter(sowAndPigletsCell__number=6).first()
        sow6 = sows_testings.create_sow_with_semination_usound(location=location6, week=4)

        location7 = Location.objects.filter(sowAndPigletsCell__number=6).first()
        sow7 = sows_testings.create_sow_with_semination_usound(location=location7, week=5)

        location8 = Location.objects.filter(workshop__number=2).first()
        sow8 = sows_testings.create_sow_with_semination_usound(location=location8, week=5)

        sows_qs = Sow.objects.filter(pk__in=[sow1.pk, sow2.pk, sow3.pk, sow4.pk, sow5.pk, sow6.pk, sow7.pk])

        # Semination.objects.mass_semination(sows_qs=sows_qs, week=8,
        #  initiator=None, semination_employee=None)

        with self.assertNumQueries(4):
            data = Sow.objects.all() \
                .select_related('location__workshop') \
                .select_related('location__sowAndPigletsCell__section', 'status', 'tour') \
                .prefetch_related('semination_set__tour') \
                .prefetch_related(
                    Prefetch(
                        'ultrasound_set',
                        queryset=Ultrasound.objects.all().select_related('u_type', 'tour'),
                    )
                )
            # print(data[0].semination_set.all())
            serializer = SowManySerializer(data, many=True)
            print(serializer.data)



# class GiltModelManagerTest(TransactionTestCase):
#     def setUp(self):
#         locations_testing.create_workshops_sections_and_cells()
#         sows_testings.create_statuses()
#         sows_events_testings.create_types()
#         piglets_testing.create_piglets_statuses()

#     def test_create_gilt(self):
#         # 1 cell 1 section
#         location = Location.objects.filter(sowAndPigletsCell__number=1).first()
#         sow = sows_testings.create_sow_with_semination_usound(location, 1)
#         SowFarrow.objects.create_sow_farrow(sow=sow, alive_quantity=10)
        
#         gilt = Gilt.objects.create_gilt(birth_id=1, mother_sow=sow)

#         self.assertEqual(gilt.mother_sow, sow)
#         self.assertEqual(gilt.tour.week_number, 1)
#         self.assertEqual(gilt.farrow, sow.get_last_farrow)
        
        # with self.assertRaises(ValidationError):
        #     # not unique birthId
        #     gilt2 = Gilt.objects.create_gilt(birth_id=1, mother_sow=sow)

        # sow2 = sows_testings.create_sow_with_location(Location.objects.get(workshop__number=3))
        # with self.assertRaises(ValidationError):
        #     gilt3 = Gilt.objects.create_gilt(birth_id=12, mother_sow=sow2)
