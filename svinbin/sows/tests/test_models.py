# -*- coding: utf-8 -*-
from freezegun import freeze_time

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
from sows.models import Sow, Gilt, Boar, SowStatus, SowStatusRecord, SowGroupRecord
from sows_events.models import SowFarrow, Ultrasound, Semination, AssingFarmIdEvent, \
    PigletsToSowsEvent, CullingSow, MarkAsGilt, CullingBoar
from tours.models import Tour
from transactions.models import SowTransaction

from sows.serializers import SowManySerializer, SowOperationSerializer, SowWithOpsSerializer


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

    def test_create_or_return_then_assing_farm_id_exist(self):
        sow = Sow.objects.get_or_create_by_farm_id(farm_id=123)
        assigned_sow = Sow.objects.create_or_return_then_assing_farm_id(farm_id=123,
            birth_id='abc')
        self.assertEqual(Sow.objects.filter(farm_id=123).count(), 1)
        self.assertEqual(AssingFarmIdEvent.objects.all().count(), 0)
        sow.refresh_from_db()
        self.assertEqual(sow.birth_id, 'abc')

    def test_create_or_return_then_assing_farm_id_from_gilt_without_birth_id(self):
        sow = Sow.objects.get_or_create_by_farm_id(farm_id=123)
        sow.farm_id = None
        sow.save()

        assigned_sow = Sow.objects.create_or_return_then_assing_farm_id(farm_id=123,
            birth_id='abc')
        self.assertEqual(Sow.objects.filter(farm_id=123).count(), 1)
        self.assertEqual(AssingFarmIdEvent.objects.all().count(), 1)

        assing_event = AssingFarmIdEvent.objects.all().first()
        self.assertEqual(assing_event.sow, assigned_sow)
        self.assertEqual(assing_event.assing_type, 'gilt')

        sow.refresh_from_db()
        self.assertEqual(sow.birth_id, 'abc')

    def test_create_or_return_then_assing_farm_id_from_gilt_with_birth_id(self):
        sow = Sow.objects.get_or_create_by_farm_id(farm_id=123, birth_id='xyz')
        sow.farm_id = None
        sow.save()

        assigned_sow = Sow.objects.create_or_return_then_assing_farm_id(farm_id=123,
            birth_id='abc')
        self.assertEqual(Sow.objects.filter(farm_id=123).count(), 1)
        self.assertEqual(AssingFarmIdEvent.objects.all().count(), 1)

        assing_event = AssingFarmIdEvent.objects.all().first()
        self.assertEqual(assing_event.sow, assigned_sow)
        self.assertEqual(assing_event.assing_type, 'gilt')
        self.assertEqual(assing_event.birth_id, 'xyz')

        sow.refresh_from_db()
        self.assertEqual(sow.birth_id, 'xyz')

    def test_create_or_return_then_assing_farm_id_from_nowhere(self):
        self.assertEqual(Sow.objects.filter(farm_id=123).count(), 0)
        rem1 = sows_testings.create_sow_remont_without_farm_id()
        rem2 = sows_testings.create_sow_remont_without_farm_id()

        assigned_sow = Sow.objects.create_or_return_then_assing_farm_id(farm_id=123)
        self.assertEqual(Sow.objects.filter(farm_id=123).count(), 1)
        self.assertEqual(AssingFarmIdEvent.objects.all().count(), 1)

        assing_event = AssingFarmIdEvent.objects.all().first()
        self.assertEqual(assing_event.sow, assigned_sow)
        self.assertEqual(assing_event.assing_type, 'gilt')

    def test_change_status_to_previous(self):
        sow = sows_testings.create_sow_and_put_in_workshop_three()
        sow.change_status_to('Ремонтная')
        sow.change_status_to('Супорос 28')
        self.assertEqual(SowStatusRecord.objects.all().count(), 2)
        self.assertEqual(sow.status.title, 'Супорос 28')

        sow.change_status_to_previous_delete_current_status_record()
        self.assertEqual(SowStatusRecord.objects.all().count(), 1)
        self.assertEqual(sow.status.title, 'Ремонтная')

    def test_has_any_event_after(self):
        with freeze_time("2021-02-2"):
            sow = sows_testings.create_sow_and_put_in_workshop_one()
            self.assertEqual(sow.has_any_event_after(created_at=datetime(2021, 2, 2, 0, 0)), False)

        with freeze_time("2021-02-3"):
            Semination.objects.create_semination(sow=sow, week=1, initiator=None,
             semination_employee=None, date=datetime(2021, 2, 3, 0, 0))
            self.assertEqual(sow.has_any_event_after(created_at=datetime(2021, 2, 2, 0, 1)), True)

        with freeze_time("2021-02-3T10:00"):
            Ultrasound.objects.create_ultrasound(sow=sow, result=True, days=60,
                 date=datetime(2021, 2, 3, 10, 0))
            self.assertEqual(sow.has_any_event_after(created_at=datetime(2021, 2, 3, 0, 0)), True)
            self.assertEqual(sow.has_any_event_after(created_at=datetime(2021, 2, 3, 20, 0)), False)

        with freeze_time("2021-02-4T10:00"):
            SowTransaction.objects.create_transaction(sow=sow, 
                to_location=Location.objects.filter(sowAndPigletsCell__isnull=False)[0],
                date=datetime(2021, 2, 4, 10, 0))
            self.assertEqual(sow.has_any_event_after(created_at=datetime(2021, 2, 4, 0, 0)), True)
            self.assertEqual(sow.has_any_event_after(created_at=datetime(2021, 2, 4, 20, 0)), False)

        with freeze_time("2021-02-5T10:00"):
            SowFarrow.objects.create_sow_farrow(sow=sow, alive_quantity=7, mummy_quantity=1,
                date=datetime(2021, 2, 5, 10, 0))
            self.assertEqual(sow.has_any_event_after(created_at=datetime(2021, 2, 5, 0, 0)), True)
            self.assertEqual(sow.has_any_event_after(created_at=datetime(2021, 2, 5, 20, 0)), False)


