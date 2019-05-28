from mixer.backend.django import mixer

from django.test import TestCase

import workshops.testing_utils as workshop_testing
import pigs.testing_utils as pigs_testings
from workshops.models import WorkShop, Section, SowSingleCell, PigletsGroupCell, SowGroupCell, \
SowAndPigletsCell
from pigs.models import Sow
from transactions.models import Location


class SowModelManagerTest(TestCase):
    def setUp(self):
        workshop_testing.create_workshops_sections_and_cells()

    def test_create_new_from_gilt(self):
        # add test
        pass

    def test_get_or_create_by_farm_id(self):
        for count_sow in range(1, 100):
            location = Location.objects.create_location(pre_location=WorkShop.objects.get(number=1))
            Sow.objects.create(farm_id=count_sow, location=location)
        for count_sow in range(1, 100):
            location = Location.objects.create_location(pre_location=WorkShop.objects.get(number=1))
            Sow.objects.create(location=location)

        Sow.objects.get_or_create_by_farm_id(1)
        self.assertEqual(Sow.objects.all().count(), 198)

        Sow.objects.get_or_create_by_farm_id(120)
        self.assertEqual(Sow.objects.all().count(), 199)        
        self.assertEqual(Sow.objects.filter(farm_id=120).count(), 1)