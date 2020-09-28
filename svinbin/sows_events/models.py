# -*- coding: utf-8 -*-
from datetime import timedelta, date, datetime

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
    sow_group = models.ForeignKey('sows.SowGroup', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        abstract = True

    
class SeminationManager(CoreModelManager):
    def create_semination_tour(self, sow, tour, initiator=None, semination_employee=None, boar=None,
         date=None):

        if not date:
            date=timezone.now()

        semination = self.create(sow=sow, tour=tour, initiator=initiator,
         semination_employee=semination_employee, date=date, boar=boar, sow_group=sow.sow_group)

        sow.update_info_after_semination(tour=tour, date=date)

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
             semination_employee=semination_employee, boar=boar, date=date, sow_group=sow.sow_group))    

        self.bulk_create(seminations)

        sows_qs.update(tour=tour)

        once_seminated_sows_qs, more_than_once_seminated_sows_qs = \
            sows_qs.get_list_of_qs_by_seminations_in_tour(tour)

        once_seminated_sows_qs.update_status(title='Осеменена 1', date=date)
        once_seminated_sows_qs.filter(sow_group__title='Ремонтная') \
            .update_group(group_title='Проверяемая', date=date)
        more_than_once_seminated_sows_qs.update_status(title='Осеменена 2', date=date)

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
        if not date:
            date=timezone.now()
            
        u_type = UltrasoundType.objects.get(days=days)

        ultrasound = self.create(sow=sow, tour=sow.tour, initiator=initiator,
         date=date, result=result, u_type=u_type, location=sow.location, sow_group=sow.sow_group)
        if result:
            if days == 30:
                sow.change_status_to(status_title='Супорос 28', date=date)
            if days == 60:
                sow.change_status_to(status_title='Супорос 35', date=date)
        else:
            sow.tour = None
            sow.change_status_to(status_title='Прохолост', date=date)
        return ultrasound

    def mass_ultrasound(self, sows_qs, initiator=None, result=False, days=None, date=None):
        if not date:
            date=timezone.now()

        u_type = UltrasoundType.objects.get(days=days)
        ultrasounds = list()
        for sow in sows_qs:
            ultrasounds.append(Ultrasound(sow=sow, tour=sow.tour, initiator=initiator,
             date=date, result=result, u_type=u_type, location=sow.location, sow_group=sow.sow_group))
        Ultrasound.objects.bulk_create(ultrasounds)

        if result:
            if days == 30:
                sows_qs.update_status(title='Супорос 28', date=date)
            if days == 60:
                sows_qs.update_status(title='Супорос 35', date=date)
        else:
            sows_qs.update(tour=None)
            sows_qs.update_status(title='Прохолост', date=date)


class Ultrasound(SowEvent):
    result = models.BooleanField()
    u_type = models.ForeignKey(UltrasoundType, on_delete=models.SET_NULL, null=True)
    location = models.ForeignKey('locations.Location', null=True, on_delete=models.SET_NULL,
     related_name='usounds_here')

    objects = UltrasoundManager()


class SowFarrowQuerySet(models.QuerySet):
    pass


class SowFarrowManager(CoreModelManager):
    def get_queryset(self):
        return SowFarrowQuerySet(self.model, using=self._db)

    def create_sow_farrow(self, sow, initiator=None,
        alive_quantity=0, dead_quantity=0, mummy_quantity=0, date=None):
        if not date:
            date=timezone.now()
        
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
                birthday=date
            )
        metatour = MetaTour.objects.create(piglets=piglets)
        MetaTourRecord.objects.create_record(metatour=metatour, tour=sow.tour,
         quantity=alive_quantity, total_quantity=alive_quantity, percentage=100)
        metatour.set_week_tour()

        farrow = self.create(sow=sow, tour=sow.tour, initiator=initiator,
                date=date, alive_quantity=alive_quantity,
                dead_quantity=dead_quantity, mummy_quantity=mummy_quantity,
                piglets_group=piglets, location=sow.location, sow_group=sow.sow_group
                )

        sow.change_status_to(status_title='Опоросилась', date=date)
        sow.change_group_to(group_title='С опоросом', date=date)

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

    location = models.ForeignKey('locations.Location', null=True, on_delete=models.SET_NULL,
        related_name='farrows_here')

    objects = SowFarrowManager()

    class Meta:
        ordering = ['date']


