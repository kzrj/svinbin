# -*- coding: utf-8 -*-
from datetime import datetime, timedelta, date
from freezegun import freeze_time

from django.test import TransactionTestCase
from django.db import models
from django.contrib.auth.models import User

import locations.testing_utils as locations_testing
import sows.testing_utils as sows_testing
import piglets.testing_utils as piglets_testing
import sows_events.utils as sows_events_testing
import staff.testing_utils as staff_testing

from sows.models import Sow
from locations.models import  Location, Section, WorkShop
from sows_events.models import SowFarrow, CullingSow
from piglets.models import Piglets
from piglets_events.models import CullingPiglets, Recount
from tours.models import Tour

from locations.serializers import (
    LocationCellSerializer, LocationSectionSerializer, SectionSerializer,
    LocationPigletsCellSerializer, LocationSowCellSerializer
    )


class LocationsTest(TransactionTestCase):
    def setUp(self):
        locations_testing.create_workshops_sections_and_cells()
        sows_testing.create_statuses()
        piglets_testing.create_piglets_statuses()
        sows_events_testing.create_types()

        self.ws3_cells = Location.objects.filter(sowAndPigletsCell__isnull=False)
        self.tour1 = Tour.objects.get_or_create_by_week_in_current_year(week_number=1)
        self.tour2 = Tour.objects.get_or_create_by_week_in_current_year(week_number=2)
        self.tour3 = Tour.objects.get_or_create_by_week_in_current_year(week_number=3)

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
        piglets_testing.create_new_group_with_metatour_by_one_tour(tour=self.tour1, location=location8,
         quantity=20)

        location9 = Location.objects.filter(pigletsGroupCell__isnull=False)[1]
        piglets_testing.create_new_group_with_metatour_by_one_tour(tour=self.tour1, location=location9,
         quantity=21)

        location10 = Location.objects.filter(pigletsGroupCell__section__number=2).first()        
        piglets_testing.create_new_group_with_metatour_by_one_tour(tour=self.tour1, location=location10,
         quantity=53)        

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

    def test_location_piglets_cell_serializer_queries(self):
        with self.assertNumQueries(3):
            data = Location.objects.all() \
                .select_related(
                    'pigletsGroupCell__section',
                    'sowAndPigletsCell__section',
                    ) \
                .prefetch_related(
                    'piglets__metatour__week_tour',
                    )
            serializer = LocationPigletsCellSerializer(data, many=True)
            serializer.data

    def test_location_sow_cell_serializer_queries(self):
        with self.assertNumQueries(4):
            data = Location.objects.all() \
                .filter(sowAndPigletsCell__isnull=False) \
                .select_related(
                    'sowAndPigletsCell__section',
                    ) \
                .prefetch_related(
                    'sow_set__tour',
                    'sow_set__status'
                    )
            serializer = LocationSowCellSerializer(data, many=True)
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
        self.piglets_cells = Location.objects.filter(pigletsGroupCell__isnull=False)

        tour1 = Tour.objects.get_or_create_by_week_in_current_year(1)

        self.sow1 = sows_testing.create_sow_with_location(location=self.ws3_cells[0])
        self.sow1.change_status_to('Супорос 35')

        self.sow2 = sows_testing.create_sow_with_location(location=self.ws3_cells[1])
        self.sow2.change_status_to('Супорос 35')

        self.sow3 = sows_testing.create_sow_with_location(location=self.ws3_cells[2])
        self.sow3.change_status_to('Супорос 35')

        self.sow4 = sows_testing.create_sow_with_location(location=self.ws3_cells[3])
        self.sow4.change_status_to('Опоросилась')

        self.sow5 = sows_testing.create_sow_with_location(location=self.ws3_cells[4])
        self.sow5.change_status_to('Кормилица')

        self.sow6 = sows_testing.create_sow_with_location(location=self.ws3_cells[50])
        self.sow6.change_status_to('Кормилица')

        self.piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(
            tour=tour1, location=self.ws3_cells[0], quantity=15,
            birthday=(datetime.today() - timedelta(days=1))
            )

        self.piglets2 = piglets_testing.create_new_group_with_metatour_by_one_tour(
            tour=tour1, location=self.ws3_cells[1], quantity=16,
            birthday=(datetime.today() - timedelta(days=5))
            )

        self.piglets3 = piglets_testing.create_new_group_with_metatour_by_one_tour(
            tour=tour1, location=self.ws3_cells[2], quantity=17,
            birthday=(datetime.today() - timedelta(days=8))
            )

        self.piglets4 = piglets_testing.create_new_group_with_metatour_by_one_tour(
            tour=tour1, location=self.ws3_cells[3], quantity=18,
            birthday=(datetime.today() - timedelta(days=20))
            )

        self.piglets5 = piglets_testing.create_new_group_with_metatour_by_one_tour(
            tour=tour1, location=self.ws3_cells[46], quantity=19,
            birthday=(datetime.today() - timedelta(days=30))
            )

    def test_add_sows_count_by_workshop(self):
        ws3 = Location.objects.filter(workshop__number=3) \
                .add_sows_count_by_workshop().first()

        self.assertEqual(ws3.sows_count, 6,)
        self.assertEqual(ws3.sows_sup_count, 3)
        self.assertEqual(ws3.sows_far_count, 1)
        self.assertEqual(ws3.sows_nurse_count, 2)

    def test_add_sows_count_by_sections(self):
        section_locs = Location.objects.filter(section__workshop__number=3,
             section__isnull=False).add_sows_count_by_sections()
        bool(section_locs)

        self.assertEqual(section_locs[0].sows_count, 5)
        self.assertEqual(section_locs[0].sows_sup_count, 3)

        self.assertEqual(section_locs[1].sows_count, 1)
        self.assertEqual(section_locs[1].sows_sup_count, 0)
    
    def test_add_pigs_count_by_workshop_by_age(self):
        today = datetime.today()
        ws3 = Location.objects.filter(workshop__number=3) \
                .add_pigs_count_by_workshop() \
                .add_pigs_count_by_workshop_by_age(date=today,
                     age_intervals=[[0, 7], [8, 14], [15, 21], [22, 28], [28, None]]) \
                .first()

        self.assertEqual(ws3.pigs_count, (15 + 16 + 17 + 18 + 19))
        self.assertEqual(ws3.count_piglets_0_7, (15 + 16))
        self.assertEqual(ws3.count_piglets_8_14, 17)
        self.assertEqual(ws3.count_piglets_15_21, 18)
        self.assertEqual(ws3.count_piglets_28_plus, 19)

    def test_add_pigs_count_by_workshop_by_age_concat_qs(self):
        today = datetime.today()
        ws3 = Location.objects.filter(workshop__number=3) \
                .add_pigs_count_by_workshop_by_age(date=today,
                     age_intervals=[[0, 7], [8, 14], [15, 21], [22, 28], [28, None]])

        ws4 = Location.objects.filter(workshop__number=4) \
                .add_pigs_count_by_workshop_by_age(date=today,
                     age_intervals=[[29, 39], [40, 50],])

        ws8 = Location.objects.filter(workshop__number=8) \
                .add_pigs_count_by_workshop_by_age(date=today,
                     age_intervals=[[60, 70], [80, 90],])

        ws34 = ws3 | ws4 | ws8
        ws34 = ws34.add_pigs_count_by_workshop()
        self.assertEqual(ws34[0].pigs_count, 85)
        self.assertEqual(ws34[1].pigs_count, None)
        self.assertEqual(ws34[0].count_piglets_0_7, 31)
        self.assertEqual(ws34[1].count_piglets_0_7, None)
        self.assertEqual(ws34[2].count_piglets_0_7, None)

    def test_add_pigs_count_by_ws_sections_by_age(self):
        today = datetime.today()
        section_locs = Location.objects.filter(section__workshop__number=3,
             section__isnull=False) \
                .add_pigs_count_by_sections() \
                .add_pigs_count_by_ws_sections_by_age(date=today,
                    age_intervals=[[0, 7], [8, 14], [15, 21], [22, 28], [28, None]])

        bool(section_locs)

        self.assertEqual(section_locs[0].pigs_count, (15 + 16 + 17 + 18))
        self.assertEqual(section_locs[0].count_piglets_0_7, (15 + 16))
        self.assertEqual(section_locs[0].count_piglets_8_14, 17)
        self.assertEqual(section_locs[0].count_piglets_15_21, 18)
        self.assertEqual(section_locs[0].count_piglets_28_plus, None)
        
        self.assertEqual(section_locs[1].pigs_count, 19)
        self.assertEqual(section_locs[1].count_piglets_0_7, None)
        self.assertEqual(section_locs[1].count_piglets_28_plus, 19)

    def test_add_section_fullness(self):
        tour1 = Tour.objects.get_or_create_by_week_in_current_year(1)
        piglets6 = piglets_testing.create_new_group_with_metatour_by_one_tour(
            tour=tour1, location=self.ws3_cells[47], quantity=19,
            birthday=(datetime.today() - timedelta(days=30))
            )
        piglets6.deactivate()

        piglets7 = piglets_testing.create_new_group_with_metatour_by_one_tour(
            tour=tour1, location=self.ws3_cells[47], quantity=19,
            birthday=(datetime.today() - timedelta(days=30))
            )
        piglets8 = piglets_testing.create_new_group_with_metatour_by_one_tour(
            tour=tour1, location=self.ws3_cells[47], quantity=19,
            birthday=(datetime.today() - timedelta(days=30))
            )

        section_locs = Location.objects.filter(section__workshop__number=3,
             section__isnull=False).add_section_fullness()

        self.assertEqual(section_locs[0].count_full, 4)
        self.assertEqual(section_locs[0].count_all, 45)
        self.assertEqual(section_locs[1].count_full, 2)

    def test_add_sows_culls_count(self):
        ws3 = Location.objects.filter(workshop__number=3).add_sows_culls_count()
        CullingSow.objects.create_culling(sow=self.sow1, culling_type='padej')
        print(ws3.first().count_sow_culls)


