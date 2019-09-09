# -*- coding: utf-8 -*-
from django.test import TestCase

from sows_events.models import Semination, Ultrasound, SowFarrow, CullingSow, \
    UltrasoundType, WeaningSow, AbortionSow
from sows.models import Sow, Boar
from piglets.models import NewBornPigletsGroup
from locations.models import Location
from transactions.models import SowTransaction

import locations.testing_utils as locations_testing
import sows.testing_utils as sows_testing
import sows_events.utils as sows_events_testing


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
        self.assertEqual(sow.status.title, 'Супорос 30')

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
        self.assertEqual(seminated_sow2.status.title, 'Супорос 30')

        Ultrasound.objects.mass_ultrasound(sows_qs=sows_qs, initiator=None, result=False, days=60)

        seminated_sow3.refresh_from_db()
        self.assertEqual(seminated_sow3.status.title, 'Прохолост')
        self.assertEqual(seminated_sow3.tour, None)


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
        self.assertEqual(sow.status.title, 'Опоросилась')
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


class WeaningSowTest(TestCase):
    def setUp(self):
        locations_testing.create_workshops_sections_and_cells()
        sows_testing.create_statuses()

    def test_create_weaning(self):
        sow = sows_testing.create_sow_and_put_in_workshop_one()
        Semination.objects.create_semination(sow=sow, week=1, initiator=None,
         semination_employee=None)
        Semination.objects.create_semination(sow=sow, week=1, initiator=None,
         semination_employee=None)
        Ultrasound.objects.create_ultrasound(sow, None, True)
        SowFarrow.objects.create_sow_farrow(sow=sow, alive_quantity=7, mummy_quantity=1)
        self.assertEqual(sow.tour.week_number, 1)
        
        to_location = Location.objects.get(workshop__number=3)
        transaction1 = SowTransaction.objects.create_transaction(sow=sow, 
            to_location=to_location)
     
        weaning1 = WeaningSow.objects.all().first()
        self.assertNotEqual(weaning1, None)
        self.assertEqual(weaning1.transaction, transaction1)
        self.assertEqual(weaning1.sow, sow)

        sow.refresh_from_db()
        self.assertEqual(sow.tour, None)

        sow2 = sows_testing.create_sow_and_put_in_workshop_one()
        Semination.objects.create_semination(sow=sow2, week=1, initiator=None,
         semination_employee=None)
        Semination.objects.create_semination(sow=sow2, week=1, initiator=None,
         semination_employee=None)
        Ultrasound.objects.create_ultrasound(sow2, None, True)

        transaction2 = SowTransaction.objects.create_transaction(sow=sow, 
            to_location=to_location)

        weaning2 = WeaningSow.objects.filter(transaction=transaction2).first()
        self.assertEqual(weaning2, None)
        sow2.refresh_from_db()
        self.assertEqual(sow2.tour.week_number, 1)

    def test_create_weaning_many(self):
        sow = sows_testing.create_sow_and_put_in_workshop_one()
        Semination.objects.create_semination(sow=sow, week=1, initiator=None,
         semination_employee=None)
        Semination.objects.create_semination(sow=sow, week=1, initiator=None,
         semination_employee=None)
        Ultrasound.objects.create_ultrasound(sow, None, True)
        SowFarrow.objects.create_sow_farrow(sow=sow, alive_quantity=7, mummy_quantity=1)
 
        sow2 = sows_testing.create_sow_and_put_in_workshop_one()
        Semination.objects.create_semination(sow=sow2, week=1, initiator=None,
         semination_employee=None)
        Semination.objects.create_semination(sow=sow2, week=1, initiator=None,
         semination_employee=None)
        Ultrasound.objects.create_ultrasound(sow2, None, True)
        SowFarrow.objects.create_sow_farrow(sow=sow2, alive_quantity=7, mummy_quantity=1)

        to_location = Location.objects.get(workshop__number=3)
        transactions_ids = SowTransaction.objects.create_many_transactions(sows=[sow, sow2], 
            to_location=to_location)

        self.assertEqual(WeaningSow.objects.all().count(), 2)
        sow.refresh_from_db()
        sow2.refresh_from_db()
        self.assertEqual(sow.tour, None)
        self.assertEqual(sow2.tour, None)


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