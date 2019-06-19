from mixer.backend.django import mixer
# from freezegun import freeze_time

from django.test import TestCase

import piglets_events.models as piglets_events_models
import piglets.models as piglets_models
import sows.models as sows_models
import tours.models as tour_models

import workshops.testing_utils as workshop_testing
import sows.testing_utils as sows_testing
import piglets.testing_utils as piglets_testing


class WeighingPigletsTest(TestCase):
    def setUp(self):
        workshop_testing.create_workshops_sections_and_cells()
        sows_testing.create_statuses()

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
        