# -*- coding: utf-8 -*-
from django.utils import timezone
from django.test import TestCase
from django.core.exceptions import ValidationError

from sows_events.models import (
    Semination, Ultrasound, SowFarrow, CullingSow,
    UltrasoundType, AbortionSow)
from sows.models import Sow, Boar
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
        sow = Sow.objects.create_new_from_gilt_and_put_in_workshop_one(1)
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

        sows_qs = Sow.objects.filter(pk__in=[sow1.pk, sow2.pk, sow3.pk])
        Semination.objects.mass_semination(sows_qs=sows_qs, week=1,
         initiator=None, semination_employee=None, boar=self.boar)
        
        self.assertEqual(Semination.objects.all().count(), 3)

        sow1.refresh_from_db()
        self.assertEqual(sow1.status.title, 'Осеменена 1')
        self.assertEqual(sow1.tour.week_number, 1)

    def test_is_there_semination(self):
        sow = Sow.objects.create_new_from_gilt_and_put_in_workshop_one(1)
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
        sow = Sow.objects.create_new_from_gilt_and_put_in_workshop_one(1)

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


class SowFarrowModelManagerTest(TestCase):
    def setUp(self):
        locations_testing.create_workshops_sections_and_cells()
        sows_testing.create_statuses()
        sows_events_testing.create_types()
        piglets_testing.create_piglets_statuses()

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
        culling = CullingSow.objects.create_culling(sow, 'spec', 'prichina')
        sow.refresh_from_db()
        self.assertEqual(sow.alive, False)
        self.assertEqual(culling.sow, sow)
        self.assertEqual(culling.culling_type, 'spec')
        self.assertEqual(culling.reason, 'prichina')


# class WeaningSowTest(TestCase):
#     def setUp(self):
#         locations_testing.create_workshops_sections_and_cells()
#         sows_testing.create_statuses()
#         sows_events_testing.create_types()
#         piglets_testing.create_piglets_statuses()

#     def test_create_weaning(self):
#         location = Location.objects.filter(sowAndPigletsCell__number=1).first()
#         sow1 = sows_testing.create_sow_with_semination_usound(location=location, week=1)

#         # first sow farrow in tour in section
#         farrow = SowFarrow.objects.create_sow_farrow(
#             sow=sow1,
#             alive_quantity=10,
#             dead_quantity=1
#             )

#         piglets = farrow.piglets_group

#         weaning1 = sow1.weaningsow_set.create_weaning(sow=sow1, piglets=piglets)
        
#         self.assertEqual(weaning1.piglets, piglets)
#         self.assertEqual(weaning1.sow, sow1)
#         self.assertEqual(weaning1.quantity, piglets.quantity)

#         sow1.refresh_from_db()
#         self.assertEqual(sow1.tour, None)


class AbortionSowTest(TestCase):
    def setUp(self):
        locations_testing.create_workshops_sections_and_cells()
        sows_testing.create_statuses()

    def test_create_abortion(self):
        sow = sows_testing.create_sow_and_put_in_workshop_one()
        Semination.objects.create_semination(sow=sow, week=1, initiator=None,
         semination_employee=None)
        Semination.objects.create_semination(sow=sow, week=1, initiator=None,
         semination_employee=None)
        Ultrasound.objects.create_ultrasound(sow, None, True)

        AbortionSow.objects.create_abortion(sow, None)
        sow.refresh_from_db()
        self.assertEqual(sow.tour, None)
        self.assertEqual(sow.status.title, 'Аборт')