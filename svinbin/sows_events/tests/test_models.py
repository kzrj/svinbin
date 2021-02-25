# -*- coding: utf-8 -*-
from datetime import datetime, date

from django.utils import timezone
from django.test import TestCase, TransactionTestCase
from django.core.exceptions import ValidationError

from sows_events.models import (
    Semination, Ultrasound, SowFarrow, CullingSow, WeaningSow,
    UltrasoundType, AbortionSow, MarkAsNurse, MarkAsGilt, CullingBoar,
    SemenBoar, PigletsToSowsEvent)
from sows.models import Sow, Boar, Gilt, SowStatusRecord, SowGroupRecord
from piglets.models import Piglets
from locations.models import Location
from transactions.models import SowTransaction
from tours.models import Tour

import locations.testing_utils as locations_testing
import sows.testing_utils as sows_testing
import sows_events.utils as sows_events_testing
import staff.testing_utils as staff_testings
import piglets.testing_utils as piglets_testing


class SeminationModelManagerTest(TestCase):
    def setUp(self):
        locations_testing.create_workshops_sections_and_cells()
        sows_testing.create_statuses()
        sows_testing.create_boars()
        sows_events_testing.create_types()
        self.boar = Boar.objects.all().first()

    def test_create_semination(self):
        sow = Sow.objects.create_new_and_put_in_workshop_one(1)
        boar = Boar.objects.all().first()
        semination = Semination.objects.create_semination(sow=sow, week=1,
         initiator=None, semination_employee=None, boar=boar)

        self.assertEqual(Semination.objects.all().count(), 1)
        self.assertEqual(semination.tour.week_number, 1)
        sow.refresh_from_db()
        self.assertEqual(sow.tour.week_number, 1)
        self.assertEqual(sow.status.title, 'Осеменена 1')

    def test_mass_semination(self):
        sow1 = sows_testing.create_sow_and_put_in_workshop_one()
        sow2 = sows_testing.create_sow_and_put_in_workshop_one()
        sow3 = sows_testing.create_sow_and_put_in_workshop_one()

        sow3.change_group_to('Ремонтная')

        sows_qs = Sow.objects.filter(pk__in=[sow1.pk, sow2.pk, sow3.pk])
        Semination.objects.mass_semination(sows_qs=sows_qs, week=1,
         initiator=None, semination_employee=None, boar=self.boar)
        
        self.assertEqual(Semination.objects.all().count(), 3)

        sow1.refresh_from_db()
        self.assertEqual(sow1.status.title, 'Осеменена 1')
        self.assertEqual(sow1.tour.week_number, 1)
        self.assertEqual(sow1.sow_group, None)

        sow3.refresh_from_db()
        self.assertEqual(sow3.sow_group.title, 'Проверяемая')

    def test_is_there_semination(self):
        sow = Sow.objects.create_new_and_put_in_workshop_one(1)
        boar = Boar.objects.all().first()
        semination = Semination.objects.create_semination(sow=sow, week=54,
         initiator=None, semination_employee=None, boar=boar)
        # tour week = 54, year = 2019
        is_there_semination1 =  Semination.objects.is_there_semination(sow, sow.tour)
        self.assertEqual(is_there_semination1, True)

        tour2 = Tour.objects.get_or_create_by_week_in_current_year(53)
        is_there_semination2 =  Semination.objects.is_there_semination(sow, tour2)
        self.assertEqual(is_there_semination2, False)

    def test_double_semination_or_not(self):
        sow = Sow.objects.create_new_and_put_in_workshop_one(1)

        shmigina = staff_testings.create_employee('ШМЫГИ')
        ivanov = staff_testings.create_employee('ИВАНО')

        boar1 = Boar.objects.get_or_create_boar(123)
        boar2 = Boar.objects.get_or_create_boar(124)

        date = timezone.now()
        tour = Tour.objects.get_or_create_by_week_in_current_year(50)

        sow, seminated = Semination.objects.double_semination_or_not(
            sow=sow, tour=tour, date=date, 
            boar1=boar1, boar2=boar2,
            semination_employee1=shmigina, semination_employee2=ivanov,
            initiator=None
            )
        self.assertEqual(seminated, True)

        is_there_semination1 = Semination.objects.is_there_semination(sow, tour)
        self.assertEqual(is_there_semination1, True)
        self.assertEqual(Semination.objects.filter(sow=sow, tour=tour).count(), 2)

        # already seminated in tour
        sow, seminated = Semination.objects.double_semination_or_not(
            sow=sow, tour=tour, date=date, 
            boar1=boar1, boar2=boar2,
            semination_employee1=shmigina, semination_employee2=ivanov,
            initiator=None
            )
        self.assertEqual(seminated, False)


