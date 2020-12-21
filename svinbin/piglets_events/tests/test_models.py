# -*- coding: utf-8 -*-
import datetime
from django.test import TestCase, TransactionTestCase
from django.core.exceptions import ValidationError
from django.db import models

from piglets.models import Piglets
from piglets_events.models import (
    PigletsMerger, PigletsSplit, WeighingPiglets,
    CullingPiglets, Recount
)
from tours.models import Tour, MetaTour
from locations.models import Location

import locations.testing_utils as locations_testing
import piglets.testing_utils as piglets_testing
import sows.testing_utils as sows_testing
import sows_events.utils as sows_events_testing


class PigletsMergerModelTest(TransactionTestCase):
    def setUp(self):
        locations_testing.create_workshops_sections_and_cells()
        sows_testing.create_statuses()
        sows_events_testing.create_types()
        piglets_testing.create_piglets_statuses()       

        self.tour1 = Tour.objects.get_or_create_by_week_in_current_year(week_number=1)
        self.tour2 = Tour.objects.get_or_create_by_week_in_current_year(week_number=2)
        self.tour3 = Tour.objects.get_or_create_by_week_in_current_year(week_number=3)
        self.tour4 = Tour.objects.get_or_create_by_week_in_current_year(week_number=4)
        self.loc_ws3 = Location.objects.get(workshop__number=3)
        self.loc_ws3_sec1 = Location.objects.get(section__workshop__number=3, section__number=1)
        self.loc_ws3_sec2 = Location.objects.get(section__workshop__number=3, section__number=2)
        self.loc_ws3_sec1_cell1 = Location.objects.get(sowAndPigletsCell__number=1, 
             sowAndPigletsCell__section__number=1)
        self.loc_ws3_sec1_cell2 = Location.objects.get(sowAndPigletsCell__number=2, 
             sowAndPigletsCell__section__number=1)
        self.loc_ws3_sec1_cell3 = Location.objects.get(sowAndPigletsCell__number=3, 
             sowAndPigletsCell__section__number=1)

    def test_create_merger_return_group_v1(self):
        piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws3, 10)
        piglets2 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour2,
            self.loc_ws3, 10)
        piglets3 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour2,
            self.loc_ws3, 10)

        # piglets_qs = Piglets.objects.all() !!!!!!!!!!!!!!!!!!!!!!!!! WRONG DANGER
        piglets_qs = [piglets1, piglets2, piglets3]

        piglets = PigletsMerger.objects.create_merger_return_group(parent_piglets=piglets_qs,
            new_location=self.loc_ws3)

        mtTourRecords = piglets.metatour.records.all()

        self.assertEqual(mtTourRecords.count(), 2)

        self.assertEqual(mtTourRecords[0].tour, self.tour1)
        self.assertEqual(mtTourRecords[0].quantity, 10)
        self.assertEqual(round(mtTourRecords[0].percentage), 33)
       
        self.assertEqual(mtTourRecords[1].tour, self.tour2)
        self.assertEqual(mtTourRecords[1].quantity, 20)
        self.assertEqual(round(mtTourRecords[1].percentage), 67)

        piglets.refresh_from_db()
        self.assertEqual(piglets.active, True)
        self.assertEqual(Piglets.objects.all().count(), 1)

        piglets1.refresh_from_db()
        self.assertEqual(piglets1.active, False)

        piglets2.refresh_from_db()
        self.assertEqual(piglets2.active, False)

        piglets3.refresh_from_db()
        self.assertEqual(piglets3.active, False)

    def test_create_merger_return_group_v2(self):
        piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws3, 10)
        piglets2 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour2,
            self.loc_ws3, 10)
        piglets3 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour2,
            self.loc_ws3, 10)
        piglets_qs1 = Piglets.objects.filter(pk__in=[piglets1.pk, piglets2.pk, piglets3.pk])
        child_piglets1 = PigletsMerger.objects.create_merger_return_group(parent_piglets=piglets_qs1,
            new_location=self.loc_ws3)

        piglets4 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour3,
            self.loc_ws3, 10)
        piglets5 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour4,
            self.loc_ws3, 10)
        piglets_qs2 = Piglets.objects.filter(pk__in=[piglets4.pk, piglets5.pk])
        child_piglets2 = PigletsMerger.objects.create_merger_return_group(parent_piglets=piglets_qs2,
            new_location=self.loc_ws3)

        piglets_qs3 = Piglets.objects.filter(pk__in=[child_piglets1.pk, child_piglets2.pk])
        child_piglets3 = PigletsMerger.objects.create_merger_return_group(parent_piglets=piglets_qs3,
            new_location=self.loc_ws3)

        mtTourRecords = child_piglets3.metatour.records.all()

        self.assertEqual(mtTourRecords.count(), 4)

        self.assertEqual(mtTourRecords[0].tour, self.tour1)
        self.assertEqual(mtTourRecords[0].quantity, 10)
        self.assertEqual(round(mtTourRecords[0].percentage), 20)
       
        self.assertEqual(mtTourRecords[1].tour, self.tour2)
        self.assertEqual(mtTourRecords[1].quantity, 20)
        self.assertEqual(round(mtTourRecords[1].percentage), 40)

        self.assertEqual(mtTourRecords[2].tour, self.tour3)
        self.assertEqual(mtTourRecords[2].quantity, 10)
        self.assertEqual(round(mtTourRecords[2].percentage), 20)
       
        self.assertEqual(mtTourRecords[3].tour, self.tour4)
        self.assertEqual(mtTourRecords[3].quantity, 10)
        self.assertEqual(round(mtTourRecords[3].percentage), 20)

        piglets1.refresh_from_db()
        self.assertEqual(piglets1.active, False)

    def test_create_from_merging_list_v1(self):
        # without change quantity
        piglets1 = piglets_testing.create_from_sow_farrow(self.tour1, self.loc_ws3_sec1_cell1, 10)
        piglets2 = piglets_testing.create_from_sow_farrow(self.tour2, self.loc_ws3_sec1_cell2, 10)
        piglets3 = piglets_testing.create_from_sow_farrow(self.tour3, self.loc_ws3_sec1_cell3, 10)

        merging_list = [
            {'piglets_id': piglets1.pk, 'quantity': 10, 'changed': False, 'gilts_contains': False},
            {'piglets_id': piglets2.pk, 'quantity': 10, 'changed': False, 'gilts_contains': False}
        ]

        nomad_piglets = PigletsMerger.objects.create_from_merging_list(merging_list, self.loc_ws3)
        
        self.assertEqual(nomad_piglets.location, self.loc_ws3)
        self.assertEqual(nomad_piglets.quantity, 20)
        piglets1.refresh_from_db()
        piglets2.refresh_from_db()
        self.assertEqual(nomad_piglets.merger_as_child, piglets1.merger_as_parent)
        self.assertEqual(nomad_piglets.merger_as_child, piglets2.merger_as_parent)

        self.assertEqual(Piglets.objects.get_all(). \
            filter(merger_as_parent=nomad_piglets.merger_as_child).count(), 2)

    def test_create_from_merging_list_v2(self):
        # with change quantity
        piglets1 = piglets_testing.create_from_sow_farrow(self.tour1,
         self.loc_ws3_sec1_cell1, 10)
        piglets2 = piglets_testing.create_from_sow_farrow(self.tour2,
         self.loc_ws3_sec1_cell2, 10)
        piglets3 = piglets_testing.create_from_sow_farrow(self.tour3,
         self.loc_ws3_sec1_cell3, 10)

        merging_list = [
            {'piglets_id': piglets1.pk, 'quantity': 7, 'changed': True,
             'gilts_contains': False},
            {'piglets_id': piglets2.pk, 'quantity': 10, 'changed': False,
             'gilts_contains': False}
        ]

        nomad_piglets = PigletsMerger.objects.create_from_merging_list(merging_list,
         self.loc_ws3)
        self.assertEqual(nomad_piglets.location, self.loc_ws3)
        self.assertEqual(nomad_piglets.quantity, 17)
        self.assertEqual(nomad_piglets.active, True)
        piglets1.refresh_from_db()
        piglets2.refresh_from_db()

        # should be 5 piglets
        self.assertEqual(Piglets.objects.get_all().count(), 6)

        #  should be 2 childs from split
        split_record = piglets1.split_as_parent
        self.assertEqual(split_record.parent_piglets, piglets1)
        self.assertEqual(split_record.parent_piglets.active, False)

        # children from split
        self.assertEqual(Piglets.objects.get_all(). \
            filter(split_as_child=split_record, active=True).count(), 1)

        self.assertEqual(Piglets.objects.get_all(). \
            filter(split_as_child=split_record, active=True).first().quantity, 3)

        self.assertEqual(Piglets.objects.get_all(). \
            filter(split_as_child=split_record, active=True).first().active, True)

        self.assertEqual(Piglets.objects.get_all(). \
            filter(split_as_child=split_record, active=False).first().quantity, 7)

        self.assertEqual(Piglets.objects.get_all(). \
            filter(split_as_child=split_record, active=False).first().active, False)

        self.assertEqual(piglets1.active, False)
        self.assertEqual(piglets2.active, False)

    def test_create_from_merging_list_sow_weaning(self):
        # with change quantity
        piglets1 = piglets_testing.create_from_sow_farrow(self.tour1, self.loc_ws3_sec1_cell1, 10)
        piglets2 = piglets_testing.create_from_sow_farrow(self.tour2, self.loc_ws3_sec1_cell2, 10)
        piglets3 = piglets_testing.create_from_sow_farrow(self.tour3, self.loc_ws3_sec1_cell3, 10)

        merging_list = [
            {'piglets_id': piglets1.pk, 'quantity': 7, 'changed': True, 'gilts_contains': False},
            {'piglets_id': piglets2.pk, 'quantity': 10, 'changed': False, 'gilts_contains': False}
        ]

        nomad_piglets = PigletsMerger.objects.create_from_merging_list(merging_list, self.loc_ws3)

        sow1 = piglets1.farrow.sow
        sow2 = piglets2.farrow.sow
        sow1.refresh_from_db()
        sow2.refresh_from_db()

        # self.assertEqual(sow1.tour, None)
        # self.assertEqual(sow2.tour, None)
        self.assertEqual(sow1.status.title, 'Отъем')
        self.assertEqual(sow2.status.title, 'Отъем')

        self.assertEqual(sow1.weaningsow_set.all().count(), 1)
        self.assertEqual(sow2.weaningsow_set.all().count(), 1)

        self.assertEqual(sow1.weaningsow_set.all().first().quantity, 7)
        self.assertEqual(sow2.weaningsow_set.all().first().quantity, 10)

    def test_create_from_merging_list_sow_weaning_v2(self):
        # with change quantity
        piglets1 = piglets_testing.create_from_sow_farrow(self.tour1, self.loc_ws3_sec1_cell1, 10)
        piglets2 = piglets_testing.create_from_sow_farrow(self.tour2, self.loc_ws3_sec1_cell2, 10)
        sow2 = piglets2.farrow.sow
        sow2.mark_as_nurse

        merging_list = [
            {'piglets_id': piglets1.pk, 'quantity': 7, 'changed': True, 'gilts_contains': False},
            {'piglets_id': piglets2.pk, 'quantity': 10, 'changed': False, 'gilts_contains': False}
        ]

        nomad_piglets = PigletsMerger.objects.create_from_merging_list(merging_list, self.loc_ws3)

        sow1 = piglets1.farrow.sow
        sow1.refresh_from_db()
        sow2.refresh_from_db()

        # self.assertEqual(sow1.tour, None)
        # self.assertEqual(sow2.tour, None)
        self.assertEqual(sow1.status.title, 'Отъем')
        self.assertEqual(sow2.status.title, 'Отъем')

        self.assertEqual(sow1.weaningsow_set.all().count(), 1)
        self.assertEqual(sow2.weaningsow_set.all().count(), 1)

    def test_create_from_merging_list_v3(self):
        # with gilts
        piglets1 = piglets_testing.create_from_sow_farrow(self.tour1,
         self.loc_ws3_sec1_cell1, 10)
        piglets2 = piglets_testing.create_from_sow_farrow(self.tour2,
         self.loc_ws3_sec1_cell2, 10)

        piglets1.add_gilts_without_increase_quantity(3)
        piglets2.add_gilts_without_increase_quantity(2)

        merging_list = [
            {'piglets_id': piglets1.pk, 'quantity': 7, 'changed': True,
             'gilts_contains': True},
            {'piglets_id': piglets2.pk, 'quantity': 10, 'changed': False,
             'gilts_contains': False}
        ]

        nomad_piglets = PigletsMerger.objects.create_from_merging_list(merging_list,
         self.loc_ws3)
        self.assertEqual(nomad_piglets.location, self.loc_ws3)
        self.assertEqual(nomad_piglets.quantity, 17)
        self.assertEqual(nomad_piglets.gilts_quantity, 5)

    def test_create_from_merging_list_v4(self):
        # without gilts
        piglets1 = piglets_testing.create_from_sow_farrow(self.tour1,
         self.loc_ws3_sec1_cell1, 10)
        piglets2 = piglets_testing.create_from_sow_farrow(self.tour2,
         self.loc_ws3_sec1_cell2, 10)
        
        piglets1.add_gilts_without_increase_quantity(3)
        piglets2.add_gilts_without_increase_quantity(2)

        merging_list = [
            {'piglets_id': piglets1.pk, 'quantity': 7, 'changed': True,
             'gilts_contains': False},
            {'piglets_id': piglets2.pk, 'quantity': 10, 'changed': False,
             'gilts_contains': False}
        ]

        nomad_piglets = PigletsMerger.objects.create_from_merging_list(merging_list,
         self.loc_ws3)
        self.assertEqual(nomad_piglets.location, self.loc_ws3)
        self.assertEqual(nomad_piglets.quantity, 17)
        self.assertEqual(nomad_piglets.gilts_quantity, 2)

    def test_create_from_merging_list_v5_validate(self):
        # without gilts
        piglets1 = piglets_testing.create_from_sow_farrow(self.tour1,
         self.loc_ws3_sec1_cell1, 10)
        piglets2 = piglets_testing.create_from_sow_farrow(self.tour2,
         self.loc_ws3_sec1_cell2, 10)
        
        piglets1.add_gilts_without_increase_quantity(3)
        piglets2.add_gilts_without_increase_quantity(2)

        merging_list = [
            {'piglets_id': piglets1.pk, 'quantity': 8, 'changed': True,
             'gilts_contains': False},
            {'piglets_id': piglets2.pk, 'quantity': 10, 'changed': False,
             'gilts_contains': False}
        ]

        with self.assertRaises(ValidationError):
            nomad_piglets = PigletsMerger.objects.create_from_merging_list(merging_list,
             self.loc_ws3)
       
    def test_merge_piglets_in_location(self):
        piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws3_sec1_cell1, 10)
        piglets1.add_gilts_without_increase_quantity(3)
        piglets2 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour2,
            self.loc_ws3_sec1_cell1, 10)
        piglets2.add_gilts_without_increase_quantity(2)

        merged_piglets = PigletsMerger.objects.merge_piglets_in_location(
            self.loc_ws3_sec1_cell1)
        self.assertEqual(merged_piglets.quantity, 20)
        self.assertEqual(merged_piglets.gilts_quantity, 5)

        piglets1.refresh_from_db()
        piglets2.refresh_from_db()
        self.assertEqual(piglets1.active, False)

    def test_create_from_merging_list_v5_with_gilts_quantity(self):
        # without gilts
        piglets1 = piglets_testing.create_from_sow_farrow(self.tour1,
         self.loc_ws3_sec1_cell1, 10)
        piglets2 = piglets_testing.create_from_sow_farrow(self.tour2,
         self.loc_ws3_sec1_cell2, 10)
        
        piglets1.add_gilts_without_increase_quantity(3)
        piglets2.add_gilts_without_increase_quantity(2)

        merging_list = [
            {'piglets_id': piglets1.pk, 'quantity': 7, 'changed': True,
             'gilts_contains': False, 'gilts_quantity': 7},
            {'piglets_id': piglets2.pk, 'quantity': 10, 'changed': False,
             'gilts_contains': True, 'gilts_quantity': 5}
        ]

        nomad_piglets = PigletsMerger.objects.create_from_merging_list(merging_list,
         self.loc_ws3)

        self.assertEqual(nomad_piglets.location, self.loc_ws3)
        self.assertEqual(nomad_piglets.quantity, 17)
        self.assertEqual(nomad_piglets.gilts_quantity, 12)


