# -*- coding: utf-8 -*-
from django.test import TestCase, TransactionTestCase
from django.core.exceptions import ValidationError

# import sows.models as sows_models
import piglets.models as piglets_models
# import piglets_events.models as piglets_events_models
# import tours.models as tours_models
# import locations.models as locations_models

import locations.testing_utils as locations_testing
# import sows.testing_utils as sows_testing
import piglets.testing_utils as piglets_testing


class PigletsModelManagerQuerysetTest(TestCase):
    def setUp(self):
        locations_testing.create_workshops_sections_and_cells()
        # sows_testing.create_statuses()

    def test_groups_with_gilts(self):
        print('hello')
        # new_born_group1 = piglets_testing.create_new_born_group(cell_number=5)
#         sow1 = new_born_group1.farrows.first().sow
#         gilt1 = sows_models.Gilt.objects.create_gilt(1, new_born_group1)
#         new_born_group1.refresh_from_db()
        
#         new_born_group2 = piglets_testing.create_new_born_group(cell_number=6)
#         sow2 = new_born_group2.farrows.first().sow
#         gilt2 = sows_models.Gilt.objects.create_gilt(2, new_born_group2)

#         new_born_group3 = piglets_testing.create_new_born_group(cell_number=4)

#         self.assertEqual(piglets_models.NewBornPigletsGroup.objects.groups_with_gilts().count(), 2)
#         self.assertEqual(piglets_models.NewBornPigletsGroup.objects.all().count(), 3)

#     def test_create_new_born_group(self):
#         sow = sows_testing.create_sow_and_put_in_workshop_three(section_number=1, cell_number=1)
#         tour = tours_models.Tour.objects.get_or_create_by_week_in_current_year(45)
#         piglets = piglets_models.NewBornPigletsGroup.objects.create_new_born_group(sow.location, tour)
#         self.assertEqual(piglets.tour, tour)
#         self.assertEqual(piglets.location, sow.location)
#         self.assertRaises(ValidationError, piglets_models.NewBornPigletsGroup.objects\
#             .create_new_born_group, sow.location, tour)

#     def test_get_all_in_workshop(self):
#         piglets_testing.create_new_born_group(section_number=1, cell_number=1)
        
#         nbp2 = piglets_testing.create_new_born_group(section_number=1, cell_number=2)
#         nbp2.location = locations_models.Location.objects.get(workshop__number=3)
#         nbp2.save()

#         nbp3 = piglets_testing.create_new_born_group(section_number=1, cell_number=3)
#         nbp3.location = locations_models.Location.objects.get(workshop__number=2)
#         nbp3.save()

#         workshop = locations_models.WorkShop.objects.filter(number=3).first()
#         piglets_qs = piglets_models.NewBornPigletsGroup.objects.all().get_all_in_workshop(workshop)
#         self.assertEqual(piglets_qs.count(), 2)


# class NomadPigletsModelManagerTest(TransactionTestCase):
#     def setUp(self):
#         locations_testing.create_workshops_sections_and_cells()
#         piglets_testing.create_piglets_statuses()
#         sows_testing.create_statuses()

#         self.piglets_group1 = piglets_testing.create_new_born_group(1, 1, 1, 10)
#         self.piglets_group2 = piglets_testing.create_new_born_group(1, 2, 1, 12)
#         self.piglets_group3 = piglets_testing.create_new_born_group(1, 3, 2, 15)

#         self.piglets_group4 = piglets_testing.create_new_born_group(
#             section_number=1,
#             cell_number=4,
#             week=1,
#             quantity=10)
#         self.piglets_group5 = piglets_testing.create_new_born_group(1, 5, 1, 12)
        
#         piglets_groups_same_tour = piglets_models.NewBornPigletsGroup.objects.filter(pk__in=
#             [self.piglets_group4.pk, self.piglets_group5.pk])
#         piglets_groups_two_tours = piglets_models.NewBornPigletsGroup.objects.filter(pk__in=
#             [self.piglets_group1.pk, self.piglets_group2.pk, self.piglets_group3.pk])

#         self.new_born_merger_same_tour = piglets_events_models.NewBornPigletsMerger.objects \
#             .create_merger_and_return_nomad_piglets_group(piglets_groups_same_tour, 
#                 part_number=1)[0]
#         self.new_born_merger_two_tours = piglets_events_models.NewBornPigletsMerger.objects \
#             .create_merger_and_return_nomad_piglets_group(piglets_groups_two_tours, 
#                 part_number=2)[0]

#     def test_merger_part_number(self):
#         nomad_group1 = self.new_born_merger_same_tour.nomad_group
#         nomad_group2 = self.new_born_merger_two_tours.nomad_group
#         self.assertEqual(nomad_group1.merger_part_number, 1)
#         self.assertEqual(nomad_group2.merger_part_number, 2)

#     def test_cells_numbers_from_merger(self):
#         nomad_group1 = self.new_born_merger_same_tour.nomad_group
#         nomad_group2 = self.new_born_merger_two_tours.nomad_group
#         self.assertEqual(list(nomad_group1.cells_numbers_from_merger), 
#             list(self.new_born_merger_same_tour.cells))
#         self.assertEqual(list(nomad_group2.cells_numbers_from_merger), 
#             list(self.new_born_merger_two_tours.cells))

#     def test_piglets_without_weighing_record(self):
#         nomad_group1 = self.new_born_merger_same_tour.nomad_group
#         nomad_group2 = self.new_born_merger_two_tours.nomad_group

#         piglets_events_models.WeighingPiglets.objects.create_weighing(nomad_group1, 100, '3/4')

#         self.assertEqual(piglets_models.NomadPigletsGroup.objects\
#                 .piglets_without_weighing_record('3/4').count(), 1)
#         self.assertEqual(piglets_models.NomadPigletsGroup.objects\
#                 .piglets_without_weighing_record('3/4').first().pk, nomad_group2.pk)
#         self.assertEqual(piglets_models.NomadPigletsGroup.objects\
#             .piglets_without_weighing_record('4/8').count(), 2)

#     def test_piglets_with_weighing_record(self):
#         nomad_group1 = self.new_born_merger_same_tour.nomad_group
#         nomad_group2 = self.new_born_merger_two_tours.nomad_group

#         piglets_events_models.WeighingPiglets.objects.create_weighing(nomad_group1, 100, '3/4')

#         self.assertEqual(piglets_models.NomadPigletsGroup.objects\
#                 .piglets_with_weighing_record('3/4').count(), 1)
#         self.assertEqual(piglets_models.NomadPigletsGroup.objects\
#                 .piglets_with_weighing_record('3/4').first().pk, nomad_group1.pk)
#         self.assertEqual(piglets_models.NomadPigletsGroup.objects\
#             .piglets_with_weighing_record('4/8').count(), 0)