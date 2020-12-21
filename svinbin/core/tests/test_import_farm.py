# -*- coding: utf-8 -*-
import datetime
import re
from xlrd import open_workbook, xldate_as_tuple

from django.test import TestCase
from django.utils import timezone
from django.test import tag

from core import import_farm

import locations.testing_utils as locaions_testing
import sows.testing_utils as sows_testings
import sows_events.utils as sows_events_testings
import staff.testing_utils as staff_testings

from staff.models import WorkShopEmployee
from sows.models import Sow
from sows_events.models import Semination, Ultrasound
from tours.models import Tour


class FarmImportXlsTest(TestCase):
    def setUp(self):
        locaions_testing.create_workshops_sections_and_cells()
        sows_testings.create_statuses()
        sows_events_testings.create_types()
        staff_testings.create_svinbin_users()

    def test_create_semination_lists(self):
        shmigina = staff_testings.create_employee('ШМЫГИ')
        ivanov = staff_testings.create_employee('ИВАНО')
        semen = staff_testings.create_employee('СЕМЕН')
        boris = staff_testings.create_employee('БОРИС')

        rem1 = sows_testings.create_sow_remont_without_farm_id()
        rem2 = sows_testings.create_sow_remont_without_farm_id()
        rem3 = sows_testings.create_sow_remont_without_farm_id()
        rem4 = sows_testings.create_sow_remont_without_farm_id()
        rem5 = sows_testings.create_sow_remont_without_farm_id()
        
        # all new sows
        rows1 = [
            [1, '1a', 1, '1924', timezone.now(), 1, 'ШМЫГИ', 2, 'ШМЫГИ'],
            [2, '2a', 1, '1924', timezone.now(), 12, 'БОРИС', 23, 'БОРИС'],
            [3, '3a', 1, '1924', timezone.now(), 13, 'СЕМЕН', 24, 'СЕМЕН'],
            [4, '4a', 1, '1924', timezone.now(), 14, 'ШМЫГИ', 25, 'ШМЫГИ'],
        ]

        seminated_list, already_seminated_in_tour, sows_in_another_tour, proholost_list = \
            import_farm.create_semination_lists(rows1, shmigina)

        monday_24_week = Tour.objects.get_monday_date_by_week_number(week_number=24, year=2019)
        self.assertEqual(seminated_list[0].tour.week_number, 24)
        self.assertEqual(len(seminated_list), 4)
        self.assertEqual(len(already_seminated_in_tour), 0)
        self.assertEqual(len(sows_in_another_tour), 0)

        # sows already seminated in tour
        rows2 = [
            [1, '1a', 1, '1924', timezone.now(), 1, 'ШМЫГИ', 2, 'ШМЫГИ'],
            [2, '2a', 1, '1924', timezone.now(), 12, 'БОРИС', 23, 'БОРИС'],
            [3, '3a', 1, '1924', timezone.now(), 13, 'СЕМЕН', 24, 'СЕМЕН'],
            [4, '4a', 1, '1924', timezone.now(), 14, 'ШМЫГИ', 25, 'ШМЫГИ'],
        ]

        seminated_list, already_seminated_in_tour, sows_in_another_tour, proholost_list = \
            import_farm.create_semination_lists(rows2, shmigina)

        self.assertEqual(len(seminated_list), 0)
        self.assertEqual(len(already_seminated_in_tour), 4)
        self.assertEqual(len(sows_in_another_tour), 0)

        # sows in another tour still
        rows3 = [
            [1, '1a', 1, '1923', timezone.now(), 1, 'ШМЫГИ', 2, 'ШМЫГИ'],
            [2, '2a', 1, '1923', timezone.now(), 12, 'БОРИС', 23, 'БОРИС'],
            [3, '3a', 1, '1923', timezone.now(), 13, 'СЕМЕН', 24, 'СЕМЕН'],
            [4, '4a', 1, '1923', timezone.now(), 14, 'ШМЫГИ', 25, 'ШМЫГИ'],
        ]

        seminated_list, already_seminated_in_tour, sows_in_another_tour, proholost_list = \
            import_farm.create_semination_lists(rows3, shmigina)

        self.assertEqual(len(seminated_list), 0)
        self.assertEqual(len(already_seminated_in_tour), 0)
        self.assertEqual(len(sows_in_another_tour), 4)

        # mixed
        rows4 = [
            [1, '1a', 1, '1924', timezone.now(), 1, 'ШМЫГИ', 2, 'ШМЫГИ'],
            [2, '2a', 1, '1924', timezone.now(), 12, 'БОРИС', 23, 'БОРИС'],
            [3, '3a', 1, '1924', timezone.now(), 13, 'СЕМЕН', 24, 'СЕМЕН'],
            [4, '4a', 1, '1923', timezone.now(), 14, 'ШМЫГИ', 25, 'ШМЫГИ'],
            [5, '5a', 1, '1924', timezone.now(), 14, 'ШМЫГИ', 25, 'ШМЫГИ'],
        ]

        seminated_list, already_seminated_in_tour, sows_in_another_tour, proholost_list = \
            import_farm.create_semination_lists(rows4, shmigina)

        self.assertEqual(len(seminated_list), 1)
        self.assertEqual(len(already_seminated_in_tour), 3)
        self.assertEqual(len(sows_in_another_tour), 1)

    @tag('with_file')
    def test_repeated_seminations(self):
        wb = open_workbook('../data/seminations2.xls')
        rows = import_farm.get_semenation_rows(wb)
        shmigina = staff_testings.create_employee('ШМЫГИ')

        seminated_list, already_seminated_in_tour, sows_in_another_tour, proholost_list = \
            import_farm.create_semination_lists(rows, shmigina)

        self.assertEqual(Sow.objects.filter(tour__week_number=6).count(), 75)
        sow = Sow.objects.get(farm_id=19403)
        self.assertEqual(sow.birth_id, 'A0278')

    @tag('with_file')
    def test_repeated_seminations_v2(self):
        # файл с более поздними осеменениями
        wb = open_workbook('../data/seminations2_short.xls')
        rows = import_farm.get_semenation_rows(wb)
        shmigina = staff_testings.create_employee('ШМЫГИ')

        seminated_list, already_seminated_in_tour, sows_in_another_tour, proholost_list = \
            import_farm.create_semination_lists(rows, shmigina)

        self.assertEqual(Sow.objects.filter(tour__week_number=6).count(), 75)

        wb = open_workbook('../data/seminations2.xls')
        rows = import_farm.get_semenation_rows(wb)
        shmigina = staff_testings.create_employee('ШМЫГИ')

        seminated_list, already_seminated_in_tour, sows_in_another_tour, proholost_list = \
            import_farm.create_semination_lists(rows, shmigina)

        self.assertEqual(Sow.objects.filter(tour__week_number=6).count(), 75)
        self.assertEqual(Sow.objects.filter(tour__week_number=7).count(), 75)

    @tag('with_file')
    def test_repeated_seminations_v3(self):
        # файл с более поздними осеменениями. По факту узи есть в файле нет.
        wb = open_workbook('../data/seminations2.xls')
        rows = import_farm.get_semenation_rows(wb)
        shmigina = staff_testings.create_employee('ШМЫГИ')

        seminated_list, already_seminated_in_tour, sows_in_another_tour, proholost_list = \
            import_farm.create_semination_lists(rows, shmigina)

        self.assertEqual(Sow.objects.filter(tour__week_number=6).count(), 75)
        self.assertEqual(Sow.objects.filter(tour__week_number=7).count(), 75)

        # We have done usound by hand. Then FARM update file.
        # sow.farm_id = 20095 - usound - false by hand. file updated. tour 7
        sow = Sow.objects.filter(farm_id=20095).first()
        Ultrasound.objects.create_ultrasound(sow=sow, result=False, initiator=shmigina)

        wb = open_workbook('../data/seminations2_custom_uzi.xls')
        rows = import_farm.get_semenation_rows(wb)
        shmigina = staff_testings.create_employee('ШМЫГИ')

        seminated_list, already_seminated_in_tour, sows_in_another_tour, proholost_list = \
            import_farm.create_semination_lists(rows, shmigina)

        self.assertEqual(Sow.objects.filter(tour__week_number=6).count(), 75)
        self.assertEqual(Sow.objects.filter(tour__week_number=7).count(), 74)

        self.assertEqual(Ultrasound.objects.filter(sow=sow).count(), 1)

    @tag('with_file')
    def test_repeated_seminations_v4(self):
        # файл с более поздними осеменениями. По факту узи есть в файле нет.
        wb = open_workbook('../data/seminations2.xls')
        rows = import_farm.get_semenation_rows(wb)
        shmigina = staff_testings.create_employee('ШМЫГИ')

        seminated_list, already_seminated_in_tour, sows_in_another_tour, proholost_list = \
            import_farm.create_semination_lists(rows, shmigina)

        self.assertEqual(Sow.objects.filter(tour__week_number=6).count(), 75)
        self.assertEqual(Sow.objects.filter(tour__week_number=7).count(), 75)

        sow = Sow.objects.filter(farm_id=20095).first().delete()

        wb = open_workbook('../data/seminations2.xls')
        rows = import_farm.get_semenation_rows(wb)
        shmigina = staff_testings.create_employee('ШМЫГИ')

        seminated_list, already_seminated_in_tour, sows_in_another_tour, proholost_list = \
            import_farm.create_semination_lists(rows, shmigina)
