# -*- coding: utf-8 -*-
from django.test import TestCase
from django.utils import timezone

from core import import_farm

import locations.testing_utils as locaions_testing
import sows.testing_utils as sows_testings
import sows_events.utils as sows_events_testings
import staff.testing_utils as staff_testings

from staff.models import WorkShopEmployee


class WorkshopEmployeeManagerTest(TestCase):
    def setUp(self):
        locaions_testing.create_workshops_sections_and_cells()
        sows_testings.create_statuses()
        sows_events_testings.create_types()

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

        seminated_list, already_seminated_in_tour, sows_in_another_tour = \
            import_farm.create_semination_lists(rows1, shmigina)

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

        seminated_list, already_seminated_in_tour, sows_in_another_tour = \
            import_farm.create_semination_lists(rows2, shmigina)

        self.assertEqual(len(seminated_list), 0)
        self.assertEqual(len(already_seminated_in_tour), 4)
        self.assertEqual(len(sows_in_another_tour), 0)

        # sows in another tour still
        rows3 = [
            [1, '1a', 1, '1925', timezone.now(), 1, 'ШМЫГИ', 2, 'ШМЫГИ'],
            [2, '2a', 1, '1925', timezone.now(), 12, 'БОРИС', 23, 'БОРИС'],
            [3, '3a', 1, '1925', timezone.now(), 13, 'СЕМЕН', 24, 'СЕМЕН'],
            [4, '4a', 1, '1925', timezone.now(), 14, 'ШМЫГИ', 25, 'ШМЫГИ'],
        ]

        seminated_list, already_seminated_in_tour, sows_in_another_tour = \
            import_farm.create_semination_lists(rows3, shmigina)

        self.assertEqual(len(seminated_list), 0)
        self.assertEqual(len(already_seminated_in_tour), 0)
        self.assertEqual(len(sows_in_another_tour), 4)

        # mixed
        rows4 = [
            [1, '1a', 1, '1924', timezone.now(), 1, 'ШМЫГИ', 2, 'ШМЫГИ'],
            [2, '2a', 1, '1924', timezone.now(), 12, 'БОРИС', 23, 'БОРИС'],
            [3, '3a', 1, '1924', timezone.now(), 13, 'СЕМЕН', 24, 'СЕМЕН'],
            [4, '4a', 1, '1925', timezone.now(), 14, 'ШМЫГИ', 25, 'ШМЫГИ'],
            [5, '5a', 1, '1924', timezone.now(), 14, 'ШМЫГИ', 25, 'ШМЫГИ'],
        ]

        seminated_list, already_seminated_in_tour, sows_in_another_tour = \
            import_farm.create_semination_lists(rows4, shmigina)

        self.assertEqual(len(seminated_list), 1)
        self.assertEqual(len(already_seminated_in_tour), 3)
        self.assertEqual(len(sows_in_another_tour), 1)