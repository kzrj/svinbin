# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import Q, Prefetch
from django.core import exceptions

from core.models import CoreModel, CoreModelManager
from locations.models import Location


class SowStatus(CoreModel):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class GiltStatus(CoreModel):
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

    def update_tour(self, title):
        return self.update(status=SowStatus.objects.get(title=title))


class SowManager(CoreModelManager):
    def get_queryset(self):
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
        sow = Sow.objects.filter(farm_id=farm_id).first()
        if not sow:
            return self.create_new_from_gilt_and_put_in_workshop_one(farm_id)
        return sow

    def get_by_farm_id(self, farm_id):
        sow = Sow.objects.filter(farm_id=farm_id).first()
        # if not sow:
        #     raise error
        return sow

    def get_all_sows_in_workshop(self, workshop):
        return self.get_queryset().filter(
            models.Q(
                models.Q(location__workshop=workshop) |
                models.Q(location__section__workshop=workshop) |
                models.Q(location__sowGroupCell__workshop=workshop) |
                models.Q(location__sowSingleCell__workshop=workshop) |
                models.Q(location__sowAndPigletsCell__workshop=workshop)
                )
            )

    def get_not_suporos_in_workshop(self, workshop):
        return self.get_queryset().filter(
            Q(
                ~Q(status__title='Супорос'), 
            ),
            location=workshop.location
            )

    def get_suporos_in_workshop(self, workshop):
        return self.get_queryset().filter(
            Q(
                Q(status__title='Супорос') 
                ),
            location=workshop.location
            )

    def get_not_seminated_not_suporos_in_workshop(self, workshop):
        return self.get_queryset().filter(
            Q(
                ~Q(status__title='Супорос'), 
                ~Q(status__title='Осеменена'),
                Q(farm_id__isnull=False),
                ),
            location=workshop.location
            )

    def get_without_farm_id_in_workshop(self, workshop):
        return self.get_queryset().filter(
            farm_id__isnull=True,            
            location=workshop.location
            )

    def get_suporos_30(self):
        return self.get_queryset().filter(
                ~Q(ultrasound__u_type__days=60),
                tour__isnull=False,
                ultrasound__u_type__days=30,
            )

    def get_suporos_60(self):
        return self.get_queryset().filter(
                sowfarrow__sow__farm_id__isnull=True,
                tour__isnull=False,
                ultrasound__u_type__days=60,
            )

    def get_seminated(self):
        # here cant use Prefetch with semination model because of circular import
        # just return sow with tour(seminated), without usound and farrow
        return self.get_queryset().filter(
            ultrasound__sow__farm_id__isnull=True,
            sowfarrow__sow__farm_id__isnull=True,
            tour__isnull=False,
            )
            # ).prefetch_related(
            #     Prefetch(
            #         'semination_set',
            #         queryset=
            #     )
            # )


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

    def get_last_farrow(self):
        # print(self._meta.get_fields())
        return self.sowfarrow_set.all().order_by('-created_at')

    def assing_farm_id(self, farm_id):
        self.farm_id = farm_id
        self.status = SowStatus.objects.get(title='Ожидает осеменения')
        self.save()

    def get_seminations_by_tour(self, tour):
        return self.semination_set.filter(tour=tour)      

    def get_ultrasounds1_by_tour(self, tour):
        return self.ultrasound_set.filter(tour=tour)

    def get_ultrasoundsv2_by_tour(self, tour):
        return self.ultrasoundv2_set.filter(tour=tour)

    def get_farrows_by_tour(self, tour):
        return self.sowfarrow_set.filter(tour=tour)

    def get_tours_pk(self):
        return self.semination_set.all().values_list('tour', flat=True).distinct()


class GiltManager(CoreModelManager):
    def create_gilt(self, birth_id, mother_sow, cell=None):
        # carefully, here I get FIRST group.
        new_born_group = mother_sow.location.get_located_active_new_born_groups().first()

        gilt = self.create(birth_id=birth_id, mother_sow=mother_sow,
         location=mother_sow.location,
         new_born_group=new_born_group, tour=mother_sow.tour
         )
        new_born_group.add_gilts(1)

        return gilt

    def from_list_to_queryset(self, gilts_list): # test + in gilt merger
        pks = [gilt.pk for gilt in gilts_list]
        return self.get_queryset().filter(pk__in=pks)


class Gilt(Pig):
    mother_sow = models.ForeignKey(Sow, on_delete=models.SET_NULL, null=True)
    tour = models.ForeignKey('tours.Tour', on_delete=models.SET_NULL, null=True)
    status = models.ForeignKey(GiltStatus, on_delete=models.SET_NULL, null=True)
    new_born_group = models.ForeignKey('piglets.NewBornPigletsGroup', on_delete=models.SET_NULL,
     null=True, related_name='gilts')
    merger = models.ForeignKey('gilts_events.GiltMerger', on_delete=models.SET_NULL, null=True,
        related_name='gilts')
    casting_list_to_seven_five = models.ForeignKey('gilts_events.CastingListToSevenFiveEvent',
     on_delete=models.SET_NULL, null=True, related_name='gilts')

    objects = GiltManager()

    def __str__(self):
        return 'Gilt #%s' % self.birth_id


class BoarManager(CoreModelManager):
    def create_boar(self, birth_id):
        return self.create(birth_id=birth_id, location=Location.objects.get(workshop__number=1))

    def get_create_boar(self, birth_id):
        return self.get_or_create(birth_id=birth_id, location=Location.objects.get(workshop__number=1))


class Boar(Pig):
    objects = BoarManager()