class LocationRecountsTest(TransactionTestCase):
    def setUp(self):
        locations_testing.create_workshops_sections_and_cells()
        piglets_testing.create_piglets_statuses()
        staff_testing.create_svinbin_users()

        self.brig8 = User.objects.get(username='brigadir8')
        self.admin = User.objects.get(username='test_admin1')
        self.shmigina = User.objects.get(username='shmigina')

        self.tour1 = Tour.objects.get_or_create_by_week_in_current_year(week_number=1)
        self.locs_ws3 = Location.objects.filter(sowAndPigletsCell__isnull=False)
        self.locs_ws5 = Location.objects.filter(pigletsGroupCell__workshop__number=5)

        self.piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.locs_ws3[0], 10)
        self.piglets2 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.locs_ws5[0], 100)

    def test_add_ws_recounts_balance_in_daterange(self):
        with freeze_time("2021-02-25"):
            Recount.objects.create_recount(piglets=self.piglets1, new_quantity=12)
            Recount.objects.create_recount(piglets=self.piglets2, new_quantity=105)

        date1 = date(2021,1,1)
        date2 = date(2021,2,28)

        wss = Location.objects.filter(workshop__number__in=[3,4,5,6,7,8]) \
                    .add_ws_recounts_balance_in_daterange(start_date=date1, end_date=date2)
        
        self.assertEqual(wss.get(workshop__number=3).recounts_balance_sum, -2)
        self.assertEqual(wss.get(workshop__number=3).recounts_balance_count, 1)
        self.assertEqual(wss.get(workshop__number=5).recounts_balance_sum, -5)
        self.assertEqual(wss.get(workshop__number=5).recounts_balance_count, 1)

        wss = Location.objects.filter(workshop__number__in=[3,4,5,6,7,8]) \
                    .add_ws_recounts_balance_in_daterange(start_date=date2)
        
        self.assertEqual(wss.get(workshop__number=3).recounts_balance_sum, None)
        self.assertEqual(wss.get(workshop__number=3).recounts_balance_count, 0)
        self.assertEqual(wss.get(workshop__number=5).recounts_balance_sum, None)
        self.assertEqual(wss.get(workshop__number=5).recounts_balance_count, 0)

        wss = Location.objects.filter(workshop__number__in=[3,4,5,6,7,8]) \
                    .add_ws_recounts_balance_in_daterange()
        
        self.assertEqual(wss.get(workshop__number=3).recounts_balance_sum, -2)
        self.assertEqual(wss.get(workshop__number=3).recounts_balance_count, 1)
        self.assertEqual(wss.get(workshop__number=5).recounts_balance_sum, -5)
        self.assertEqual(wss.get(workshop__number=5).recounts_balance_count, 1)
