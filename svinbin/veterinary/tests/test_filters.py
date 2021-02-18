# -*- coding: utf-8 -*-
import datetime

from django.test import TestCase

import locations.testing_utils as locations_testing
import sows.testing_utils as pigs_testings
import sows_events.utils as sows_events_testing
import piglets.testing_utils as piglets_testing

from veterinary.models import PigletsVetEvent, Drug, Recipe
from locations.models import Location, Section
from tours.models import Tour

from veterinary import filters


class PVEFiltersTest(TestCase):
    def setUp(self):
        locations_testing.create_workshops_sections_and_cells()
        pigs_testings.create_statuses()
        sows_events_testing.create_types()
        piglets_testing.create_piglets_statuses()

        self.tour1 = Tour.objects.get_or_create_by_week_in_current_year(week_number=1)
        self.tour2 = Tour.objects.get_or_create_by_week_in_current_year(week_number=2)
        self.tour3 = Tour.objects.get_or_create_by_week_in_current_year(week_number=3)

        self.drug = Drug.objects.create(name='test drug')
        self.recipe = Recipe.objects.create(drug=self.drug, med_type='vac', med_method='inj', doze=1)

        self.loc_ws4 = Location.objects.get(workshop__number=4)
        self.loc_ws4_cells = Location.objects.filter(pigletsGroupCell__workshop__number=4)
        self.loc_ws5_cells = Location.objects.filter(pigletsGroupCell__workshop__number=5)
        self.loc_ws3_cells = Location.objects.filter(sowAndPigletsCell__workshop__number=3)

        self.piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(
            tour=self.tour1,
            location=self.loc_ws3_cells[0],
            quantity=100,
            birthday=datetime.datetime(2020,5,5,0,0)
            )
        self.piglets2 = piglets_testing.create_new_group_with_metatour_by_one_tour(
            tour=self.tour2,
            location=self.loc_ws4_cells[0],
            quantity=100,
            birthday=datetime.datetime(2020,5,8,0,0)
            )
        self.piglets3 = piglets_testing.create_new_group_with_metatour_by_one_tour(
            tour=self.tour3,
            location=self.loc_ws5_cells[0],
            quantity=100,
            birthday=datetime.datetime(2020,5,8,0,0)
            )

    def test_sections_filter(self):
        pve1 = PigletsVetEvent.objects.create_vet_event(piglets=self.piglets1, recipe=self.recipe)
        pve2 = PigletsVetEvent.objects.create_vet_event(piglets=self.piglets2, recipe=self.recipe)
        pve3 = PigletsVetEvent.objects.create_vet_event(piglets=self.piglets3, recipe=self.recipe)

        qs = PigletsVetEvent.objects.all()
        sec3_1 = Section.objects.filter(workshop__number=3).first()
        sec4_1 = Section.objects.filter(workshop__number=4).first()
        sec5_1 = Section.objects.filter(workshop__number=5).first()

        f = filters.PigletsVetEventFilter(
            {'sections': f'{sec3_1.pk}, {sec4_1.pk}'}, queryset=qs)
        self.assertTrue(pve1.pk in f.qs.values_list('pk', flat=True))
        self.assertTrue(pve2.pk in f.qs.values_list('pk', flat=True))

        f = filters.PigletsVetEventFilter(
            {'sections': f'{sec5_1.pk}'}, queryset=qs)
        self.assertTrue(pve3.pk in f.qs.values_list('pk', flat=True))