# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import Q
from django.core.exceptions import ValidationError as DjangoValidationError

from core.models import CoreModel, CoreModelManager


class PigletsStatus(CoreModel):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class PigletsQuerySet(models.QuerySet):
    def get_total_quantity(self):
        return self.aggregate(models.Sum('quantity'))['quantity__sum']

    def get_total_gilts_quantity(self):
        return self.aggregate(models.Sum('gilts_quantity'))['gilts_quantity__sum']

    def active(self):
        return self.filter(active=True)

    def inactive(self):
        return self.filter(active=True)

    # def with_farrows(self, tour):
        # self.filter()


class PigletsManager(CoreModelManager):
    def get_queryset(self):
        return PigletsQuerySet(self.model, using=self._db).select_related('metatour').active()

    def get_inactive(self):
        return PigletsQuerySet(self.model, using=self._db).select_related('metatour').inactive()


class Piglets(CoreModel):
    location = models.ForeignKey('locations.Location', on_delete=models.SET_NULL,
        null=True, related_name='piglets')
    status = models.ForeignKey(PigletsStatus, on_delete=models.SET_NULL, null=True)

    start_quantity = models.IntegerField()
    quantity = models.IntegerField()
    gilts_quantity = models.IntegerField(default=0)

    merger_as_parent = models.ForeignKey('piglets_events.PigletsMerger', on_delete=models.SET_NULL,
        null=True, related_name='piglets_as_parents')

    split_as_child = models.ForeignKey('piglets_events.PigletsSplit', on_delete=models.SET_NULL,
        null=True, related_name='piglets_as_child')

    active = models.BooleanField(default=True)  

    objects = PigletsManager()

    def __str__(self):
        return 'Piglets {}'.format(self.pk)

    def deactivate(self):
        self.active = False
        self.save()

    def remove_piglets(self, quantity):
        self.quantity = self.quantity - quantity
        self.save()

    def remove_gilts(self, quantity):
        if self.gilts_quantity > 0:
            self.quantity -= quantity
            self.gilts_quantity -= quantity
            self.save()

    def change_status_to(self, status_title):
        self.status = PigletsStatus.objects.get(title=status_title)
        self.save()

    def add_piglets(self, quantity):
        self.quantity = self.quantity + quantity
        self.save()

    # def add_gilts(self, quantity):
    #     self.gilts_quantity += quantity
    #     self.save()

    # def add_gilts_increase_quantity(self, quantity):
    #     self.quantity += quantity
    #     self.gilts_quantity += quantity
    #     self.save()


# class NewBornPigletsQuerySet(models.QuerySet):
#     def remove_gilts_and_update_quantity(self): # test+ in gilt merger
#         return self.update(quantity=(models.F('quantity') - models.F('gilts_quantity')),
#          gilts_quantity=0) 

#     def filter_by_weighing_place_reverse(self, value):
#         return self.select_related('weighing_records') \
#                     .filter(~Q(weighing_records__place=value)) \
#                     .distinct()

#     def get_all_in_workshop(self, workshop):
#         return self.filter(
#             models.Q(
#                 models.Q(location__workshop=workshop) |
#                 models.Q(location__section__workshop=workshop) |
#                 models.Q(location__pigletsGroupCell__workshop=workshop) |
#                 models.Q(location__sowAndPigletsCell__workshop=workshop)
#                 )
#             )

# class NewBornPigletsGroupManager(PigletsGroupManager):
#     def get_queryset(self):
#         return NewBornPigletsQuerySet(self.model, using=self._db).filter(active=True) \
#             .select_related('location')

#     def get_with_inactive(self):
#         return NewBornPigletsQuerySet(self.model, using=self._db)

#     def groups_with_gilts(self):
#         return self.get_queryset().filter(active=True, gilts_quantity__gt=0)

#     def groups_with_gilts_by_gilts_queryset(self, gilts):
#         new_born_group_pk_queryset = gilts.values_list('new_born_group', flat=True)
#         return self.get_queryset().filter(pk__in=new_born_group_pk_queryset)

#     def from_list_to_queryset(self, groups_list):
#         pks = [group.pk for group in groups_list]
#         return self.get_queryset().filter(pk__in=pks)

#     def remove_gilts_and_update_quantity(self):
#         return self.get_queryset().remove_gilts_and_update_quantity()

#     # use only when create nurse sow. Sows anf Piglets weaning. mb temporary
#     def create_new_born_group(self, location, tour):
#         if location.newbornpigletsgroup_set.all().first():
#             raise DjangoValidationError(message='В клетке есть другие поросята.')
#         return self.create(quantity=0, start_quantity=0, location=location, tour=tour)


# class NewBornPigletsGroup(PigletsGroup):
#     LABELS = [
#         ('s', 'Small'),
#         ('m', 'Medium'),
#         ('l', 'Large'),
#     ]
#     merger = models.ForeignKey('piglets_events.NewBornPigletsMerger', on_delete=models.SET_NULL, null=True,
#         related_name='piglets_groups')
#     tour = models.ForeignKey('tours.Tour', on_delete=models.SET_NULL, null=True,
#      related_name="new_born_piglets")

#     size_label = models.CharField(max_length=1, choices=LABELS, null=True)

#     objects = NewBornPigletsGroupManager()

#     def __str__(self):
#         return 'NBPiglets #{} {}'.format(self.pk, self.location)

#     def mark_size_label(self, size_label):
#         self.size_label = size_label


# class NomadPigletsQuerySet(models.QuerySet):
#     def reset_quantity_and_deactivate(self):
#         return self.update(quantity=0, active=False)

#     def piglets_with_weighing_record(self, place):
#         return self.prefetch_related('weighing_records') \
#                     .filter(weighing_records__place=place) \
#                     .distinct()

#     def piglets_without_weighing_record(self, place):
#         return self.prefetch_related('weighing_records') \
#                     .filter(~Q(weighing_records__place=place)) \
#                     .distinct()


# class NomadPigletsGroupManager(PigletsGroupManager):
#     def get_queryset(self):
#         return NomadPigletsQuerySet(self.model, using=self._db).filter(active=True)

#     def reset_quantity_and_deactivate(self):
#         return self.get_queryset().reset_quantity_and_deactivate()

#     def piglets_with_weighing_record(self, place):
#         return self.get_queryset().piglets_with_weighing_record(place)

#     def piglets_without_weighing_record(self, place):
#         return self.get_queryset().piglets_without_weighing_record(place)


# class NomadPigletsGroup(PigletsGroup):
#     split_record = models.ForeignKey('piglets_events.SplitNomadPigletsGroup',
#          on_delete=models.SET_NULL, null=True)
#     groups_merger = models.ForeignKey('piglets_events.NomadPigletsGroupMerger',
#          on_delete=models.SET_NULL, null=True, related_name="groups_merger")

#     objects = NomadPigletsGroupManager()

#     def __str__(self):
#         return 'NomadPiglets group #%s' % self.pk

#     def reset_quantity_and_deactivate(self):
#         self.quantity = 0
#         self.active = False
#         self.save()

#     @property
#     def merger_part_number(self):
#         if self.creating_new_born_merger:
#             return self.creating_new_born_merger.part_number
#         return None

#     @property
#     def cells_numbers_from_merger(self):
#         if self.creating_new_born_merger:
#             return self.creating_new_born_merger.cells
#         return None