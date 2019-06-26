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


class NewBornModelManagerTest(TestCase):
    def setUp(self):
        workshop_testing.create_workshops_sections_and_cells()
        sows_testing.create_statuses()

    def test_groups_with_gilts(self):
        new_born_group1 = piglets_testing.create_new_born_group(cell_number=5)
        sow1 = new_born_group1.farrows.first().sow
        gilt1 = sows_models.Gilt.objects.create_gilt(1, sow1)
        new_born_group1.refresh_from_db()
        
        new_born_group2 = piglets_testing.create_new_born_group(cell_number=6)
        sow2 = new_born_group2.farrows.first().sow
        gilt2 = sows_models.Gilt.objects.create_gilt(2, sow2)

        new_born_group3 = piglets_testing.create_new_born_group(cell_number=4)

        self.assertEqual(piglets_models.NewBornPigletsGroup.objects.groups_with_gilts().count(), 2)
        self.assertEqual(piglets_models.NewBornPigletsGroup.objects.all().count(), 3)

