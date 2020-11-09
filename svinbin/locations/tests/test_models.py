# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from django.test import TransactionTestCase
from django.db import models

import locations.testing_utils as locations_testing
import sows.testing_utils as sows_testing
import piglets.testing_utils as piglets_testing
import sows_events.utils as sows_events_testing

from locations.models import  Location, Section
from sows_events.models import SowFarrow
from piglets.models import Piglets
from tours.models import Tour

from locations.serializers import (
    LocationCellSerializer, LocationSectionSerializer, SectionSerializer
    )


class LocationsTest(TransactionTestCase):
    def setUp(self):
        locations_testing.create_workshops_sections_and_cells()
        sows_testing.create_statuses()
        piglets_testing.create_piglets_statuses()
        sows_events_testing.create_types()

        self.ws3_cells = Location.objects.filter(sowAndPigletsCell__isnull=False)

        location1 = Location.objects.filter(sowAndPigletsCell__number=1).first()
        sow1 = sows_testing.create_sow_with_semination_usound(location=location1, week=1)
        location2 = Location.objects.filter(sowAndPigletsCell__number=2).first()
        sow2 = sows_testing.create_sow_with_semination_usound(location=location2, week=1)
        location3 = Location.objects.filter(sowAndPigletsCell__number=3).first()
        sow3 = sows_testing.create_sow_with_semination_usound(location=location3, week=2)
        location4 = Location.objects.filter(sowAndPigletsCell__number=4).first()
        sow4 = sows_testing.create_sow_with_semination_usound(location=location4, week=2)
        location5 = Location.objects.filter(sowAndPigletsCell__number=5).first()
        sow5 = sows_testing.create_sow_with_semination_usound(location=location5, week=3)
        location6 = Location.objects.filter(sowAndPigletsCell__number=6).first()
        sow6 = sows_testing.create_sow_with_semination_usound(location=location6, week=4)
        location7 = Location.objects.filter(sowAndPigletsCell__number=7).first()
        sow7 = sows_testing.create_sow_with_semination_usound(location=location7, week=5)

        SowFarrow.objects.create_sow_farrow(sow=sow1, alive_quantity=10)
        SowFarrow.objects.create_sow_farrow(sow=sow2, alive_quantity=10)
        SowFarrow.objects.create_sow_farrow(sow=sow3, alive_quantity=10)
        SowFarrow.objects.create_sow_farrow(sow=sow4, alive_quantity=10)
        SowFarrow.objects.create_sow_farrow(sow=sow5, alive_quantity=10)
        SowFarrow.objects.create_sow_farrow(sow=sow6, alive_quantity=10)
        SowFarrow.objects.create_sow_farrow(sow=sow7, alive_quantity=10)
 
        piglets3_7= location7.piglets.all().first()
        piglets3_7.deactivate()

        location8 = Location.objects.filter(pigletsGroupCell__isnull=False).first()
        Piglets.objects.init_piglets_by_farrow_date('2020-01-01', location8, 20)

        location9 = Location.objects.filter(pigletsGroupCell__isnull=False)[1]
        Piglets.objects.init_piglets_by_farrow_date('2020-01-02', location9, 21)

        location10 = Location.objects.filter(pigletsGroupCell__section__number=2).first()
        Piglets.objects.init_piglets_by_farrow_date('2020-01-02', location10, 53)

    def test_location_cell_serializer_queries(self):
        with self.assertNumQueries(6):
            data = Location.objects.all() \
                .select_related(
                    'pigletsGroupCell__section',
                    'sowAndPigletsCell__section',
                    'sowSingleCell__section',
                    'sowGroupCell__section',
                    ) \
                .prefetch_related(
                    'sow_set__tour',
                    'sow_set__status',
                    'piglets__metatour__week_tour',
                    )
            serializer = LocationCellSerializer(data, many=True)
            serializer.data

    def test_location_section_serializer_queries(self):
        with self.assertNumQueries(1):
            data = Location.objects.all() \
                .select_related(
                    'section__workshop',
                    ) 
            serializer = LocationSectionSerializer(data, many=True)
            serializer.data

    def test_section_serializer_queries(self):
        with self.assertNumQueries(1):
            data = Section.objects.all() \
                .select_related(
                    'location',
                    ) 
            serializer = SectionSerializer(data, many=True)
            serializer.data

    def test_add_sows_count_by_sections(self):
        location8 = Location.objects.filter(sowAndPigletsCell__number=8).first()
        sow8 = sows_testing.create_sow_with_semination_usound(location=location8, week=5)

        location9 = Location.objects.filter(sowAndPigletsCell__number=9).first()
        sow9 = sows_testing.create_sow_with_semination_usound(location=location9, week=5)
        sow9.alive = False
        sow9.save()

        with self.assertNumQueries(1):
            locs = Location.objects \
                .filter(section__workshop__number=3, section__isnull=False) \
                .add_sows_count_by_sections() 

            bool(locs)
            self.assertEqual(locs[0].sows_count, 8)

    def test_gen_sections_pigs_count_dict(self):
        with self.assertNumQueries(2):
            data = Location.objects.all().gen_sections_pigs_count_dict()
            bool(data)
            # 70p-10p from farrows + 94p from inits + 7s = 161
            self.assertEqual(data['ws_total'], 161)

    def test_add_pigs_count_by_sections(self):

        with self.assertNumQueries(1):
            locs = Location.objects \
                .filter(section__workshop__number=3, section__isnull=False) \
                .add_pigs_count_by_sections() 

            bool(locs)
            self.assertEqual(locs[0].pigs_count, 60)


