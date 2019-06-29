# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import Q

from core.models import CoreModel, CoreModelManager


class PigletsStatus(CoreModel):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class PigletsGroupManager(CoreModelManager):
    def reset_quantity_and_deactivate(self):
        self.update(quantity=0, active=False)
        # return self.update(quantity=0, active=False)

    def piglets_in_workshop_not_in_cells(self):
        return self.filter(~Q(location__workshop=None))


class PigletsGroup(CoreModel):
    location = models.ForeignKey('locations.Location', on_delete=models.SET_NULL,
     null=True)
    start_quantity = models.IntegerField()
    quantity = models.IntegerField()
    active = models.BooleanField(default=True)
    transfer_label = models.BooleanField(default=False)

    status = models.ForeignKey(PigletsStatus, on_delete=models.SET_NULL, null=True)

    gilts_quantity = models.IntegerField(default=0)

    class Meta:
        abstract = True

    def is_quantities_same(self, quantity):
        return self.quantity == quantity

    def mark_for_transfer(self):
        self.transfer_label = True
        self.save()

    def change_quantity(self, quantity):
        self.quantity = quantity
        self.save()

    def change_current_location(self, to_location):
        self.location = to_location
        self.save()

    def add_piglets(self, quantity):
        self.quantity = self.quantity + quantity
        self.save()

    def remove_piglets(self, quantity):
        self.quantity = self.quantity - quantity
        self.save()

    def change_status_to(self, status_title):
        self.status = PigletsStatus.objects.get(title=status_title)
        self.save()

    def reset_status(self):
        self.status = None
        self.save()

    def add_gilts(self, quantity):
        self.gilts_quantity += quantity
        self.save()

    def add_gilts_increase_quantity(self, quantity):
        self.quantity += quantity
        self.gilts_quantity += quantity
        self.save()

    def remove_gilts(self, quantity):
        self.quantity -= quantity
        self.gilts_quantity -= quantity
        self.save()


class NewBornPigletsQuerySet(models.QuerySet):
    def remove_gilts_and_update_quantity(self): # test+ in gilt merger
        return self.update(quantity=(models.F('quantity') - models.F('gilts_quantity')),
         gilts_quantity=0) 


class NewBornPigletsGroupManager(PigletsGroupManager):
    def get_queryset(self):
        return NewBornPigletsQuerySet(self.model, using=self._db)

    def groups_with_gilts(self):
        return self.get_queryset().filter(active=True, gilts_quantity__gt=0)

    def groups_with_gilts_by_gilts_queryset(self, gilts):
        new_born_group_pk_queryset = gilts.values_list('new_born_group', flat=True)
        return self.get_queryset().filter(pk__in=new_born_group_pk_queryset)

    def from_list_to_queryset(self, groups_list):
        pks = [group.pk for group in groups_list]
        return self.get_queryset().filter(pk__in=pks)

    def remove_gilts_and_update_quantity(self):
        return self.get_queryset().remove_gilts_and_update_quantity()


class NewBornPigletsGroup(PigletsGroup):
    LABELS = [
        ('s', 'Small'),
        ('m', 'Medium'),
        ('l', 'Large'),
    ]
    merger = models.ForeignKey('piglets_events.NewBornPigletsMerger', on_delete=models.SET_NULL, null=True,
        related_name='piglets_groups')
    tour = models.ForeignKey('tours.Tour', on_delete=models.SET_NULL, null=True,
     related_name="new_born_piglets")

    size_label = models.CharField(max_length=1, choices=LABELS, null=True)

    objects = NewBornPigletsGroupManager()

    def __str__(self):
        return 'NewBornPiglets group #%s' % self.pk

    def mark_size_label(self, size_label):
        self.size_label = size_label


class NomadPigletsQuerySet(models.QuerySet):
    def reset_quantity_and_deactivate(self):
        return self.update(quantity=0, active=False)

    def piglets_with_weighing_record(self, place):
        return self.filter(weighing_records__place=place)

    def piglets_without_weighing_record(self, place):
        return self.filter(~Q(weighing_records__place=place))


class NomadPigletsGroupManager(PigletsGroupManager):
    def get_queryset(self):
        return NomadPigletsQuerySet(self.model, using=self._db)

    def reset_quantity_and_deactivate(self):
        return self.get_queryset().reset_quantity_and_deactivate()

    def piglets_with_weighing_record(self, place):
        return self.get_queryset().piglets_with_weighing_record(place)

    def piglets_without_weighing_record(self, place):
        return self.get_queryset().piglets_without_weighing_record(place)


class NomadPigletsGroup(PigletsGroup):
    split_record = models.ForeignKey('piglets_events.SplitNomadPigletsGroup',
         on_delete=models.SET_NULL, null=True)
    groups_merger = models.ForeignKey('piglets_events.NomadPigletsGroupMerger',
         on_delete=models.SET_NULL, null=True, related_name="groups_merger")

    objects = NomadPigletsGroupManager()

    def __str__(self):
        return 'NomadPiglets group #%s' % self.pk

    def reset_quantity_and_deactivate(self):
        self.quantity = 0
        self.active = False
        self.save()