class CullingSowManager(CoreModelManager):
    def create_culling(self, sow, culling_type, weight=None, reason=None, initiator=None, date=None):
        if not date:
            date = timezone.now()
        culling = self.create(sow=sow, initiator=initiator, tour=sow.tour, reason=reason, date=date,
         culling_type=culling_type, location=sow.location, sow_status=sow.status, weight=weight,
         sow_group=sow.sow_group)
        sow.change_status_to(status_title='Брак', alive=False, date=date)
        return culling

    def in_ws(self, ws_locs, start_date=date(2020, 1, 1), end_date=datetime.today()):
        return self.filter(date__date__gte=start_date, date__date__lte=end_date,
            location__in=ws_locs)


class CullingSow(SowEvent):
    CULLING_TYPES = [('spec', 'spec uboi'), ('padej', 'padej'), ('prirezka', 'prirezka'),
     ('vinuzhd', 'vinuzhdennii uboi')]
    culling_type = models.CharField(max_length=50, choices=CULLING_TYPES)
    reason = models.CharField(max_length=300, null=True)
    location = models.ForeignKey('locations.Location', null=True, on_delete=models.SET_NULL,
     related_name='sow_cullings_here')

    sow_status = models.ForeignKey('sows.SowStatus', on_delete=models.SET_NULL, null=True, blank=True)

    weight = models.FloatField(null=True)

    objects = CullingSowManager()


class WeaningSowManager(CoreModelManager):
    def create_weaning(self, sow, piglets, tour=None, initiator=None, date=None):
        if not date:
            date = timezone.now()
        weaning = self.create(sow=sow, tour=tour, piglets=piglets, quantity=piglets.quantity,
         initiator=initiator, date=date, sow_group=sow.sow_group)

        # when set tour to None
        sow.tour = None
        sow.change_status_to(status_title='Отъем', date=date)
        return weaning


