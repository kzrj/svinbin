# -*- coding: utf-8 -*-
from rest_framework.test import APITestCase, APIClient

import locations.testing_utils as locations_testing
import sows.testing_utils as sows_testing
import piglets.testing_utils as piglets_testing
import staff.testing_utils as staff_testing


# class AuthViewSetTest(APITestCase):
#     def setUp(self):
#         self.client = APIClient()
#         locations_testing.create_workshops_sections_and_cells()
#         sows_testing.create_statuses()
#         piglets_testing.create_piglets_statuses()

#     def test_weighing_piglets(self):
#         user = staff_testing.create_workshop_user(
#             'test_user2', 'qwerty123', 1, True, True
#             )
#         response = self.client.post('/api/jwt/api-token-auth/', 
#             {"username": "test_user2", "password": "qwerty123"})
#         self.assertEqual(response.data['user']['workshop_number'], 1)
#           