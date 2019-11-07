import datetime
from django.db import models
from django.utils import timezone
from django.apps import apps

from core.models import CoreModel, CoreModelManager
from sows_events import models as events_models
from sows import models as sows_models
from piglets import models as piglets_models
from piglets_events import models as piglets_events_models


class TourQuerySet(models.QuerySet):
    def get_recounts_balance_data(self):
        data = dict()
        for tour in self:
            data[str(tour)] = tour.get_recount_balance_info
        return data


class TourManager(CoreModelManager):
    def get_queryset(self):
        return TourQuerySet(self.model, using=self._db)

    def get_or_create_by_week(self, week_number, year):
        tour = self.get_queryset().filter(week_number=week_number, year=year).first()
        if not tour:
            tour = self.create(start_date=timezone.now(), week_number=week_number, year=year)
        return tour

    def get_or_create_by_week_in_current_year(self, week_number):
        return self.get_or_create_by_week(week_number, timezone.now().year)

    def get_tour_by_week_in_current_year(self, week_number):
        return self.get_queryset().filter(week_number=week_number, year=timezone.now().year).first()

    def get_tours_in_workshop_by_sows(self, workshop):
        tours_list = list(sows_models.Sow.objects.get_all_sows_in_workshop(workshop) \
            .values_list('tour', flat=True))
        tours_list = list(set(tours_list))
        return self.get_queryset().filter(pk__in=tours_list).prefetch_related('sows')

    # move to workshop or create analog
    def get_tours_in_workshop_by_sows_and_piglets(self, workshop):
        sows_tours_list = list(sows_models.Sow.objects.get_all_sows_in_workshop(workshop) \
            .values_list('tour', flat=True))
        piglets_tours_list = list(piglets_models.NewBornPigletsGroup.objects \
            .filter(location__workshop=workshop) \
            .values_list('tour', flat=True))
        tours_list = list(set(sows_tours_list + piglets_tours_list))
        return self.get_queryset().filter(pk__in=tours_list)

    def create_or_return_by_raw(self, raw_tour):
        week_number = int(raw_tour[2:])
        year = int('20' + raw_tour[:2])
        return self.get_or_create_by_week(week_number, year)


class Tour(CoreModel):
    start_date = models.DateTimeField()
    week_number = models.IntegerField()
    year = models.IntegerField()

    objects = TourManager()

    def __str__(self):
        return "Тур {} {}г".format(self.week_number, self.year)

    @property
    def get_inseminated_sows(self):
        seminations = events_models.Semination.objects.filter(tour=self)
        return sows_models.Sow.objects.filter(semination__in=seminations)

    @property
    def get_ultrasounded_sows(self):
        ultrasounds = events_models.Ultrasound.objects.filter(tour=self)
        return sows_models.Sow.objects.filter(ultrasound__in=ultrasounds)

    @property
    def get_ultrasounded_sows_success(self):
        ultrasounds = events_models.Ultrasound.objects.filter(tour=self, result=True)
        return sows_models.Sow.objects.filter(ultrasound__in=ultrasounds)

    @property
    def get_ultrasounded_sows_fail(self):
        ultrasounds = events_models.Ultrasound.objects.filter(tour=self, result=False)
        return sows_models.Sow.objects.filter(ultrasound__in=ultrasounds)

    @property
    def get_positive_recounts_balance(self):
        return piglets_events_models.NewBornPigletsGroupRecount.objects \
            .get_recounts_with_positive_balance(self.new_born_piglets.all()) \
            .get_sum_balance()

    @property
    def get_negative_recounts_balance(self):
        return piglets_events_models.NewBornPigletsGroupRecount.objects \
            .get_recounts_with_negative_balance(self.new_born_piglets.all()) \
            .get_sum_balance()

    @property
    def get_recount_balance_info(self):
        negative, positive = self.get_negative_recounts_balance, self.get_positive_recounts_balance
        return {
            'negative': negative,
            'positive': positive,
            'balance': negative + positive,
            'count_newborn_piglets': self.new_born_piglets.all().aggregate(models.Sum('quantity'))\
                ['quantity__sum']
        }
