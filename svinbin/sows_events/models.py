# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError as DjangoValidationError

from core.models import Event, CoreModel, CoreModelManager
from piglets.models import Piglets, PigletsStatus
from tours.models import Tour, MetaTour, MetaTourRecord
from piglets_events.models import PigletsMerger


class SowEvent(Event):
    sow = models.ForeignKey('sows.Sow', on_delete=models.CASCADE)
    tour = models.ForeignKey('tours.Tour', null=True, on_delete=models.CASCADE)

    class Meta:
        abstract = True

    
class SeminationManager(CoreModelManager):
    def create_semination_tour(self, sow, tour, initiator=None, semination_employee=None, boar=None,
         date=None):

        if not date:
            date=timezone.now()

        semination = self.create(sow=sow, tour=tour, initiator=initiator,
         semination_employee=semination_employee, date=date, boar=boar)

        sow.update_info_after_semination(tour)

        return semination

    def create_semination(self, sow, week, initiator=None, semination_employee=None, boar=None,
         date=None):
        if not date:
            date=timezone.now()
        tour = Tour.objects.get_or_create_by_week_in_current_year(week)
        return self.create_semination_tour(sow, tour, initiator, semination_employee, boar, date)

    def mass_semination(self, sows_qs, week, initiator=None, semination_employee=None,
            boar=None, date=None):
        # sows needs as qs
        if not date:
            date=timezone.now()

        tour = Tour.objects.get_or_create_by_week_in_current_year(week)
        seminations = list()
        for sow in sows_qs:
            seminations.append(Semination(sow=sow, tour=tour, initiator=initiator,
             semination_employee=semination_employee, boar=boar, date=date))    

        self.bulk_create(seminations)

        sows_qs.update(tour=tour)

        once_seminated_sows_qs, more_than_once_seminated_sows_qs = \
            sows_qs.get_list_of_qs_by_seminations_in_tour(tour)

        once_seminated_sows_qs.update_status('Осеменена 1')
        more_than_once_seminated_sows_qs.update_status('Осеменена 2')

    def is_there_semination(self, sow, tour):
        if self.get_queryset().filter(sow=sow, tour=tour).first():
            return True
        return False

    def double_semination_or_not(self, sow, tour, boar1, semination_employee1, boar2,
         semination_employee2, date, initiator=None):
        
        if self.is_there_semination(sow, tour):
            # sow has seminated already. skip/
            return sow, False

        # seminate two times
        seminations1 = self.create_semination_tour(sow=sow, tour=tour, date=date, initiator=initiator,
            boar=boar1, semination_employee=semination_employee1)

        seminations2 = self.create_semination_tour(sow=sow, tour=tour, date=date, initiator=initiator,
            boar=boar2, semination_employee=semination_employee2)

        return sow, True


class Semination(SowEvent):
    semination_employee = models.ForeignKey(User,
     on_delete=models.SET_NULL, null=True, related_name="semination_employee")
    boar = models.ForeignKey('sows.Boar', on_delete=models.SET_NULL, null=True)

    objects = SeminationManager()


class UltrasoundType(CoreModel):
    title = models.CharField(max_length=100, null=True)
    days = models.IntegerField()
    final = models.BooleanField(default=False)

    def __str__(self):
        return 'UZI %d' % self.days


class UltrasoundManager(CoreModelManager):
    def create_ultrasound(self, sow, initiator=None, result=False, days=30, date=timezone.now()):
        u_type = UltrasoundType.objects.get(days=days)

        ultrasound = self.create(sow=sow, tour=sow.tour, initiator=initiator,
         date=date, result=result, u_type=u_type)
        if result:
            if days == 30:
                sow.change_status_to('Супорос 28')
            if days == 60:
                sow.change_status_to('Супорос 35')
        else:
            sow.tour = None
            sow.change_status_to('Прохолост')
        return ultrasound

    def mass_ultrasound(self, sows_qs, initiator=None, result=False, days=None):
        u_type = UltrasoundType.objects.get(days=days)
        ultrasounds = list()
        for sow in sows_qs:
            ultrasounds.append(Ultrasound(sow=sow, tour=sow.tour, initiator=initiator,
             date=timezone.now(), result=result, u_type=u_type))
        Ultrasound.objects.bulk_create(ultrasounds)

        if result:
            if days == 30:
                sows_qs.update_status('Супорос 28')
            if days == 60:
                sows_qs.update_status('Супорос 35')
        else:
            sows_qs.update(tour=None)
            sows_qs.update_status('Прохолост')


