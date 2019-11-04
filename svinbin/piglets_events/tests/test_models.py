# -*- coding: utf-8 -*-
from django.test import TestCase
from django.core.exceptions import ValidationError

import piglets_events.models as piglets_events_models
import piglets.models as piglets_models
import locations.models as locations_models

import locations.testing_utils as locations_testing
import sows.testing_utils as sows_testing
import piglets.testing_utils as piglets_testing


class NewBornMergerModelTest(TestCase):
    def setUp(self):
        locations_testing.create_workshops_sections_and_cells()
        sows_testing.create_statuses()
        piglets_testing.create_piglets_statuses()

        self.piglets_group1 = piglets_testing.create_new_born_group(1, 1, 1, 10)
        self.piglets_group2 = piglets_testing.create_new_born_group(1, 2, 1, 12)
        self.piglets_group3 = piglets_testing.create_new_born_group(1, 3, 2, 15)

        self.piglets_group4 = piglets_testing.create_new_born_group(
            section_number=1,
            cell_number=4,
            week=1,
            quantity=10)
        self.piglets_group5 = piglets_testing.create_new_born_group(1, 5, 1, 12)
        

        self.piglets_groups_same_tour = piglets_models.NewBornPigletsGroup.objects.filter(pk__in=
            [self.piglets_group4.pk, self.piglets_group5.pk])
        self.piglets_groups_two_tours = piglets_models.NewBornPigletsGroup.objects.filter(pk__in=
            [self.piglets_group1.pk, self.piglets_group2.pk, self.piglets_group3.pk])

        self.new_born_merger_same_tour = piglets_events_models.NewBornPigletsMerger.objects \
            .create_merger(self.piglets_groups_same_tour)
        self.new_born_merger_two_tours = piglets_events_models.NewBornPigletsMerger.objects \
            .create_merger(self.piglets_groups_two_tours)

        self.tour1 = self.new_born_merger_two_tours.get_first_tour()

    def test_get_first_tour(self):
        self.assertEqual(self.tour1.week_number, 1)

    def test_get_next_tour(self):
        next_tour = self.new_born_merger_two_tours.get_next_tour([self.tour1])
        self.assertEqual(next_tour.week_number, 2)

    def test_get_piglets_groups_by_tour(self):
        tour1_piglets = self.new_born_merger_two_tours.get_piglets_groups_by_tour(self.tour1)
        quantity_piglets_by_tour = self.new_born_merger_two_tours.count_quantity_by_tour(self.tour1)
        self.assertEqual(quantity_piglets_by_tour, 22)

    def test_count_all_piglets(self):
        quantity_all_piglets = self.new_born_merger_two_tours.count_all_piglets()
        self.assertEqual(quantity_all_piglets, 37)

    def test_get_percentage_by_tour(self):
        model_percentage = self.new_born_merger_two_tours.get_percentage_by_tour(self.tour1)
        percentage = (self.new_born_merger_two_tours.count_quantity_by_tour(self.tour1) * 100) \
         / self.new_born_merger_two_tours.count_all_piglets()
        self.assertEqual(model_percentage, percentage)

    # def test_count_quantity_and_percentage_by_tours(self):
    #     print(self.new_born_merger_two_tours.count_quantity_and_percentage_by_tours())
    #     # to write

    def test_create_records(self):
        self.new_born_merger_two_tours.create_records()
        self.assertEqual(self.new_born_merger_two_tours.create_records().first().tour.week_number, 1)
        self.assertEqual(self.new_born_merger_two_tours.create_records().first().quantity, 22)
        self.assertEqual(self.new_born_merger_two_tours.records.all().count(), 2)

    def tes_deactivate_groups(self):    
        self.piglets_group1.refresh_from_db()
        self.assertEqual(self.piglets_group1.quantity, 0)
        self.assertEqual(self.piglets_group1.active, False)

        self.piglets_group2.refresh_from_db()
        self.assertEqual(self.piglets_group2.quantity, 0)
        self.assertEqual(self.piglets_group2.active, False)

        self.piglets_group3.refresh_from_db()
        self.assertEqual(self.piglets_group3.quantity, 0)
        self.assertEqual(self.piglets_group3.active, False)

    def test_cells(self):
        cell2_list = [ cell_number for cell_number in  self.new_born_merger_two_tours.cells]
        cell1_list = [ cell_number for cell_number in  self.new_born_merger_same_tour.cells]
        self.assertEqual([self.piglets_group1.location.get_cell_number,
            self.piglets_group2.location.get_cell_number, self.piglets_group3.location.get_cell_number],
            cell2_list)
        self.assertEqual([self.piglets_group4.location.get_cell_number,
            self.piglets_group5.location.get_cell_number],
            cell1_list)

    def test_sow_status_update_after_merge(self):
        new_born_merger_same_tour = piglets_events_models.NewBornPigletsMerger.objects \
            .create_merger(self.piglets_groups_same_tour)