class WeaningSow(SowEvent):
    piglets = models.ForeignKey('piglets.Piglets', on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()

    objects = WeaningSowManager()


class AbortionSowManager(CoreModelManager):
    def create_abortion(self, sow, initiator=None, date=None):
        if not date:
            date = timezone.now()
        abortion = self.create(sow=sow, tour=sow.tour, initiator=initiator, date=date,
             location=sow.location, sow_group=sow.sow_group)
        sow.tour = None
        sow.change_status_to(status_title='Аборт', date=date)
        return abortion


class AbortionSow(SowEvent):
    location = models.ForeignKey('locations.Location', null=True, on_delete=models.SET_NULL,
     related_name='abort_here')
    objects = AbortionSowManager()


class MarkAsNurseManager(CoreModelManager):
    def create_nurse_event(self, sow, initiator=None, date=timezone.now()):
        if sow.status.title != 'Опоросилась':
            raise DjangoValidationError(message='Кормилицей свинья может стать только после опороса.')

        mark_as_nurse_event = self.create(sow=sow, tour=sow.tour, date=date,
          location=sow.location, initiator=initiator)
        sow.mark_as_nurse
        return mark_as_nurse_event


class MarkAsNurse(SowEvent):
    objects = MarkAsNurseManager()
    location = models.ForeignKey('locations.Location', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['date']


class MarkAsGiltManager(CoreModelManager):
    def create_init_gilt_event(self, gilt, initiator=None, date=None):
        if not date:
            date = timezone.now()
        return self.create(gilt=gilt, sow=gilt.mother_sow, tour=gilt.tour,
         location=gilt.mother_sow.location, initiator=initiator, date=date)      


class MarkAsGilt(SowEvent):
    gilt = models.OneToOneField('sows.Gilt', on_delete=models.CASCADE, related_name='mark_as_gilt_event')

    location = models.ForeignKey('locations.Location', on_delete=models.SET_NULL, null=True, blank=True)

    objects = MarkAsGiltManager()

    class Meta:
        ordering = ['date']


class PigletsToSowsEventManager(CoreModelManager):
    def create_event(self, piglets, initiator=None, date=None):
        if not date:
            date = timezone.now()

        event = self.create(piglets=piglets, metatour=piglets.metatour, quantity=piglets.quantity,
            initiator=initiator, date=date)
        event.sows.create_bulk_sows_from_event(event=event)
        piglets.deactivate()
        return event


class PigletsToSowsEvent(Event):
    piglets = models.OneToOneField('piglets.Piglets', on_delete=models.SET_NULL, null=True)
    metatour = models.OneToOneField('tours.MetaTour', on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()

    objects = PigletsToSowsEventManager()


class AssingFarmIdEventManager(CoreModelManager):
    def create_event(self, sow, assing_type, farm_id, birth_id=None, initiator=None, date=None):
        if not date:
            date = timezone.now()

        event = self.create(sow=sow, assing_type=assing_type, farm_id=farm_id, birth_id=birth_id,
         initiator=initiator)
        return event


class AssingFarmIdEvent(Event):
    sow = models.OneToOneField('sows.Sow', on_delete=models.SET_NULL, null=True)
    ASSING_TYPES = [('gilt', 'from gilt'), ('nowhere', 'nowhere')]
    assing_type = models.CharField(max_length=10, choices=ASSING_TYPES)
    farm_id = models.IntegerField(null=True)
    birth_id = models.CharField(max_length=10, null=True) 

    objects = AssingFarmIdEventManager()


# Boar Events
class CullingBoarManager(CoreModelManager):
    def create_culling_boar(self, boar, culling_type, reason, weight=None,
         initiator=None, date=None):
        if not date:
            date = timezone.now()
        boar.active = False
        boar.save()
        return self.create(boar=boar, location=boar.location, initiator=initiator,
         culling_type=culling_type, reason=reason, date=date)


class CullingBoar(Event):
    boar = models.ForeignKey('sows.Boar', on_delete=models.CASCADE)

    CULLING_TYPES = [('padej', 'padej'), ('vinuzhd', 'vinuzhdennii uboi')]
    culling_type = models.CharField(max_length=50, choices=CULLING_TYPES)
    reason = models.CharField(max_length=300, null=True)

    location = models.ForeignKey('locations.Location', null=True, on_delete=models.SET_NULL,
     related_name='boar_cullings_here')

    weight = models.FloatField(null=True)

    objects = CullingBoarManager()


class SemenBoarManager(CoreModelManager):
    def create_semen_boar(self, boar, a, b, d, morphology_score=0, final_motility_score=0,
         initiator=None, date=None):
        if not date:
            date = timezone.now()
        c = a * b / 1000
        e = c * d / 100
        f = e / 2.0
        f2 = (e / 2.1) / (e / 1.8)
        g = f * 90
        h = g - a
        return self.create(boar=boar, a=a, b=b, c=c, d=d, e=e, f=f, f2=f2, g=g, h=h,
         morphology_score=morphology_score, final_motility_score=final_motility_score,
         initiator=initiator, date=date)


class SemenBoar(Event):
    boar = models.ForeignKey('sows.Boar', on_delete=models.CASCADE)

    a = models.FloatField(verbose_name='Ejaculate volume (ml)')
    b = models.FloatField(verbose_name='Sperm Concentration (million / ml)')
    c = models.FloatField(verbose_name='Total Sperms in Ejaculate (billion)')
    d = models.FloatField(verbose_name='Motility Score')
    e = models.FloatField(verbose_name='Total Viable Sperms in Ejaculate (billion)')
    f = models.FloatField(verbose_name='Doses from this Collection v1')
    f2 = models.FloatField(verbose_name='Doses from this Collection v2')
    g = models.FloatField(verbose_name='Actual Volume of Diluted Semen Required  ')
    h = models.FloatField(verbose_name='Actual Volume of Diluent Required')

    morphology_score = models.FloatField()
    final_motility_score = models.FloatField()

    objects = SemenBoarManager()