class Ultrasound(SowEvent):
    result = models.BooleanField()
    u_type = models.ForeignKey(UltrasoundType, on_delete=models.SET_NULL, null=True)

    objects = UltrasoundManager()


class SowFarrowQuerySet(models.QuerySet):
    pass


class SowFarrowManager(CoreModelManager):
    def get_queryset(self):
        return SowFarrowQuerySet(self.model, using=self._db)

    def create_sow_farrow(self, sow, initiator=None,
        alive_quantity=0, dead_quantity=0, mummy_quantity=0, date=timezone.now()):
        
        # validate
        if not sow.tour:
            raise DjangoValidationError(message='У свиньи нет тура.')

        if self.get_queryset().filter(sow=sow, tour=sow.tour).first():
            raise DjangoValidationError(message='Свинья уже опоросилась в этом туре.')

        if not sow.location.sowAndPigletsCell:
            raise DjangoValidationError(message='Свинья не в клетке 3-го цеха.')            

        if alive_quantity == 0 and dead_quantity == 0 and mummy_quantity == 0:
            raise DjangoValidationError(message='Не может быть 0 поросят.')

        # We assume that sow has one farrow per tour.
        piglets = Piglets.objects.create(
                location=sow.location,
                status=PigletsStatus.objects.get(title='Родились, кормятся'),
                start_quantity=alive_quantity,
                quantity=alive_quantity,
            )
        metatour = MetaTour.objects.create(piglets=piglets)
        MetaTourRecord.objects.create_record(metatour, sow.tour, alive_quantity, alive_quantity)
        metatour.set_week_tour()

        farrow = self.create(sow=sow, tour=sow.tour, initiator=initiator,
                date=date, alive_quantity=alive_quantity,
                dead_quantity=dead_quantity, mummy_quantity=mummy_quantity,
                piglets_group=piglets
                )

        sow.change_status_to('Опоросилась')

        if alive_quantity <= 0:
            piglets.deactivate()
        
        if sow.location.piglets.all().count() > 1:
            # merge piglets
            PigletsMerger.objects.create_merger_return_group(parent_piglets=sow.location.piglets.all(),
                new_location=sow.location, initiator=initiator)

        return farrow


class SowFarrow(SowEvent):
    piglets_group = models.OneToOneField('piglets.Piglets', on_delete=models.SET_NULL,
     null=True, related_name='farrow')
    alive_quantity = models.IntegerField(default=0)
    dead_quantity = models.IntegerField(default=0)
    mummy_quantity = models.IntegerField(default=0)

    objects = SowFarrowManager()

    class Meta:
        ordering = ['date']


class CullingSowManager(CoreModelManager):
    def create_culling(self, sow, culling_type, reason=None, initiator=None, date=timezone.now()):
        culling = self.create(sow=sow, initiator=initiator, tour=sow.tour, reason=reason,
         date=date, culling_type=culling_type)
        sow.change_status_to(status_title='Брак', alive=False)
        return culling


class CullingSow(SowEvent):
    CULLING_TYPES = [('spec', 'spec uboi'), ('padej', 'padej'), ('prirezka', 'prirezka'),
     ('vinuzhd', 'vinuzhdennii uboi')]
    culling_type = models.CharField(max_length=50, choices=CULLING_TYPES)
    reason = models.CharField(max_length=300, null=True)

    objects = CullingSowManager()


class WeaningSowManager(CoreModelManager):
    def create_weaning(self, sow, piglets, tour=None, initiator=None, date=timezone.now()):
        weaning = self.create(sow=sow, tour=tour, piglets=piglets, quantity=piglets.quantity,
         initiator=initiator, date=date)

        # when set tour to None
        sow.tour = None
        sow.change_status_to(status_title='Отъем')
        return weaning


class WeaningSow(SowEvent):
    piglets = models.OneToOneField('piglets.Piglets', on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()

    objects = WeaningSowManager()


class AbortionSowManager(CoreModelManager):
    def create_abortion(self, sow, initiator=None, date=timezone.now()):
        abortion = self.create(sow=sow, tour=sow.tour, initiator=initiator, date=date)
        sow.tour = None
        sow.change_status_to(status_title='Аборт')
        return abortion


class AbortionSow(SowEvent):
    objects = AbortionSowManager()