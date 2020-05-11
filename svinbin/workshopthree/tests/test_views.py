# -*- coding: utf-8 -*-
from rest_framework.test import APIClient
from rest_framework.test import APITestCase

import locations.testing_utils as locations_testing
import sows.testing_utils as sows_testing
import sows_events.utils as sows_events_testings
import piglets.testing_utils as piglets_testing
import staff.testing_utils as staff_testing

from sows.models import Gilt
from sows_events.models import SowFarrow
from locations.models import WorkShop, SowAndPigletsCell, Location
from transactions.models import PigletsTransaction, SowTransaction
from tours.models import Tour


class WorkshopThreeSowsViewSetTest(APITestCase):
    def setUp(self):
        locations_testing.create_workshops_sections_and_cells()
        sows_testing.create_statuses()
        sows_events_testings.create_types()
        piglets_testing.create_piglets_statuses()
        self.client = APIClient()
        self.user = staff_testing.create_employee()
        self.client.force_authenticate(user=self.user)

    def test_sow_farrow(self):
        sow = sows_testing.create_sow_seminated_usouded_ws3_section(section_number=1, week=7)
        location = Location.objects.filter(sowAndPigletsCell__isnull=False).first()
        sow.change_sow_current_location(location)
        response = self.client.post('/api/workshopthree/sows/%s/sow_farrow/' %
          sow.pk, {'alive_quantity': 10, 'dead_quantity': 1, 'mummy_quantity': 2, 'week': 7 })

        self.assertEqual(response.data['sow']['id'], sow.pk)
        self.assertEqual(response.data['sow']['farm_id'], sow.farm_id)
        self.assertEqual(response.data['sow']['tour'], 'Тур 7 2020г')
        self.assertEqual(response.data['sow']['status'], 'Опоросилась')
        self.assertEqual(response.data['farrow']['alive_quantity'], 10)
        self.assertEqual(response.data['farrow']['dead_quantity'], 1)
        self.assertEqual(response.data['farrow']['mummy_quantity'], 2)

    def test_mark_as_nurse_without_creating_piglets(self):
        sow = sows_testing.create_sow_seminated_usouded_ws3_section(section_number=1, week=7)
        location = Location.objects.filter(sowAndPigletsCell__isnull=False).first()
        sow.change_sow_current_location(location)
        SowFarrow.objects.create_sow_farrow(sow=sow, alive_quantity=10)
        response = self.client.post('/api/workshopthree/sows/%s/mark_as_nurse/' % sow.pk)
        sow.refresh_from_db()
        self.assertEqual(sow.status.title, 'Кормилица')
        self.assertEqual(response.data['message'], 'Свинья помечена как кормилица.')