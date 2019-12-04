# -*- coding: utf-8 -*-
from django.test import TestCase, TransactionTestCase
from django.core.exceptions import ValidationError

from piglets.models import Piglets
from piglets_events.models import PigletsMerger, PigletsSplit, WeighingPiglets, CullingPiglets
from tours.models import Tour
from locations.models import Location

import locations.testing_utils as locations_testing
import piglets.testing_utils as piglets_testing


class PigletsMergerModelTest(TransactionTestCase):
    def setUp(self):
        locations_testing.create_workshops_sections_and_cells()
        # sows_testing.create_statuses()
        piglets_testing.create_piglets_statuses()       

        self.tour1 = Tour.objects.get_or_create_by_week_in_current_year(week_number=1)
        self.tour2 = Tour.objects.get_or_create_by_week_in_current_year(week_number=2)
        self.tour3 = Tour.objects.get_or_create_by_week_in_current_year(week_number=3)
        self.tour4 = Tour.objects.get_or_create_by_week_in_current_year(week_number=4)
        self.loc_ws3 = Location.objects.get(workshop__number=3)
        self.loc_ws3_sec1 = Location.objects.get(section__workshop__number=3, section__number=1)
        self.loc_ws3_sec2 = Location.objects.get(section__workshop__number=3, section__number=2)

    def test_create_merger_return_group_v1(self):
        piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws3, 10)
        piglets2 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour2,
            self.loc_ws3, 10)
        piglets3 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour2,
            self.loc_ws3, 10)

        piglets_qs = Piglets.objects.all()

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

        piglets1.refresh_from_db()
        self.assertEqual(piglets1.active, False)

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
        piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws3_sec1, 10)
        piglets2 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour2,
            self.loc_ws3_sec1, 10)
        piglets3 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour3,
            self.loc_ws3_sec1, 10)

        merging_list = [
            {'id': piglets1.pk, 'quantity': 10, 'changed': False},
            {'id': piglets2.pk, 'quantity': 10, 'changed': False}
        ]

        nomad_piglets = PigletsMerger.objects.create_from_merging_list(merging_list, self.loc_ws3)
        
        self.assertEqual(nomad_piglets.location, self.loc_ws3)
        self.assertEqual(nomad_piglets.quantity, 20)
        piglets1.refresh_from_db()
        piglets2.refresh_from_db()
        self.assertEqual(nomad_piglets.merger_as_child, piglets1.merger_as_parent)
        self.assertEqual(nomad_piglets.merger_as_child, piglets2.merger_as_parent)
        self.assertEqual(nomad_piglets.merger_as_child.piglets_as_parents.get_inactive().count(), 2)

    def test_create_from_merging_list_v2(self):
        # with change quantity
        piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws3_sec1, 10)
        piglets2 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour2,
            self.loc_ws3_sec1, 10)

        merging_list = [
            {'id': piglets1.pk, 'quantity': 7, 'changed': True},
            {'id': piglets2.pk, 'quantity': 10, 'changed': False}
        ]

        nomad_piglets = PigletsMerger.objects.create_from_merging_list(merging_list, self.loc_ws3)
        self.assertEqual(nomad_piglets.location, self.loc_ws3)
        self.assertEqual(nomad_piglets.quantity, 17)
        self.assertEqual(nomad_piglets.active, True)
        piglets1.refresh_from_db()
        piglets2.refresh_from_db()

        # should be 5 piglets
        self.assertEqual(Piglets.objects.get_active_and_inactive().count(), 5)
        #  should be 2 childs from split
        split_record = piglets1.split_as_parent
        self.assertEqual(split_record.parent_piglets, piglets1)
        self.assertEqual(split_record.parent_piglets.active, False)

        # children from split
        self.assertEqual(split_record.piglets_as_child.get_active().count(), 1)
        self.assertEqual(split_record.piglets_as_child.get_active()[0].quantity, 3)
        self.assertEqual(split_record.piglets_as_child.get_active()[0].active, True)
        self.assertEqual(split_record.piglets_as_child.get_inactive()[0].quantity, 7)
        self.assertEqual(split_record.piglets_as_child.get_inactive()[0].active, False)

        self.assertEqual(piglets1.active, False)
        self.assertEqual(piglets2.active, False)

        # with self.assertNumQueries(1):
        #     print('split active ', split_record.piglets_as_child.get_active())

        # with self.assertNumQueries(1):
        #     print('split active ', split_record.piglets_as_child.all().active())
       

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
        
        # child_pidlets1 records        
        self.assertEqual(child_piglets1.metatour.records.all().count(), 2)
        self.assertEqual(child_piglets1.metatour.records.all()[0].tour, self.tour1)
        self.assertEqual(child_piglets1.metatour.records.all()[0].quantity, 33)
        self.assertEqual(child_piglets1.metatour.records.all()[0].percentage, 33.0)

        self.assertEqual(child_piglets1.metatour.records.all()[1].tour, self.tour2)
        self.assertEqual(child_piglets1.metatour.records.all()[1].quantity, 67)
        self.assertEqual(child_piglets1.metatour.records.all()[1].percentage, 67.0)

        # child_pidlets2 records
        self.assertEqual(child_piglets2.metatour.records.all().count(), 2)
        self.assertEqual(child_piglets2.metatour.records.all()[0].tour, self.tour1)
        self.assertEqual(child_piglets2.metatour.records.all()[0].quantity, 33)
        self.assertEqual(child_piglets2.metatour.records.all()[0].percentage, 33.0)

        self.assertEqual(child_piglets2.metatour.records.all()[1].tour, self.tour2)
        self.assertEqual(child_piglets2.metatour.records.all()[1].quantity, 67)
        self.assertEqual(child_piglets2.metatour.records.all()[1].percentage, 67.0)

        # test piglets manager
        split_record = piglets.split_as_parent
        self.assertEqual(split_record.piglets_as_child.all().count(), 2)
        self.assertEqual(split_record.piglets_as_child.get_inactive().count(), 0)
        self.assertEqual(split_record.piglets_as_child.get_active_and_inactive().count(), 2)
        
    def test_split_validate(self):
        piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws3, 100)
        piglets_qs = Piglets.objects.all()
        piglets = PigletsMerger.objects.create_merger_return_group(parent_piglets=piglets_qs,
            new_location=self.loc_ws3)

        with self.assertRaises(ValidationError):
            child_piglets1, child_piglets2 = PigletsSplit.objects.split_return_groups(
                parent_piglets=piglets, new_amount=100)