class SowManagerV2Test(TransactionTestCase):
    def setUp(self):
        locations_testing.create_workshops_sections_and_cells()
        sows_testings.create_statuses()
        sows_events_testings.create_types()
        piglets_testing.create_piglets_statuses()

        self.tour1 = Tour.objects.get_or_create_by_week(week_number=1, year=2020)
        self.tour2 = Tour.objects.get_or_create_by_week(week_number=2, year=2020)
        self.cells = Location.objects.filter(pigletsGroupCell__isnull=False)
        self.piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(tour=self.tour1, 
            location=self.cells[0], quantity=100, birthday=date(2020, 1, 1))
        self.piglets2 = piglets_testing.create_new_group_with_metatour_by_one_tour(tour=self.tour1, 
            location=self.cells[1], quantity=100, birthday=date(2020, 1, 1))

    def test_get_sows_at_date(self):
        to_gilts_date = date(2020, 5, 5)
        target_date = date(2020, 10, 10)
        to_gilt_event = PigletsToSowsEvent.objects.create_event(piglets=self.piglets1, date=to_gilts_date)

        sow1 = Sow.objects.all().first()
        CullingSow.objects.create_culling(sow=sow1, culling_type='padej', date=date(2020, 9, 9))

        sow2 = Sow.objects.all()[1]
        CullingSow.objects.create_culling(sow=sow2, culling_type='padej', date=date(2020, 10, 12))
       
        sows = Sow.objects.get_sows_at_date(date=target_date)
        self.assertEqual(sows.count(), 99)

    def test_count_sows_at_date(self):
        to_gilts_date = date(2020, 5, 5)
        target_date = date(2020, 10, 10)
        to_gilt_event = PigletsToSowsEvent.objects.create_event(piglets=self.piglets1, date=to_gilts_date)

        sow1 = Sow.objects.all().first()
        CullingSow.objects.create_culling(sow=sow1, culling_type='padej', date=date(2020, 9, 9))

        sow2 = Sow.objects.all()[1]
        CullingSow.objects.create_culling(sow=sow2, culling_type='padej', date=date(2020, 10, 12))

        sows_count = Sow.objects.count_sows_at_date(date=target_date)
        self.assertEqual(sows_count, 99)

    def test_update_info_after_semination1(self):
        sow1 = sows_testings.create_sow_and_put_in_workshop_one()
        sow1.change_status_to('Ремонтная')
        sow1.change_group_to('Ремонтная')

        Semination.objects.create_semination_tour(sow=sow1, tour=self.tour1)
        sow1.refresh_from_db()
        self.assertEqual(sow1.sow_group.title, 'Проверяемая')

        sow1.change_group_to('С опоросом')
        Semination.objects.create_semination_tour(sow=sow1, tour=self.tour1)
        sow1.refresh_from_db()
        self.assertEqual(sow1.sow_group.title, 'С опоросом')

        
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

    def test_get_tours(self):
        location1 = Location.objects.filter(workshop__number=1).first()
        sow1 = sows_testings.create_sow_with_semination_usound(location=location1, week=1)
        sow2 = sows_testings.create_sow_with_semination_usound(location=location1, week=1)
        sow3 = sows_testings.create_sow_with_semination_usound(location=location1, week=2)

        location2 = Location.objects.filter(workshop__number=2).first()
        sow4 = sows_testings.create_sow_with_semination_usound(location=location2, week=2)
        sow5 = sows_testings.create_sow_with_semination_usound(location=location2, week=3)

        location6 = Location.objects.filter(sowAndPigletsCell__number=6).first()
        sow6 = sows_testings.create_sow_with_semination_usound(location=location6, week=4)
        location7 = Location.objects.filter(sowAndPigletsCell__number=6).first()
        sow7 = sows_testings.create_sow_with_semination_usound(location=location7, week=5)

        ws1_tours = Sow.objects.all().get_tours_pks(workshop_number=1)
        # self.assertEqual(ws1_tours[0], 1)
        # self.assertEqual(ws1_tours[1], 2)
        ws2_tours = Sow.objects.all().get_tours_pks(workshop_number=2)
        # self.assertEqual(ws2_tours[0], 2)
        # self.assertEqual(ws2_tours[1], 3)
        ws3_tours = Sow.objects.all().get_tours_pks(workshop_number=3)        
        # self.assertEqual(ws3_tours[0], 4)
        # self.assertEqual(ws3_tours[1], 5)

    def test_mark_as_gilt_qs(self):
        cells = Location.objects.filter(sowAndPigletsCell__isnull=False)
        sow = sows_testings.create_sow_with_semination_usound(cells[0], 1)
        farrow = SowFarrow.objects.create_sow_farrow(sow=sow, alive_quantity=10)
        piglets = farrow.piglets_group
        gilt1 = Gilt.objects.create_gilt(birth_id='1a', mother_sow_farm_id=sow.farm_id,
             piglets=piglets)
        mg1 = MarkAsGilt.objects.create_init_gilt_event(gilt=gilt1)
        gilt2 = Gilt.objects.create_gilt(birth_id='2a', mother_sow_farm_id=sow.farm_id,
             piglets=piglets)
        mg2 = MarkAsGilt.objects.create_init_gilt_event(gilt=gilt2)

        sow2 = sows_testings.create_sow_with_semination_usound(cells[1], 1)
        farrow2 = SowFarrow.objects.create_sow_farrow(sow=sow2, alive_quantity=10)
        piglets2 = farrow2.piglets_group
        gilt3 = Gilt.objects.create_gilt(birth_id='3a', mother_sow_farm_id=sow2.farm_id,
             piglets=piglets2)
        mg3 = MarkAsGilt.objects.create_init_gilt_event(gilt=gilt3)
        gilt4 = Gilt.objects.create_gilt(birth_id='4a', mother_sow_farm_id=sow2.farm_id,
             piglets=piglets2)
        mg4 = MarkAsGilt.objects.create_init_gilt_event(gilt=gilt4)

        sow3 = sows_testings.create_sow_with_semination_usound(cells[2], 1)
        farrow3 = SowFarrow.objects.create_sow_farrow(sow=sow3, alive_quantity=10)
        piglets3 = farrow3.piglets_group
        gilt5 = Gilt.objects.create_gilt(birth_id='5a', mother_sow_farm_id=sow3.farm_id,
             piglets=piglets3)
        mg5 = MarkAsGilt.objects.create_init_gilt_event(gilt=gilt5)
        gilt6 = Gilt.objects.create_gilt(birth_id='6a', mother_sow_farm_id=sow3.farm_id,
             piglets=piglets3)
        mg6 = MarkAsGilt.objects.create_init_gilt_event(gilt=gilt6)

        sows_qs = Sow.objects.get_queryset_with_not_alive()\
                             .add_mark_as_gilt_last_date_and_last_tour() \
                             .order_by('-last_date_mark')
        self.assertEqual(sows_qs.first().last_date_mark, mg6.date)
        self.assertEqual(sows_qs.first().last_week_mark, mg6.tour.week_number)


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


