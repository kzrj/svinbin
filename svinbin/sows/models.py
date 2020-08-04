# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
from django.db.models import Q, Prefetch, Subquery, OuterRef, Count, F, Value
from django.db.models.functions import Coalesce
from django.core.exceptions import ValidationError as DjangoValidationError

from core.models import CoreModel, CoreModelManager
from locations.models import Location
from sows_events.models import Semination
from tours.models import Tour


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


class Pig(CoreModel):
    birth_id = models.CharField(max_length=10, unique=True, null=True, blank=True)
    location = models.ForeignKey("locations.Location", on_delete=models.SET_NULL, null=True)

    class Meta:
        abstract = True


class SowsQuerySet(models.QuerySet):
    def update_status(self, title):
        status = SowStatus.objects.get(title=title)
        SowStatusRecord.objects.bulk_create(
            (SowStatusRecord(sow=sow, status_before=sow.status, status_after=status) for sow in self)
            )
            
        return self.update(status=status)

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


class SowManager(CoreModelManager):
    def get_queryset(self):
        return SowsQuerySet(self.model, using=self._db).filter(alive=True)

    def get_queryset_with_not_alive(self):
        return SowsQuerySet(self.model, using=self._db)

    def create_new_from_noname(self, farm_id, workshop):
        noname_sow = self.get_without_farm_id_in_workshop(workshop).first()
        if noname_sow:
            noname_sow.assing_farm_id(farm_id)
        return noname_sow

    def create_new_from_gilt_without_farm_id(self):
        # For init
        return self.create(location=Location.objects.get(workshop__number=1))

    def create_new_and_put_in_workshop_one(self, farm_id):
        return self.create(farm_id=farm_id,
            location=Location.objects.get(workshop__number=1))

    def create_new_from_gilt_and_put_in_workshop_one(self, farm_id):
        # DECREASE GILT QUANTITY!!!
        
        return self.create(farm_id=farm_id,
            location=Location.objects.get(workshop__number=1))

    def get_or_create_by_farm_id(self, farm_id):
        sow = self.get_queryset().filter(farm_id=farm_id).first()
        if not sow:
            return self.create_new_from_gilt_and_put_in_workshop_one(farm_id)
        return sow

    def get_without_farm_id_in_workshop(self, workshop):
        return self.get_queryset().filter(
            farm_id__isnull=True,            
            location=workshop.location
            )

    def create_or_return(self, farm_id):
        sow = self.get_queryset_with_not_alive().filter(farm_id=farm_id).first()
        if not sow:
            return self.create_new_and_put_in_workshop_one(farm_id), True

        return sow, False

    def create_from_gilts_group(self, piglets):
        # if gilt birth id = sow.farm_id
        for i in range(0, piglets.quantity):
            self.create_new_from_gilt_without_farm_id()
        

class Sow(Pig):
    farm_id = models.IntegerField(null=True, unique=True)
    status = models.ForeignKey(SowStatus, on_delete=models.SET_NULL, null=True)
    tour = models.ForeignKey('tours.Tour', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='sows')
    alive = models.BooleanField(default=True)

    objects = SowManager()

    def __str__(self):
        return 'Sow #%s' % self.farm_id

    def change_status_to(self, status_title, alive=True):
        status = SowStatus.objects.get(title=status_title)
        self.status_records.create(sow=self, status_before=self.status, status_after=status)

        self.status = status
        self.alive = alive
        self.save()

    def change_sow_current_location(self, to_location):
        self.location = to_location
        self.save()

    @property
    def get_last_farrow(self):
        return self.sowfarrow_set.all().order_by('-created_at').first()

    def assing_farm_id(self, farm_id):
        self.farm_id = farm_id
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

    def update_info_after_semination(self, tour):
        self.tour = tour
        if len(self.semination_set.filter(tour=self.tour)) == 1:
            self.change_status_to('Осеменена 1')
        if len(self.semination_set.filter(tour=self.tour)) > 1:
            self.change_status_to('Осеменена 2')

    @property
    def mark_as_nurse(self):
        if self.status.title != 'Опоросилась':
            raise DjangoValidationError(message='Кормилицей свинья может стать только после опороса.')
        self.tour = None
        self.change_status_to('Кормилица')

    @property
    def get_location(self):
        return str(self.location.get_location)


class GiltManager(CoreModelManager):
    def create_gilt(self, birth_id, mother_sow_farm_id, piglets):
        mother_sow = Sow.objects.filter(farm_id=mother_sow_farm_id).first()

        if not mother_sow:
            raise DjangoValidationError(message=f'Нет свиноматки с {mother_sow_farm_id}.')
        
        if not mother_sow.tour:
            raise DjangoValidationError(message=f'У свиноматки {mother_sow.farm_id} не текущего тура.')

        gilt = self.create(
            birth_id=birth_id,
            mother_sow=mother_sow,
            tour=mother_sow.tour,
            farrow=mother_sow.get_last_farrow
         )

        piglets.add_gilts_without_increase_quantity(1)

        return gilt


class Gilt(Pig):
    mother_sow = models.ForeignKey(Sow, on_delete=models.SET_NULL, null=True)
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
    def create_boar(self, birth_id, breed=None):
        if self.filter(birth_id=birth_id).first():
            raise DjangoValidationError(message=f'Хряк с номером {birth_id} уже существует или уже забракован')

        return self.create(birth_id=birth_id, location=Location.objects.get(workshop__number=1), breed=breed)

    def get_or_create_boar(self, birth_id, breed=None):
        return self.get_or_create(birth_id=birth_id, breed=breed,
            location=Location.objects.get(workshop__number=1))[0]


class Boar(Pig):
    breed = models.ForeignKey(BoarBreed, on_delete=models.SET_NULL, null=True)
    active = models.BooleanField(default=True)
    objects = BoarManager()