class UltrasoundModelManagerTest(TestCase):
    def setUp(self):
        locations_testing.create_workshops_sections_and_cells()
        sows_testing.create_statuses()
        sows_events_testing.create_types()

    def test_create_ultrasound(self):
        sow = Sow.objects.create_new_and_put_in_workshop_one(1)
        semination = Semination.objects.create_semination(sow=sow, week=1,
         initiator=None, semination_employee=None)

        ultrasound = Ultrasound.objects.create_ultrasound(sow=sow,
         initiator=None, result=False)

        self.assertEqual(Ultrasound.objects.all().count(), 1)
        self.assertEqual(ultrasound.tour.week_number, 1)
        self.assertEqual(ultrasound.location, sow.location)
        sow.refresh_from_db()
        self.assertEqual(sow.status.title, 'Прохолост')

        Ultrasound.objects.create_ultrasound(sow=sow, 
         initiator=None, result=True, days=30)
        sow.refresh_from_db()
        self.assertEqual(sow.status.title, 'Супорос 28')

        Ultrasound.objects.create_ultrasound(sow=sow, 
         initiator=None, result=False, days=60)
        sow.refresh_from_db()
        self.assertEqual(sow.status.title, 'Прохолост')

    def test_mass_ultrasound(self):
        location = Location.objects.get(workshop__number=1)
        seminated_sow1 =  sows_testing.create_sow_with_semination(location, 1)
        seminated_sow2 =  sows_testing.create_sow_with_semination(location, 1)
        seminated_sow3 =  sows_testing.create_sow_with_semination(location, 1)

        sows_qs = Sow.objects.filter(pk__in=[seminated_sow1.pk, seminated_sow2.pk, seminated_sow3.pk])
        Ultrasound.objects.mass_ultrasound(sows_qs=sows_qs, initiator=None, result=True, days=30)

        seminated_sow2.refresh_from_db()
        self.assertEqual(seminated_sow2.status.title, 'Супорос 28')

        Ultrasound.objects.mass_ultrasound(sows_qs=sows_qs, initiator=None, result=False, days=60)

        seminated_sow3.refresh_from_db()
        self.assertEqual(seminated_sow3.status.title, 'Прохолост')
        self.assertEqual(seminated_sow3.tour, None)


