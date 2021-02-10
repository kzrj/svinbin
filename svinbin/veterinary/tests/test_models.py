# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from django.test import TransactionTestCase
from django.db import models

import locations.testing_utils as locations_testing
import sows.testing_utils as sows_testing
import piglets.testing_utils as piglets_testing
import sows_events.utils as sows_events_testing

from veterinary.models import PigletsVetEvent
from tours.models import Tour
from locations.models import Location
from piglets_events.models import PigletsSplit, PigletsMerger
from piglets.models import Piglets


class PigletsVetEventModelTest(TransactionTestCase):
    def setUp(self):
        locations_testing.create_workshops_sections_and_cells()
        piglets_testing.create_piglets_statuses()

        self.tour1 = Tour.objects.get_or_create_by_week_in_current_year(week_number=1)
        self.tour2 = Tour.objects.get_or_create_by_week_in_current_year(week_number=2)
        self.loc_ws3 = Location.objects.get(workshop__number=3)

    def test_model_manager_create(self):
        piglets = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws3, 101)

        pve = PigletsVetEvent.objects.create_vet_event(piglets=piglets, recipe=None)
        self.assertEqual(pve.location, self.loc_ws3)
        self.assertEqual(pve.week_tour, self.tour1)
        self.assertEqual(pve.target_piglets, piglets)
        self.assertEqual(pve.piglets_quantity, 101)
        self.assertEqual(pve.piglets.all().count(), 1)
        self.assertEqual(pve.piglets.all().first(), piglets)

    def test_split_event(self):
        piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws3, 100)

        PigletsVetEvent.objects.create_vet_event(piglets=piglets1, recipe=None)
        PigletsVetEvent.objects.create_vet_event(piglets=piglets1, recipe=None)

        piglets2 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws3, 100)

        PigletsVetEvent.objects.create_vet_event(piglets=piglets2, recipe=None)

        child_piglets1, child_piglets2 = PigletsSplit.objects.split_return_groups(
            parent_piglets=piglets1, new_amount=40)

        self.assertEqual(piglets1.pigletsvetevent_set.all().count(), 2)
        self.assertEqual(child_piglets1.pigletsvetevent_set.all().count(), 2)
        self.assertEqual(child_piglets2.pigletsvetevent_set.all().count(), 2)

    def test_merge_event(self):
        # created piglets should get pves fron bigger group
        piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws3, 40)

        piglets2 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws3, 60)

        pve_p1_1 = PigletsVetEvent.objects.create_vet_event(piglets=piglets1, recipe=None)
        pve_p1_2 = PigletsVetEvent.objects.create_vet_event(piglets=piglets1, recipe=None)

        pve_p2_1 = PigletsVetEvent.objects.create_vet_event(piglets=piglets2, recipe=None)

        piglets_qs = Piglets.objects.all()
        piglets3 = PigletsMerger.objects.create_merger_return_group(parent_piglets=piglets_qs,
            new_location=self.loc_ws3)

        self.assertEqual(piglets3.pigletsvetevent_set.all().count(), 1)
        self.assertEqual(piglets3.pigletsvetevent_set.all().first(), pve_p2_1)