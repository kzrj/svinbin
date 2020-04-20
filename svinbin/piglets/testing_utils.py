# -*- coding: utf-8 -*-
from piglets.models import PigletsStatus, Piglets
from tours.models import Tour, MetaTour, MetaTourRecord
from sows_events.models import SowFarrow
import sows.testing_utils as sows_testing


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
    meta_tour.set_week_tour()

    return piglets


def create_from_sow_farrow(tour, location, quantity=0, gilts_quantity=0, status=None):
    sow1 = sows_testing.create_sow_with_semination_usound(location=location, week=tour.week_number)
    alive_quantity = 10

    if quantity > 0:
        alive_quantity = quantity

    farrow = SowFarrow.objects.create_sow_farrow(
        sow=sow1,
        alive_quantity=alive_quantity,
        dead_quantity=1
        )

    return farrow.piglets_group

def create_from_sow_farrow_by_week(**kwargs):
    tour = Tour.objects.get_or_create_by_week_in_current_year(kwargs['week'])
    kwargs['tour'] = tour
    kwargs.pop('week', None)
    return create_from_sow_farrow(**kwargs)