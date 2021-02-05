# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from django.test import TestCase, TransactionTestCase
from django.core.exceptions import ValidationError

from piglets.models import Piglets
from piglets_events.models import PigletsMerger, CullingPiglets, WeighingPiglets
from tours.models import Tour
from locations.models import Location

from piglets.serializers import PigletsSerializer, PigletsSimpleSerializer

import locations.testing_utils as locations_testing
import piglets.testing_utils as piglets_testing
import sows.testing_utils as sows_testings
import sows_events.utils as sows_events_testings


class PigletsModelTest(TestCase):
    def setUp(self):
        locations_testing.create_workshops_sections_and_cells()
        piglets_testing.create_piglets_statuses()

        self.tour1 = Tour.objects.get_or_create_by_week_in_current_year(week_number=1)
        self.tour2 = Tour.objects.get_or_create_by_week_in_current_year(week_number=2)
        self.loc_ws3 = Location.objects.get(workshop__number=3)
        self.piglets = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws3, 101)
        self.piglets.gilts_quantity = 10
        self.piglets.save()

        self.piglets2 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour2,
            self.loc_ws3, 232)

    def test_deactivate(self):
        self.piglets.deactivate()
        self.assertEqual(self.piglets.active, False)

    def test_remove_piglets(self):
        self.piglets.remove_piglets(1)
        self.assertEqual(self.piglets.quantity, 100)

    def test_remove_gilts(self):
        self.piglets.remove_gilts(1)
        self.assertEqual(self.piglets.quantity, 100)
        self.assertEqual(self.piglets.gilts_quantity, 9)

    def test_change_status_to(self):
        self.piglets.change_status_to('Родились, кормятся')
        self.assertEqual(self.piglets.status.title, 'Родились, кормятся')

    def test_has_weighed_after_date(self):
        weighing = WeighingPiglets.objects.create_weighing(piglets_group=self.piglets, total_weight=100,
         place='3/4', date=datetime(2021, 2, 3, 0, 0))

        self.assertEqual(self.piglets.has_weighed_after_date(date=datetime(2021, 2, 3, 0, 1)), False)
        self.assertEqual(self.piglets.has_weighed_after_date(date=datetime(2021, 2, 3, 0, 0)), True)


class PigletsModelmanagerTest(TestCase):
    def setUp(self):
        locations_testing.create_workshops_sections_and_cells()
        piglets_testing.create_piglets_statuses()

        self.tour1 = Tour.objects.get_or_create_by_week_in_current_year(week_number=1)
        self.tour2 = Tour.objects.get_or_create_by_week_in_current_year(week_number=2)
        self.loc_ws3 = Location.objects.get(workshop__number=3)
        self.piglets = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws3, 101)
        self.piglets.gilts_quantity = 10
        self.piglets.save()

        self.piglets2 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour2,
            self.loc_ws3, 232)
        
    def test_manager_get_total_quantity(self):
        total = Piglets.objects.all().get_total_quantity()
        self.assertEqual(total, 333)

    def test_manager_get_total_gilts_quantity(self):
        total_gilts = Piglets.objects.all().get_total_gilts_quantity()
        self.assertEqual(total_gilts, 10)

    def test_init_piglets_by_farrow_date(self):
        piglets = Piglets.objects.init_piglets_by_farrow_date(farrow_date='2019-12-31', location=self.loc_ws3,
         quantity=100, gilts_quantity=10)
        self.assertEqual(piglets.quantity, 100)
        self.assertEqual(piglets.gilts_quantity, 10)        
        self.assertEqual(piglets.metatour.records.all().first().tour.week_number, 33)


