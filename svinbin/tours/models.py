from django.db import models


class Tour(models.Model):
    number = models.IntegerField()
    start_date = models.DateTimeField(null=True)
    week_number = models.IntegerField(null=True)
    # status

    def __str__(self):
        return "Tour #%s" % self.number


class InfoTourForSow(models.Model):
    sow = models.ForeignKey('sows.Sow', on_delete=models.CASCADE)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    sow_status_in_tour = models.CharField(max_length=30, null=True)
    closed = models.BoolaenField(default=False)

    def __str__(self):
        return "Info Tour#{} for sow #{}".format(self.tour.number, self.sow.birth_id)