class SowGroupTest(TransactionTestCase):
    def setUp(self):
        locations_testing.create_workshops_sections_and_cells()
        sows_testings.create_statuses()
        sows_events_testings.create_types()
        piglets_testing.create_piglets_statuses()

    def test_qs_update_group(self):
        sow1 = sows_testings.create_sow_and_put_in_workshop_one()
        sow2 = sows_testings.create_sow_and_put_in_workshop_one()

        sows = Sow.objects.all()
        sows.update_group(group_title='Ремонтная')

        sow1.refresh_from_db()
        sow2.refresh_from_db()
        self.assertEqual(sow1.sow_group.title, 'Ремонтная')
        self.assertEqual(sow2.sow_group.title, 'Ремонтная')

        self.assertEqual(sow1.group_records.all().count(), 1)
        self.assertEqual(sow2.group_records.all().count(), 1)

        sow1_group_record = sow1.group_records.all().first()
        sow2_group_record = sow2.group_records.all().first()
        self.assertEqual(sow1_group_record.group_before, None)
        self.assertEqual(sow1_group_record.group_after.title, 'Ремонтная')
        self.assertEqual(sow2_group_record.group_before, None)
        self.assertEqual(sow2_group_record.group_after.title, 'Ремонтная')

    def test_model_change_group_to(self):
        sow1 = sows_testings.create_sow_and_put_in_workshop_one()
        sow1.change_group_to('Ремонтная')
 
        sow1.refresh_from_db()
        self.assertEqual(sow1.sow_group.title, 'Ремонтная')

        self.assertEqual(sow1.group_records.all().count(), 1)

        sow1_group_record = sow1.group_records.all().first()
        self.assertEqual(sow1_group_record.group_before, None)
        self.assertEqual(sow1_group_record.group_after.title, 'Ремонтная')

    def test_model_change_group_to2(self):
        sow1 = sows_testings.create_sow_and_put_in_workshop_one()
        sow1.change_group_to('С опоросом')
 
        sow1.refresh_from_db()
        self.assertEqual(sow1.sow_group.title, 'С опоросом')
        self.assertEqual(sow1.group_records.all().count(), 1)

        sow1.change_group_to('С опоросом')
        self.assertEqual(sow1.group_records.all().count(), 1)
        sow1.refresh_from_db()
        self.assertEqual(sow1.sow_group.title, 'С опоросом')

        sow1.change_group_to('Проверяемая')
        self.assertEqual(sow1.group_records.all().count(), 1)
        sow1.refresh_from_db()
        self.assertEqual(sow1.sow_group.title, 'С опоросом')

    def test_model_change_group_to_restrict1(self):
        # should not change to Проверяемая if not Ремонтная
        sow1 = sows_testings.create_sow_and_put_in_workshop_one()
        sow1.change_group_to('Проверяемая')
 
        sow1.refresh_from_db()
        self.assertEqual(sow1.sow_group, None)
        self.assertEqual(sow1.group_records.all().count(), 0)

        sow1.change_group_to('Ремонтная')
        sow1.change_group_to('Проверяемая')
        sow1.refresh_from_db()
        self.assertEqual(sow1.sow_group.title, 'Проверяемая')
        self.assertEqual(sow1.group_records.all().count(), 2)

        sow1_group_record = sow1.group_records.all().first()
        self.assertEqual(sow1_group_record.group_before.title, 'Ремонтная')
        self.assertEqual(sow1_group_record.group_after.title, 'Проверяемая')

    def test_model_change_group_to_restrict2(self):
        # should not create new records if С опоросом already
        sow1 = sows_testings.create_sow_and_put_in_workshop_one()

        sow1.change_group_to('Ремонтная')
        sow1.change_group_to('Проверяемая')
        sow1.change_group_to('С опоросом')
        sow1.refresh_from_db()
        self.assertEqual(sow1.sow_group.title, 'С опоросом')
        self.assertEqual(sow1.group_records.all().count(), 3)

        sow1_group_record = sow1.group_records.all().first()
        self.assertEqual(sow1_group_record.group_before.title, 'Проверяемая')
        self.assertEqual(sow1_group_record.group_after.title, 'С опоросом') 

        sow1.change_group_to('С опоросом')
        sow1.refresh_from_db()
        self.assertEqual(sow1.sow_group.title, 'С опоросом')
        self.assertEqual(sow1.group_records.all().count(), 3)

        sow1_group_record = sow1.group_records.all().first()
        self.assertEqual(sow1_group_record.group_before.title, 'Проверяемая')
        self.assertEqual(sow1_group_record.group_after.title, 'С опоросом')

    def test_qs_add_group_at_date(self):
        # add_group_at_date
        date1 = date(2020, 5, 1)
        date2 = date(2020, 5, 15)
        date3 = date(2020, 6, 25)

        sow1 = sows_testings.create_sow_and_put_in_workshop_one()
        sow2 = sows_testings.create_sow_and_put_in_workshop_one()
        sow3 = sows_testings.create_sow_and_put_in_workshop_one()

        sows = Sow.objects.all()
        sows.update_group(group_title='Ремонтная', date=date1)
        sows.update_group(group_title='Проверяемая', date=date2)
        sows.update_group(group_title='С опоросом', date=date3)

        sows = sows.add_group_at_date(date=date1)
        sow = sows.first()
        self.assertEqual(sow.sow_group.title, 'С опоросом')
        self.assertEqual(sow.group_at_date, 'Ремонтная')

        sows = sows.add_group_at_date(date=date2)
        sow = sows.first()
        self.assertEqual(sow.sow_group.title, 'С опоросом')
        self.assertEqual(sow.group_at_date, 'Проверяемая')

        sows = sows.add_group_at_date(date=date3)
        sow = sows.first()
        self.assertEqual(sow.sow_group.title, 'С опоросом')
        self.assertEqual(sow.group_at_date, 'С опоросом')
        
        self.assertEqual(sow.group_records.all().count(), 3)
        sow = sows.first()
        sow.change_group_to(group_title='С опоросом')
        self.assertEqual(sow.group_records.all().count(), 3)

    def test_qs_add_group_count_at_date(self):
        date1 = date(2020, 5, 1)
        date2 = date(2020, 5, 15)
        date3 = date(2020, 6, 25)

        sow1 = sows_testings.create_sow_and_put_in_workshop_one()
        sow2 = sows_testings.create_sow_and_put_in_workshop_one()
        sow3 = sows_testings.create_sow_and_put_in_workshop_one()

        sows = Sow.objects.all()
        sows.update_group(group_title='Ремонтная', date=date1)
        sows.update_group(group_title='Проверяемая', date=date2)
        sows.update_group(group_title='С опоросом', date=date3)

        sows = sows.add_group_at_date(date=date1) \
                   .add_group_at_date_count('Ремонтная', 'rem') \
                   .add_group_at_date_count('Проверяемая', 'check') \
                   .add_group_at_date_count('С опоросом', 'oporos')

        sow = sows.first()
        self.assertEqual(sow.count_group_rem, 3)
        self.assertEqual(sow.count_group_check, 0)
        self.assertEqual(sow.count_group_oporos, 0)

        sows = sows.add_group_at_date(date=date2) \
                   .add_group_at_date_count('Ремонтная', 'rem') \
                   .add_group_at_date_count('Проверяемая', 'check') \
                   .add_group_at_date_count('С опоросом', 'oporos')

        sow = sows.first()
        self.assertEqual(sow.count_group_rem, 0)
        self.assertEqual(sow.count_group_check, 3)
        self.assertEqual(sow.count_group_oporos, 0)

        sows = sows.add_group_at_date(date=date3) \
                   .add_group_at_date_count('Ремонтная', 'rem') \
                   .add_group_at_date_count('Проверяемая', 'check') \
                   .add_group_at_date_count('С опоросом', 'oporos')

        sow = sows.first()
        self.assertEqual(sow.count_group_rem, 0)
        self.assertEqual(sow.count_group_check, 0)
        self.assertEqual(sow.count_group_oporos, 3)

    def test_manager_count_prov_to_osn_in_daterange(self):
        date1 = date(2020, 5, 1)
        date2 = date(2020, 5, 15)
        date3 = date(2020, 6, 25)

        sow1 = sows_testings.create_sow_and_put_in_workshop_one()
        sow2 = sows_testings.create_sow_and_put_in_workshop_one()
        sow3 = sows_testings.create_sow_and_put_in_workshop_one()

        sows = Sow.objects.all()
        sows.update_group(group_title='Ремонтная', date=date1)
        sows.update_group(group_title='Проверяемая', date=date2)
        sows.update_group(group_title='С опоросом', date=date3)

        data = (SowGroupRecord.objects.all().count_group_tranfer_in_daterange(
            start_date=date(2020, 5, 1), end_date=date(2020, 5, 16)
            ))
        self.assertEqual(data['count_prov_to_osn'], 0)
        self.assertEqual(data['count_rem_to_prov'], 3)

        data = (SowGroupRecord.objects.all().count_group_tranfer_in_daterange(
            start_date=date(2020, 5, 16), end_date=date(2020, 6, 26)
            ))
        self.assertEqual(data['count_prov_to_osn'], 3)
        self.assertEqual(data['count_rem_to_prov'], 0)