class SowFarrowModelManagerTest(TransactionTestCase):
    def setUp(self):
        locations_testing.create_workshops_sections_and_cells()
        sows_testing.create_statuses()
        sows_events_testing.create_types()
        piglets_testing.create_piglets_statuses()

        self.tour1 = Tour.objects.get_or_create_by_week_in_current_year(week_number=1)
        self.tour2 = Tour.objects.get_or_create_by_week_in_current_year(week_number=2)

    def test_create_farrow(self):
        location = Location.objects.filter(sowAndPigletsCell__number=1).first()
        sow1 = sows_testing.create_sow_with_semination_usound(location=location, week=1)

        # first sow farrow in tour in section
        farrow = SowFarrow.objects.create_sow_farrow(
            sow=sow1,
            alive_quantity=10,
            dead_quantity=1
            )

        self.assertEqual(farrow.piglets_group.quantity, 10)
        self.assertEqual(farrow.piglets_group.metatour.records.all().count(), 1)
        self.assertEqual(farrow.piglets_group.metatour.records.all().first().tour, sow1.tour)
        self.assertEqual(farrow.piglets_group.metatour.records.all().first().quantity, 10)
        self.assertEqual(farrow.piglets_group.metatour.records.all().first().percentage, 100.0)
        
        self.assertEqual(farrow.alive_quantity, 10)
        self.assertEqual(farrow.dead_quantity, 1)

    def test_create_farrow_v2(self):
        # there are another piglets in cell
        location = Location.objects.filter(sowAndPigletsCell__number=1).first()
        piglets2 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour2,
            location, 10)

        sow1 = sows_testing.create_sow_with_semination_usound(location=location, week=1)

        farrow = SowFarrow.objects.create_sow_farrow(
            sow=sow1,
            alive_quantity=10,
            dead_quantity=1
            )

        self.assertEqual(farrow.piglets_group.quantity, 10)
        self.assertEqual(location.piglets.all().count(), 1)
        new_piglets = location.piglets.all().first()
        self.assertEqual(new_piglets.metatour.records.all().count(), 2)

    def test_create_farrow_validation_location(self):
        sow1 = sows_testing.create_sow_seminated_usouded_ws3_section(week=1, section_number=1)

        # sow should be in ws3 cell
        with self.assertRaises(ValidationError):
            farrow = SowFarrow.objects.create_sow_farrow(
                sow=sow1,
                alive_quantity=10,
                dead_quantity=1
                )
    
    def test_create_farrow_farrow_twice(self):
        location = Location.objects.filter(sowAndPigletsCell__number=1).first()
        sow1 = sows_testing.create_sow_with_semination_usound(location=location, week=1)

        farrow = SowFarrow.objects.create_sow_farrow(sow=sow1, alive_quantity=10)
        with self.assertRaises(ValidationError):
            farrow = SowFarrow.objects.create_sow_farrow(
                sow=sow1,
                alive_quantity=10,
                dead_quantity=1
                )

    def test_create_farrow_without_tour(self):
        location = Location.objects.filter(sowAndPigletsCell__number=1).first()
        sow1 = sows_testing.create_sow_with_semination_usound(location=location, week=1)
        sow1.tour = None
        sow1.save()

        with self.assertRaises(ValidationError):
            farrow = SowFarrow.objects.create_sow_farrow(
                sow=sow1,
                alive_quantity=10,
                dead_quantity=1
                )


class CullingSowManagerTest(TestCase):
    def setUp(self):
        locations_testing.create_workshops_sections_and_cells()
        sows_testing.create_statuses()

    def test_create_farrow(self):
        sow = sows_testing.create_sow_and_put_in_workshop_three(1, 1)
        culling = CullingSow.objects.create_culling(sow=sow, culling_type='spec',
         reason='prichina')
        sow.refresh_from_db()
        self.assertEqual(sow.alive, False)
        self.assertEqual(culling.sow, sow)
        self.assertEqual(culling.location, sow.location)
        self.assertEqual(culling.culling_type, 'spec')
        self.assertEqual(culling.reason, 'prichina')

    def test_mass_cullings(self):
        location = Location.objects.get(workshop__number=1)
        seminated_sow1 =  sows_testing.create_sow_with_semination(location, 1)
        seminated_sow2 =  sows_testing.create_sow_with_semination(location, 1)
        seminated_sow3 =  sows_testing.create_sow_with_semination(location, 1)

        sows_qs = Sow.objects.filter(pk__in=[seminated_sow1.pk, seminated_sow2.pk, seminated_sow3.pk])
        CullingSow.objects.mass_culling(sows_qs=sows_qs, initiator=None,
            culling_type='padej')

        seminated_sow2.refresh_from_db()
        self.assertEqual(seminated_sow2.status.title, 'Брак')
        self.assertEqual(seminated_sow2.alive, False)

        seminated_sow3.refresh_from_db()
        self.assertEqual(seminated_sow3.status.title, 'Брак')
        self.assertEqual(seminated_sow3.alive, False)

        self.assertEqual(CullingSow.objects.all().count(), 3)


class WeaningSowTest(TestCase):
    def setUp(self):
        locations_testing.create_workshops_sections_and_cells()
        sows_testing.create_statuses()
        sows_events_testing.create_types()
        piglets_testing.create_piglets_statuses()

    def test_create_weaning(self):
        location = Location.objects.filter(sowAndPigletsCell__number=1).first()
        sow1 = sows_testing.create_sow_with_semination_usound(location=location, week=1)

        # first sow farrow in tour in section
        farrow = SowFarrow.objects.create_sow_farrow(
            sow=sow1,
            alive_quantity=10,
            dead_quantity=1
            )

        piglets = farrow.piglets_group

        weaning1 = sow1.weaningsow_set.create_weaning(sow=sow1, piglets=piglets)
        
        self.assertEqual(weaning1.piglets, piglets)
        self.assertEqual(weaning1.sow, sow1)
        self.assertEqual(weaning1.quantity, piglets.quantity)

        sow1.refresh_from_db()
        self.assertEqual(sow1.tour.week_number, 1)
        self.assertEqual(sow1.status.title, 'Отъем')


