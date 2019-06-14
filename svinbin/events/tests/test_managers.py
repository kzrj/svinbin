from mixer.backend.django import mixer
# from freezegun import freeze_time

from django.test import TestCase

from events.models import Semination, Ultrasound, SowFarrow, NewBornPigletsMerger, \
 SplitNomadPigletsGroup, NomadPigletsGroupMerger, NomadMergerRecord, \
 NewBornPigletsGroupRecount, NomadPigletsGroupRecount
from pigs.models import Sow, NewBornPigletsGroup, NomadPigletsGroup
from tours.models import Tour

import workshops.testing_utils as workshop_testing
import pigs.testing_utils as pigs_testing


class SeminationModelManagerTest(TestCase):
    def setUp(self):
        workshop_testing.create_workshops_sections_and_cells()
        pigs_testing.create_statuses()

    def test_create_semination(self):
        sow = Sow.objects.create_new_from_gilt_and_put_in_workshop_one(1)
        semination = Semination.objects.create_semination(sow_farm_id=1, week=1,
         initiator=None, semination_employee=None)

        self.assertEqual(Semination.objects.all().count(), 1)
        self.assertEqual(semination.tour.week_number, 1)
        sow.refresh_from_db()
        self.assertEqual(sow.tour.week_number, 1)



class UltrasoundModelManagerTest(TestCase):
    def setUp(self):
        workshop_testing.create_workshops_sections_and_cells()
        pigs_testing.create_statuses()

    def test_create_ultrasound(self):
        sow = Sow.objects.create_new_from_gilt_and_put_in_workshop_one(1)
        semination = Semination.objects.create_semination(sow_farm_id=1, week=1,
         initiator=None, semination_employee=None)

        ultrasound = Ultrasound.objects.create_ultrasound(sow_farm_id=1, week=1,
         initiator=None, result=False)

        self.assertEqual(Ultrasound.objects.all().count(), 1)
        self.assertEqual(ultrasound.tour.week_number, 1)
        sow.refresh_from_db()
        self.assertEqual(sow.status.title, 'proholost')

        Ultrasound.objects.create_ultrasound(sow_farm_id=1, week=1,
         initiator=None, result=True)
        sow.refresh_from_db()
        self.assertEqual(sow.status.title, 'pregnant in workshop one')


class SowFarrowModelManagerTest(TestCase):
    def setUp(self):
        workshop_testing.create_workshops_sections_and_cells()
        pigs_testing.create_statuses()

    def test_create_farrow(self):
        sow = pigs_testing.create_sow_and_put_in_workshop_three(1, 1)
        Semination.objects.create_semination(sow_farm_id=sow.farm_id, week=1,
         initiator=None, semination_employee=None)

        # first sow farrow in tour
        farrow1 = SowFarrow.objects.create_sow_farrow(
            sow_farm_id=sow.farm_id,
            week=1,
            alive_quantity=10,
            dead_quantity=1
            )
        
        self.assertEqual(NewBornPigletsGroup.objects.all().count(), 1)
        sow.refresh_from_db()
        self.assertEqual(sow.status.title, 'farrow, feed')
        piglets_group1 = farrow1.new_born_piglets_group
        self.assertEqual(sow.tour, piglets_group1.tour)
        self.assertEqual(sow.location.get_location, piglets_group1.location.get_location)

        self.assertEqual(piglets_group1.quantity, farrow1.alive_quantity)
        self.assertEqual(piglets_group1.start_quantity, farrow1.alive_quantity)

        # second sow farrow in tour
        farrow2 = SowFarrow.objects.create_sow_farrow(
            sow_farm_id=sow.farm_id,
            week=1,
            alive_quantity=7,
            mummy_quantity=1
            )

        self.assertEqual(NewBornPigletsGroup.objects.all().count(), 1)
        piglets_group2 = farrow2.new_born_piglets_group
        self.assertEqual(piglets_group1, piglets_group2)
        self.assertEqual(piglets_group2.quantity, 17)
        self.assertEqual(piglets_group2.start_quantity, 10)