class SowModelOperationsTest(TransactionTestCase):
    def setUp(self):
        locations_testing.create_workshops_sections_and_cells()
        sows_testings.create_statuses()
        sows_events_testings.create_types()
        piglets_testing.create_piglets_statuses()

    def test_operations(self):
        loc = Location.objects.get(workshop__number=1)
        sow = sows_testings.create_sow_with_location(location=loc)

        Semination.objects.create_semination(sow=sow, week=10, date=date(2020, 6, 1))
        Ultrasound.objects.create_ultrasound(sow=sow, result=True, 
            days=30, date=date(2020, 6, 30))
        Ultrasound.objects.create_ultrasound(sow=sow, result=True, 
            days=60, date=date(2020, 7, 15))

        loc2 = Location.objects.get(workshop__number=2)
        SowTransaction.objects.create_transaction(sow=sow, to_location=loc2,
            date=date(2020, 7, 17))

        with self.assertNumQueries(5):
            ops = SowOperationSerializer(sow.last_operations, many=True).data
            self.assertEqual(ops[0]['op_label'], 'перемещение')


class SowDowntimeTest(TransactionTestCase):
    def setUp(self):
        locations_testing.create_workshops_sections_and_cells()
        sows_testings.create_statuses()
        sows_events_testings.create_types()
        piglets_testing.create_piglets_statuses()

    def test_add_last_status_record_date(self):
        loc = Location.objects.get(workshop__number=1)
        sow = sows_testings.create_sow_with_location(location=loc)

        with freeze_time("2021-02-5T10:00"):
            sow.change_status_to('Ремонтная')

        with freeze_time("2021-02-10T10:00"):
            sow.change_status_to('Ожидает осеменения')

        with freeze_time("2021-02-15T10:00"):
            sow.change_status_to('Осеменена 1')

        marked_sows = Sow.objects.all().add_last_status_record_date()
        self.assertEqual(marked_sows.first().last_record_date, datetime(2021,2,15,10,0))

    def test_add_last_status_record_date_substract_now_date(self):
        loc = Location.objects.get(workshop__number=1)
        sow1 = sows_testings.create_sow_with_location(location=loc)
        with freeze_time("2021-02-5T10:00"):
            sow1.change_status_to('Ремонтная')

        sow2 = sows_testings.create_sow_with_location(location=loc)
        with freeze_time("2021-02-10T10:00"):
            sow2.change_status_to('Ремонтная')

        with freeze_time("2021-02-25T10:00"):
            sows = Sow.objects.all().add_last_status_record_date() \
                .add_last_status_record_date_substract_now_date()
            self.assertEqual(sows.get(pk=sow1.pk).sub_result_days.days, 20)
            self.assertEqual(sows.get(pk=sow2.pk).sub_result_days.days, 15)

    def test_sows_by_statuses_count_and_downtime_qs(self):
        loc = Location.objects.get(workshop__number=1)
        sow1 = sows_testings.create_sow_with_location(location=loc)
        with freeze_time("2021-02-5T10:00"):
            sow1.change_status_to('Ремонтная')

        sow2 = sows_testings.create_sow_with_location(location=loc)
        with freeze_time("2021-02-10T10:00"):
            sow2.change_status_to('Ремонтная')

        sow3 = sows_testings.create_sow_with_location(location=loc)
        with freeze_time("2021-02-15T10:00"):
            sow3.change_status_to('Ремонтная')

        with freeze_time("2021-02-25T10:00"):
            waiting_sem_count, downtime_sows_qs = Sow.objects.all() \
                .sows_by_statuses_count_and_downtime_qs(statuses=["Ожидает осеменения", "Прохолост",
                    "Аборт", "Ремонтная"], days_limit=11)
            self.assertEqual(waiting_sem_count, 3)
            self.assertEqual(downtime_sows_qs.count(), 2)
            self.assertTrue(sow1.pk in downtime_sows_qs.values_list('pk', flat=True))
            self.assertTrue(sow2.pk in downtime_sows_qs.values_list('pk', flat=True))
            self.assertEqual(downtime_sows_qs.get(pk=sow1.pk).sub_result_days.days, 20)

    def test_queries(self):
        loc = Location.objects.get(workshop__number=1)
        sow1 = sows_testings.create_sow_with_location(location=loc)
        with freeze_time("2021-01-5T10:00"):
            sow1.change_status_to('Ремонтная')

        sow2 = sows_testings.create_sow_with_location(location=loc)
        with freeze_time("2021-01-5T10:00"):
            sow2.change_status_to('Осеменена 2')

        sow3 = sows_testings.create_sow_with_location(location=loc)
        with freeze_time("2021-01-5T10:00"):
            sow3.change_status_to('Супорос 35')

        sow4 = sows_testings.create_sow_with_location(location=loc)
        with freeze_time("2021-01-5T10:00"):
            sow4.change_status_to('Опоросилась')

        with self.assertNumQueries(1):
            waiting_sem_count, downtime_sows_qs = Sow.objects.all() \
                .sows_by_statuses_count_and_downtime_qs(statuses=["Ожидает осеменения", "Прохолост",
                    "Аборт", "Ремонтная"], days_limit=11)


