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
# import staff.testing_utils as piglets_testing

from locations.models import Location
from sows.models import Sow, Gilt, Boar
from sows_events.models import SowFarrow, Ultrasound, Semination
from tours.models import Tour


class SowStatusesTest(TestCase):
    def setUp(self):
        locaions_testing.create_workshops_sections_and_cells()
        sows_testings.create_statuses()
        sows_testings.create_boars()
        self.boar = Boar.objects.all().first()
        sows_events_testings.create_types()

    def test_seminated_statuses(self):
        sow = sows_testings.create_sow_and_put_in_workshop_one()
        
        # 1 semination
        Semination.objects.create_semination(sow=sow, week=1, initiator=None,
         semination_employee=None)
        self.assertEqual(sow.does_once_seminate_in_tour, True)
        self.assertEqual(sow.status.title, 'Осеменена 1')

        # 2 seminations
        Semination.objects.create_semination(sow=sow, week=1, initiator=None,
         semination_employee=None)
        sow.refresh_from_db()
        self.assertEqual(sow.does_once_seminate_in_tour, False)
        self.assertEqual(sow.status.title, 'Осеменена 2')

        Ultrasound.objects.create_ultrasound(sow=sow, result=False, days=30)
        sow.refresh_from_db()
        self.assertEqual(sow.tour, None)
        self.assertNotEqual(sow.status.title, 'Осеменена 2')
        self.assertNotEqual(sow.status.title, 'Осеменена 1')

        # not seminated
        sow.refresh_from_db()
        self.assertEqual(sow.does_once_seminate_in_tour, False)

        # 1 semination in another tour
        Semination.objects.create_semination(sow=sow, week=2, initiator=None,
         semination_employee=None)
        self.assertEqual(sow.does_once_seminate_in_tour, True)
        self.assertEqual(sow.status.title, 'Осеменена 1')

        # 2 semination in anopther tour
        Semination.objects.create_semination(sow=sow, week=2, initiator=None,
         semination_employee=None)
        self.assertEqual(sow.does_once_seminate_in_tour, False)
        self.assertEqual(sow.status.title, 'Осеменена 2')

    def test_mass_seminated_statuses(self):
        sow1 = sows_testings.create_sow_and_put_in_workshop_one()
        sow2 = sows_testings.create_sow_and_put_in_workshop_one()
        sow3 = sows_testings.create_sow_and_put_in_workshop_one()
        
        # 1 semination
        sows_qs = Sow.objects.filter(pk__in=[sow1.pk, sow2.pk, sow3.pk])
        Semination.objects.mass_semination(sows_qs=sows_qs, week=1, initiator=None,
         semination_employee=None)
        sow1.refresh_from_db()
        self.assertEqual(sow1.status.title, 'Осеменена 1')
        sow2.refresh_from_db()
        self.assertEqual(sow2.status.title, 'Осеменена 1')
        sow3.refresh_from_db()
        self.assertEqual(sow3.status.title, 'Осеменена 1')

        # 2 semination
        sows_qs = Sow.objects.filter(pk__in=[sow1.pk, sow2.pk, sow3.pk])
        Semination.objects.mass_semination(sows_qs=sows_qs, week=1, initiator=None,
         semination_employee=None)
        sow1.refresh_from_db()
        self.assertEqual(sow1.status.title, 'Осеменена 2')
        sow2.refresh_from_db()
        self.assertEqual(sow2.status.title, 'Осеменена 2')
        sow3.refresh_from_db()
        self.assertEqual(sow3.status.title, 'Осеменена 2')

        sows_qs.update(tour=None)
        # 1 semination 2 week
        sows_qs = Sow.objects.filter(pk__in=[sow1.pk, sow2.pk, sow3.pk])
        Semination.objects.mass_semination(sows_qs=sows_qs, week=2, initiator=None,
         semination_employee=None)
        sow1.refresh_from_db()
        self.assertEqual(sow1.status.title, 'Осеменена 1')
        sow2.refresh_from_db()
        self.assertEqual(sow2.status.title, 'Осеменена 1')
        sow3.refresh_from_db()
        self.assertEqual(sow3.status.title, 'Осеменена 1')

        # 2 semination 2 week
        sows_qs = Sow.objects.filter(pk__in=[sow1.pk, sow2.pk, sow3.pk])
        Semination.objects.mass_semination(sows_qs=sows_qs, week=2, initiator=None,
         semination_employee=None)
        sow1.refresh_from_db()
        self.assertEqual(sow1.status.title, 'Осеменена 2')
        sow2.refresh_from_db()
        self.assertEqual(sow2.status.title, 'Осеменена 2')
        sow3.refresh_from_db()
        self.assertEqual(sow3.status.title, 'Осеменена 2')