class AbortionSowTest(TestCase):
    def setUp(self):
        locations_testing.create_workshops_sections_and_cells()
        sows_testing.create_statuses()
        sows_events_testing.create_types()

    def test_create_abortion(self):
        sow = sows_testing.create_sow_and_put_in_workshop_one()
        Semination.objects.create_semination(sow=sow, week=1, initiator=None,
         semination_employee=None)
        Semination.objects.create_semination(sow=sow, week=1, initiator=None,
         semination_employee=None)
        Ultrasound.objects.create_ultrasound(sow, None, True)

        abort = AbortionSow.objects.create_abortion(sow, None)
        sow.refresh_from_db()
        self.assertEqual(sow.tour, None)
        self.assertEqual(sow.status.title, 'Аборт')
        self.assertEqual(abort.location, sow.location)


class MarkAsNurseTest(TestCase):
    def setUp(self):
        locations_testing.create_workshops_sections_and_cells()
        sows_testing.create_statuses()
        sows_events_testing.create_types()
        piglets_testing.create_piglets_statuses()

    def test_create_nurse_event(self):
        sow = sows_testing.create_sow_and_put_in_workshop_one()
        Semination.objects.create_semination(sow=sow, week=1, initiator=None,
         semination_employee=None)
        Semination.objects.create_semination(sow=sow, week=1, initiator=None,
         semination_employee=None)
        Ultrasound.objects.create_ultrasound(sow, None, True)
        location = Location.objects.filter(sowAndPigletsCell__number=1).first()
        sow.change_sow_current_location(location)

        SowFarrow.objects.create_sow_farrow(
            sow=sow,
            alive_quantity=10,
            dead_quantity=1
            )

        sow.markasnurse_set.create_nurse_event(sow)
        sow.refresh_from_db()
        self.assertEqual(sow.tour, None)
        self.assertEqual(sow.status.title, 'Кормилица')

    def test_create_nurse_event_error(self):
        sow = sows_testing.create_sow_and_put_in_workshop_one()
        Semination.objects.create_semination(sow=sow, week=1, initiator=None,
         semination_employee=None)
        Semination.objects.create_semination(sow=sow, week=1, initiator=None,
         semination_employee=None)
        Ultrasound.objects.create_ultrasound(sow, None, True)

        with self.assertRaises(ValidationError):
            sow.markasnurse_set.create_nurse_event(sow)


class MarkAsGiltTest(TestCase):
    def setUp(self):
        locations_testing.create_workshops_sections_and_cells()
        sows_testing.create_statuses()
        sows_events_testing.create_types()
        piglets_testing.create_piglets_statuses()

    def test_create_gilt(self):
        # 1 cell 1 section
        location = Location.objects.filter(sowAndPigletsCell__number=1).first()
        sow = sows_testing.create_sow_with_semination_usound(location, 1)
        farrow = SowFarrow.objects.create_sow_farrow(sow=sow, alive_quantity=10)
        piglets = farrow.piglets_group
        
        gilt = Gilt.objects.create_gilt(birth_id='1a', mother_sow_farm_id=sow.farm_id,
             piglets=piglets)

        MarkAsGilt.objects.create_init_gilt_event(gilt=gilt)

        marks_as_gilt_event = MarkAsGilt.objects.all().first()

        self.assertEqual(marks_as_gilt_event.gilt, gilt)
        self.assertEqual(marks_as_gilt_event.sow, gilt.mother_sow)
        self.assertEqual(marks_as_gilt_event.tour, gilt.tour)


