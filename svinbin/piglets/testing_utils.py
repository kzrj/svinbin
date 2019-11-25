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
