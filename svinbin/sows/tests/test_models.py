# -*- coding: utf-8 -*-
from datetime import datetime, date
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
from sows.models import Sow, Gilt, Boar, SowStatus, SowStatusRecord
from sows_events.models import SowFarrow, Ultrasound, Semination
from tours.models import Tour

from sows.serializers import SowManySerializer


class SowModelTest(TransactionTestCase):
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

    def test_create_or_return(self):
        sow, created = Sow.objects.create_or_return(123)
        self.assertEqual(sow.farm_id, 123)
        self.assertEqual(created, True)

        sow, created = Sow.objects.create_or_return(123)
        self.assertEqual(sow.farm_id, 123)
        self.assertEqual(created, False)

    def test_change_status_and_create_status_record(self):
        sow1 = sows_testings.create_sow_and_put_in_workshop_one()

        status1 = SowStatus.objects.get(title='Ожидает осеменения')
        status2 = SowStatus.objects.get(title='Осеменена 1')
        status3 = SowStatus.objects.get(title='Супорос 35')

        sow1.change_status_to('Ожидает осеменения')

        self.assertEqual(SowStatusRecord.objects.all().count(), 1)
        status_record = SowStatusRecord.objects.all().first()
        self.assertEqual(status_record.status_before, None)
        self.assertEqual(status_record.status_after.title, 'Ожидает осеменения')

        sow1.change_status_to('Осеменена 1')

        status_record = SowStatusRecord.objects.all().order_by('-created_at').first()
        self.assertEqual(status_record.status_before.title, 'Ожидает осеменения')
        self.assertEqual(status_record.status_after.title, 'Осеменена 1')

    def test_qs_update_status(self):
        sow1 = sows_testings.create_sow_and_put_in_workshop_one()
        sow2 = sows_testings.create_sow_and_put_in_workshop_one()
        sow3 = sows_testings.create_sow_and_put_in_workshop_one()

        sows = Sow.objects.all()
        sows.update_status(title='Ожидает осеменения')

        self.assertEqual(SowStatusRecord.objects.all().count(), 3)

    def test_qs_add_status_at_date(self):
        date1 = date(2020, 5, 1)
        date2 = date(2020, 5, 3)
        date3 = date(2020, 4, 25)

        sow1 = sows_testings.create_sow_and_put_in_workshop_one()
        sow2 = sows_testings.create_sow_and_put_in_workshop_one()
        sow3 = sows_testings.create_sow_and_put_in_workshop_one()

        sows = Sow.objects.all()
        sows.update_status(title='Ожидает осеменения')

        sows.update_status(title='Осеменена 1')

        s_records = SowStatusRecord.objects.filter(status_after__title='Осеменена 1')
        s_record = s_records.first()

        s_record.date = date1
        s_record.save()

        sow = sows.add_status_at_date(date=date2).filter(pk=s_record.sow.pk).first()
        self.assertEqual(sow.status_at_date, 'Осеменена 1')

        sow = sows.add_status_at_date(date=date3).filter(pk=s_record.sow.pk).first()
        self.assertEqual(sow.status_at_date, None)

        sow = sows.add_status_at_date(date=date2).add_status_at_date_count('Осеменена 1', 'osem')\
            .filter(pk=s_record.sow.pk).first()
        self.assertEqual(sow.count_status_osem, 1)        


class SowQueryTest(TransactionTestCase):
    def setUp(self):
        locations_testing.create_workshops_sections_and_cells()
        sows_testings.create_statuses()
        sows_events_testings.create_types()
        piglets_testing.create_piglets_statuses()

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
            serializer = SowManySerializer(data, many=True)
            serializer.data


class GiltModelManagerTest(TransactionTestCase):
    def setUp(self):
        locations_testing.create_workshops_sections_and_cells()
        sows_testings.create_statuses()
        sows_events_testings.create_types()
        piglets_testing.create_piglets_statuses()

    def test_create_gilt(self):
        # 1 cell 1 section
        location = Location.objects.filter(sowAndPigletsCell__number=1).first()
        sow = sows_testings.create_sow_with_semination_usound(location, 1)
        farrow = SowFarrow.objects.create_sow_farrow(sow=sow, alive_quantity=10)
        piglets = farrow.piglets_group
        
        gilt = Gilt.objects.create_gilt(birth_id='1a', mother_sow_farm_id=sow.farm_id,
             piglets=piglets)

        self.assertEqual(gilt.mother_sow, sow)
        self.assertEqual(gilt.tour.week_number, 1)
        self.assertEqual(gilt.farrow, sow.get_last_farrow)
        self.assertEqual(piglets.gilts_quantity, 1)