class LocationQsPopulationTest(TransactionTestCase):
    def setUp(self):
        locations_testing.create_workshops_sections_and_cells()
        sows_testing.create_statuses()
        piglets_testing.create_piglets_statuses()
        sows_events_testing.create_types()

        self.ws3_cells = Location.objects.filter(sowAndPigletsCell__isnull=False)

        tour1 = Tour.objects.get_or_create_by_week_in_current_year(1)

        sow1 = sows_testing.create_sow_with_location(location=self.ws3_cells[0])
        sow1.change_status_to('Супорос 35')

        sow2 = sows_testing.create_sow_with_location(location=self.ws3_cells[1])
        sow2.change_status_to('Супорос 35')

        sow3 = sows_testing.create_sow_with_location(location=self.ws3_cells[2])
        sow3.change_status_to('Супорос 35')

        sow4 = sows_testing.create_sow_with_location(location=self.ws3_cells[3])
        sow4.change_status_to('Опоросилась')

        sow5 = sows_testing.create_sow_with_location(location=self.ws3_cells[4])
        sow5.change_status_to('Кормилица')

        sow6 = sows_testing.create_sow_with_location(location=self.ws3_cells[50])
        sow6.change_status_to('Кормилица')

        piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(
            tour=tour1, location=self.ws3_cells[0], quantity=15,
            gilts_quantity=0,
            birthday=(datetime.today() - timedelta(days=1))
            )

        piglets2 = piglets_testing.create_new_group_with_metatour_by_one_tour(
            tour=tour1, location=self.ws3_cells[1], quantity=16,
            gilts_quantity=5,
            birthday=(datetime.today() - timedelta(days=5))
            )

        piglets3 = piglets_testing.create_new_group_with_metatour_by_one_tour(
            tour=tour1, location=self.ws3_cells[2], quantity=17,
            gilts_quantity=5,
            birthday=(datetime.today() - timedelta(days=8))
            )

        piglets4 = piglets_testing.create_new_group_with_metatour_by_one_tour(
            tour=tour1, location=self.ws3_cells[3], quantity=18,
            gilts_quantity=0,
            birthday=(datetime.today() - timedelta(days=20))
            )

        piglets5 = piglets_testing.create_new_group_with_metatour_by_one_tour(
            tour=tour1, location=self.ws3_cells[46], quantity=19,
            gilts_quantity=6,
            birthday=(datetime.today() - timedelta(days=30))
            )

    def test_add_sows_count_by_workshop(self):
        ws3 = Location.objects.filter(workshop__number=3) \
                .add_sows_count_by_workshop().first()

        self.assertEqual(ws3.sows_count, 6,)
        self.assertEqual(ws3.sows_sup_count, 3)

    def test_add_sows_count_by_sections(self):
        section_locs = Location.objects.filter(section__workshop__number=3,
             section__isnull=False).add_sows_count_by_sections()
        bool(section_locs)

        self.assertEqual(section_locs[0].sows_count, 5)
        self.assertEqual(section_locs[0].sows_sup_count, 3)

        self.assertEqual(section_locs[1].sows_count, 1)
        self.assertEqual(section_locs[1].sows_sup_count, 0)
    
    def test_add_pigs_count_by_workshop3_by_age(self):
        today = datetime.today()
        ws3 = Location.objects.filter(workshop__number=3) \
                .add_pigs_count_by_workshop() \
                .add_pigs_count_by_workshop3_by_age(date=today) \
                .first()

        self.assertEqual(ws3.pigs_count, (15 + 16 + 17 + 18 + 19))
        self.assertEqual(ws3.count_piglets_0_7, (15 + 16))
        self.assertEqual(ws3.count_piglets_8_14, 17)
        self.assertEqual(ws3.count_piglets_15_21, 18)
        self.assertEqual(ws3.count_piglets_28_plus, 19)

        self.assertEqual(ws3.gilts_count, (5 + 5 + 6))

    def test_add_pigs_count_by_ws3_sections_by_age(self):
        today = datetime.today()
        section_locs = Location.objects.filter(section__workshop__number=3,
             section__isnull=False) \
                .add_pigs_count_by_sections() \
                .add_pigs_count_by_ws3_sections_by_age(date=today)

        bool(section_locs)

        self.assertEqual(section_locs[0].pigs_count, (15 + 16 + 17 + 18))
        self.assertEqual(section_locs[0].count_piglets_0_7, (15 + 16))
        self.assertEqual(section_locs[0].count_piglets_8_14, 17)
        self.assertEqual(section_locs[0].count_piglets_15_21, 18)
        self.assertEqual(section_locs[0].count_piglets_28_plus, None)
        self.assertEqual(section_locs[0].gilts_count, (5 + 5))
        
        self.assertEqual(section_locs[1].pigs_count, 19)
        self.assertEqual(section_locs[1].count_piglets_0_7, None)
        self.assertEqual(section_locs[1].count_piglets_28_plus, 19)
        self.assertEqual(section_locs[1].gilts_count, 6)