#to do MergerRecordsTest

class NomadPigletsGroupMergerTest(TestCase):
    def setUp(self):
        locations_testing.create_workshops_sections_and_cells()
        sows_testing.create_statuses()
        piglets_testing.create_piglets_statuses()

        self.piglets_group1 = piglets_testing.create_nomad_group_from_three_new_born()
        self.piglets_group2 = piglets_testing.create_nomad_group_from_three_new_born()

        self.cell = locations_models.PigletsGroupCell.objects.get(workshop__number=4,
             section__number=1, number=1)
        self.new_location = locations_models.Location.objects.get(pigletsGroupCell=self.cell)

        self.merger = piglets_events_models.NomadPigletsGroupMerger.objects \
            .create_nomad_merger(
                nomad_groups=[self.piglets_group1, self.piglets_group2],
                new_location=self.new_location
                )

    def test_create_merger_and_return_nomad_piglets_group(self):
        merged_group = piglets_events_models.NomadPigletsGroupMerger.objects \
            .create_merger_and_return_nomad_piglets_group(
                nomad_groups=[self.piglets_group1, self.piglets_group2],
                new_location=self.new_location
                )
        self.assertEqual(merged_group.location, self.new_location)
        self.assertEqual(merged_group.location.pigletsGroupCell, self.cell)
        self.assertEqual(merged_group.quantity, self.piglets_group1.start_quantity 
            + self.piglets_group2.start_quantity)
        
        self.piglets_group1.refresh_from_db()
        self.piglets_group2.refresh_from_db()
        self.assertEqual(self.piglets_group1.active, False)
        self.assertEqual(self.piglets_group2.active, False)
        self.assertEqual(self.piglets_group1.quantity, 0)
        self.assertEqual(self.piglets_group2.quantity, 0)
    
    def test_count_all_piglets(self):
        count_all = self.merger.count_all_piglets()
        self.assertEqual(count_all, 74)

    def test_count_all_gilts(self):
        count_all = self.merger.count_all_gilts()
        self.assertEqual(count_all, 0)

    def test_create_nomad_group(self):
        nomad_group = self.merger.create_nomad_group()
        self.assertEqual(nomad_group.location, self.new_location)
        self.assertEqual(nomad_group.location.pigletsGroupCell, self.cell)
        self.assertEqual(nomad_group.quantity, self.piglets_group1.start_quantity 
            + self.piglets_group2.start_quantity)


class NomadMergerRecordManagerTest(TestCase):
    def setUp(self):
        locations_testing.create_workshops_sections_and_cells()
        sows_testing.create_statuses()
        piglets_testing.create_piglets_statuses()

        self.piglets_group1 = piglets_testing.create_nomad_group_from_three_new_born()
        self.piglets_group2 = piglets_testing.create_nomad_group_from_three_new_born()

        self.cell = locations_models.PigletsGroupCell.objects.get(workshop__number=4,
             section__number=1, number=1)
        self.new_location = locations_models.Location.objects.get(pigletsGroupCell=self.cell)

        self.merger = piglets_events_models.NomadPigletsGroupMerger.objects \
            .create_nomad_merger(
                nomad_groups=[self.piglets_group1, self.piglets_group2],
                new_location=self.new_location
                )

    def test_create_records(self):
        records = piglets_events_models.NomadMergerRecord.objects.create_records(self.merger)
        self.assertEqual(records.count(), 2)
        self.assertEqual(records.first().merger, self.merger)
        self.assertEqual(records.first().nomad_group, self.piglets_group1)
        self.assertEqual(records.first().nomad_group.quantity, self.piglets_group1.quantity)
        self.assertEqual(records.first().percentage, self.piglets_group1.quantity *100 / \
            self.merger.count_all_piglets())


