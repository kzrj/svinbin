# -*- coding: utf-8 -*-
import datetime
import re
from xlrd import open_workbook, xldate_as_tuple

from django.test import TestCase
from django.utils import timezone

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
        
        # all new sows
        rows1 = [
            [1, '1a', 1, '1924', timezone.now(), 1, 'ШМЫГИ', 2, 'ШМЫГИ'],
            [2, '2a', 1, '1924', timezone.now(), 12, 'БОРИС', 23, 'БОРИС'],
            [3, '3a', 1, '1924', timezone.now(), 13, 'СЕМЕН', 24, 'СЕМЕН'],
            [4, '4a', 1, '1924', timezone.now(), 14, 'ШМЫГИ', 25, 'ШМЫГИ'],
        ]

        seminated_list, already_seminated_in_tour, sows_in_another_tour, proholost_list = \
            import_farm.create_semination_lists(rows1, shmigina)

        print(seminated_list[0].tour.start_date)
        print(seminated_list[0].tour.week_number)
        monday_24_week = Tour.objects.get_monday_date_by_week_number(week_number=24, year=2019)
        print(monday_24_week)
        print(monday_24_week.strftime("%V"))
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

    def test_repeated_seminations(self):
        wb = open_workbook('../data/seminations2.xls')
        rows = import_farm.get_semenation_rows(wb)
        shmigina = staff_testings.create_employee('ШМЫГИ')

        seminated_list, already_seminated_in_tour, sows_in_another_tour, proholost_list = \
            import_farm.create_semination_lists(rows, shmigina)

        self.assertEqual(Sow.objects.filter(tour__week_number=6).count(), 75)

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

    def test_missing_sow(self):
        # грузили 51-52 туры, на завелась свиноматка 2376
        wb = open_workbook('../data/51-52.xls')
        rows = import_farm.get_semenation_rows(wb)
        shmigina = staff_testings.create_employee('ШМЫГИ')

        seminated_list, already_seminated_in_tour, sows_in_another_tour, proholost_list = \
            import_farm.create_semination_lists(rows, shmigina)

        self.assertEqual(Sow.objects.get_queryset_with_not_alive()
            .filter(tour__week_number=51).count(), 75)


       
# class FarmImportJsonTest(TestCase):
#     def setUp(self):
#         locaions_testing.create_workshops_sections_and_cells()
#         sows_testings.create_statuses()
#         sows_events_testings.create_types()
#         staff_testings.create_svinbin_users()

    # def test_init_ceh3(self):
    #     import_farm.import_from_json_to_ws3()
    #     self.assertNotEqual(Sow.objects.all().count(), 0)
        
    #     sow1 = Sow.objects.all().first()

    #     self.assertEqual(sow1.location.workshop.number, 3)

    #     semination = Semination.objects.filter(sow=sow1).first()
    #     ultrasound = Ultrasound.objects.filter(sow=sow1).first()
    #     self.assertNotEqual(semination, None)
    #     self.assertNotEqual(semination.semination_employee, None)
    #     self.assertNotEqual(semination.boar, None)
    #     self.assertNotEqual(semination.tour, None)
    #     self.assertNotEqual(ultrasound, None)
    #     self.assertEqual(ultrasound.result, True)
    #     self.assertEqual(ultrasound.date, semination.date + datetime.timedelta(days=28))

    # def test_init_ceh2(self):
    #     import_farm.import_from_json_to_ws2()
    #     self.assertNotEqual(Sow.objects.all().count(), 0)
        
    #     sow1 = Sow.objects.all().first()

    #     self.assertEqual(sow1.location.workshop.number, 2)

    #     semination = Semination.objects.filter(sow=sow1).first()
    #     ultrasound = Ultrasound.objects.filter(sow=sow1).first()
    #     self.assertNotEqual(semination, None)
    #     self.assertNotEqual(semination.semination_employee, None)
    #     self.assertNotEqual(semination.boar, None)
    #     self.assertNotEqual(semination.tour, None)
    #     self.assertNotEqual(ultrasound, None)
    #     self.assertEqual(ultrasound.result, True)
    #     self.assertEqual(ultrasound.date, semination.date + datetime.timedelta(days=28))


    # def test_import_from_json_to_ws2_3(self):
    #     json_file = open('../data/ceh03.json', 'r')
    #     sows_created1, sows_passed1 = import_farm.import_from_json_to_ws2_3(json_file, 3)
    #     print(sows_created1)
    #     # sows_created2, sows_passed2 = import_farm.import_from_json_to_ws2_3(json_file, 3)

        # self.assertEqual(len(sows_created1), len(sows_passed2))

    # def test
        