class Sow24fReportTest(TransactionTestCase):
    def setUp(self):
        locations_testing.create_workshops_sections_and_cells()
        sows_testings.create_statuses()
        sows_events_testings.create_types()
        piglets_testing.create_piglets_statuses()

    def test_get_sows_at_date(self):
        tour = Tour.objects.get_or_create_by_week_in_current_year(week_number=10)
        location = Location.objects.filter(pigletsGroupCell__isnull=False).first()
        piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(
            tour=tour, location=location, quantity=10)
        piglets2 = piglets_testing.create_new_group_with_metatour_by_one_tour(
            tour=tour, location=location, quantity=15)

        date0 = date(2020, 6, 5)
        event = PigletsToSowsEvent.objects.create_event(piglets=piglets1, date=date0)

        date01 = date(2020, 6, 25)
        event = PigletsToSowsEvent.objects.create_event(piglets=piglets2, date=date01)

        date02 = date(2020, 7, 1)
        sow1 = Sow.objects.all().first()
        CullingSow.objects.create_culling(sow=sow1, culling_type='padej', date=date02)

        date03 = date(2020, 7, 5)
        sow2 = Sow.objects.all().first()
        CullingSow.objects.create_culling(sow=sow2, culling_type='padej', date=date03)

        with self.assertNumQueries(3):
            date1 = date(2020, 8, 5)
            sows = Sow.objects.get_sows_at_date(date=date1)
            self.assertEqual(len(sows), 23)

        date2 = date(2020, 7, 2)
        sows = Sow.objects.get_sows_at_date(date=date2)
        self.assertEqual(len(sows), 24)

    def test_qs_add_label_is_oporos_before(self):
        tour = Tour.objects.get_or_create_by_week_in_current_year(week_number=10)
        location = Location.objects.filter(pigletsGroupCell__isnull=False).first()
        piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(
            tour=tour, location=location, quantity=10)

        date0 = date(2020, 6, 5)
        event = PigletsToSowsEvent.objects.create_event(piglets=piglets1, date=date0)

        date01 = date(2020, 6, 25)
        sow1 = Sow.objects.all().first()
        sow1.farm_id = '123'
        sow1.tour = tour
        sow1.location = Location.objects.filter(sowAndPigletsCell__isnull=False).first()
        sow1.save()
        event = SowFarrow.objects.create_sow_farrow(sow=sow1, alive_quantity=11, date=date01)

        date2 = date(2020, 7, 2)
        sows = Sow.objects.get_sows_at_date(date=date2)
        self.assertEqual(len(sows), 10)

        sows = sows.add_label_is_oporos_before(date=date2).add_status_at_date(date=date2)

        sow1  = sows.get(farm_id=123)
        self.assertEqual(sow1.is_oporos_before, True)
        self.assertEqual(sow1.status_at_date, 'Опоросилась')

        sow2  = sows.filter(farm_id__isnull=True).first()
        self.assertEqual(sow2.is_oporos_before, False)
        self.assertEqual(sow2.status_at_date, 'Ремонтная')

    def test_qs_add_label_is_checking(self):
        tour = Tour.objects.get_or_create_by_week_in_current_year(week_number=10)
        location = Location.objects.filter(pigletsGroupCell__isnull=False).first()
        piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(
            tour=tour, location=location, quantity=10)

        date0 = date(2020, 6, 5)
        event = PigletsToSowsEvent.objects.create_event(piglets=piglets1, date=date0)

        # one sow farrow
        date01 = date(2020, 6, 10)
        sow1 = Sow.objects.all().first()
        sow1.farm_id = '123'
        sow1.tour = tour
        sow1.location = Location.objects.filter(sowAndPigletsCell__isnull=False).first()
        sow1.save()
        event = SowFarrow.objects.create_sow_farrow(sow=sow1, alive_quantity=11, date=date01)

        # one sow semination
        date02 = date(2020, 6, 12)
        sow2 = Sow.objects.filter(farm_id__isnull=True).first()
        sow2.farm_id = '124'
        sow2.save()
        event = Semination.objects.create_semination_tour(sow=sow2, tour=tour, date=date02)

        date2 = date(2020, 7, 2)
        sows = Sow.objects.get_sows_at_date(date=date2)
        self.assertEqual(len(sows), 10)

        sows = sows.add_label_is_oporos_before(date=date2) \
                   .add_status_at_date(date=date2) \
                   .add_label_is_checking()

        sow1  = sows.get(farm_id=123)
        self.assertEqual(sow1.is_oporos_before, True)
        self.assertEqual(sow1.status_at_date, 'Опоросилась')
        self.assertEqual(sow1.is_checking, False)

        sow2  = sows.get(farm_id=124)
        self.assertEqual(sow2.is_oporos_before, False)
        self.assertEqual(sow2.is_checking, True)
        self.assertEqual(sow2.status_at_date, 'Осеменена 1')

        sow3  = sows.filter(farm_id__isnull=True).first()
        self.assertEqual(sow3.is_oporos_before, False)
        self.assertEqual(sow3.status_at_date, 'Ремонтная')
        self.assertEqual(sow3.is_checking, False)

    def test_count_boar_at_date(self):
        with freeze_time("2020-11-5T10:00"):
            boar1 = Boar.objects.get_or_create_boar(farm_id=100)

        with freeze_time("2020-11-15T10:00"):
            boar2 = Boar.objects.get_or_create_boar(farm_id=101)

        with freeze_time("2020-11-25T10:00"):
            boar3 = Boar.objects.get_or_create_boar(farm_id=102)

        with freeze_time("2020-12-25T10:00"):
            boar4 = Boar.objects.get_or_create_boar(farm_id=103)

        with freeze_time("2021-01-07T10:00"):
            boar5 = Boar.objects.get_or_create_boar(farm_id=104)
            boar6 = Boar.objects.get_or_create_boar(farm_id=105)
            boar7 = Boar.objects.get_or_create_boar(farm_id=106)

        with freeze_time("2021-01-5T10:00"):
            CullingBoar.objects.create_culling_boar(boar=boar1, culling_type='padej')

        with freeze_time("2021-01-10T10:00"):
            CullingBoar.objects.create_culling_boar(boar=boar2, culling_type='padej')

        with freeze_time("2021-01-15T10:00"):
            CullingBoar.objects.create_culling_boar(boar=boar3 , culling_type='padej')

        self.assertEqual(Boar.objects.count_alive_at_date(date=date(2021, 1, 3)), 4)

        self.assertEqual(Boar.objects.count_alive_at_date(date=date(2021, 1, 5)), 4)
        self.assertEqual(Boar.objects.count_alive_at_date(date=date(2021, 1, 5),
         count_at_end_date=True), 3)
        self.assertEqual(Boar.objects.count_alive_at_date(date=date(2021, 1, 6)), 3)

        self.assertEqual(Boar.objects.count_alive_at_date(date=date(2021, 1, 7)), 3)
        self.assertEqual(Boar.objects.count_alive_at_date(date=date(2021, 1, 7),
         count_at_end_date=True), 6)
        self.assertEqual(Boar.objects.count_alive_at_date(date=date(2021, 1, 8)), 6)

        self.assertEqual(Boar.objects.count_alive_at_date(date=date(2021, 1, 10)), 6)
        self.assertEqual(Boar.objects.count_alive_at_date(date=date(2021, 1, 10),
         count_at_end_date=True), 5)
        self.assertEqual(Boar.objects.count_alive_at_date(date=date(2021, 1, 11)), 5)

        self.assertEqual(Boar.objects.count_alive_at_date(date=date(2021, 1, 15)), 5)
        self.assertEqual(Boar.objects.count_alive_at_date(date=date(2021, 1, 15),
         count_at_end_date=True), 4)
        self.assertEqual(Boar.objects.count_alive_at_date(date=date(2021, 1, 16)), 4)


