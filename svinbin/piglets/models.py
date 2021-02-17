# -*- coding: utf-8 -*-
from datetime import datetime

from django.db import models
from django.utils import timezone
from django.db.models import Q, Sum, Avg
from django.core.exceptions import ValidationError as DjangoValidationError

from core.models import CoreModel, CoreModelManager
from tours.models import MetaTour, MetaTourRecord, Tour


class PigletsStatus(CoreModel):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class PigletsQuerySet(models.QuerySet):
    def get_total_quantity(self):
        return self.aggregate(models.Sum('quantity'))['quantity__sum']

    def active(self):
        return self.filter(active=True)

    def inactive(self):
        return self.filter(active=False)

    def piglets_with_weighing_record(self, place):
        return self.prefetch_related('weighing_records') \
                    .filter(weighing_records__place=place) \
                    .distinct()

    def piglets_without_weighing_record(self, place):
        return self.prefetch_related('weighing_records') \
                    .filter(~Q(weighing_records__place=place)) \
                    .distinct()

    def with_tour(self, week_number):
        return self.filter(metatour__records__tour__week_number=week_number)

    def all_in_workshop(self, workshop_number):
        return self.filter(Q(
            Q(location__workshop__number=workshop_number) |
            Q(location__section__workshop__number=workshop_number) |
            Q(location__pigletsGroupCell__workshop__number=workshop_number) |
            Q(location__sowAndPigletsCell__workshop__number=workshop_number)
            )
        )

    def gen_avg_birthday(self, total_quantity=None):
        if not total_quantity:
            total_quantity = self.get_total_quantity()
        avg_ts = 0

        for piglets in self:

            if not piglets.birthday:
                return None

            ts = datetime.timestamp(piglets.birthday)
            avg_item = ts * piglets.quantity / total_quantity
            avg_ts += avg_item

        return datetime.fromtimestamp(avg_ts)

    def get_bigger_group(self):
        return self.order_by('-quantity').first()


class PigletsManager(CoreModelManager):
    def get_queryset(self):
        return PigletsQuerySet(self.model, using=self._db).select_related('metatour').active()

    def get_all(self):
        return PigletsQuerySet(self.model, using=self._db)


class Piglets(CoreModel):
    location = models.ForeignKey('locations.Location', on_delete=models.SET_NULL,
        null=True, related_name='piglets')
    status = models.ForeignKey(PigletsStatus, on_delete=models.SET_NULL, null=True)

    start_quantity = models.IntegerField()
    quantity = models.IntegerField()

    merger_as_parent = models.ForeignKey('piglets_events.PigletsMerger', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='piglets_as_parents')

    split_as_child = models.ForeignKey('piglets_events.PigletsSplit', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='piglets_as_child')

    transfer_part_number = models.IntegerField(null=True, blank=True)

    active = models.BooleanField(default=True)

    birthday = models.DateTimeField(null=True, blank=True)

    objects = PigletsManager()

    class Meta:
        ordering = ['pk',]

    def __str__(self):
        return 'Piglets {}'.format(self.pk)

    def activate(self):
        self.active = True
        self.save()

    def deactivate(self):
        self.active = False
        self.save()

    def remove_piglets(self, quantity):
        self.quantity = self.quantity - quantity
        if self.quantity <= 0:
            self.active = False
        self.save()

    def change_status_to(self, status_title):
        self.status = PigletsStatus.objects.get(title=status_title)
        self.save()

    def change_status_to_without_save(self, status_title):
        self.status = PigletsStatus.objects.get(title=status_title)

    def add_piglets(self, quantity):
        self.quantity = self.quantity + quantity
        self.active = True
        self.save()

    @property
    def metatour_repr(self):
        return self.metatour.records_repr()

    def change_location(self, location):
        self.location = location
        self.save()

    def assign_transfer_part_number(self, number):
        self.transfer_part_number = number
        self.save()

    @property
    def age(self):
        if not self.birthday:
            return None
        
        return (timezone.now() - self.birthday)

    def age_at_date(self, date):
        if not self.birthday:
            return None

        return (date - self.birthday).days

    @property
    def has_splitted_as_parent(self):
        return hasattr(self, 'split_as_parent')

    @property
    def has_merged_as_parent(self):
        return self.merger_as_parent

    def has_weighed_after_date(self, created_at):
        return self.weighing_records.filter(created_at__gt=created_at).exists()

    def has_culled_after_date(self, created_at):
        return self.cullings.filter(created_at__gt=created_at).exists()

    def has_transacted_after_date(self, created_at):
        return self.transactions.filter(created_at__gt=created_at).exists()