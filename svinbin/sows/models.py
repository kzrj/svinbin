# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q, Prefetch, Subquery, OuterRef, Count, F, Value, Exists
from django.db.models.functions import Coalesce
from django.core.exceptions import ValidationError as DjangoValidationError

from core.models import CoreModel, CoreModelManager
from locations.models import Location
from sows_events.models import Semination, AssingFarmIdEvent, PigletsToSowsEvent, CullingSow, SowFarrow, \
    MarkAsGilt
from tours.models import Tour
from transactions.models import SowTransaction


class SowStatus(CoreModel):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class SowStatusRecord(CoreModel):
    status_before = models.ForeignKey(SowStatus, null=True, on_delete=models.CASCADE,
        related_name='records_before')
    status_after = models.ForeignKey(SowStatus, null=True, on_delete=models.CASCADE,
        related_name='records_after')
    sow = models.ForeignKey('sows.Sow', on_delete=models.CASCADE, related_name='status_records')
    date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f'sow status record {self.pk}'


class SowGroup(CoreModel):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class SowGroupRecord(CoreModel):
    group_before = models.ForeignKey(SowGroup, null=True, on_delete=models.CASCADE,
        related_name='records_before')
    group_after = models.ForeignKey(SowGroup, null=True, on_delete=models.CASCADE,
        related_name='records_after')
    sow = models.ForeignKey('sows.Sow', on_delete=models.CASCADE, related_name='group_records')
    date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f'sow group record {self.pk}'


class Pig(CoreModel):
    birth_id = models.CharField(max_length=10, unique=True, null=True, blank=True)
    location = models.ForeignKey("locations.Location", on_delete=models.SET_NULL, null=True)
    birthday = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True


class SowsQuerySet(models.QuerySet):
    def update_status(self, title, date=None):
        if not date:
            date=timezone.now()

        status = SowStatus.objects.get(title=title)
        SowStatusRecord.objects.bulk_create(
            (SowStatusRecord(sow=sow, status_before=sow.status, status_after=status, date=date) for sow in self)
            )
            
        return self.update(status=status)

    def update_group(self, group_title, date=None):
        if not date:
            date=timezone.now()

        sow_group = SowGroup.objects.get(title=group_title)
        SowGroupRecord.objects.bulk_create(
            (SowGroupRecord(sow=sow, group_before=sow.sow_group, group_after=sow_group, date=date) for sow in self)
            )
            
        return self.update(sow_group=sow_group)

    def get_with_seminations_in_tour(self, tour):
        return self.prefetch_related(
                Prefetch(
                    'semination_set',
                    queryset=Semination.objects.filter(tour=tour),
                    to_attr="seminations_by_tour"
                )
            )

    def get_list_of_qs_by_seminations_in_tour(self, tour):
        once_seminated_sows = list()
        more_than_once_seminated_sows = list()
        for sow in self.get_with_seminations_in_tour(tour):
            if len(sow.seminations_by_tour) == 1:
                once_seminated_sows.append(sow.pk)

            if len(sow.seminations_by_tour) > 1:
                more_than_once_seminated_sows.append(sow.pk)

        return self.filter(pk__in=once_seminated_sows), self.filter(pk__in=more_than_once_seminated_sows)

    def add_status_at_date(self, date):
        status = Subquery(SowStatusRecord.objects.filter(sow__pk=OuterRef('pk'), date__date__lte=date) \
            .values('status_after__title')[:1])

        return self.annotate(status_at_date=status)

    def add_status_at_date_count(self, status_title, en_name=''):
        data = {f'count_status_{en_name}': 
            Coalesce(Subquery(
                self.filter(status_at_date=status_title) \
                    .annotate(flag_group=Value(0)) \
                    .values('flag_group') \
                    .annotate(cnt=Count('*')) \
                    .values('cnt')
                ), 0)
        }
        return self.annotate(**data)

    def count_sows_by_statuses_at_date(self, date):
        return self.add_status_at_date(date=date) \
                .add_status_at_date_count(status_title='Супорос 35', en_name='sup35') \
                .add_status_at_date_count(status_title='Опоросилась', en_name='oporos') \
                .add_status_at_date_count(status_title='Отъем', en_name='otiem') \
                .add_status_at_date_count(status_title='Кормилица', en_name='korm') \
                .add_status_at_date_count(status_title='Аборт', en_name='abort') \

    def add_label_is_oporos_before(self, date):
        subquery = Exists(
            SowFarrow.objects.filter(sow__pk=OuterRef('pk'), date__date__lte=date))
        return self.annotate(is_oporos_before=subquery)

    def add_label_is_checking(self):
        # use after add_label_is_oporos_before
        subquery = Exists(self.filter(pk=OuterRef('pk'), is_oporos_before=False, 
          status__title__in=["Ожидат осеменения", "Осеменена 1", 
          "Осеменена 2", "Супорос 28", "Супорос 35", "Прохолост", "Аборт"]))

        return self.annotate(is_checking=subquery)

    def add_group_at_date(self, date):
        group = Subquery(SowGroupRecord.objects.filter(sow__pk=OuterRef('pk'), date__date__lte=date) \
            .values('group_after__title')[:1])

        return self.annotate(group_at_date=group)

    def add_group_at_date_count(self, group_title, en_name=''):
        data = {f'count_group_{en_name}': 
            Coalesce(Subquery(
                self.filter(group_at_date=group_title) \
                    .annotate(flag_group=Value(0)) \
                    .values('flag_group') \
                    .annotate(cnt=Count('*')) \
                    .values('cnt')
                ), 0)
        }
        return self.annotate(**data)

    def get_tours_pks(self, workshop_number):
        if workshop_number in [1, 2]:
            return self.filter(location__workshop__number=workshop_number).values_list('tour__pk', flat=True)\
                .distinct()
        if workshop_number == 3:
            return self.filter(
                    Q(location__sowAndPigletsCell__isnull=False) 
                    | Q(location__workshop__number=workshop_number))\
                    .values_list('tour__pk', flat=True).distinct()

    def add_mark_as_gilt_last_date_and_last_tour(self):
        last_date = MarkAsGilt.objects.filter(sow__pk=OuterRef('pk')) \
            .order_by('-date').values('date')[:1]
        last_tour_week = MarkAsGilt.objects.filter(sow__pk=OuterRef('pk')) \
            .order_by('-date').values('tour__week_number')[:1]

        return self.annotate(last_date_mark=Subquery(last_date), last_week_mark=Subquery(last_tour_week))

    def add_last_status_record_date(self):
        last_record_date = Subquery(
                SowStatusRecord.objects.filter(sow__pk=OuterRef('pk')).order_by('-date') \
                .values('date')[:1])

        return self.annotate(last_record_date=last_record_date)

    def add_last_status_record_date_substract_now_date(self):
        return self.annotate(sub_result_days=(timezone.now() - F('last_record_date')))

    def sows_by_statuses_count_and_downtime_qs(self, statuses, days_limit):
        sows = self.filter(status__title__in=statuses)
        return  sows.count(), \
                sows.add_last_status_record_date() \
                    .filter(last_record_date__lt=(timezone.now() - timedelta(days_limit))) \
                    .add_last_status_record_date_substract_now_date() \
                    .order_by('-sub_result_days') \
                    .select_related('location__workshop') \
                    .select_related('location__sowAndPigletsCell__section')


