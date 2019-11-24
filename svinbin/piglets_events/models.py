# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError as DjangoValidationError

from core.models import Event, CoreModel, CoreModelManager
from piglets.models import Piglets, PigletsStatus
from locations.models import Location
from tours.models import MetaTour, MetaTourRecord, Tour


class PigletsEvent(Event):
    class Meta:
        abstract = True


class PigletsMergerManager(CoreModelManager):
    def create_merger_return_group(self, parent_piglets, new_location, initiator=None,
         date=timezone.now()):
        if isinstance(parent_piglets, list):
            pks = [group.pk for group in new_born_piglets_groups]
            parent_piglets = Piglets.objects.filter(pk__in=pks)

        # create child piglets
        total_quantity = parent_piglets.get_total_quantity()
        gilts_quantity = parent_piglets.get_total_gilts_quantity()

        piglets = Piglets.objects.create(location=new_location, status=None, start_quantity=total_quantity,
            quantity=total_quantity, gilts_quantity=gilts_quantity)

        # create metatour
        metatour = MetaTour.objects.create(piglets=piglets)

        # get all relative metatour records of parent piglets
        parent_records = MetaTourRecord.objects.filter(metatour__piglets__in=parent_piglets)

        # get set of tours from records then create records for each tour
        for tour in parent_records.get_set_of_tours():
            tour.metatourrecords.create_record(metatour=metatour, tour=tour,
             quantity=parent_records.sum_quantity_by_tour(tour),
             total_quantity=total_quantity)

        # create merger
        merger = self.create(created_piglets=piglets, initiator=initiator, date=timezone.now())

        # deactivate and update piglets 
        parent_piglets.update(active=False, merger_as_parent=merger)

        return piglets


class PigletsMerger(PigletsEvent):
    created_piglets = models.OneToOneField(Piglets, on_delete=models.SET_NULL, null=True,
     related_name='merger_as_child')

    objects = PigletsMergerManager()


class PigletsSplitManager(CoreModelManager):
    def split_return_groups(self, parent_piglets, new_amount, new_gilts_amount=0, initiator=None,
         date=timezone.now()):
        if isinstance(parent_piglets, list):
            pks = [group.pk for group in new_born_piglets_groups]
            parent_piglets = Piglets.objects.filter(pk__in=pks)

        # validate
        if new_amount >= parent_piglets.quantity:
            raise DjangoValidationError(message='new_amount >= parent_piglets.quantity')

        # create split record
        split_record = self.create(parent_piglets=parent_piglets)

        # create two groups with metatours
        piglets1 = Piglets.objects.create(location=parent_piglets.location,
            status=None,
            start_quantity=(parent_piglets.quantity - new_amount),
            quantity=(parent_piglets.quantity - new_amount),
            gilts_quantity=(parent_piglets.gilts_quantity - new_gilts_amount),
            split_as_child=split_record)
        metatour1 = MetaTour.objects.create(piglets=piglets1)

        piglets2 = Piglets.objects.create(location=parent_piglets.location,
            status=None,
            start_quantity=new_amount,
            quantity=new_amount,
            gilts_quantity=new_gilts_amount,
            split_as_child=split_record)
        metatour2 = MetaTour.objects.create(piglets=piglets2)
        
        # create metarecodrs
        for parent_record in parent_piglets.metatour.records.all():
            # notice how quantity is calculated
            MetaTourRecord.objects.create_record(
                metatour=metatour1,
                tour=parent_record.tour,
                quantity=round(parent_record.percentage * new_amount / 100),
                total_quantity=new_amount)

            MetaTourRecord.objects.create_record(
                metatour=metatour2,
                tour=parent_record.tour,
                quantity=round(parent_record.percentage * new_amount / 100),
                total_quantity=new_amount)

        parent_piglets.deactivate()

        return piglets1, piglets2


class PigletsSplit(PigletsEvent):
    parent_piglets = models.OneToOneField(Piglets, on_delete=models.SET_NULL, null=True,
     related_name='piglets_split')

    objects = PigletsSplitManager()

    def __str__(self):
        return 'PigletsSplit {}'.format(self.pk)


