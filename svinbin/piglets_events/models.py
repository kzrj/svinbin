# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone

from core.models import Event, CoreModel, CoreModelManager
from sows.models import Sow
from piglets.models import NewBornPigletsGroup, NomadPigletsGroup
from tours.models import Tour
from workshops.models import WorkShop
from transactions.models import Location


class PigletsEvent(Event):
    class Meta:
        abstract = True


class PigletsMerger(PigletsEvent):
    class Meta:
        abstract = True


class PigletsMergerManager(CoreModelManager):
    pass


class NewBornPigletsMergerManager(PigletsMergerManager):
    def create_merger_without_groups(self, initiator=None):
        new_born_merger = self.create(initiator=initiator, date=timezone.now())
        return new_born_merger

    def create_merger(self, new_born_piglets_groups, initiator=None):
        new_born_merger = self.create(initiator=initiator, date=timezone.now())
        if isinstance(new_born_piglets_groups, list):
            pks = [group.pk for group in new_born_piglets_groups]
            new_born_piglets_groups = NewBornPigletsGroup.objects.filter(pk__in=pks)
        
        new_born_piglets_groups.update(merger=new_born_merger)
        return new_born_merger

    def create_merger_and_return_nomad_piglets_group(self, new_born_piglets_groups, initiator=None):
        new_born_merger = self.create_merger(new_born_piglets_groups, initiator=initiator)
        return new_born_merger.create_nomad_group()


class NewBornPigletsMerger(PigletsMerger):
    nomad_group = models.OneToOneField(NomadPigletsGroup, on_delete=models.SET_NULL, null=True,
     related_name='creating_new_born_merger')

    objects = NewBornPigletsMergerManager()

    def add_piglets_group(self, new_born_piglets_group):
        new_born_piglets_group.update(merger=self)

    def get_first_tour(self):
        return self.piglets_groups.all().first().tour

    def get_next_tour(self, existing_tours):
        group = self.piglets_groups.exclude(tour__in=existing_tours).first()
        if group:
            return group.tour
        return group

    def get_piglets_groups_by_tour(self, tour):
        return self.piglets_groups.filter(tour=tour)

    def count_all_piglets(self):
        return self.piglets_groups.aggregate(models.Sum('quantity'))['quantity__sum']

    def count_quantity_by_tour(self, tour):
        piglets_groups = self.get_piglets_groups_by_tour(tour)
        return piglets_groups.aggregate(models.Sum('quantity'))['quantity__sum']

    def get_percentage_by_tour(self, tour):
        count_piglets_by_tour = self.count_quantity_by_tour(tour)
        count_all_piglets = self.count_all_piglets()

        return (count_piglets_by_tour * 100) / count_all_piglets

    def get_percentage_by_tour_less_queries(self, count_piglets_by_tour, count_all_piglets):
        return (count_piglets_by_tour * 100) / count_all_piglets

    def count_quantity_and_percentage_by_tours(self):
        tour = self.get_first_tour()
        tours = [tour]
        quantity_by_tours = list()
        quantity_all_piglets = self.count_all_piglets()
        
        while tour:
            count_quantity_by_tour = self.count_quantity_by_tour(tour)

            quantity_by_tours.append((tour, count_quantity_by_tour,
             self.get_percentage_by_tour_less_queries(count_quantity_by_tour, quantity_all_piglets)))

            tour = self.get_next_tour(tours)
            tours.append(tour)

        return quantity_by_tours

    def create_records(self):
        return NewBornMergerRecord.objects.create_records(self)

    def create_nomad_group(self):
        location = Location.objects.create_location(WorkShop.objects.get(number=3))
        self.create_records()
        nomad_group = NomadPigletsGroup.objects.create(location=location,
         start_quantity=self.count_all_piglets(), quantity=self.count_all_piglets())
        self.nomad_group = nomad_group
        self.save()
        self.piglets_groups.reset_quantity_and_deactivate()
        return nomad_group

    def add_new_born_group(self, new_born_group):
        new_born_group.merger = self
        new_born_group.save()


class MergerRecord(CoreModel):
    class Meta:
        abstract = True


class MergerRecordManager(CoreModelManager):
    pass


class NewBornMergerRecordManager(MergerRecordManager):
    def create_records(self, merger):
        if not merger.records.all().first():
            for init_data in merger.count_quantity_and_percentage_by_tours():
                self.create(merger=merger, tour=init_data[0], quantity=init_data[1],
                 percentage=init_data[2])

        return merger.records.all()