class WeighingPigletsTest(TestCase):
    def setUp(self):
        locations_testing.create_workshops_sections_and_cells()
        piglets_testing.create_piglets_statuses()
        self.tour1 = Tour.objects.get_or_create_by_week_in_current_year(week_number=1)
        self.loc_ws3 = Location.objects.get(workshop__number=3)

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


class CullingPigletsTest(TestCase):
    def setUp(self):
        locations_testing.create_workshops_sections_and_cells()
        piglets_testing.create_piglets_statuses()

        self.tour1 = Tour.objects.get_or_create_by_week_in_current_year(week_number=1)
        self.loc_ws3 = Location.objects.get(workshop__number=3)
        self.piglets = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws3, 101)

    def test_create_culling_piglets(self):
        culling = CullingPiglets.objects.create_culling_piglets(
            piglets_group=self.piglets, culling_type='padej', reason='xz'
            )

        self.piglets.refresh_from_db()
        self.assertEqual(self.piglets.quantity, 100)
        self.assertEqual(culling.piglets_group, self.piglets)
        self.assertEqual(culling.culling_type, 'padej')
        self.assertEqual(culling.reason, 'xz')
        


# class RecountManagerTest(TestCase):
#     def setUp(self):
#         locations_testing.create_workshops_sections_and_cells()
#         sows_testing.create_statuses()
#         piglets_testing.create_piglets_statuses()

#     def test_create_recount_nomad_group(self):
#         # quantity 37
#         nomad_group = piglets_testing.create_nomad_group_from_three_new_born()
#         recount = piglets_events_models.NomadPigletsGroupRecount.objects. \
#             create_recount(nomad_group, 35)
#         self.assertEqual(recount.quantity_before, 37)
#         self.assertEqual(recount.quantity_after, 35)
#         self.assertEqual(recount.balance, -2)

#     def test_create_recount_nomad_group2(self):
#         # quantity 37
#         nomad_group = piglets_testing.create_nomad_group_from_three_new_born()
#         recount = piglets_events_models.NomadPigletsGroupRecount.objects. \
#             create_recount(nomad_group, 39)
#         self.assertEqual(recount.quantity_before, 37)
#         self.assertEqual(recount.quantity_after, 39)
#         self.assertEqual(recount.balance, 2)

#     def test_create_recount_new_born_group(self):
#         # quantity 10
#         new_born_group = piglets_testing.create_new_born_group()
#         recount = piglets_events_models.NewBornPigletsGroupRecount.objects. \
#             create_recount(new_born_group, 8)
#         self.assertEqual(recount.quantity_before, 10)
#         self.assertEqual(recount.quantity_after, 8)
#         self.assertEqual(recount.balance, -2)

#     def test_create_recount_new_born_group2(self):
#         # quantity 10
#         new_born_group = piglets_testing.create_new_born_group()
#         recount = piglets_events_models.NewBornPigletsGroupRecount.objects. \
#             create_recount(new_born_group, 12)
#         self.assertEqual(recount.quantity_before, 10)
#         self.assertEqual(recount.quantity_after, 12)
#         self.assertEqual(recount.balance, 2)

#     def test_get_recounts(self):
#         # create newborngroups tour=1, qnty=10
#         for cell_number in range(1, 11):
#             piglets_testing.create_new_born_group(section_number=1, cell_number=cell_number,
#                 week=1, quantity=10)

#         piglets_group_qs = piglets_models.NewBornPigletsGroup.objects.all()

#         # get 1 piglet from every group. recount -1. negative recount
#         for nbgroup in piglets_group_qs:
#             piglets_events_models.NewBornPigletsGroupRecount.objects.create_recount(nbgroup, 9)

#         # add 1 piglet to every group. recount +1. positive recount
#         for nbgroup in piglets_group_qs:
#             piglets_events_models.NewBornPigletsGroupRecount.objects.create_recount(nbgroup, 10)

#         self.assertEqual(piglets_events_models.NewBornPigletsGroupRecount.objects \
#                 .get_recounts_from_groups(piglets_group_qs).count(), 20)

#         self.assertEqual(piglets_events_models.NewBornPigletsGroupRecount.objects \
#                 .get_recounts_with_negative_balance(piglets_group_qs).count(), 10)

#         self.assertEqual(piglets_events_models.NewBornPigletsGroupRecount.objects \
#                 .get_recounts_with_positive_balance(piglets_group_qs).count(), 10)

#         self.assertEqual(piglets_events_models.NewBornPigletsGroupRecount.objects \
#                 .get_recounts_with_negative_balance(piglets_group_qs).get_sum_balance(), -10)

#         self.assertEqual(piglets_events_models.NewBornPigletsGroupRecount.objects \
#                 .get_recounts_with_positive_balance(piglets_group_qs).get_sum_balance(), 10)