class WeighingPigletsManager(CoreModelManager):
    def create_weighing(self, piglets_group, total_weight, place, initiator=None):
        weighing_record = self.create(
            piglets_group=piglets_group,
            total_weight=total_weight,
            average_weight=round((total_weight / piglets_group.quantity), 2),
            place=place,
            piglets_quantity=piglets_group.quantity,
            initiator=initiator,
            date=timezone.now())

        piglets_group.change_status_to('Взвешены, готовы к заселению')
        return weighing_record


class WeighingPiglets(PigletsEvent):
    WEIGHING_PLACES = [('3/4', '3/4'), ('4/8', '4/8'), ('8/5', '8/5'), ('8/6', '8/6'),
        ('8/7', '8/7')]

    piglets_group = models.ForeignKey(Piglets, on_delete=models.CASCADE, related_name="weighing_records")
    total_weight = models.FloatField()
    average_weight = models.FloatField()
    piglets_quantity = models.IntegerField()
    place = models.CharField(max_length=10, choices=WEIGHING_PLACES)

    objects = WeighingPigletsManager()


# class CullingPigletsManager(CoreModelManager):
#     def create_culling_piglets(self, piglets_group, culling_type, quantity=1, reason=None, initiator=None):
#         culling = self.create(piglets_group=piglets_group, culling_type=culling_type, reason=reason,
#             date=timezone.now(), initiator=initiator, quantity=1)
#         piglets_group.remove_piglets(quantity)
#         return culling

#     def create_culling_gilt(self, piglets_group, culling_type, quantity=1, reason=None, initiator=None):
#         culling = self.create(piglets_group=piglets_group, culling_type=culling_type, reason=reason,
#             date=timezone.now(), initiator=initiator, quantity=1, is_it_gilt=True)
#         piglets_group.remove_gilts(quantity)
#         return culling      


# class CullingPiglets(PigletsEvent):
#     CULLING_TYPES = [('spec', 'spec uboi'), ('padej', 'padej'), ('prirezka', 'prirezka')]
#     culling_type = models.CharField(max_length=50, choices=CULLING_TYPES)
#     quantity = models.IntegerField(default=1)
#     reason = models.CharField(max_length=200, null=True)

#     is_it_gilt = models.BooleanField(default=False)

#     class Meta:
#         abstract = True


# class CullingNewBornPiglets(CullingPiglets):
#     piglets_group = models.ForeignKey(NewBornPigletsGroup, on_delete=models.CASCADE)

#     objects = CullingPigletsManager()


# class CullingNomadPiglets(CullingPiglets):
#     piglets_group = models.ForeignKey(NomadPigletsGroup, on_delete=models.CASCADE)

#     objects = CullingPigletsManager()


# class RecountQuerySet(models.QuerySet):
#     def get_sum_balance(self):
#         balance_sum = self.aggregate(models.Sum('balance'))['balance__sum']
#         if balance_sum:
#             return balance_sum
#         return 0

# class RecountManager(CoreModelManager):
#     def get_queryset(self):
#         return RecountQuerySet(self.model, using=self._db)

#     def create_recount(self, piglets_group, quantity, initiator=None):
#         recount = self.create(date=timezone.now(), initiator=initiator, piglets_group=piglets_group,
#             quantity_after=quantity, quantity_before=piglets_group.quantity,
#             balance=quantity - piglets_group.quantity)
#         piglets_group.change_quantity(quantity)
#         return recount

#     def get_recounts_from_groups(self, piglets_groups_qs):
#         return self.get_queryset().filter(piglets_group__in=piglets_groups_qs)

#     def get_recounts_with_negative_balance(self, piglets_groups_qs):
#         return self.get_queryset().filter(piglets_group__in=piglets_groups_qs, balance__lt=0)

#     def get_recounts_with_positive_balance(self, piglets_groups_qs):
#         return self.get_queryset().filter(piglets_group__in=piglets_groups_qs, balance__gt=0)


# class Recount(PigletsEvent):
#     quantity_before = models.IntegerField()
#     quantity_after = models.IntegerField()
#     balance = models.IntegerField()

#     objects = RecountManager()

#     class Meta:
#         abstract = True


# class NewBornPigletsGroupRecount(Recount):
#     piglets_group = models.ForeignKey(NewBornPigletsGroup, on_delete=models.CASCADE, 
#         related_name="recounts")


# class NomadPigletsGroupRecount(Recount):
#     piglets_group = models.ForeignKey(NomadPigletsGroup, on_delete=models.CASCADE,
#         related_name="recounts")