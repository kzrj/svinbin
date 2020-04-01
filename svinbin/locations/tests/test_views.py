# -*- coding: utf-8 -*-
from rest_framework.test import APIClient
from rest_framework.test import APITestCase

import locations.testing_utils as locations_testing
import sows.testing_utils as sows_testing
import piglets.testing_utils as piglets_testing
import staff.testing_utils as staff_testing
import sows_events.utils as sows_events_testing

from piglets.models import Piglets
from locations.models import Location
from tours.models import Tour
from sows_events.models import SowFarrow


class LocationsViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        locations_testing.create_workshops_sections_and_cells()
        sows_testing.create_statuses()
        sows_events_testing.create_types()
        piglets_testing.create_piglets_statuses()
        self.user = staff_testing.create_employee()
        self.client.force_authenticate(user=self.user)

        self.tour1 = Tour.objects.get_or_create_by_week_in_current_year(week_number=1)
        self.tour2 = Tour.objects.get_or_create_by_week_in_current_year(week_number=2)
        self.tour3 = Tour.objects.get_or_create_by_week_in_current_year(week_number=3)
        self.loc_ws3 = Location.objects.get(workshop__number=3)
        self.piglets = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws3, 101)

        location1 = Location.objects.filter(sowAndPigletsCell__number=1).first()
        sow1 = sows_testing.create_sow_with_semination_usound(location=location1, week=1)

        location2 = Location.objects.filter(sowAndPigletsCell__number=2).first()
        sow2 = sows_testing.create_sow_with_semination_usound(location=location2, week=1)

        location3 = Location.objects.filter(sowAndPigletsCell__number=3).first()
        sow3 = sows_testing.create_sow_with_semination_usound(location=location3, week=1)

        SowFarrow.objects.create_sow_farrow(sow=sow1, alive_quantity=10)
        SowFarrow.objects.create_sow_farrow(sow=sow2, alive_quantity=10)
        SowFarrow.objects.create_sow_farrow(sow=sow3, alive_quantity=10)

        location8 = Location.objects.filter(pigletsGroupCell__isnull=False).first()
        Piglets.objects.init_piglets_by_farrow_date('2020-01-01', location8, 20)

        location9 = Location.objects.filter(pigletsGroupCell__isnull=False)[1]
        Piglets.objects.init_piglets_by_farrow_date('2020-01-02', location9, 21)

        location10 = Location.objects.filter(pigletsGroupCell__section__number=2).first()
        Piglets.objects.init_piglets_by_farrow_date('2020-01-02', location10, 53)

    def test_common_list_locations(self):
        response = self.client.get('/api/locations/')
        location = response.data['results'][0]
        self.assertNotEqual(location.get('workshop', False), False)

    def test_cells_list_locations(self):
        section = Location.objects.filter(section__number=1, section__workshop__number=3).first()
        response = self.client.get(f'/api/locations/?by_section={section.section.pk}&cells=true')
        self.assertEqual(len(response.data['results']) > 0, True)

    def test_sections_list_locations(self):
        workshop = Location.objects.filter(workshop__number=4).first()
        response = self.client.get(f'/api/locations/?sections_by_workshop_number={workshop.workshop.number}&sections=true')
        self.assertEqual(len(response.data['results']) > 0, True)

        section = response.data['results'][0]
        self.assertEqual(section['pigs_count'], 41)