class SowManager(CoreModelManager):
    def get_queryset(self):
        return SowsQuerySet(self.model, using=self._db).filter(alive=True)

    def get_queryset_with_not_alive(self):
        return SowsQuerySet(self.model, using=self._db)

    def create_new_and_put_in_workshop_one(self, farm_id, birth_id=None):
        return self.create(farm_id=farm_id, birth_id=birth_id,
            location=Location.objects.get(workshop__number=1))

    def get_or_create_by_farm_id(self, farm_id, birth_id=None):
        sow = self.get_queryset().filter(farm_id=farm_id).first()
        if not sow:
            return self.create_new_and_put_in_workshop_one(farm_id, birth_id)
        return sow

    def create_or_return_then_assing_farm_id(self, farm_id, birth_id=None, initiator=None):
        sow = self.get_queryset_with_not_alive().filter(farm_id=farm_id).first()
        if not sow:
            sow = self.filter(farm_id__isnull=True, location__workshop__number__in=[1]).first()
            if sow:
                sow.assing_farm_id(farm_id=farm_id, birth_id=birth_id)
                AssingFarmIdEvent.objects.create_event(sow=sow, assing_type='gilt',
                    farm_id=farm_id, birth_id=sow.birth_id)
            else:
                raise DjangoValidationError(message=f'Больше нет ремонтных свинок в Цехе 1. Переведите из Цеха 2')
        else:
            if not sow.birth_id:
                sow.birth_id = birth_id
                sow.save()
        return sow
        
    def create_bulk_sows_from_event(self, event):
        # tested in sows_events test_models
        to_location = Location.objects.get(workshop__number=2)

        self.bulk_create([
            Sow(creation_event=event, location=event.piglets.location) 
                for i in range(0, event.quantity)])
        sows = event.sows.all()
        sows.update_status(title='Ремонтная', date=event.date)
        sows.update_group(group_title='Ремонтная', date=event.date)

        sows.first().transactions.create_many_without_status_check(sows=sows, to_location=to_location,
         initiator=event.initiator, date=event.date)

    def get_sows_at_date(self, date):
        init_events = PigletsToSowsEvent.objects.filter(date__date__lte=date)
        all_init_sows_pk = self.get_queryset_with_not_alive().filter(creation_event__in=init_events) \
            .values_list('pk', flat=True)

        all_culls_sows_pk = CullingSow.objects.filter(date__date__lte=date).values_list('sow__pk', flat=True)

        # all_sows = all_init_sows.difference(all_culls_sows)
        # after difference we cant use annotate, so hasnt used it
        pks = [sow_pk for sow_pk in all_init_sows_pk if sow_pk not in all_culls_sows_pk]

        return self.get_queryset_with_not_alive().filter(pk__in=pks)

    def count_sows_at_date(self, date):
        count_init = PigletsToSowsEvent.objects.filter(date__date__lte=date) \
            .aggregate(models.Sum('quantity'))['quantity__sum']

        count_culls = CullingSow.objects.filter(date__date__lte=date).count()

        return count_init - count_culls