class PigletsSplitModelTest(TestCase):
    def setUp(self):
        locations_testing.create_workshops_sections_and_cells()
        # sows_testing.create_statuses()
        piglets_testing.create_piglets_statuses()       

        self.tour1 = Tour.objects.get_or_create_by_week_in_current_year(week_number=1)
        self.tour2 = Tour.objects.get_or_create_by_week_in_current_year(week_number=2)
        self.tour3 = Tour.objects.get_or_create_by_week_in_current_year(week_number=3)
        self.tour4 = Tour.objects.get_or_create_by_week_in_current_year(week_number=4)
        self.loc_ws3 = Location.objects.get(workshop__number=3)

    def test_split(self):
        piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws3, 100)
        piglets2 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour2,
            self.loc_ws3, 100)
        piglets3 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour2,
            self.loc_ws3, 100)
        piglets_qs = Piglets.objects.all()
        piglets = PigletsMerger.objects.create_merger_return_group(parent_piglets=piglets_qs,
            new_location=self.loc_ws3)

        child_piglets1, child_piglets2 = PigletsSplit.objects.split_return_groups(
            parent_piglets=piglets, new_amount=100)

        self.assertEqual(child_piglets1.split_as_child.parent_piglets, piglets)
        self.assertEqual(piglets.active, False)

        self.assertEqual(child_piglets1.quantity, 200)
        self.assertEqual(child_piglets2.quantity, 100)
        
        # child_pidlets1 records        
        self.assertEqual(child_piglets1.metatour.records.all().count(), 2)
        self.assertEqual(child_piglets1.metatour.records.all()[0].tour, self.tour1)
        self.assertEqual(round(child_piglets1.metatour.records.all()[0].quantity, 2),
             66.67)
        self.assertEqual(round(child_piglets1.metatour.records.all()[0].percentage, 2),
             33.33)

        self.assertEqual(child_piglets1.metatour.records.all()[1].tour, self.tour2)
        self.assertEqual(round(child_piglets1.metatour.records.all()[1].quantity, 2),
             133.33)
        self.assertEqual(round(child_piglets1.metatour.records.all()[1].percentage, 2),
             66.67)

        # child_pidlets2 records
        self.assertEqual(child_piglets2.metatour.records.all().count(), 2)
        self.assertEqual(child_piglets2.metatour.records.all()[0].tour, self.tour1)
        self.assertEqual(round(child_piglets2.metatour.records.all()[0].quantity, 2),
             33.33)
        self.assertEqual(round(child_piglets2.metatour.records.all()[0].percentage ,2), 33.33)

        self.assertEqual(child_piglets2.metatour.records.all()[1].tour, self.tour2)
        self.assertEqual(round(child_piglets2.metatour.records.all()[1].quantity, 2), 66.67)
        self.assertEqual(round(child_piglets2.metatour.records.all()[1].percentage, 2), 66.67)

        # test piglets manager
        split_record = piglets.split_as_parent
        self.assertEqual(split_record.piglets_as_child.all().count(), 2)
        self.assertEqual(Piglets.objects.get_all(). \
            filter(split_as_child=split_record, active=False).count(), 0)

        self.assertEqual(Piglets.objects.get_all(). \
            filter(split_as_child=split_record).count(), 2)

    def test_split_with_gilts(self):
        piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws3, 100)
        piglets1.add_gilts_without_increase_quantity(10)

        self.assertEqual(piglets1.gilts_quantity, 10)
        self.assertEqual(piglets1.quantity, 100)

        child_piglets1, child_piglets2 = PigletsSplit.objects.split_return_groups(
            parent_piglets=piglets1, new_amount=50, gilts_to_new=True)

        self.assertEqual(child_piglets1.gilts_quantity, 0)
        self.assertEqual(child_piglets1.quantity, 50)

        self.assertEqual(child_piglets2.gilts_quantity, 10)
        self.assertEqual(child_piglets2.quantity, 50)
       
    def test_split_validate(self):
        piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws3, 100)
        piglets_qs = Piglets.objects.all()
        piglets = PigletsMerger.objects.create_merger_return_group(parent_piglets=piglets_qs,
            new_location=self.loc_ws3)

        with self.assertRaises(ValidationError):
            child_piglets1, child_piglets2 = PigletsSplit.objects.split_return_groups(
                parent_piglets=piglets, new_amount=100)

    def test_split_with_gilts_validate(self):
        piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws3, 100)
        piglets1.add_gilts_without_increase_quantity(10)

        with self.assertRaises(ValidationError):
            child_piglets1, child_piglets2 = PigletsSplit.objects.split_return_groups(
                parent_piglets=piglets1, new_amount=9, gilts_to_new=True)


    def test_split_with_gilts_validate2(self):
        piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws3, 100)
        piglets1.add_gilts_without_increase_quantity(10)

        with self.assertRaises(ValidationError):
            child_piglets1, child_piglets2 = PigletsSplit.objects.split_return_groups(
                parent_piglets=piglets1, new_amount=91, gilts_to_new=False)


