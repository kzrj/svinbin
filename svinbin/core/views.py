# -*- coding: utf-8 -*-
from rest_framework import viewsets

import locations.testing_utils as locations_testing
import sows.testing_utils as sows_testing
import piglets.testing_utils as piglets_testing
import staff.testing_utils as staff_testing


class CreateWorkshopsView(viewsets.ViewSet):
    @action(methods=['get'], detail=False)
    def test_inits(self, request):
    	locations_testing.create_workshops_sections_and_cells()
    	sows_testing.create_statuses()
    	piglets_testing.create_piglets_statuses()
    	staff_testing.create_test_users()