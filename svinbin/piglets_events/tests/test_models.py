from mixer.backend.django import mixer
# from freezegun import freeze_time

from django.test import TestCase

import piglets_events.models as piglets_events_models
import piglets.models as piglets_models
import sows.models as sows_models
import sows_events.models as sows_events_models
import tours.models as tour_models
import transactions.models as transactions_models
import workshops.models as workshops_models

import workshops.testing_utils as workshop_testing
import sows.testing_utils as sows_testing
import piglets.testing_utils as piglets_testing


class NewBornMergerModelTest(TestCase):
    def setUp(self):
        workshop_testing.create_workshops_sections_and_cells()
        sows_testing.create_statuses()
        piglets_testing.create_piglets_statuses()

    def test_get_first_tour(self):
        piglets_group1 = piglets_testing.create_new_born_group(1, 1, 1, 10)
        piglets_group2 = piglets_testing.create_new_born_group(1, 2, 1, 12)
        piglets_group3 = piglets_testing.create_new_born_group(1, 3, 2, 15)

        piglets_groups_same_tour = piglets_models.NewBornPigletsGroup.objects.filter(pk__in=
            [piglets_group1.pk, piglets_group2.pk])
        piglets_groups_two_tours = piglets_models.NewBornPigletsGroup.objects.filter(pk__in=
            [piglets_group1.pk, piglets_group2.pk, piglets_group3.pk])

        new_born_merger_same_tour = piglets_events_models.NewBornPigletsMerger.objects \
            .create_merger(piglets_groups_same_tour)
        new_born_merger_two_tours = piglets_events_models.NewBornPigletsMerger.objects \
            .create_merger(piglets_groups_two_tours)

        tour1 = new_born_merger_two_tours.get_first_tour()
        self.assertEqual(tour1.week_number, 1)
        next_tour = new_born_merger_two_tours.get_next_tour([tour1])
        self.assertEqual(next_tour.week_number, 2)

        tour1_piglets = new_born_merger_two_tours.get_piglets_groups_by_tour(tour1)
        
        quantity_piglets_by_tour = new_born_merger_two_tours.count_quantity_by_tour(tour1)
        self.assertEqual(quantity_piglets_by_tour, 22)

        quantity_all_piglets = new_born_merger_two_tours.count_all_piglets()
        print(quantity_all_piglets)

        print(new_born_merger_two_tours.get_percentage_by_tour(tour1))

        print(new_born_merger_two_tours.count_quantity_and_percentage_by_tours())

        print(new_born_merger_two_tours.create_records())
        self.assertEqual(new_born_merger_two_tours.create_records().first().tour.week_number, 1)
        self.assertEqual(new_born_merger_two_tours.create_records().first().quantity, 22)
        self.assertEqual(new_born_merger_two_tours.records.all().count(), 2)

        nomad_group = new_born_merger_two_tours.create_nomad_group()
        self.assertEqual(nomad_group.quantity, 37)

        piglets_group1.refresh_from_db()
        self.assertEqual(piglets_group1.quantity, 0)
        self.assertEqual(piglets_group1.active, False)

        piglets_group2.refresh_from_db()
        self.assertEqual(piglets_group2.quantity, 0)
        self.assertEqual(piglets_group2.active, False)

        piglets_group3.refresh_from_db()
        self.assertEqual(piglets_group3.quantity, 0)
        self.assertEqual(piglets_group3.active, False)


# class WeighingPigletsTest(TestCase):
#     def setUp(self):
#         workshop_testing.create_workshops_sections_and_cells()
#         sows_testing.create_statuses()
#         piglets_testing.create_piglets_statuses()

#     def test_create_weighing(self):
#         piglets_group = piglets_testing.create_nomad_group_from_three_new_born()
#         weighing_record = piglets_events_models.WeighingPiglets.objects.create_weighing(
#             piglets_group=piglets_group, total_weight=670, place='3/4'
#             )
#         self.assertEqual(weighing_record.piglets_group, piglets_group)
#         self.assertEqual(weighing_record.total_weight, 670)
#         self.assertEqual(weighing_record.average_weight, 670/piglets_group.quantity)
#         self.assertEqual(weighing_record.piglets_quantity, piglets_group.quantity)
#         self.assertEqual(weighing_record.place, '3/4')


