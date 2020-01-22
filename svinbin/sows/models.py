# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import Q, Prefetch
from django.core import exceptions
from django.core.exceptions import ValidationError as DjangoValidationError

from core.models import CoreModel, CoreModelManager
from locations.models import Location
from sows_events.models import Semination
from tours.models import Tour


class SowStatus(CoreModel):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Pig(CoreModel):
    birth_id = models.CharField(max_length=10, unique=True, null=True)
    location = models.ForeignKey("locations.Location", on_delete=models.SET_NULL, null=True)

    class Meta:
        abstract = True


class SowsQuerySet(models.QuerySet):
    def update_status(self, title):
        return self.update(status=SowStatus.objects.get(title=title))

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

    def get_all_sows_in_workshop(self, workshop):
        return self.filter(
            models.Q(
                models.Q(location__workshop=workshop) |
                models.Q(location__section__workshop=workshop) |
                models.Q(location__sowGroupCell__workshop=workshop) |
                models.Q(location__sowSingleCell__workshop=workshop) |
                models.Q(location__sowAndPigletsCell__workshop=workshop)
                )
            )


class SowManager(CoreModelManager):
    def get_queryset(self):
        return SowsQuerySet(self.model, using=self._db).filter(alive=True)

    def get_queryset_with_bot_alive(self):
        return SowsQuerySet(self.model, using=self._db)

    def init_only_create_new(self, farm_id, location):
        # for init only
        return self.create(farm_id=farm_id, location=location)

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

    def get_by_farm_id(self, farm_id):
        sow = self.get_queryset().filter(farm_id=farm_id).first()
        # if not sow:
        #     raise error
        return sow

    def get_all_sows_in_workshop(self, workshop):
        return self.get_queryset().get_all_sows_in_workshop(workshop)

    def get_without_farm_id_in_workshop(self, workshop):
        return self.get_queryset().filter(
            farm_id__isnull=True,            
            location=workshop.location
            )

    # for init at ws2
    def split_free_and_exist_farm_ids(self, farm_ids):
        exist_farm_ids = list(
            self.get_queryset().filter(farm_id__in=farm_ids).values_list('farm_id', flat=True)
            )
        free_farm_ids = list(set(farm_ids) - set(exist_farm_ids))
        return free_farm_ids, exist_farm_ids

    def create_bulk_at_ws(self, farm_ids, location):
        free_farm_ids, exist_farm_ids = self.split_free_and_exist_farm_ids(farm_ids)

        for farm_id in free_farm_ids:
            self.bulk_create([Sow(farm_id=farm_id, location=location)])

        return free_farm_ids, exist_farm_ids

    def create_or_return(self, farm_id):
        sow = self.get_queryset().filter(farm_id=farm_id).first()
        if not sow:
            return self.create_new_and_put_in_workshop_one(farm_id), True

        return sow, False

    def get_tours_with_count_sows_by_location(self, location):
        # https://medium.com/@hansonkd/the-dramatic-benefits-of-django-subqueries-and-annotations-4195e0dafb16
        sows_query = self.get_queryset() \
            .filter(
                location=location,
                tour=models.OuterRef('id')
                ) \
            .values('tour_id') \
            .annotate(cnt=models.Count('*')) \
            .values('cnt')[:1]

        tours_ids = self.get_queryset().filter(location=location).values('tour')

        tours = Tour.objects.filter(id__in=tours_ids) \
            .annotate(
                count_sows=models.Subquery(
                   sows_query, 
                   output_field=models.IntegerField()
                )
            ).values('week_number', 'count_sows')

        return tours

    def create_from_gilts_group(self, piglets):
        # if gilt birth id = sow.farm_id
        for i in range(0, piglets.quantity):
            self.create_new_from_gilt_without_farm_id()
        

class Sow(Pig):
    farm_id = models.IntegerField(null=True, unique=True)
    status = models.ForeignKey(SowStatus, on_delete=models.SET_NULL, null=True)
    tour = models.ForeignKey('tours.Tour', on_delete=models.SET_NULL, null=True, 
        related_name='sows')
    alive = models.BooleanField(default=True)

    objects = SowManager()

    def __str__(self):
        return 'Sow #%s' % self.farm_id

    def change_status_to(self, status_title, alive=True):
        self.status = SowStatus.objects.get(title=status_title)
        self.alive = alive
        self.save()

    def change_status_without_save(self, status_title):
        self.status = SowStatus.objects.get(title=status_title)

    def change_sow_current_location(self, to_location):
        self.location = to_location
        self.save()

    @property
    def get_last_farrow(self):
        return self.sowfarrow_set.all().order_by('-created_at').first()

    @property
    def is_farrow_in_current_tour(self):
        if self.sowfarrow_set.filter(tour=self.tour).first():
            return True
        return False

    def assing_farm_id(self, farm_id):
        self.farm_id = farm_id
        self.status = SowStatus.objects.get(title='Ожидает осеменения')
        self.save()

    def get_seminations_by_tour(self, tour):
        return self.semination_set.filter(tour=tour)      

    def get_seminations_by_tour_values_list(self, tour):
        return self.semination_set.filter(tour=tour).values_list('date', flat=True)

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
            self.change_status_without_save('Осеменена 1')
        if len(self.semination_set.filter(tour=self.tour)) > 1:
            self.change_status_without_save('Осеменена 2')
        self.save()

    @property
    def mark_as_nurse(self):
        if self.status.title != 'Опоросилась':
            raise DjangoValidationError(message='Кормилицей свинья может стать только после опороса.')
        self.tour = None
        self.change_status_to('Кормилица')

    @property
    def repr_location(self):
        return str(self.location.get_location)

    @property
    def get_cell(self):
        return str(self.location.sowAndPigletsCell)


class GiltManager(CoreModelManager):
    def create_gilt(self, birth_id, mother_sow):
        if not mother_sow.tour:
            raise DjangoValidationError(message=f'У свиноматки {mother_sow.farm_id} не текущего тура.')

        if mother_sow.get_last_farrow.piglets_group.active == False:
            raise DjangoValidationError(message=f'Рожденная группа поросят {mother_sow.piglets_group.pk} \
                неактивна')            

        gilt = self.create(
            birth_id=birth_id,
            mother_sow=mother_sow,
            tour=mother_sow.tour,
            farrow=mother_sow.get_last_farrow
         )

        mother_sow.get_last_farrow.piglets_group.add_gilts_without_increase_quantity(1)

        return gilt


class Gilt(Pig):
    mother_sow = models.ForeignKey(Sow, on_delete=models.SET_NULL, null=True)
    tour = models.ForeignKey('tours.Tour', on_delete=models.SET_NULL, null=True)
    farrow = models.ForeignKey('sows_events.SowFarrow', on_delete=models.SET_NULL, null=True)

    objects = GiltManager()

    def __str__(self):
        return 'Gilt #%s' % self.birth_id


class BoarManager(CoreModelManager):
    def create_boar(self, birth_id):
        return self.create(birth_id=birth_id, location=Location.objects.get(workshop__number=1))

    def get_or_create_boar(self, birth_id):
        return self.get_or_create(birth_id=birth_id, location=Location.objects.get(workshop__number=1))[0]


class Boar(Pig):
    objects = BoarManager()