class NewBornMergerRecord(MergerRecord):
    merger = models.ForeignKey(NewBornPigletsMerger, on_delete=models.CASCADE, related_name="records")
    tour = models.ForeignKey('tours.Tour', on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()
    percentage = models.FloatField()

    objects = NewBornMergerRecordManager()


class SplitPigletsGroup(PigletsEvent):
    class Meta:
        abstract = True


class SplitNomadPigletsGroupManager(CoreModelManager):
    def _create_split_group(self, split_event, quantity, initiator=None):
        parent_nomad_group = split_event.parent_group
        location = Location.objects.create_location(parent_nomad_group.location.get_location)
        return NomadPigletsGroup.objects.create(location=location,
            start_quantity=quantity,
            quantity=quantity,
            split_record=split_event
            )

    def split_group(self, parent_nomad_group, new_group_piglets_amount, initiator=None):
        split_event = self.create(date=timezone.now(), initiator=initiator,
            parent_group=parent_nomad_group)
        
        first_group = self._create_split_group(split_event,
         (parent_nomad_group.quantity - new_group_piglets_amount), initiator)

        second_group = self._create_split_group(split_event, new_group_piglets_amount, initiator)

        parent_nomad_group.reset_quantity_and_deactivate()

        return first_group, second_group
       

class SplitNomadPigletsGroup(SplitPigletsGroup):
    parent_group = models.OneToOneField(NomadPigletsGroup, on_delete=models.SET_NULL, null=True)

    objects = SplitNomadPigletsGroupManager()


class NomadPigletsGroupMergerManager(PigletsMergerManager):
    def create_nomad_merger(self, nomad_groups, nomad_group_join_to, initiator=None):
        nomad_groups_merger = self.create(date=timezone.now(), nomad_group_join_to=nomad_group_join_to,
         initiator=initiator)
        nomad_groups.update(groups_merger=nomad_groups_merger)
        return nomad_groups_merger

    def create_merger_and_return_nomad_piglets_group(self, nomad_groups, nomad_group_join_to,
     initiator=None):
        nomad_merger = self.create_nomad_merger(nomad_groups, nomad_group_join_to=nomad_group_join_to,
         initiator=initiator, date=timezone.now())
        nomad_merger.create_records()
        return nomad_merger.create_nomad_group()


class NomadPigletsGroupMerger(PigletsMerger):
    nomad_group = models.OneToOneField(NomadPigletsGroup, on_delete=models.SET_NULL, null=True,
     related_name='creating_nomad_merger')
    nomad_group_join_to = models.OneToOneField(NomadPigletsGroup, on_delete=models.SET_NULL, null=True,
     related_name='nomad_group_join_to')

    objects =  NomadPigletsGroupMergerManager()

    def count_all_piglets(self):
        return self.groups_merger.aggregate(models.Sum('quantity'))['quantity__sum']

    def create_records(self):
        return NomadMergerRecord.objects.create_records(self)

    def create_nomad_group(self):
        quantity = self.count_all_piglets()
        location = Location.objects.create_location(self.nomad_group_join_to.location.get_location)
        nomad_group = NomadPigletsGroup.objects.create(start_quantity=quantity,
            quantity=quantity, location=location)
        self.nomad_group = nomad_group
        self.save()
        self.groups_merger.reset_quantity_and_deactivate()
        return nomad_group


class NomadMergerRecordManager(MergerRecordManager):
    def create_records(self, merger):
        if not merger.records.all().first():
            for merge_nomad_group in merger.groups_merger.all():
                percentage = (merge_nomad_group.quantity * 100) / merger.count_all_piglets()
                self.create(merger=merger, quantity=merge_nomad_group.quantity,
                 nomad_group=merge_nomad_group,
                 percentage=percentage)

        return merger.records.all()


class NomadMergerRecord(MergerRecord):
    merger = models.ForeignKey(NomadPigletsGroupMerger, on_delete=models.CASCADE,
     related_name="records")
    nomad_group = models.OneToOneField(NomadPigletsGroup, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()
    percentage = models.FloatField()

    objects = NomadMergerRecordManager()


class RecountManager(CoreModelManager):
    def create_recount(self, piglets_group, quantity, initiator=None):
        if not piglets_group.is_quantities_same(quantity):
            recount = self.create(date=timezone.now(), initiator=initiator, piglets_group=piglets_group,
                quantity_after=quantity, quantity_before=piglets_group.quantity,
                balance=quantity-piglets_group.quantity)
            piglets_group.change_quantity(quantity)
            return recount
        return None


class Recount(PigletsEvent):
    quantity_before = models.IntegerField()
    quantity_after = models.IntegerField()
    balance = models.IntegerField()

    objects = RecountManager()

    class Meta:
        abstract = True


class NewBornPigletsGroupRecount(Recount):
    piglets_group = models.ForeignKey(NewBornPigletsGroup, on_delete=models.CASCADE, 
        related_name="recounts")


class NomadPigletsGroupRecount(Recount):
    piglets_group = models.ForeignKey(NomadPigletsGroup, on_delete=models.CASCADE,
        related_name="recounts")


class CullingPigletsManager(CoreModelManager):
    def create_culling_piglets(self, piglets_group, culling_type, quantity=1, reason=None, initiator=None):
        culling = self.create(piglets_group=piglets_group, culling_type=culling_type, reason=reason,
            date=timezone.now(), initiator=initiator, quantity=1)
        piglets_group.remove_piglets(quantity)
        return culling      


class CullingPiglets(PigletsEvent):
    CULLING_TYPES = [('spec', 'spec uboi'), ('padej', 'padej'), ('prirezka', 'prirezka')]
    culling_type = models.CharField(max_length=50, choices=CULLING_TYPES)
    quantity = models.IntegerField(default=1)
    reason = models.CharField(max_length=200, null=True)

    class Meta:
        abstract = True


class CullingNewBornPiglets(CullingPiglets):
    piglets_group = models.ForeignKey(NewBornPigletsGroup, on_delete=models.CASCADE)

    objects = CullingPigletsManager()


class CullingNomadPiglets(CullingPiglets):
    piglets_group = models.ForeignKey(NomadPigletsGroup, on_delete=models.CASCADE)

    objects = CullingPigletsManager()