class PigletsQueryTest(TransactionTestCase):
    def setUp(self):
        locations_testing.create_workshops_sections_and_cells()
        sows_testings.create_statuses()
        sows_events_testings.create_types()
        piglets_testing.create_piglets_statuses()

        location_cell1 = Location.objects.filter(sowAndPigletsCell__section__number=1)[0]
        piglets1 = piglets_testing.create_from_sow_farrow_by_week(location=location_cell1,
            week=1)

        location_cell2 = Location.objects.filter(sowAndPigletsCell__section__number=1)[1]
        piglets2 = piglets_testing.create_from_sow_farrow_by_week(location=location_cell2,
            week=1)

        location_cell3 = Location.objects.filter(sowAndPigletsCell__section__number=1)[2]
        piglets3 = piglets_testing.create_from_sow_farrow_by_week(location=location_cell3,
            week=2)

        self.tour1 = Tour.objects.get_or_create_by_week_in_current_year(week_number=1)
        self.tour2 = Tour.objects.get_or_create_by_week_in_current_year(week_number=2)

        self.loc_ws4 = Location.objects.get(workshop__number=4)
        # piglets in ws
        piglets4 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws4, 100)
        piglets5 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour2,
            self.loc_ws4, 100)

        #  piglets in pigletsCell in ws
        self.loc_cell_ws4_1 = Location.objects.filter(pigletsGroupCell__workshop__number=4)[0]
        piglets6 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour2,
            self.loc_cell_ws4_1, 100)
        self.loc_cell_ws4_2 = Location.objects.filter(pigletsGroupCell__workshop__number=4)[1]
        piglets7 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour2,
            self.loc_cell_ws4_2, 100)

        self.loc_cell_ws4_3 = Location.objects.filter(pigletsGroupCell__workshop__number=4)[2]
        piglets8 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour2,
            self.loc_cell_ws4_3, 100)
        piglets8.deactivate()
        self.loc_cell_ws4_4 = Location.objects.filter(pigletsGroupCell__workshop__number=4)[3]
        piglets9 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour2,
            self.loc_cell_ws4_4, 100)
        piglets9.deactivate()

        # piglets in section
        self.loc_section_ws4_1 = Location.objects.filter(section__workshop__number=4)[0]
        piglets10 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour2,
            self.loc_section_ws4_1, 100)


        self.loc_ws5 = Location.objects.get(workshop__number=5)
        # piglets in ws
        piglets11 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws5, 100)
        piglets12 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour2,
            self.loc_ws5, 100)

        piglets13 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws5, 100)
        piglets14 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour2,
            self.loc_ws5, 50)

        self.loc_cell_ws5_1 = Location.objects.filter(pigletsGroupCell__workshop__number=5)[0]
        merged_piglets1 = PigletsMerger.objects.create_merger_return_group(
            parent_piglets=[piglets13, piglets14], new_location=self.loc_cell_ws5_1)

        piglets15 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour1,
            self.loc_ws5, 30)
        piglets16 = piglets_testing.create_new_group_with_metatour_by_one_tour(self.tour2,
            self.loc_ws5, 50)

        loc_cell_ws5_2 = Location.objects.filter(pigletsGroupCell__workshop__number=5)[1]
        merged_piglets2 = PigletsMerger.objects.create_merger_return_group(
            parent_piglets=[piglets15, piglets16], new_location=loc_cell_ws5_2)

    def test_queryset_serializer(self):
        with self.assertNumQueries(2):
            data = Piglets.objects.all() \
                .prefetch_related('metatour__week_tour') 
            serializer = PigletsSimpleSerializer(data, many=True)
            serializer.data

    def test_all_in_workshop(self):
        self.assertEqual(Piglets.objects.all().all_in_workshop(workshop_number=4).count(), 5)        
        self.assertEqual(Piglets.objects.get_all().all_in_workshop(workshop_number=4).count(), 7)

    def test_with_tour(self):
        self.assertEqual(Piglets.objects.all().with_tour(week_number=1).count(), 6)


class PigletsAgeTest(TransactionTestCase):
    def setUp(self):
        locations_testing.create_workshops_sections_and_cells()
        sows_testings.create_statuses()
        sows_events_testings.create_types()
        piglets_testing.create_piglets_statuses()

        self.tour1 = Tour.objects.get_or_create_by_week_in_current_year(week_number=1)
        self.tour2 = Tour.objects.get_or_create_by_week_in_current_year(week_number=2)

        self.loc_ws5 = Location.objects.get(workshop__number=5)

    def test_gen_anf_birthday(self):
        now = datetime.today()

        piglets1_born_date = now - timedelta(10)
        piglets1 = piglets_testing.create_new_group_with_metatour_by_one_tour(
            tour=self.tour2, location=self.loc_ws5, quantity=15,
            birthday=piglets1_born_date)

        piglets2_born_date = now - timedelta(15)
        piglets2 = piglets_testing.create_new_group_with_metatour_by_one_tour(
            tour=self.tour1, location=self.loc_ws5, quantity=4,
            birthday=piglets2_born_date)

        piglets3_born_date = now - timedelta(20)
        piglets3 = piglets_testing.create_new_group_with_metatour_by_one_tour(
            tour=self.tour1, location=self.loc_ws5, quantity=8,
            birthday=piglets3_born_date)

        piglets_qs = Piglets.objects.filter(pk__in=[piglets1.pk, piglets2.pk, piglets3.pk,])

        avg_birthday = piglets_qs.gen_avg_birthday()
        self.assertEqual((now - avg_birthday).days, 13)