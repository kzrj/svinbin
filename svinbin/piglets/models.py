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
    location = models.OneToOneField('transactions.Location', on_delete=models.SET_NULL,
     null=True)
    start_quantity = models.IntegerField()
    quantity = models.IntegerField()
    active = models.BooleanField(default=True)
    transfer_label = models.BooleanField(default=False)

    status = models.ForeignKey(PigletsStatus, on_delete=models.SET_NULL, null=True)

    gilts_count = models.IntegerField(default=0)

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


class NewBornPigletsGroupManager(PigletsGroupManager):
    pass


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

    # def piglets_in_workshop_not_in_cells(self):
    #     return self.filter(~Q(location__workshop=None))

    def reset_quantity_and_deactivate(self):
        return self.update(quantity=0, active=False)

    def piglets_in_workshop_not_in_cells(self, workshop):
        return self.filter(location__workshop=workshop)

    def piglets_with_weighing_record(self, place):
        return self.filter(weighing_records__place=place)

    def piglets_with_new_born_merger(self):
        return self.filter(~Q(creating_new_born_merger=None))
        # return self.filter(creating_new_born_merger__nomad_group__isnull=False)

    # def piglets_without_new_born_merger(self):
    #     return self.filter(~Q(creating_new_born_merger=None))

    def piglets_without_weighing_record(self, place):
        return self.filter(~Q(weighing_records__place=place))


class NomadPigletsGroupManager(PigletsGroupManager):
    def get_queryset(self):
        return NomadPigletsQuerySet(self.model, using=self._db)

    def reset_quantity_and_deactivate(self):
        return self.get_queryset().reset_quantity_and_deactivate()

    def move_to(self, piglets_group_pk, pre_location, initiator=None):
        location = Location.objects.create_location(pre_location)
        piglets_group = self.get(pk=piglets_group_pk)
        transaction = PigletsTransactionManager.objects.create_transaction(                
                initiator=initiator,
                to_location=location,
                piglets_group=piglets_group
                )
        return piglets_group, transaction

    def piglets_to_weighing_v1(self, from_workshop):
        return self.get_queryset().filter(transactions__from_location__workshop=from_workshop  
            )
    
    def piglets_in_workshop_not_in_cells(self, workshop):
        return self.get_queryset().piglets_in_workshop_not_in_cells(workshop)

    def piglets_with_weighing_record(self, place):
        return self.get_queryset().piglets_with_weighing_record(place)

    def piglets_without_weighing_record(self, place):
        return self.get_queryset().piglets_without_weighing_record(place)

    def piglets_with_new_born_merger(self):
        return self.get_queryset().piglets_with_new_born_merger()

    # def piglets_weighted_in_workshop_4(self)


class NomadPigletsGroup(PigletsGroup):
    split_record = models.ForeignKey('piglets_events.SplitNomadPigletsGroup', on_delete=models.SET_NULL, null=True)
    groups_merger = models.ForeignKey('piglets_events.NomadPigletsGroupMerger', on_delete=models.SET_NULL, null=True,
        related_name="groups_merger")

    objects = NomadPigletsGroupManager()

    def __str__(self):
        return 'NomadPiglets group #%s' % self.pk

    def reset_quantity_and_deactivate(self):
        self.quantity = 0
        self.active = False
        self.save()