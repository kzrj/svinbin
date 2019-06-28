# -*- coding: utf-8 -*-
from django.test import TestCase

import gilts_events.models as gilts_events_models
import sows.models as sows_models
import locations.models as locations_models

import locations.testing_utils as locations_testing
import sows.testing_utils as sows_testing
import piglets.testing_utils as piglets_testing


class GiltMergerManagerTest(TestCase):
    def setUp(self):
        locations_testing.create_workshops_sections_and_cells()
        sows_testing.create_statuses()

    def test__get_gilts_from_group_update_group(self):
        new_born_group1 = piglets_testing.create_new_born_group(cell_number=5)
        sow1 = new_born_group1.farrows.first().sow
        gilt1 = sows_models.Gilt.objects.create_gilt(1, sow1)
        new_born_group1.refresh_from_db()
        
        new_born_group2 = piglets_testing.create_new_born_group(cell_number=6)
        sow2 = new_born_group2.farrows.first().sow
        gilt2 = sows_models.Gilt.objects.create_gilt(2, sow2)
        gilt3 = sows_models.Gilt.objects.create_gilt(3, sow2)
        new_born_group2.refresh_from_db()
        self.assertEqual(new_born_group2.gilts.all().count(), 2)
        self.assertEqual(new_born_group2.gilts_quantity, 2)

        new_born_group3 = piglets_testing.create_new_born_group(cell_number=4)

        gilts_list = [gilt1, gilt2, gilt3]
        groups = [new_born_group1, new_born_group2, new_born_group3]

        gilts_events_models.GiltMerger.objects._get_gilts_from_group_update_group(groups)
        
        new_born_group1.refresh_from_db()
        self.assertEqual(new_born_group1.gilts_quantity, 0)
        self.assertEqual(new_born_group1.quantity, 9)

        new_born_group2.refresh_from_db()
        self.assertEqual(new_born_group2.gilts_quantity, 0)
        self.assertEqual(new_born_group2.quantity, 8)

    def test_create_merger_and_return_nomad_group(self):
        # include create_gilt_merger and model.create_gilt_merger
        new_born_group1 = piglets_testing.create_new_born_group(cell_number=5)
        sow1 = new_born_group1.farrows.first().sow
        gilt1 = sows_models.Gilt.objects.create_gilt(1, sow1)
        
        new_born_group2 = piglets_testing.create_new_born_group(cell_number=6)
        sow2 = new_born_group2.farrows.first().sow
        gilt2 = sows_models.Gilt.objects.create_gilt(2, sow2)
        gilt3 = sows_models.Gilt.objects.create_gilt(3, sow2)

        merger = gilts_events_models.GiltMerger.objects.create_gilt_merger([gilt1, gilt2, gilt3])
        self.assertEqual(merger.gilts.all().count(), 3)
        gilt1.refresh_from_db()
        self.assertEqual(gilt1.merger, merger)

        nomad_group = merger.create_nomad_group()
        self.assertEqual(nomad_group.start_quantity, 3)
        self.assertEqual(nomad_group.quantity, 3)
        self.assertEqual(nomad_group.gilts_quantity, 3)
        self.assertEqual(nomad_group.creating_gilt_merger, merger)
        self.assertEqual(nomad_group.location.get_location,
            locations_models.WorkShop.objects.get(number=3))


class CastingListToSevenFiveEventManagerTest(TestCase):
    def setUp(self):
        workshop_testing.create_workshops_sections_and_cells()
        sows_testing.create_statuses()

    def test_create_casting_list(self):
        new_born_group1 = piglets_testing.create_new_born_group(cell_number=5)
        sow1 = new_born_group1.farrows.first().sow
        gilt1 = sows_models.Gilt.objects.create_gilt(1, sow1)

        new_born_group2 = piglets_testing.create_new_born_group(cell_number=6)
        sow2 = new_born_group2.farrows.first().sow
        gilt2 = sows_models.Gilt.objects.create_gilt(2, sow2)
        gilt3 = sows_models.Gilt.objects.create_gilt(3, sow2)
        merger1 = gilts_events_models.GiltMerger.objects.create_gilt_merger([gilt1, gilt2, gilt3])
        nomad_group1 = merger1.create_nomad_group()

        new_born_group3 = piglets_testing.create_new_born_group(cell_number=1)
        sow3 = new_born_group3.farrows.first().sow
        gilt4 = sows_models.Gilt.objects.create_gilt(4, sow3)
        
        new_born_group4 = piglets_testing.create_new_born_group(cell_number=2)
        sow4 = new_born_group4.farrows.first().sow
        gilt5 = sows_models.Gilt.objects.create_gilt(5, sow4)
        gilt6 = sows_models.Gilt.objects.create_gilt(6, sow4)
        merger2 = gilts_events_models.GiltMerger.objects.create_gilt_merger([gilt4, gilt5, gilt6])
        nomad_group2 = merger1.create_nomad_group()

        self.assertEqual(nomad_group1.quantity, 3)
        self.assertEqual(nomad_group2.quantity, 3)

        input_data = [
            {'nomad_group': nomad_group1, 'gilts': [gilt1, gilt2]},
            {'nomad_group': nomad_group2, 'gilts': [gilt6]},
        ]
        
        casting_event = gilts_events_models.CastingListToSevenFiveEvent.objects.create_casting_list(
            input_data)

        nomad_group1.refresh_from_db()
        nomad_group2.refresh_from_db()
        self.assertEqual(nomad_group1.quantity, 1)
        self.assertEqual(nomad_group2.quantity, 2)
        self.assertEqual(nomad_group1.gilts_quantity, 1)
        self.assertEqual(nomad_group2.gilts_quantity, 2)

        self.assertEqual(list(casting_event.gilts.all().values_list('id', flat=True)),
            [gilt1.pk, gilt2.pk, gilt6.pk])
