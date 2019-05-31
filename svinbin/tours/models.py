from django.db import models
from django.utils import timezone
from django.apps import apps

from pigs.models import Sow
from events import models as events_models


class TourManager(models.Manager):
    def get_or_create_by_week_in_current_year(self, week_number):
        tour = Tour.objects.filter(week_number=week_number, year=timezone.now().year).first()
        if not tour:
            return self.create(start_date=timezone.now(), week_number=week_number, year=timezone.now().year)
        return tour

    def get_tour_by_week_in_current_year(self, week_number):
        return Tour.objects.filter(week_number=week_number, year=timezone.now().year).first()


class Tour(models.Model):
    start_date = models.DateTimeField()
    week_number = models.IntegerField()
    year = models.IntegerField()
    # status

    objects = TourManager()

    def __str__(self):
        return "Tour #%s" % self.week_number

    @property
    def get_inseminated_sows(self):
        seminations = events_models.Semination.objects.filter(tour=self)
        return Sow.objects.filter(semination__in=seminations)

    @property
    def get_ultrasounded_sows(self):
        ultrasounds = events_models.Ultrasound.objects.filter(tour=self)
        return Sow.objects.filter(ultrasound__in=ultrasounds)

    @property
    def get_ultrasounded_sows_success(self):
        ultrasounds = events_models.Ultrasound.objects.filter(tour=self, result=True)
        return Sow.objects.filter(ultrasound__in=ultrasounds)

    @property
    def get_ultrasounded_sows_fail(self):
        ultrasounds = events_models.Ultrasound.objects.filter(tour=self, result=False)
        return Sow.objects.filter(ultrasound__in=ultrasounds)


# class SowInfoTourManager(models.Manager):
#     def create_sow_info_tour_record(self, week, sow):
#         tour = Tour.objects.get_or_create_by_week_in_current_year(week)
#         return self.create(tour=tour, sow=sow)


# class SowInfoTour(models.Model):
#     sow = models.ForeignKey('sows.Sow', on_delete=models.CASCADE)
#     tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
#     sow_status_in_tour = models.CharField(max_length=30, null=True)
#     closed = models.BooleanField(default=False)

#     objects = SowInfoTourManager()

#     def __str__(self):
#         return "Info Tour#{} for sow #{}".format(self.tour.number, self.sow.birth_id)