class WeighingPigletsTest(TestCase):
    def setUp(self):
        locations_testing.create_workshops_sections_and_cells()
        piglets_testing.create_piglets_statuses()
        self.loc_ws3 = Location.objects.get(workshop__number=3)

        self.tour1 = Tour.objects.get_or_create_by_week_in_current_year(week_number=1)
        self.tour2 = Tour.objects.get_or_create_by_week_in_current_year(week_number=2)

        self.loc_ws4 = Location.objects.get(workshop__number=4)
        # piglets in ws
        piglets4 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws4, 100)
        piglets5 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour2,
            self.loc_ws4, 100)

        #  piglets in pigletsCell in ws
        self.loc_cell_ws4_1 = Location.objects.filter(pigletsGroupCell__workshop__number=4)[0]
        piglets6 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour2,
            self.loc_cell_ws4_1, 100)
        self.loc_cell_ws4_2 = Location.objects.filter(pigletsGroupCell__workshop__number=4)[1]
        piglets7 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour2,
            self.loc_cell_ws4_2, 100)

        self.loc_cell_ws4_3 = Location.objects.filter(pigletsGroupCell__workshop__number=4)[2]
        piglets8 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour2,
            self.loc_cell_ws4_3, 100)
        piglets8.deactivate()
        self.loc_cell_ws4_4 = Location.objects.filter(pigletsGroupCell__workshop__number=4)[3]
        piglets9 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour2,
            self.loc_cell_ws4_4, 100)
        piglets9.deactivate()

        # piglets in section
        self.loc_section_ws4_1 = Location.objects.filter(section__workshop__number=4)[0]
        piglets10 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour2,
            self.loc_section_ws4_1, 100)


        self.loc_ws5 = Location.objects.get(workshop__number=5)
        self.loc_ws5_cells = Location.objects.filter(pigletsGroupCell__workshop__number=5)
        # piglets in ws
        self.piglets11 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws5, 100)
        self.piglets12 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour2,
            self.loc_ws5, 100)

        piglets13 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws5, 100)
        piglets14 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour2,
            self.loc_ws5, 50)

        self.loc_cell_ws5_1 = Location.objects.filter(pigletsGroupCell__workshop__number=5)[0]
        self.merged_piglets1 = PigletsMerger.objects.create_merger_return_group(
            parent_piglets=[piglets13, piglets14], new_location=self.loc_cell_ws5_1)

    def test_create_weighing(self):
        piglets = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws3, 101)

        weighing_record = WeighingPiglets.objects.create_weighing(
            piglets_group=piglets, total_weight=670, place='3/4'
            )
        self.assertEqual(weighing_record.piglets_group, piglets)
        self.assertEqual(weighing_record.total_weight, 670)
        self.assertEqual(weighing_record.average_weight, round((670 / piglets.quantity), 2))
        self.assertEqual(weighing_record.piglets_quantity, piglets.quantity)
        self.assertEqual(weighing_record.place, '3/4')

    def test_queryset_get_tour_data_by_place(self):
        piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(
            tour=self.tour1,
            location=self.loc_ws4,
            quantity=100,
            birthday=datetime.datetime(2020,5,5,0,0)
            )
        piglets2 = piglets_testing.create_new_group_with_metatour_by_one_tour(
            tour=self.tour1,
            location=self.loc_ws4,
            quantity=100,
            birthday=datetime.datetime(2020,5,8,0,0)
            )

        WeighingPiglets.objects.create_weighing(piglets_group=piglets1, total_weight=120,
            place='3/4', date=datetime.datetime.today())
        WeighingPiglets.objects.create_weighing(piglets_group=piglets1, total_weight=150,
            place='3/4', date=datetime.datetime(2020,9,25,0,0))

        WeighingPiglets.objects.create_weighing(piglets_group=piglets2, total_weight=360,
            place='4/8', date=datetime.datetime(2020,9,15,0,0))

        qs, total = WeighingPiglets.objects.all().get_tour_data_by_place(tour=self.tour1, place='3/4')
        self.assertEqual(qs.first().place, '3/4')
        self.assertEqual(total['total_quantity'], 200)