class NewBornMergerModelTest(TestCase):
    def setUp(self):
        workshop_testing.create_workshops_sections_and_cells()
        pigs_testing.create_statuses()

    def test_get_first_tour(self):
        sow1 = pigs_testing.create_sow_and_put_in_workshop_three(1, 1)
        Semination.objects.create_semination(sow_farm_id=sow1.farm_id, week=1,
         initiator=None, semination_employee=None)

        farrow1 = SowFarrow.objects.create_sow_farrow(sow_farm_id=sow1.farm_id, week=1,
         alive_quantity=10)

        sow2 = pigs_testing.create_sow_and_put_in_workshop_three(1, 2)
        Semination.objects.create_semination(sow_farm_id=sow2.farm_id, week=1,
         initiator=None, semination_employee=None)
        farrow2 = SowFarrow.objects.create_sow_farrow(sow_farm_id=sow2.farm_id, week=1,
            alive_quantity=12)

        sow3 = pigs_testing.create_sow_and_put_in_workshop_three(1, 3)
        Semination.objects.create_semination(sow_farm_id=sow3.farm_id, week=2,
         initiator=None, semination_employee=None)
        farrow3 = SowFarrow.objects.create_sow_farrow(sow_farm_id=sow3.farm_id, week=2,
            alive_quantity=15)

        piglets_group1 = farrow1.new_born_piglets_group
        piglets_group2 = farrow2.new_born_piglets_group
        piglets_group3 = farrow3.new_born_piglets_group

        piglets_groups_same_tour = NewBornPigletsGroup.objects.filter(pk__in=
            [piglets_group1.pk, piglets_group2.pk])
        piglets_groups_two_tours = NewBornPigletsGroup.objects.filter(pk__in=
            [piglets_group1.pk, piglets_group2.pk, piglets_group3.pk])

        new_born_merger_same_tour = NewBornPigletsMerger.objects.create_merger(piglets_groups_same_tour)
        new_born_merger_two_tours = NewBornPigletsMerger.objects.create_merger(piglets_groups_two_tours)


        tour1 = new_born_merger_two_tours.get_first_tour()
        self.assertEqual(tour1.week_number, 1)
        next_tour = new_born_merger_two_tours.get_next_tour([tour1])
        # self.assertEqual(next_tour, None)
        self.assertEqual(next_tour.week_number, 2)

        tour1_piglets = new_born_merger_two_tours.get_piglets_groups_by_tour(tour1)
        # check tour piglets
        # print(tour1_piglets)
        
        quantity_piglets_by_tour = new_born_merger_two_tours.count_quantity_by_tour(tour1)
        self.assertEqual(quantity_piglets_by_tour, 22)

        quantity_all_piglets = new_born_merger_two_tours.count_all_piglets()
        print(quantity_all_piglets)

        print(new_born_merger_two_tours.get_percentage_by_tour(tour1))

        print(new_born_merger_two_tours.count_quantity_and_percentage_by_tours())

        print(new_born_merger_two_tours.create_records())
        self.assertEqual(new_born_merger_two_tours.create_records().first().tour.week_number, 1)
        self.assertEqual(new_born_merger_two_tours.create_records().first().quantity, 22)
        self.assertEqual(new_born_merger_two_tours.records.all().count(), 2)

        nomad_group = new_born_merger_two_tours.create_nomad_group()
        self.assertEqual(nomad_group.quantity, 37)

        piglets_group1.refresh_from_db()
        self.assertEqual(piglets_group1.quantity, 0)
        self.assertEqual(piglets_group1.active, False)

        piglets_group2.refresh_from_db()
        self.assertEqual(piglets_group2.quantity, 0)
        self.assertEqual(piglets_group2.active, False)

        piglets_group3.refresh_from_db()
        self.assertEqual(piglets_group3.quantity, 0)
        self.assertEqual(piglets_group3.active, False)


