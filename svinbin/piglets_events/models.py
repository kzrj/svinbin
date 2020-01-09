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


class PigletsSplitManager(CoreModelManager):
    def split_return_groups(self, parent_piglets, new_amount, gilts_to_new=False, initiator=None,
         date=timezone.now()):
        
        # validate
        if new_amount >= parent_piglets.quantity:
            raise DjangoValidationError(message=f'new_amount >= parent_piglets.quantity.\
                Группа {parent_piglets.pk}')

        # if gilts to new. Check parent gilts quantity should be less or equal new amount
        if gilts_to_new and parent_piglets.gilts_quantity > new_amount:
            raise DjangoValidationError(message=f'new_amount должно быть больше количества ремонток \
                в родительской группе {parent_piglets.pk}. Клетка {parent_piglets.location.get_location}')

        if not gilts_to_new and (new_amount + parent_piglets.gilts_quantity) > parent_piglets.quantity:
            raise DjangoValidationError(message=f'количество в родительской группе {parent_piglets.pk} \
                меньше чем new_amount + количество ремонток')

        # create split record
        split_record = self.create(parent_piglets=parent_piglets)

        # gilts
        piglets1_group_gilts_quantity = parent_piglets.gilts_quantity
        piglets2_new_group_gilts_quantity = 0
        
        if gilts_to_new:
            piglets1_group_gilts_quantity = 0
            piglets2_new_group_gilts_quantity = parent_piglets.gilts_quantity

        # create two groups with metatours
        piglets1 = Piglets.objects.create(location=parent_piglets.location,
            status=parent_piglets.status,
            start_quantity=(parent_piglets.quantity - new_amount),
            quantity=(parent_piglets.quantity - new_amount),
            gilts_quantity=piglets1_group_gilts_quantity,
            split_as_child=split_record)
        metatour1 = MetaTour.objects.create(piglets=piglets1)

        piglets2_new_amount = Piglets.objects.create(location=parent_piglets.location,
            status=parent_piglets.status,
            start_quantity=new_amount,
            quantity=new_amount,
            gilts_quantity=piglets2_new_group_gilts_quantity,
            split_as_child=split_record)
        metatour2 = MetaTour.objects.create(piglets=piglets2_new_amount)
        
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

        return piglets1, piglets2_new_amount


class PigletsSplit(PigletsEvent):
    parent_piglets = models.OneToOneField(Piglets, on_delete=models.SET_NULL, null=True,
     related_name='split_as_parent')

    objects = PigletsSplitManager()

    def __str__(self):
        return 'PigletsSplit {}'.format(self.pk)


class PigletsMergerManager(CoreModelManager):
    def create_merger_return_group(self, parent_piglets, new_location, initiator=None,
         date=timezone.now()):
        if isinstance(parent_piglets, list):
            if isinstance(parent_piglets[0], int):
                parent_piglets = Piglets.objects.filter(pk__in=parent_piglets)
            else:
                pks = [group.pk for group in parent_piglets]
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
        # !!! when input parent_piglets is queryset it can include created piglets, qs is lazy.
        parent_piglets.exclude(pk=piglets.pk).update(active=False, merger_as_parent=merger)

        return piglets

    def merge_piglets_in_location(self, location, initiator=None, date=timezone.now()):
        piglets = location.piglets.all()

        if len(piglets) == 0:
            raise DjangoValidationError(message=f'в локации {location.pk} нет поросят.')

        if len(piglets) == 1:
            return piglets.first()

        if len(piglets) > 1:
            return self.create_merger_return_group(parent_piglets=piglets, new_location=location,
                        initiator=initiator)


    def create_from_merging_list(self, merging_list, new_location, initiator=None, date=timezone.now()):
        # parse and parentpiglets
        parent_piglets_ids = list()
        for merging_record in merging_list:
            piglets = Piglets.objects.get(id=merging_record['piglets_id'])
            weaning_piglets = piglets

            if not merging_record['changed']:
                parent_piglets_ids.append(merging_record['piglets_id'])

            else:
                # split piglets return group id with quantity
                not_merging_piglets, merging_piglets = \
                    PigletsSplit.objects.split_return_groups(parent_piglets=piglets,
                    new_amount=merging_record['quantity'],
                    gilts_to_new=merging_record['gilts_contains'],
                    initiator=initiator,
                    date=date)
                weaning_piglets = merging_piglets
                parent_piglets_ids.append(merging_piglets.id)

            # sow weaning
            sow = piglets.farrow.sow
            if sow.status.title == 'Опоросилась':
                sow.weaningsow_set.create_weaning(sow=sow, piglets=weaning_piglets, initiator=initiator,
                    date=date)

        return self.create_merger_return_group(parent_piglets_ids, new_location, initiator, date)
                

class PigletsMerger(PigletsEvent):
    created_piglets = models.OneToOneField(Piglets, on_delete=models.SET_NULL, null=True,
     related_name='merger_as_child')

    objects = PigletsMergerManager()


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


class CullingPigletsManager(CoreModelManager):
    def create_culling_piglets(self, piglets_group, culling_type, reason=None, initiator=None):
        culling = self.create(piglets_group=piglets_group, culling_type=culling_type, reason=reason,
            date=timezone.now(), initiator=initiator)
        piglets_group.remove_piglets(1)
        return culling

    def create_culling_gilt(self, piglets_group, culling_type, reason=None, initiator=None):
        piglets_group.remove_gilts(1)
        return self.create(piglets_group=piglets_group, culling_type=culling_type, reason=reason,
            date=timezone.now(), initiator=initiator, is_it_gilt=True)      


class CullingPiglets(PigletsEvent):
    CULLING_TYPES = [
        ('spec', 'spec uboi'), ('padej', 'padej'),
        ('prirezka', 'prirezka'), ('vinuzhd', 'vinuzhdennii uboi')]

    culling_type = models.CharField(max_length=50, choices=CULLING_TYPES)
    reason = models.CharField(max_length=200, null=True)
    piglets_group = models.ForeignKey(Piglets, on_delete=models.CASCADE, related_name="cullings")
    is_it_gilt = models.BooleanField(default=False)

    objects = CullingPigletsManager()


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