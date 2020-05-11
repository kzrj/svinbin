# -*- coding: utf-8 -*-     
from rest_framework.test import APIClient
from rest_framework.test import APITestCase

import locations.testing_utils as locations_testing
import sows.testing_utils as sows_testing
import sows_events.utils as sows_events_testing
import staff.testing_utils as staff_testing
import piglets.testing_utils as piglets_testing

from locations.models import Location
from tours.models import Tour


class SowViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        locations_testing.create_workshops_sections_and_cells()
        sows_testing.create_statuses()
        sows_testing.create_boars()
        sows_events_testing.create_types()
        piglets_testing.create_piglets_statuses()
        self.user = staff_testing.create_employee()
        self.tour1 = Tour.objects.get_or_create_by_week_in_current_year(1)
        
    def test_handler_model_exception(self):
        self.client.force_authenticate(user=self.user)
        location = Location.objects.filter(sowAndPigletsCell__number=1).first()
        piglets = piglets_testing.create_from_sow_farrow(self.tour1, location)

        location2 = Location.objects.filter(sowAndPigletsCell__number=2).first()

        response = self.client.post('/api/piglets/%s/move_piglets/' % piglets.pk,
            {'to_location': location2.pk, 'merge': False, 'new_amount': 100})

        self.assertEqual('new_amount' in response.data['message'], True)
