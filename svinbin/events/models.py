# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone

from pigs.models import Sow, NewBornPigletsGroup, NomadPigletsGroup
from tours.models import Tour
from workshops.models import WorkShop
from transactions.models import Location


class Event(models.Model):
    date = models.DateTimeField(null=True)
    initiator = models.ForeignKey('workshops.WorkShopEmployee',
     on_delete=models.SET_NULL, null=True)
    
    class Meta:
        abstract = True


class SowEvent(Event):
    sow = models.ForeignKey('pigs.Sow', on_delete=models.CASCADE)
    tour = models.ForeignKey('tours.Tour', null=True, on_delete=models.CASCADE)

    class Meta:
        abstract = True

    
class SeminationManager(models.Manager):
    def create_semination(self, sow_farm_id, week, initiator=None, semination_employee=None):
        sow = Sow.objects.get_by_farm_id(sow_farm_id)
        tour = Tour.objects.get_or_create_by_week_in_current_year(week)
        semination = self.create(sow=sow, tour=tour, initiator=initiator,
         semination_employee=semination_employee, date=timezone.now())
        sow.tour = tour
        sow.change_status_to('just seminated')
        return semination


class Semination(SowEvent):
    semination_employee = models.ForeignKey('workshops.WorkShopEmployee',
     on_delete=models.SET_NULL, null=True, related_name="semination_employee")
    # boar 

    objects = SeminationManager()


class UltrasoundManager(models.Manager):
    def create_ultrasound(self, sow_farm_id, week, initiator=None, result=False):
        sow = Sow.objects.get_by_farm_id(sow_farm_id)
        tour = Tour.objects.get_tour_by_week_in_current_year(week)
        ultrasound = self.create(sow=sow, tour=tour, initiator=initiator,
         date=timezone.now(), result=result)
        if result:
            sow.change_status_to('pregnant in workshop one')
        else:
            sow.change_status_to('proholost')
        return ultrasound


class Ultrasound(SowEvent):
    result = models.BooleanField()

    objects = UltrasoundManager()


class SowFarrowManager(models.Manager):
    def create_sow_farrow(self, sow_farm_id, week, initiator=None,
        alive_quantity=0, dead_quantity=0, mummy_quantity=0):
        sow = Sow.objects.get_by_farm_id(sow_farm_id)
        sow.change_status_to('farrow, feed')
        tour = Tour.objects.get_tour_by_week_in_current_year(week)

        # check is it first sow_farrow in courrent tour
        farrow = SowFarrow.objects.filter(sow=sow, tour=tour).first()
        if farrow:
            farrow.new_born_piglets_group.add_piglets(alive_quantity)
        else:
            new_born_piglets_group = NewBornPigletsGroup.objects.create(
                location=sow.location,
                start_quantity=alive_quantity,
                quantity=alive_quantity,
                tour=tour
                )
            farrow = self.create(sow=sow, tour=tour, initiator=initiator,
                date=timezone.now(), alive_quantity=alive_quantity,
                dead_quantity=dead_quantity, mummy_quantity=mummy_quantity,
                new_born_piglets_group=new_born_piglets_group
                )

        return farrow


class SowFarrow(SowEvent):
    new_born_piglets_group = models.ForeignKey('pigs.NewBornPigletsGroup', on_delete=models.SET_NULL, null=True)
    alive_quantity = models.IntegerField(default=0)
    dead_quantity = models.IntegerField(default=0)
    mummy_quantity = models.IntegerField(default=0)

    objects = SowFarrowManager()


class SlaughterSowManager(models.Manager):
    def create_slaughter(self, sow_farm_id, slaughter_type, initiator=None, result=False):
        sow = Sow.objects.get_by_farm_id(sow_farm_id)
        slaughter = self.create(sow=sow, initiator=initiator,
         date=timezone.now(), slaughter_type=slaughter_type)
        sow.change_status_to(status_title='has slaughtered special', alive=False)

        return slaughter


class SlaughterSow(SowEvent):
    SLAUGHTER_TYPES = [('spec', 'spec uboi'), ('padej', 'padej'), ('prirezka', 'prirezka')]
    slaughter_type = models.CharField(max_length=50, choices=SLAUGHTER_TYPES)

    objects = SlaughterSowManager()


class PigletsMerger(Event):
    class Meta:
        abstract = True


class NewBornPigletsMergerManager(models.Manager):
    def create_merger(self, new_born_piglets_groups, initiator=None):
        new_born_merger = self.create(initiator=initiator, date=timezone.now())
        new_born_piglets_groups.update(merger=new_born_merger)
        return new_born_merger

    def create_merger_and_return_nomad_piglets_group(self, new_born_piglets_groups, initiator=None):
        new_born_merger = self.create_merger(new_born_piglets_groups, initiator=initiator, date=timezone.now())
        new_born_merger.create_records()
        return new_born_merger.create_nomad_group()
        

class NewBornPigletsMerger(PigletsMerger):
    nomad_group = models.OneToOneField(NomadPigletsGroup, on_delete=models.SET_NULL, null=True)

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
        nomad_group = NomadPigletsGroup.objects.create(location=location,
         start_quantity=self.count_all_piglets(), quantity=self.count_all_piglets())
        self.nomad_group = nomad_group
        self.save()
        self.piglets_groups.reset_quantity_and_deactivate()
        return nomad_group


class MergerRecord(models.Model):
    class Meta:
        abstract = True


class NewBornMergerRecordManager(models.Manager):
    def create_records(self, merger):
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
