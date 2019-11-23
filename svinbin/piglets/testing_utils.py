# -*- coding: utf-8 -*-
from piglets.models import PigletsStatus, Piglets
from tours.models import Tour, MetaTour, MetaTourRecord


def create_piglets_statuses():
    if PigletsStatus.objects.all().count() < 1:
        PigletsStatus.objects.bulk_create([
            PigletsStatus(title='Родились, кормятся'),
            PigletsStatus(title='Готовы ко взвешиванию'),
            PigletsStatus(title='Взвешены, готовы к заселению'),
            PigletsStatus(title='Кормятся'),
            PigletsStatus(title='Объединены с другой группой'),
            ])


def create_new_group_with_metatour_by_one_tour(tour, location, quantity, gilts_quantity=0, status=None):
    piglets = Piglets.objects.create(location=location, quantity=quantity, start_quantity=quantity,
        gilts_quantity=gilts_quantity, status=status)

    meta_tour = MetaTour.objects.create(piglets=piglets)
    meta_tour.records.create_record(meta_tour, tour, piglets.quantity, piglets.quantity)

    return piglets


    
# def create_new_born_group(section_number=1, cell_number=1, week=1, quantity=10):
#     sow = sows_testing_utils.create_sow_and_put_in_workshop_three(section_number, cell_number)
#     Semination.objects.create_semination(sow=sow, week=week,
#      initiator=None, semination_employee=None)
#     farrow = SowFarrow.objects.create_sow_farrow(sow=sow, alive_quantity=quantity)
#     return farrow.new_born_piglets_group


# def create_nomad_group_from_new_born_groups(new_born_groups):
#     new_born_merger = NewBornPigletsMerger.objects.create_merger(new_born_groups)
#     new_born_merger.create_records()
#     return new_born_merger.create_nomad_group()


# def create_nomad_group_from_three_new_born():
#     piglets_group1 = create_new_born_group(1, 1, 1, 10)
#     piglets_group2 = create_new_born_group(1, 2, 1, 12)
#     piglets_group3 = create_new_born_group(1, 3, 1, 15)

#     piglets_groups = NewBornPigletsGroup.objects.filter(pk__in=
#         [piglets_group1.pk, piglets_group2.pk, piglets_group3.pk])

#     nomad_group = create_nomad_group_from_new_born_groups(piglets_groups)

#     return nomad_group

# def create_nomad_group_from_three_new_born_two_tours():
#     piglets_group1 = create_new_born_group(1, 4, 2, 10)
#     piglets_group2 = create_new_born_group(1, 5, 2, 10)
#     piglets_group3 = create_new_born_group(1, 6, 3, 10)

#     piglets_groups_two_tours = NewBornPigletsGroup.objects.filter(pk__in=
#         [piglets_group1.pk, piglets_group2.pk, piglets_group3.pk])

#     nomad_group = create_nomad_group_from_new_born_groups(piglets_groups_two_tours)

#     return nomad_group

# def create_nomad_and_move_to_cell_in_workshop_four():
#     nomad_group = create_nomad_group_from_three_new_born()

#     section = Section.objects.get(workshop__number=4, number=1)
#     piglet_group_cell = PigletsGroupCell.objects.get(section=section, number=1)
#     to_location = Location.objects.get(pigletsGroupCell=piglet_group_cell)

#     transaction = PigletsTransaction.objects.create_transaction(to_location,
#             nomad_group)

#     return nomad_group