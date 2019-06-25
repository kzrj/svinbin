from mixer.backend.django import mixer
# from freezegun import freeze_time

from django.test import TestCase

import piglets_events.models as piglets_events_models
import piglets.models as piglets_models
import sows.models as sows_models
import tours.models as tour_models
import transactions.models as transactions_models
import workshops.models as workshops_models

import workshops.testing_utils as workshop_testing
import sows.testing_utils as sows_testing
import piglets.testing_utils as piglets_testing


class WeighingPigletsTest(TestCase):
    def setUp(self):
        workshop_testing.create_workshops_sections_and_cells()
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


class NomadPigletsGroupMergerTest(TestCase):
    def setUp(self):
        workshop_testing.create_workshops_sections_and_cells()
        sows_testing.create_statuses()
        piglets_testing.create_piglets_statuses()

    def test_create_merger_and_return_nomad_piglets_group(self):
        piglets_group1 = piglets_testing.create_nomad_group_from_three_new_born()
        piglets_group2 = piglets_testing.create_nomad_group_from_three_new_born()

        cell = workshops_models.PigletsGroupCell.objects.get(workshop__number=4,
             section__number=1, number=1)
        new_location = transactions_models.Location.objects.create_location(cell)

        merged_group = piglets_events_models.NomadPigletsGroupMerger.objects \
            .create_merger_and_return_nomad_piglets_group(
                nomad_groups=[piglets_group1, piglets_group2],
                new_location=new_location
                )

        self.assertEqual(merged_group.location, new_location)
        self.assertEqual(merged_group.location.get_location, cell)
        self.assertEqual(merged_group.quantity, piglets_group1.start_quantity 
            + piglets_group2.start_quantity)
        
        piglets_group1.refresh_from_db()
        piglets_group2.refresh_from_db()
        self.assertEqual(piglets_group1.active, False)
        self.assertEqual(piglets_group2.active, False)
        self.assertEqual(piglets_group1.quantity, 0)
        self.assertEqual(piglets_group2.quantity, 0)
        

class SplitNomadPigletsGroupTest(TestCase):
    def setUp(self):
        workshop_testing.create_workshops_sections_and_cells()
        sows_testing.create_statuses()
        piglets_testing.create_piglets_statuses()

    def test_split_group(self):
        parent_piglets_group = piglets_testing.create_nomad_group_from_three_new_born()
        self.assertEqual(parent_piglets_group.location.get_location.number, 3)
        self.assertEqual(parent_piglets_group.quantity, 37)

        first_group, second_group = piglets_events_models.SplitNomadPigletsGroup \
            .objects.split_group(parent_piglets_group, 10)

        self.assertEqual(first_group.quantity, 27)
        self.assertEqual(second_group.quantity, 10)
        self.assertEqual(first_group.location.get_location.number, 3)
        self.assertEqual(second_group.location.get_location.number, 3)
        self.assertEqual(first_group.status, parent_piglets_group.status)
        self.assertEqual(second_group.status, parent_piglets_group.status)
        self.assertEqual(first_group.active, True)
        self.assertEqual(second_group.active, True)
        self.assertEqual(parent_piglets_group.quantity, 0)
        self.assertEqual(parent_piglets_group.active, False)
        self.assertEqual(first_group.split_record, parent_piglets_group.split_event)
        