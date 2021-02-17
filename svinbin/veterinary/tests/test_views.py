# -*- coding: utf-8 -*-
import datetime

from django.contrib.auth.models import User

from rest_framework.test import APIClient
from rest_framework.test import APITestCase

import locations.testing_utils as locations_testing
import sows.testing_utils as sows_testing
import piglets.testing_utils as piglets_testing
import staff.testing_utils as staff_testing

from piglets.models import Piglets
from locations.models import Location
from tours.models import Tour
from veterinary.models import PigletsVetEvent, Recipe, Drug


class RecipeDrugsViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        locations_testing.create_workshops_sections_and_cells()
        sows_testing.create_statuses()
        piglets_testing.create_piglets_statuses()
        staff_testing.create_svinbin_users()

        self.tour1 = Tour.objects.get_or_create_by_week_in_current_year(week_number=1)
        self.tour2 = Tour.objects.get_or_create_by_week_in_current_year(week_number=2)
        self.tour3 = Tour.objects.get_or_create_by_week_in_current_year(week_number=3)
        self.tour4 = Tour.objects.get_or_create_by_week_in_current_year(week_number=4)
        self.loc_ws3 = Location.objects.get(workshop__number=3)
        self.loc_ws3_sec1 = Location.objects.get(section__workshop__number=3, section__number=1)
        self.loc_ws3_sec2 = Location.objects.get(section__workshop__number=3, section__number=2)

        self.loc_ws4 = Location.objects.get(workshop__number=4)
        self.loc_ws4_cell1 = Location.objects.filter(pigletsGroupCell__isnull=False)[0]
        self.loc_ws4_cell2 = Location.objects.filter(pigletsGroupCell__isnull=False)[1]

        self.veterinar = User.objects.get(username='veterinar')
        self.brig3 = User.objects.get(username='brigadir3')
        self.operator = User.objects.get(username='shmigina')

    def test_create_drug_recipe(self):
        self.client.force_authenticate(user=self.veterinar)
        response = self.client.post(f'/api/veterinary/drugs/', 
            data={'name': 'Пеницилин'})
        self.assertEqual(response.status_code, 201)

        drug = Drug.objects.all().first()
        response = self.client.post(f'/api/veterinary/recipes/', 
            data={'med_type': 'vac', 'med_method': 'inj', 'drug': drug.pk, })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['doze'], None)

        recipe = Recipe.objects.all().first()
        response = self.client.patch(f'/api/veterinary/recipes/{recipe.pk}/', 
            data={'med_type': 'vac', 'med_method': 'inj', 'doze': 1})
        self.assertEqual(response.data['doze'], '1')

        response = self.client.delete(f'/api/veterinary/recipes/{recipe.pk}/')
        self.assertEqual(response.status_code, 200)

        self.client.logout()

    def test_permissions(self):
        response = self.client.post(f'/api/veterinary/drugs/', 
            data={'name': 'Пеницилин'})
        self.assertEqual(response.status_code, 401)

        self.client.force_authenticate(user=self.brig3)
        response = self.client.post(f'/api/veterinary/drugs/', 
            data={'name': 'Пеницилин'})
        self.assertEqual(response.status_code, 403)

        response = self.client.patch(f'/api/veterinary/drugs/1/', 
            data={'name': 'Пеницилин'})
        self.assertEqual(response.status_code, 403)

        response = self.client.delete(f'/api/veterinary/drugs/1/', 
            data={'name': 'Пеницилин'})
        self.assertEqual(response.status_code, 403)
        self.client.logout()