# class NomadPigletsGroupMergerTest(TestCase):
#     def setUp(self):
#         workshop_testing.create_workshops_sections_and_cells()
#         sows_testing.create_statuses()
#         piglets_testing.create_piglets_statuses()

#     def test_create_merger_and_return_nomad_piglets_group(self):
#         piglets_group1 = piglets_testing.create_nomad_group_from_three_new_born()
#         piglets_group2 = piglets_testing.create_nomad_group_from_three_new_born()

#         cell = workshops_models.PigletsGroupCell.objects.get(workshop__number=4,
#              section__number=1, number=1)
#         new_location = transactions_models.Location.objects.create_location(cell)

#         merged_group = piglets_events_models.NomadPigletsGroupMerger.objects \
#             .create_merger_and_return_nomad_piglets_group(
#                 nomad_groups=[piglets_group1, piglets_group2],
#                 new_location=new_location
#                 )

#         self.assertEqual(merged_group.location, new_location)
#         self.assertEqual(merged_group.location.get_location, cell)
#         self.assertEqual(merged_group.quantity, piglets_group1.start_quantity 
#             + piglets_group2.start_quantity)
        
#         piglets_group1.refresh_from_db()
#         piglets_group2.refresh_from_db()
#         self.assertEqual(piglets_group1.active, False)
#         self.assertEqual(piglets_group2.active, False)
#         self.assertEqual(piglets_group1.quantity, 0)
#         self.assertEqual(piglets_group2.quantity, 0)
        

# class SplitNomadPigletsGroupTest(TestCase):
#     def setUp(self):
#         workshop_testing.create_workshops_sections_and_cells()
#         sows_testing.create_statuses()
#         piglets_testing.create_piglets_statuses()

#     def test_split_group(self):
#         parent_piglets_group = piglets_testing.create_nomad_group_from_three_new_born()
#         self.assertEqual(parent_piglets_group.location.get_location.number, 3)
#         self.assertEqual(parent_piglets_group.quantity, 37)

#         first_group, second_group = piglets_events_models.SplitNomadPigletsGroup \
#             .objects.split_group(parent_piglets_group, 10)

#         self.assertEqual(first_group.quantity, 27)
#         self.assertEqual(second_group.quantity, 10)
#         self.assertEqual(first_group.location.get_location.number, 3)
#         self.assertEqual(second_group.location.get_location.number, 3)
#         self.assertEqual(first_group.status, parent_piglets_group.status)
#         self.assertEqual(second_group.status, parent_piglets_group.status)
#         self.assertEqual(first_group.active, True)
#         self.assertEqual(second_group.active, True)
#         self.assertEqual(parent_piglets_group.quantity, 0)
#         self.assertEqual(parent_piglets_group.active, False)
#         self.assertEqual(first_group.split_record, parent_piglets_group.split_event)
        

# class SplitNomadPigletsGroupManagerTest(TestCase):
#     def setUp(self):
#         workshop_testing.create_workshops_sections_and_cells()
#         sows_testing.create_statuses()
#         piglets_testing.create_piglets_statuses()

#     def test_split_group(self):
#         # quantity 37
#         nomad_group = piglets_testing.create_nomad_group_from_three_new_born()
#         nomad_group.gilts_quantity = 10
#         nomad_group.save()

#         first_group, second_group = piglets_events_models.SplitNomadPigletsGroup \
#             .objects.split_group(parent_nomad_group=nomad_group, new_group_piglets_amount=5,
#             initiator=None, new_group_gilts_quantity=1)
#         self.assertEqual(first_group.quantity, 32)
#         self.assertEqual(second_group.quantity, 5)

#         self.assertEqual(first_group.gilts_quantity, 9)
#         self.assertEqual(second_group.gilts_quantity, 1)