class CullingPigletsTest(TestCase):
    def setUp(self):
        locations_testing.create_workshops_sections_and_cells()
        piglets_testing.create_piglets_statuses()

        self.tour1 = Tour.objects.get_or_create_by_week_in_current_year(week_number=1)
        self.loc_ws3 = Location.objects.get(workshop__number=3)
        self.loc_ws4 = Location.objects.get(workshop__number=4)
        self.loc_ws5_cells = Location.objects.filter(pigletsGroupCell__workshop__number=5)

        self.piglets = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws3, 101)

    def test_create_culling_piglets(self):
        piglets = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws3, 101)

        culling = CullingPiglets.objects.create_culling_piglets(
            piglets_group=piglets, culling_type='padej', reason='xz', quantity=10, 
            total_weight=100, date='2020-03-09'
            )

        self.piglets.refresh_from_db()
        self.assertEqual(piglets.quantity, 91)
        self.assertEqual(culling.piglets_group, piglets)
        self.assertEqual(culling.culling_type, 'padej')
        self.assertEqual(culling.reason, 'xz')
        self.assertEqual(culling.total_weight, 100)
        self.assertEqual(culling.avg_weight, 10)
        self.assertEqual(culling.date.day, 9)
        self.assertEqual(culling.location, self.loc_ws3)

        piglets.location = self.loc_ws4
        piglets.save()

        culling.refresh_from_db()
        self.assertEqual(culling.location, self.loc_ws3)

    def test_manager_get_culling_data_by_piglets(self):
        piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws4, 101)
        piglets2 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws4, 99)
        piglets3 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws4, 105)

        CullingPiglets.objects.create_culling_piglets(
            piglets_group=piglets1, culling_type='padej', reason='xz', quantity=10, 
            total_weight=100, date='2020-03-09'
            )
        CullingPiglets.objects.create_culling_piglets(
            piglets_group=piglets1, culling_type='padej', reason='xz', quantity=1, 
            total_weight=9.5, date='2020-03-09'
            )
        CullingPiglets.objects.create_culling_piglets(
            piglets_group=piglets2, culling_type='padej', reason='xz', quantity=2, 
            total_weight=18, date='2020-03-09'
            )

        CullingPiglets.objects.create_culling_piglets(
            piglets_group=piglets3, culling_type='spec', reason='xz', quantity=2, 
            total_weight=18, date='2020-03-09'
            )

        CullingPiglets.objects.create_culling_piglets(
            piglets_group=piglets2, culling_type='spec', reason='xz', quantity=5, 
            total_weight=53, date='2020-03-09'
            )

        piglets = Piglets.objects.all().with_tour(week_number=1)

        culling_total_data1 = CullingPiglets.objects.get_culling_by_piglets(culling_type='spec',
            piglets=piglets)
        self.assertEqual(culling_total_data1['total_quantity'], 7)
        self.assertEqual(culling_total_data1['total_weight'], 71)
        self.assertEqual(culling_total_data1['avg_weight'], 9.8)

        culling_total_data2 = CullingPiglets.objects.get_culling_by_piglets(culling_type='padej',
            piglets=piglets)
        self.assertEqual(culling_total_data2['total_quantity'], 13)
        self.assertEqual(culling_total_data2['total_weight'], 127.5)
        self.assertEqual(culling_total_data2['avg_weight'], 9.5)

    def test_get_by_tour_and_ws_number(self):
        piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws5_cells[0], 101)
        piglets2 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws5_cells[1], 99)
        piglets3 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws5_cells[2], 105)

        CullingPiglets.objects.create_culling_piglets(
            piglets_group=piglets1, culling_type='padej', reason='xz', quantity=10, 
            total_weight=100, date='2020-12-09'
            )
        CullingPiglets.objects.create_culling_piglets(
            piglets_group=piglets1, culling_type='padej', reason='xz', quantity=1, 
            total_weight=9.5, date='2020-12-09'
            )
        CullingPiglets.objects.create_culling_piglets(
            piglets_group=piglets2, culling_type='padej', reason='xz', quantity=2, 
            total_weight=18, date='2020-12-09'
            )

        CullingPiglets.objects.create_culling_piglets(
            piglets_group=piglets3, culling_type='spec', reason='xz', quantity=2, 
            total_weight=18, date='2020-12-09'
            )

        CullingPiglets.objects.create_culling_piglets(
            piglets_group=piglets2, culling_type='spec', reason='xz', quantity=5, 
            total_weight=53, date='2020-12-09'
            )

        qs, total = CullingPiglets.objects\
            .get_by_tour_and_ws_number(tour=self.tour1, ws_number=5, culling_type='spec')

        self.assertEqual(qs.count(), 2)
        self.assertEqual(total['total_quantity'], 7)
        self.assertEqual(total['total_total_weight'], 71)


