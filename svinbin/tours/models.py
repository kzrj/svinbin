from django.db import models
from django.utils import timezone


class TourManager(models.Manager):
    def get_or_create_by_week_in_current_year(self, week_number):
        tour = Tour.objects.filter(week_number=week_number, year=timezone.now().year).first()
        if not tour:
            return self.create(start_date=timezone.now(), week_number=week_number, year=timezone.now().year)
        return tour


class Tour(models.Model):
    start_date = models.DateTimeField()
    week_number = models.IntegerField()
    year = models.IntegerField()
    # status

    objects = TourManager()

    def __str__(self):
        return "Tour #%s" % self.week_number


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