class SplitNomadPigletsGroupManagerTest(TestCase):
    def setUp(self):
        locations_testing.create_workshops_sections_and_cells()
        sows_testing.create_statuses()
        piglets_testing.create_piglets_statuses()

    def test_split_group(self):
        # quantity 37
        nomad_group = piglets_testing.create_nomad_group_from_three_new_born()
        nomad_group.gilts_quantity = 10
        nomad_group.save()

        first_group, second_group = piglets_events_models.SplitNomadPigletsGroup \
            .objects.split_group(parent_nomad_group=nomad_group, new_group_piglets_amount=5,
            initiator=None, new_group_gilts_quantity=1)
        self.assertEqual(first_group.quantity, 32)
        self.assertEqual(second_group.quantity, 5)

        self.assertEqual(first_group.gilts_quantity, 9)
        self.assertEqual(second_group.gilts_quantity, 1)

        self.assertEqual(first_group.location, nomad_group.location)
        self.assertEqual(second_group.location, nomad_group.location)

        self.assertEqual(nomad_group.quantity, 0)
        self.assertEqual(nomad_group.active, False)

    def test_validate(self):
        # quantity 37
        parent_piglets_group = piglets_testing.create_nomad_group_from_three_new_born()
        # first_group, second_group = piglets_events_models.SplitNomadPigletsGroup \
        #     .objects.split_group(parent_piglets_group, 40)
        self.assertRaises(ValidationError, piglets_events_models.SplitNomadPigletsGroup \
            .objects.split_group, parent_piglets_group, 40)


class NomadPigletsGroupMergerManagerTest(TestCase):
    def setUp(self):
        locations_testing.create_workshops_sections_and_cells()
        sows_testing.create_statuses()
        piglets_testing.create_piglets_statuses()

    def test_create_nomad_merger(self):
        # quantity 37
        nomad_group1 = piglets_testing.create_nomad_group_from_three_new_born()
        first_group, second_group = piglets_events_models.SplitNomadPigletsGroup.objects.split_group(nomad_group1, 5)

        # quantity 30
        nomad_group2 = piglets_testing.create_nomad_group_from_three_new_born_two_tours()
        third_group, fourth_group = piglets_events_models.SplitNomadPigletsGroup.objects.split_group(nomad_group2, 7)
        self.assertEqual(third_group.quantity, 23)

        merge_groups = piglets_models.NomadPigletsGroup.objects.filter(pk__in=[first_group.pk, fourth_group.pk])
        new_location = first_group.location
        nomad_merger = piglets_events_models.NomadPigletsGroupMerger.objects.create_nomad_merger(merge_groups,
         new_location)

        first_group.refresh_from_db()
        fourth_group.refresh_from_db()
        self.assertEqual(first_group.groups_merger, nomad_merger)
        self.assertEqual(fourth_group.groups_merger, nomad_merger)

        merge_records = piglets_events_models.NomadMergerRecord.objects.create_records(nomad_merger)
        self.assertEqual(merge_records.first().quantity, 32)
        self.assertEqual(merge_records.first().nomad_group, first_group)
        # print(merge_records.first().percentage)

        self.assertEqual(merge_records[1].quantity, 7)
        self.assertEqual(merge_records[1].nomad_group, fourth_group)
        # print(merge_records[1].percentage)

        # print(merge_records[0].nomad_group.location)
        # print(merge_records[0].nomad_group.location)
        # print(type(merge_records[0].nomad_group.location))

        nomad_group = nomad_merger.create_nomad_group()
        first_group.refresh_from_db()
        fourth_group.refresh_from_db()
        self.assertEqual(first_group.quantity, 0)
        self.assertEqual(first_group.active, False)
        self.assertEqual(fourth_group.quantity, 0)
        self.assertEqual(fourth_group.active, False)

        self.assertEqual(nomad_group.quantity, 39)
        self.assertEqual(nomad_group.start_quantity, 39)
        self.assertEqual(nomad_group.location, first_group.location)
        self.assertEqual(nomad_group.creating_nomad_merger, nomad_merger)