class BoarEventTest(TestCase):
    def setUp(self):
        locations_testing.create_workshops_sections_and_cells()
        sows_testing.create_statuses()
        sows_testing.create_boars()
        sows_events_testing.create_types()
        self.boar1 = Boar.objects.all().first()

    def test_culling_boar(self):
        boar = Boar.objects.all().first()
        culling = CullingBoar.objects.create_culling_boar(boar=boar,
         culling_type='padej', reason='test reason', weight=100)

        self.assertEqual(culling.boar, boar)
        self.assertEqual(culling.culling_type, 'padej')
        self.assertEqual(culling.reason, 'test reason')

    def test_semen_boar(self):
        boar = Boar.objects.all().first()
        a = 100
        b = 1
        d = 50
        c = a * b / 1000
        e = c * d / 100
        f_denom = 2
        f = e / f_denom
        g = f * 90
        h = g - a
        final_motility_score = 70

        semen_boar = SemenBoar.objects.create_semen_boar(boar=boar,
          a=a, b=b, d=d, f_denom=f_denom,
          final_motility_score=final_motility_score)

        self.assertEqual(semen_boar.boar, boar)
        self.assertEqual(semen_boar.a, a)
        self.assertEqual(semen_boar.b, b)
        self.assertEqual(semen_boar.c, c)
        self.assertEqual(semen_boar.d, d)
        self.assertEqual(semen_boar.e, e)
        self.assertEqual(semen_boar.g, g)
        self.assertEqual(semen_boar.h, h)
        self.assertEqual(semen_boar.f, f)
        self.assertEqual(semen_boar.final_motility_score, final_motility_score)


class PigletsToSowsEventTest(TestCase):
    def setUp(self):
        locations_testing.create_workshops_sections_and_cells()
        sows_testing.create_statuses()
        sows_events_testing.create_types()

    def test_create_event(self):
        sow = Sow.objects.create_new_and_put_in_workshop_one(farm_id=123)

        tour = Tour.objects.get_or_create_by_week_in_current_year(week_number=10)
        location = Location.objects.filter(pigletsGroupCell__workshop__number=5).first()
        piglets = piglets_testing.create_new_group_with_metatour_by_one_tour(
            tour=tour, location=location, quantity=50)

        event = PigletsToSowsEvent.objects.create_event(piglets=piglets)

        self.assertEqual(event.piglets, piglets)
        self.assertEqual(event.metatour, piglets.metatour)
        self.assertEqual(event.sows.all().count(), 50)
        self.assertEqual(Sow.objects.all().count(), 51)

        sow1 = Sow.objects.all()[1]
        self.assertEqual(sow1.location.workshop.number, 2)
        self.assertEqual(sow1.status.title, 'Ремонтная')
        self.assertEqual(sow1.location.workshop.number, 2)
        self.assertEqual(sow1.sow_group.title, 'Ремонтная')

        self.assertEqual(SowStatusRecord.objects.all().count(), 50)
        self.assertEqual(SowGroupRecord.objects.all().count(), 50)
        piglets.refresh_from_db()
        self.assertEqual(piglets.active, False)

        self.assertEqual(SowTransaction.objects.filter(to_location__workshop__number=2).count(), 50)

        sows = Sow.objects.all().add_status_at_date(date=datetime.today())
        self.assertEqual(sows[1].status_at_date, 'Ремонтная')
        self.assertEqual(sows[1].location.workshop.number, 2)

    def test_delete_event_sows_transactions(self):
        tour = Tour.objects.get_or_create_by_week_in_current_year(week_number=10)
        location1 = Location.objects.filter(pigletsGroupCell__workshop__number=5).first()
        location2 = Location.objects.filter(pigletsGroupCell__workshop__number=5)[1]
        piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(
            tour=tour, location=location1, quantity=50)
        event1 = PigletsToSowsEvent.objects.create_event(piglets=piglets1)

        piglets2 = piglets_testing.create_new_group_with_metatour_by_one_tour(
            tour=tour, location=location2, quantity=15)
        event2 = PigletsToSowsEvent.objects.create_event(piglets=piglets2)

        event1.delete_event_sows_transactions()
        self.assertEqual(SowTransaction.objects.filter(to_location__workshop__number=2).count(), 15)
        self.assertEqual(Sow.objects.all().count(), 15)
        self.assertEqual(PigletsToSowsEvent.objects.all().count(), 1)