class RecountManagerTest(TestCase):
    def setUp(self):
        locations_testing.create_workshops_sections_and_cells()
        sows_testing.create_statuses()
        piglets_testing.create_piglets_statuses()
        self.tour1 = Tour.objects.get_or_create_by_week_in_current_year(1)
        self.ws3_cells = Location.objects.filter(sowAndPigletsCell__isnull=False)

    def test_create_recount(self):
        tour = Tour.objects.get_or_create_by_week_in_current_year(1)
        tour2 = Tour.objects.get_or_create_by_week_in_current_year(2)
        location = Location.objects.get(section__number=1, section__workshop__number=3)
        piglets = Piglets.objects.create(location=location, quantity=100, start_quantity=100,
        gilts_quantity=0, status=None)
        meta_tour = MetaTour.objects.create(piglets=piglets)

        record1 = meta_tour.records.create_record(meta_tour, tour, 60, piglets.quantity)
        record2 = meta_tour.records.create_record(meta_tour, tour2, 40, piglets.quantity)

        recount = Recount.objects.create_recount(piglets, 110)
        self.assertEqual(recount.quantity_before, 100)
        self.assertEqual(recount.quantity_after, 110)
        self.assertEqual(recount.balance, -10)
        self.assertEqual(recount.location, location)

        piglets.refresh_from_db()
        self.assertEqual(piglets.quantity, 110)

    def test_sum_balances_by_locations(self):
        #section 1
        piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(
            quantity=10, tour=self.tour1, location=self.ws3_cells[0])
        piglets2 = piglets_testing.create_new_group_with_metatour_by_one_tour(
            quantity=15, tour=self.tour1, location=self.ws3_cells[1])

        # section 2
        piglets3 = piglets_testing.create_new_group_with_metatour_by_one_tour(
            quantity=11, tour=self.tour1, location=self.ws3_cells[50])

        recount1 = Recount.objects.create_recount(piglets=piglets1, new_quantity=9)
        recount2 = Recount.objects.create_recount(piglets=piglets2, new_quantity=13)
        recount3 = Recount.objects.create_recount(piglets=piglets3, new_quantity=14)

        ws3_locs = Location.objects.all().get_workshop_location_by_number(workshop_number=3)
        self.assertEqual(
            Recount.objects.sum_balances_by_locations(locations=ws3_locs), 0)

        sec1 = Location.objects.filter(section__number=1, 
                section__workshop__number=3).first().section
        sec1_locs = Location.objects.all().get_locations_in_section(sec1)
        self.assertEqual(Recount.objects.sum_balances_by_locations(locations=sec1_locs), 3)

        sec2 = Location.objects.filter(section__number=2, 
                section__workshop__number=3).first().section
        sec2_locs = Location.objects.all().get_locations_in_section(sec2)
        self.assertEqual(Recount.objects.sum_balances_by_locations(locations=sec2_locs), -3)