class RecountManagerTest(TestCase):
    def setUp(self):
        locations_testing.create_workshops_sections_and_cells()
        sows_testing.create_statuses()
        piglets_testing.create_piglets_statuses()

    def test_create_recount_nomad_group(self):
        # quantity 37
        nomad_group = piglets_testing.create_nomad_group_from_three_new_born()
        recount = piglets_events_models.NomadPigletsGroupRecount.objects. \
            create_recount(nomad_group, 35)
        self.assertEqual(recount.quantity_before, 37)
        self.assertEqual(recount.quantity_after, 35)
        self.assertEqual(recount.balance, -2)

    def test_create_recount_nomad_group2(self):
        # quantity 37
        nomad_group = piglets_testing.create_nomad_group_from_three_new_born()
        recount = piglets_events_models.NomadPigletsGroupRecount.objects. \
            create_recount(nomad_group, 39)
        self.assertEqual(recount.quantity_before, 37)
        self.assertEqual(recount.quantity_after, 39)
        self.assertEqual(recount.balance, 2)

    def test_create_recount_new_born_group(self):
        # quantity 10
        new_born_group = piglets_testing.create_new_born_group()
        recount = piglets_events_models.NewBornPigletsGroupRecount.objects. \
            create_recount(new_born_group, 8)
        self.assertEqual(recount.quantity_before, 10)
        self.assertEqual(recount.quantity_after, 8)
        self.assertEqual(recount.balance, -2)

    def test_create_recount_new_born_group2(self):
        # quantity 10
        new_born_group = piglets_testing.create_new_born_group()
        recount = piglets_events_models.NewBornPigletsGroupRecount.objects. \
            create_recount(new_born_group, 12)
        self.assertEqual(recount.quantity_before, 10)
        self.assertEqual(recount.quantity_after, 12)
        self.assertEqual(recount.balance, 2)


class WeighingPigletsTest(TestCase):
    def setUp(self):
        locations_testing.create_workshops_sections_and_cells()
        sows_testing.create_statuses()
        piglets_testing.create_piglets_statuses()

    def test_create_weighing(self):
        piglets_group = piglets_testing.create_nomad_group_from_three_new_born()
        weighing_record = piglets_events_models.WeighingPiglets.objects.create_weighing(
            piglets_group=piglets_group, total_weight=670, place='3/4'
            )
        self.assertEqual(weighing_record.piglets_group, piglets_group)
        self.assertEqual(weighing_record.total_weight, 670)
        self.assertEqual(weighing_record.average_weight, 670/piglets_group.quantity)
        self.assertEqual(weighing_record.piglets_quantity, piglets_group.quantity)
        self.assertEqual(weighing_record.place, '3/4')


class CullingPigletsTest(TestCase):
    def setUp(self):
        locations_testing.create_workshops_sections_and_cells()
        sows_testing.create_statuses()
        piglets_testing.create_piglets_statuses()

    def test_create_culling_piglets(self):
        new_born_group = piglets_testing.create_new_born_group()
        self.assertEqual(new_born_group.quantity, 10)
        culling_new_born = piglets_events_models.CullingNewBornPiglets.objects.create_culling_piglets(
            piglets_group=new_born_group, culling_type='padej', reason='xz'
            )
        new_born_group.refresh_from_db()
        self.assertEqual(new_born_group.quantity, 9)
        self.assertEqual(culling_new_born.quantity, 1)
        self.assertEqual(culling_new_born.is_it_gilt, False)
        self.assertEqual(culling_new_born.culling_type, 'padej')
        self.assertEqual(culling_new_born.reason, 'xz')

        piglets_group = piglets_testing.create_nomad_group_from_three_new_born()
        piglets_group.add_gilts_increase_quantity(1)
        self.assertEqual(piglets_group.quantity, 38)
        culling_nomad = piglets_events_models.CullingNomadPiglets.objects.create_culling_gilt(
            piglets_group=piglets_group, culling_type='padej', reason='xz'
            )
        piglets_group.refresh_from_db()
        self.assertEqual(piglets_group.quantity, 37)
        self.assertEqual(culling_nomad.quantity, 1)
        self.assertEqual(piglets_group.gilts_quantity, 0)
        self.assertEqual(culling_nomad.is_it_gilt, True)
        self.assertEqual(culling_nomad.culling_type, 'padej')
        self.assertEqual(culling_nomad.reason, 'xz')