class Sow(Pig):
    farm_id = models.IntegerField(null=True, unique=True)
    status = models.ForeignKey(SowStatus, on_delete=models.SET_NULL, null=True)
    tour = models.ForeignKey('tours.Tour', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='sows')
    creation_event = models.ForeignKey('sows_events.PigletsToSowsEvent', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='sows')

    sow_group = models.ForeignKey(SowGroup, on_delete=models.SET_NULL, null=True, blank=True)

    alive = models.BooleanField(default=True)

    objects = SowManager()

    def __str__(self):
        return 'Sow #%s' % self.farm_id

    def change_status_to(self, status_title, alive=True, date=None):
        if not date:
            date=timezone.now()
            
        status = SowStatus.objects.get(title=status_title)
        self.status_records.create(sow=self, status_before=self.status, status_after=status, date=date)

        self.status = status
        self.alive = alive
        self.save()

    def change_group_to(self, group_title, alive=True, date=None):
        if not date:
            date=timezone.now()

        if group_title == 'Проверяемая':
            if not self.sow_group or self.sow_group.title != 'Ремонтная':
                return None

        if group_title == 'С опоросом' and self.sow_group and self.sow_group.title == 'С опоросом':
            return None
            
        sow_group = SowGroup.objects.get(title=group_title)
        self.group_records.create(sow=self, group_before=self.sow_group, group_after=sow_group, date=date)

        self.sow_group = sow_group
        self.save()

    def change_sow_current_location(self, to_location):
        self.location = to_location
        self.save()

    @property
    def get_last_farrow(self):
        return self.sowfarrow_set.all().order_by('-created_at').first()

    def assing_farm_id(self, farm_id, birth_id=None):
        self.farm_id = farm_id
        if not self.birth_id:
            self.birth_id = birth_id
        self.status = SowStatus.objects.get(title='Ожидает осеменения')
        self.save()

    def get_seminations_by_tour(self, tour):
        return self.semination_set.filter(tour=tour)      

    @property
    def does_once_seminate_in_tour(self):
        if len(self.get_seminations_by_current_tour_values_list) == 1:
            return True
        return False

    @property
    def get_seminations_by_current_tour_values_list(self):  
        return list( 
            semination.date.strftime('%d-%m-%Y') 
            for semination in self.semination_set.all() if semination.tour == self.tour) 
    
    @property
    def get_ultrasound_30_by_current_tour_values_list(self):
        return list( 
            ultrasound.date.strftime('%d-%m-%Y')
            for ultrasound in self.ultrasound_set.all() 
                if ultrasound.tour == self.tour and ultrasound.u_type.days == 30)

    @property
    def get_ultrasound_60_by_current_tour_values_list(self):
        return list( 
            ultrasound.date.strftime('%d-%m-%Y')
            for ultrasound in self.ultrasound_set.all() 
                if ultrasound.tour == self.tour and ultrasound.u_type.days == 60)

    def get_ultrasounds1_by_tour(self, tour):
        return self.ultrasound_set.filter(tour=tour)

    def get_ultrasoundsv2_by_tour(self, tour):
        return self.ultrasoundv2_set.filter(tour=tour)

    def get_farrows_by_tour(self, tour):
        return self.sowfarrow_set.filter(tour=tour)

    def get_tours_pk(self):
        return self.semination_set.all().values_list('tour', flat=True).distinct()

    def update_info_after_semination(self, tour, date=None):
        self.tour = tour
        if len(self.semination_set.filter(tour=self.tour)) == 1:
            self.change_status_to(status_title='Осеменена 1', date=date)
            self.change_group_to(group_title='Проверяемая', date=date)
        if len(self.semination_set.filter(tour=self.tour)) > 1:
            self.change_status_to(status_title='Осеменена 2', date=date)

    @property
    def mark_as_nurse(self):
        if self.status.title != 'Опоросилась':
            raise DjangoValidationError(message='Кормилицей свинья может стать только после опороса.')
        self.tour = None
        self.change_status_to('Кормилица')

    @property
    def get_location(self):
        return str(self.location.get_location)

    def prepare_for_double_semenation(self):
        if self.location.get_workshop.number != 1:
            raise DjangoValidationError(message='Свиноматка не в Цехе 1.')

        if self.tour or not self.alive:
            self.tour = None
            self.change_status_to('Ожидает осеменения')

    @property
    def gilt_list_by_last_tour(self):
        return self.gilts.filter(tour__week_number=self.last_week_mark).values_list('birth_id', flat=True)

    @property
    def last_operations(self):
        return self.transactions.all() \
                .prepare_and_return_union_values(fields=['result',], label='перемещение') \
        .union(self.semination_set.all() \
                .prepare_and_return_union_values(fields=['result', 'from_location', 'to_location'],
                                                 label='осеменение')) \
        .union(self.ultrasound_set.all() \
                .prepare_and_return_union_values(fields=['from_location', 'to_location'], label='узи')) \
        .union(self.cullingsow_set.all() \
                .prepare_and_return_union_values(fields=['result','from_location', 'to_location'],
                                                 label='выбытие')) \
        .union(self.abortionsow_set.all() \
            .prepare_and_return_union_values(fields=['result','from_location', 'to_location'],
                                             label='аборт')) \
        .union(self.sowfarrow_set.all() \
            .prepare_and_return_union_values(fields=['result','from_location', 'to_location'], 
                                            label='опорос')) \
        .union(self.weaningsow_set.all() \
            .prepare_and_return_union_values(fields=['result','from_location', 'to_location'], 
                                            label='отъем')) \
        .union(self.markasnurse_set.all() \
            .prepare_and_return_union_values(fields=['result','from_location', 'to_location'], 
                                            label='кормилица')) \
        .order_by('-op_date')[:10]

    def change_status_to_previous_delete_current_status_record(self):
        last_record = self.status_records.first()
        self.status = last_record.status_before
        self.save()
        last_record.delete()

    def has_any_event_after(self, created_at):
        return self.semination_set.filter(created_at__gt=created_at).exists() \
               or self.ultrasound_set.filter(created_at__gt=created_at).exists() \
               or self.sowfarrow_set.filter(created_at__gt=created_at).exists() \
               or self.abortionsow_set.filter(created_at__gt=created_at).exists() \
               or self.markasnurse_set.filter(created_at__gt=created_at).exists() \
               or self.cullingsow_set.filter(created_at__gt=created_at).exists() \
               or self.transactions.filter(created_at__gt=created_at).exists()


