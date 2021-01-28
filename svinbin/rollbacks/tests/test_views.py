# -*- coding: utf-8 -*-
from datetime import datetime

from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User

import locations.testing_utils as locations_testing
import sows.testing_utils as sows_testing
import sows_events.utils as sows_events_testing
import piglets.testing_utils as piglets_testing
import staff.testing_utils as staff_testing

from rollbacks.models import Rollback
from locations.models import Location
from tours.models import Tour, MetaTour
from piglets_events.models import WeighingPiglets, CullingPiglets


class ReportDateViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = staff_testing.create_employee()
        self.client.force_authenticate(user=self.user)

        locations_testing.create_workshops_sections_and_cells()
        sows_testing.create_statuses()
        sows_events_testing.create_types()
        piglets_testing.create_piglets_statuses()
        staff_testing.create_svinbin_users()

        self.tour1 = Tour.objects.get_or_create_by_week_in_current_year(week_number=1)
        self.tour2 = Tour.objects.get_or_create_by_week_in_current_year(week_number=2)

        self.locs_ws3 = Location.objects.filter(sowAndPigletsCell__workshop__number=3)
        self.locs_ws4 = Location.objects.filter(pigletsGroupCell__workshop__number=4)
        self.locs_ws5 = Location.objects.filter(pigletsGroupCell__workshop__number=5)

        self.brig3 = User.objects.get(username='brigadir3')
        self.brig4 = User.objects.get(username='brigadir4')
        self.brig5 = User.objects.get(username='brigadir5')
        self.operator = User.objects.get(username='shmigina')

    def test_weighing_piglets_rollback(self):
        piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.locs_ws4[0], 10)

        operation = WeighingPiglets.objects.create_weighing(piglets_group=piglets1, total_weight=100,
            place='3/4', initiator=self.brig4, date=datetime(10,10,20))

        piglets1.refresh_from_db()
        self.assertEqual(piglets1.status.title, 'Взвешены, готовы к заселению')

        self.client.force_authenticate(self.operator)
        response = self.client.post('/api/rollbacks/', {'operation_name': 'piglets_weighing',
            'event_pk': operation.pk, 'operation_name': 'ws3_weighing'})

        self.assertEqual(response.data['message'], 'Операция отменена.')

        piglets1.refresh_from_db()
        self.assertEqual(piglets1.status.title, 'Готовы ко взвешиванию')
        self.assertEqual(WeighingPiglets.objects.all().count(), 0)
        self.client.logout()

    def test_rollback_permissions(self):
        piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.locs_ws4[0], 10)

        operation = WeighingPiglets.objects.create_weighing(piglets_group=piglets1, total_weight=100,
            place='3/4', initiator=self.brig4, date=datetime(10,10,20))
        
        self.client.force_authenticate(self.brig4)
        response = self.client.post('/api/rollbacks/', {'operation_name': 'piglets_weighing',
            'event_pk': operation.pk, 'operation_name': 'ws3_weighing'})

        self.assertEqual(response.status_code, 403)
