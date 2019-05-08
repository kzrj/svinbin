from mixer.backend.django import mixer

from django.test import TestCase

import workshops.testing_utils as workshop_testing
import sows.testing_utils as sows_testings
from workshops.models import WorkShop, Section, SowSingleCell, PigletsGroupCell, SowGroupCell, \
SowAndPigletsCell
from sows.models import Sow


# class TestingUtilsTest(TestCase):
#     def setUp(self):
#         workshop_testing.create_workshops_sections_and_cells()

#     def test_create_sow_and_put_in_workshop_one(self):
#         sow = sows_testings.create_sow_and_put_in_workshop_one()
        # print(sow.pk, sow.location, sow.birth_id)
        # self.assertEqual(WorkShop.objects.all().count(), 10)
