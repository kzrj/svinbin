# -*- coding: utf-8 -*-
from rest_framework.test import APIClient
from rest_framework.test import APITestCase

import locations.testing_utils as locations_testing
import sows.testing_utils as sows_testing
import piglets.testing_utils as piglets_testing
import staff.testing_utils as staff_testing

from piglets.models import Piglets
from locations.models import Location
from tours.models import Tour


class LocationsViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        locations_testing.create_workshops_sections_and_cells()
        sows_testing.create_statuses()
        piglets_testing.create_piglets_statuses()
        self.user = staff_testing.create_employee()
        self.client.force_authenticate(user=self.user)

        self.tour1 = Tour.objects.get_or_create_by_week_in_current_year(week_number=1)
        self.tour2 = Tour.objects.get_or_create_by_week_in_current_year(week_number=2)
        self.tour3 = Tour.objects.get_or_create_by_week_in_current_year(week_number=3)
        self.loc_ws3 = Location.objects.get(workshop__number=3)
        self.piglets = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws3, 101)

    def test_location(self):
        response = self.client.get('/api/locations/')
        self.assertEqual(response.data['results'][2]['piglets'][0]['id'], self.piglets.pk)

    def test_filter_sections_by_workshop_number(self):
        sows_testings.create_sow_seminated_usouded_ws3_section(1, 1)
        sows_testings.create_sow_seminated_usouded_ws3_section(1, 1)
        sows_testings.create_sow_seminated_usouded_ws3_section(1, 2)
        sows_testings.create_sow_seminated_usouded_ws3_section(2, 1)
        sows_testings.create_sow_seminated_usouded_ws3_section(2, 2)
        sows_testings.create_sow_seminated_usouded_ws3_section(3, 1)
        sows_testings.create_sow_seminated_usouded_ws3_section(3, 1)
        sows_testings.create_sow_seminated_usouded_ws3_section(3, 1)

        response = self.client.get('/api/locations/?sections_by_workshop_number=3')
        print(response.data)
        # for location_section in response.data['results']:
            # location_section.se



        
        

# class SectionsViewSetTest(APITestCase):
#     def setUp(self):
#         self.client = APIClient()
#         locations_testing.create_workshops_sections_and_cells()
#         sows_testing.create_statuses()
#         piglets_testing.create_piglets_statuses()
#         self.user = staff_testing.create_employee()
#         self.client.force_authenticate(user=self.user)

#         self.tour1 = Tour.objects.get_or_create_by_week_in_current_year(week_number=1)
#         self.loc_ws3 = Location.objects.get(workshop__number=3)
#         self.piglets = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
#             self.loc_ws3, 101)

#     def test_sections(self):
#         response = self.client.get('/api/sections/?sections_by_workshop_number=3')
#         print(response.data)
        # self.assertEqual(response.data['results'][2]['piglets'][0]['id'], self.piglets.pk)