class GiltManager(CoreModelManager):
    def create_gilt(self, birth_id, mother_sow_farm_id, piglets=None):
        mother_sow = Sow.objects.get_queryset_with_not_alive().filter(farm_id=mother_sow_farm_id).first()

        if not mother_sow:
            raise DjangoValidationError(message=f'Нет свиноматки с {mother_sow_farm_id}.')

        if self.filter(birth_id=birth_id):
            raise DjangoValidationError(message=f'{birth_id} такая бирка уже есть.')
        
        tour = mother_sow.tour
        if not tour:
            tour = mother_sow.get_last_farrow.tour

        gilt = self.create(
            birth_id=birth_id,
            mother_sow=mother_sow,
            tour=tour,
            farrow=mother_sow.get_last_farrow
         )

        return gilt


class Gilt(Pig):
    mother_sow = models.ForeignKey(Sow, on_delete=models.SET_NULL, null=True, related_name='gilts')
    tour = models.ForeignKey('tours.Tour', on_delete=models.SET_NULL, null=True)
    farrow = models.ForeignKey('sows_events.SowFarrow', on_delete=models.SET_NULL, null=True)

    active = models.BooleanField(default=True)

    objects = GiltManager()

    def __str__(self):
        return 'Gilt #%s' % self.birth_id


class BoarBreed(CoreModel):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class BoarManager(CoreModelManager):
    def create_boar(self, farm_id, birth_id=None, breed=None):
        if self.filter(farm_id=farm_id).first():
            raise DjangoValidationError(message=f'Хряк с номером {farm_id} уже существует или уже забракован')

        return self.create(farm_id=farm_id, birth_id=birth_id, location=Location.objects.get(workshop__number=1), breed=breed)

    def get_or_create_boar(self, farm_id, breed=None):
        boar, created = self.get_or_create(farm_id=farm_id)
        if created:
            boar.location = Location.objects.get(workshop__number=1)
            boar.breed = breed
            boar.save()
        return boar


class Boar(Pig):
    farm_id = models.IntegerField(null=True, unique=True)
    breed = models.ForeignKey(BoarBreed, on_delete=models.SET_NULL, null=True)
    active = models.BooleanField(default=True)
    objects = BoarManager()

    def __str__(self):
        return str(self.farm_id)
