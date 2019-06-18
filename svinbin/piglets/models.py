# -*- coding: utf-8 -*-
from django.db import models


class PigletsGroupManager(models.Manager):
    def reset_quantity_and_deactivate(self):
        self.update(quantity=0, active=False)


class PigletsGroup(models.Model):
    location = models.OneToOneField('transactions.Location', on_delete=models.SET_NULL,
     null=True)
    start_quantity = models.IntegerField()
    quantity = models.IntegerField()
    active = models.BooleanField(default=True)
    transfer_label = models.BooleanField(default=False)

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


class NomadPigletsGroupManager(PigletsGroupManager):
    def move_to(self, piglets_group_pk, pre_location, initiator=None):
        location = Location.objects.create_location(pre_location)
        piglets_group = self.get(pk=piglets_group_pk)
        transaction = PigletsTransactionManager.objects.create_transaction(                
                initiator=initiator,
                to_location=location,
                piglets_group=piglets_group
                )
        return piglets_group, transaction


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