class Sow24fReportCalculationsInDayTest(TransactionTestCase):
    def setUp(self):
        locations_testing.create_workshops_sections_and_cells()
        sows_testings.create_statuses()
        sows_events_testings.create_types()
        piglets_testing.create_piglets_statuses()

        self.tour1 = Tour.objects.get_or_create_by_week_in_current_year(week_number=1)
        location = Location.objects.filter(pigletsGroupCell__workshop__number=5).first()
        piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(
            tour=self.tour1, location=location, quantity=30)

        # create 30 rem sows via pts event
        date0 = date(2020, 6, 5)
        event = PigletsToSowsEvent.objects.create_event(piglets=piglets1, date=date0)

    def test_rem_period_tr_in(self):
        date1 = date(2020, 6, 7)
        start_date_sows = Sow.objects.get_sows_at_date(date=date1) \
                             .add_group_at_date(date=date1) \
                             .add_group_at_date_count('Ремонтная', 'rem').first()
        self.assertEqual(start_date_sows.count_group_rem, 30)

    def test_rem_period_tr_in_some_to_prov(self):
        date2 = date(2020, 6, 12)
        sows_to_prov = Sow.objects.filter(pk__in=Sow.objects.all().values_list('pk', flat=True)[:7])
        sows_to_prov.update_group(group_title='Проверяемая', date=date2)

        date1 = date(2020, 6, 13)
        start_date_sows = Sow.objects.get_sows_at_date(date=date1) \
                             .add_group_at_date(date=date1) \
                             .add_group_at_date_count('Ремонтная', 'rem').first()
        self.assertEqual(start_date_sows.count_group_rem, 23)

    def test_rem_period_culls(self):
        date2 = date(2020, 6, 12)
        sows_to_padej = Sow.objects.filter(pk__in=Sow.objects.all().values_list('pk', flat=True)[:4])
        CullingSow.objects.mass_culling(sows_qs=sows_to_padej, culling_type='padej', date=date2)

        sows_to_vinuzhd = Sow.objects.filter(pk__in=Sow.objects.all().values_list('pk', flat=True)[:3])
        CullingSow.objects.mass_culling(sows_qs=sows_to_vinuzhd, culling_type='vinuzhd',
         date=date(2020, 6, 14))

        date1 = date(2020, 6, 13)
        start_date_sows = Sow.objects.get_sows_at_date(date=date1) \
                             .add_group_at_date(date=date1) \
                             .add_group_at_date_count('Ремонтная', 'rem').first()
        self.assertEqual(start_date_sows.count_group_rem, 26)

        date1 = date(2020, 6, 15)
        start_date_sows = Sow.objects.get_sows_at_date(date=date1) \
                             .add_group_at_date(date=date1) \
                             .add_group_at_date_count('Ремонтная', 'rem').first()
        self.assertEqual(start_date_sows.count_group_rem, 23)                             
