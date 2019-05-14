from mixer.backend.django import mixer

from django.test import TestCase

import workshops.testing_utils as workshops_testing
import sows.testing_utils as sows_testing
from workshops.models import WorkShop, Section, SowSingleCell, PigletsGroupCell, SowGroupCell, \
SowAndPigletsCell
from sows.models import Sow
from transactions.models import Location, SowTransaction


class TestingUtilsTest(TestCase):
    def setUp(self):
        workshops_testing.create_workshops_sections_and_cells()

    def test_create_sow_and_put_in_workshop_one(self):
        sow = sows_testing.create_sow_and_put_in_workshop_one(1, '100')
        
        self.assertEqual(sow.location.sowSingleCell.number, '100')