class SplitNomadPigletsGroupManagerTest(TestCase):
    def setUp(self):
        workshop_testing.create_workshops_sections_and_cells()
        pigs_testing.create_statuses()

    def test_split_group(self):
        # quantity 37
        nomad_group = pigs_testing.create_nomad_group_from_three_new_born()

        first_group, second_group = SplitNomadPigletsGroup.objects.split_group(nomad_group, 5)
        self.assertEqual(first_group.quantity, 32)
        self.assertEqual(second_group.quantity, 5)

        self.assertEqual(first_group.location.get_location, nomad_group.location.get_location)
        self.assertEqual(second_group.location.get_location, nomad_group.location.get_location)

        self.assertEqual(nomad_group.quantity, 0)
        self.assertEqual(nomad_group.active, False)


class NomadPigletsGroupMergerManagerTest(TestCase):
    def setUp(self):
        workshop_testing.create_workshops_sections_and_cells()
        pigs_testing.create_statuses()

    def test_split_group(self):
        # quantity 37
        nomad_group1 = pigs_testing.create_nomad_group_from_three_new_born()
        first_group, second_group = SplitNomadPigletsGroup.objects.split_group(nomad_group1, 5)

        # quantity 30
        nomad_group2 = pigs_testing.create_nomad_group_from_three_new_born2()
        third_group, fourth_group = SplitNomadPigletsGroup.objects.split_group(nomad_group2, 7)
        self.assertEqual(third_group.quantity, 23)

        merge_groups = NomadPigletsGroup.objects.filter(pk__in=[first_group.pk, fourth_group.pk])
        nomad_merger = NomadPigletsGroupMerger.objects.create_nomad_merger(merge_groups, first_group)

        first_group.refresh_from_db()
        fourth_group.refresh_from_db()
        self.assertEqual(first_group.groups_merger, nomad_merger)
        self.assertEqual(fourth_group.groups_merger, nomad_merger)

        merge_records = NomadMergerRecord.objects.create_records(nomad_merger)
        print(merge_records)
        self.assertEqual(merge_records.first().quantity, 32)
        self.assertEqual(merge_records.first().nomad_group, first_group)
        print(merge_records.first().percentage)

        print(merge_records[1])
        self.assertEqual(merge_records[1].quantity, 7)
        self.assertEqual(merge_records[1].nomad_group, fourth_group)
        print(merge_records[1].percentage)

        print(merge_records[0].nomad_group.location)
        print(merge_records[0].nomad_group.location.get_location)
        print(type(merge_records[0].nomad_group.location.get_location))

        nomad_group = nomad_merger.create_nomad_group()
        first_group.refresh_from_db()
        fourth_group.refresh_from_db()
        self.assertEqual(first_group.quantity, 0)
        self.assertEqual(first_group.active, False)
        self.assertEqual(fourth_group.quantity, 0)
        self.assertEqual(fourth_group.active, False)

        self.assertEqual(nomad_group.quantity, 39)
        self.assertEqual(nomad_group.start_quantity, 39)
        self.assertEqual(nomad_group.location.get_location, first_group.location.get_location)
        self.assertEqual(nomad_group.creating_nomad_merger, nomad_merger)


class RecountManagerTest(TestCase):
    def setUp(self):
        workshop_testing.create_workshops_sections_and_cells()
        pigs_testing.create_statuses()

    def test_create_recount_nomad_group(self):
        # quantity 37
        nomad_group = pigs_testing.create_nomad_group_from_three_new_born()
        recount = NomadPigletsGroupRecount.objects.create_recount(nomad_group, 35)
        self.assertEqual(recount.quantity_before, 37)
        self.assertEqual(recount.quantity_after, 35)
        self.assertEqual(recount.balance, -2)

    def test_create_recount_new_born_group(self):
        # quantity 10
        new_born_group = pigs_testing.create_new_born_group()
        recount = NewBornPigletsGroupRecount.objects.create_recount(new_born_group, 8)
        self.assertEqual(recount.quantity_before, 10)
        self.assertEqual(recount.quantity_after, 8)
        self.assertEqual(recount.balance, -2)