#         self.assertEqual(first_group.location.get_location, nomad_group.location.get_location)
#         self.assertEqual(second_group.location.get_location, nomad_group.location.get_location)

#         self.assertEqual(nomad_group.quantity, 0)
#         self.assertEqual(nomad_group.active, False)


# class NomadPigletsGroupMergerManagerTest(TestCase):
#     def setUp(self):
#         workshop_testing.create_workshops_sections_and_cells()
#         sows_testing.create_statuses()
#         piglets_testing.create_piglets_statuses()

#     def test_create_nomad_merger(self):
#         # quantity 37
#         nomad_group1 = piglets_testing.create_nomad_group_from_three_new_born()
#         first_group, second_group = piglets_events_models.SplitNomadPigletsGroup.objects.split_group(nomad_group1, 5)

#         # quantity 30
#         nomad_group2 = piglets_testing.create_nomad_group_from_three_new_born2()
#         third_group, fourth_group = piglets_events_models.SplitNomadPigletsGroup.objects.split_group(nomad_group2, 7)
#         self.assertEqual(third_group.quantity, 23)

#         merge_groups = piglets_models.NomadPigletsGroup.objects.filter(pk__in=[first_group.pk, fourth_group.pk])
#         new_location = first_group.location.duplicate_location_from_model()
#         nomad_merger = piglets_events_models.NomadPigletsGroupMerger.objects.create_nomad_merger(merge_groups,
#          new_location)

#         first_group.refresh_from_db()
#         fourth_group.refresh_from_db()
#         self.assertEqual(first_group.groups_merger, nomad_merger)
#         self.assertEqual(fourth_group.groups_merger, nomad_merger)

#         merge_records = piglets_events_models.NomadMergerRecord.objects.create_records(nomad_merger)
#         print(merge_records)
#         self.assertEqual(merge_records.first().quantity, 32)
#         self.assertEqual(merge_records.first().nomad_group, first_group)
#         print(merge_records.first().percentage)

#         print(merge_records[1])
#         self.assertEqual(merge_records[1].quantity, 7)
#         self.assertEqual(merge_records[1].nomad_group, fourth_group)
#         print(merge_records[1].percentage)

#         print(merge_records[0].nomad_group.location)
#         print(merge_records[0].nomad_group.location.get_location)
#         print(type(merge_records[0].nomad_group.location.get_location))

#         nomad_group = nomad_merger.create_nomad_group()
#         first_group.refresh_from_db()
#         fourth_group.refresh_from_db()
#         self.assertEqual(first_group.quantity, 0)
#         self.assertEqual(first_group.active, False)
#         self.assertEqual(fourth_group.quantity, 0)
#         self.assertEqual(fourth_group.active, False)

#         self.assertEqual(nomad_group.quantity, 39)
#         self.assertEqual(nomad_group.start_quantity, 39)
#         self.assertEqual(nomad_group.location.get_location, first_group.location.get_location)
#         self.assertEqual(nomad_group.creating_nomad_merger, nomad_merger)


# class RecountManagerTest(TestCase):
#     def setUp(self):
#         workshop_testing.create_workshops_sections_and_cells()
#         sows_testing.create_statuses()
#         piglets_testing.create_piglets_statuses()

#     def test_create_recount_nomad_group(self):
#         # quantity 37
#         nomad_group = piglets_testing.create_nomad_group_from_three_new_born()
#         recount = piglets_events_models.NomadPigletsGroupRecount.objects.create_recount(nomad_group, 35)
#         self.assertEqual(recount.quantity_before, 37)
#         self.assertEqual(recount.quantity_after, 35)
#         self.assertEqual(recount.balance, -2)

#     def test_create_recount_new_born_group(self):
#         # quantity 10
#         new_born_group = piglets_testing.create_new_born_group()
#         recount = piglets_events_models.NewBornPigletsGroupRecount.objects.create_recount(new_born_group, 8)
#         self.assertEqual(recount.quantity_before, 10)
#         self.assertEqual(recount.quantity_after, 8)
#         self.assertEqual(recount.balance, -2)