import datetime
from django.db import models
from django.utils import timezone
from django.apps import apps
from django.core.exceptions import ValidationError as DjangoValidationError

from core.models import CoreModel, CoreModelManager
from sows_events import models as events_models
from sows import models as sows_models
from piglets import models as piglets_models


class TourQuerySet(models.QuerySet):
    def add_farrow_data(self):
        subquery_alive = events_models.SowFarrow.objects.filter(tour__pk=models.OuterRef('pk')) \
                            .values('tour') \
                            .annotate(total_alive=models.Sum('alive_quantity')) \
                            .values('total_alive')

        subquery_dead = events_models.SowFarrow.objects.filter(tour__pk=models.OuterRef('pk')) \
                            .values('tour') \
                            .annotate(total_dead=models.Sum('dead_quantity')) \
                            .values('total_dead')

        subquery_mummy = events_models.SowFarrow.objects.filter(tour__pk=models.OuterRef('pk')) \
                            .values('tour') \
                            .annotate(total_mummy=models.Sum('mummy_quantity')) \
                            .values('total_mummy')

        return self.annotate(
            total_born_alive=models.Subquery(subquery_alive, output_field=models.IntegerField()),
            total_born_dead=models.Subquery(subquery_dead, output_field=models.IntegerField()),
            total_born_mummy=models.Subquery(subquery_mummy, output_field=models.IntegerField()),
            )

    def add_current_not_mixed_piglets_quantity(self):
        subquery_piglets = piglets_models.Piglets.objects.all() \
            .with_tour_not_mixed(week_number=models.OuterRef('week_number')) \
                            .values('metatour__records__tour') \
                            .annotate(qnty=models.Sum('quantity')) \
                            .values('qnty')

        return self.annotate(
            total_not_mixed_piglets=models.Subquery(subquery_piglets, output_field=models.IntegerField()),
            )

    def add_current_mixed_piglets_quantity(self):
        subquery = MetaTourRecord.objects.filter(tour__pk=models.OuterRef('pk'),
                                                 percentage__lt=100,
                                                 metatour__piglets__active=True
                                                 ) \
                                        .values('tour') \
                                        .annotate(qnty=models.Sum('quantity')) \
                                        .values('qnty')

        return self.annotate(
            total_mixed_piglets=models.Subquery(subquery, output_field=models.IntegerField()),
            ) 


class TourManager(CoreModelManager):
    def get_queryset(self):
        return TourQuerySet(self.model, using=self._db)

    def get_monday_date_by_week_number(self, week_number, year):
        start_week_number_pre = str(year) + '-W' + str(week_number)
        return datetime.datetime.strptime(start_week_number_pre + '-1', "%Y-W%W-%w")

    def get_or_create_by_week(self, week_number, year, start_date=timezone.now()):
        tour = self.get_queryset().filter(week_number=week_number, year=year).first()
        if not tour:
            tour = self.create(start_date=start_date, week_number=week_number, year=year)
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

    # for Import_From_Farm mechanism
    def create_or_return_by_raw(self, raw_tour, start_date=None):
        week_number = int(raw_tour[2:])
        year = int('20' + raw_tour[:2])
        if not start_date:
            start_date = self.get_monday_date_by_week_number(week_number, year)
            # print(int(start_date.strftime("%V")))
        return self.get_or_create_by_week(week_number, year, start_date)

    def create_tour_from_farrow_date_string(self, farrow_date, days=135):
        semination_date = datetime.datetime.strptime(farrow_date, '%Y-%m-%d') - datetime.timedelta(days)
        week_number = int(semination_date.strftime("%V"))
        return self.get_or_create_by_week(week_number, semination_date.year, semination_date)

    def get_tours_by_piglets(self, piglets):
        return self.get_queryset().filter(metatourrecords__metatour__piglets__in=piglets).distinct()


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
    def days_left_from_start(self):
        return timezone.now() - self.start_date

    @property
    def days_left_from_farrow_approx(self):
        return timezone.now() - (self.start_date + datetime.timedelta(days=135))

    @property
    def days_left_from_farrow(self):
        if self.sowfarrow_set.all().first():
            return timezone.now() - self.sowfarrow_set.all().first().date
        return None


class MetaTourManager(CoreModelManager):
    pass


class MetaTour(CoreModel):
    piglets = models.OneToOneField('piglets.Piglets', on_delete=models.CASCADE)

    objects = MetaTourManager()

    def __str__(self):
        return 'Piglets {} MetaTour {}'.format(self.piglets, self.pk)

    def records_repr(self):
        # analog qs.values()
        return [{
                    'tour': record.tour.week_number, 
                    'percentage': round(record.percentage, 2),
                    'days_left_from_farrow_approx': str((record.tour.days_left_from_farrow_approx).days),
                    'days_left_from_farrow': str((record.tour.days_left_from_farrow).days) 
                        if record.tour.days_left_from_farrow else None
                } 
            for record in self.records.all()]


class MetaTourRecordQuerySet(models.QuerySet):
    def sum_quantity_by_tour(self, tour):
        return self.filter(tour=tour).aggregate(models.Sum('quantity'))['quantity__sum']

    def get_set_of_tours(self):
        return Tour.objects.filter(metatourrecords__in=self).distinct()


class MetaTourRecordManager(CoreModelManager):
    def get_queryset(self):
        return MetaTourRecordQuerySet(self.model, using=self._db)

    def create_record(self, metatour, tour, quantity, total_quantity):
        # total quantity is quantity by all metatour records
        if quantity <= 0 or total_quantity <= 0:
            quantity = 1
            total_quantity = 1
            
        percentage = (quantity * 100) / total_quantity
        note = None
        # validate
        if percentage > 100:
            percentage = 100
            note = f'Неверно подсчитались проценты {percentage}, \
                 у группы с количеством {metatour.piglets.quantity}, \
                 Данные : тур={tour.week_number}, quantity={quantity}, total_quantity={total_quantity}, \
                 percentage={percentage}. Проценты изменены на 100. \
                 ID piglets {metatour.piglets.pk}, piglets.quantty={metatour.piglets.quantity}, \
                 piglets.quantty={metatour.piglets.start_quantity},'

            # raise DjangoValidationError(message=f'Неверно подсчитались проценты {percentage}, \
            #      у группы с количеством {metatour.piglets.quantity}, \
            #      Данные : тур={tour.week_number}, quantity={quantity}, total_quantity={total_quantity}, \
            #      percentage={percentage}.  \
            #      ID piglets {metatour.piglets.pk}, piglets.quantty={metatour.piglets.quantity}, \
            #      piglets.quantty={metatour.piglets.start_quantity},')

        return self.create(metatour=metatour, tour=tour, quantity=quantity, percentage=percentage, note=note)

    def recount_records_by_total_quantity(self, new_total_quantity):
        self.get_queryset().update(quantity=(models.F('percentage') * new_total_quantity / 100))


class MetaTourRecord(CoreModel):
    metatour = models.ForeignKey(MetaTour, on_delete=models.CASCADE, related_name='records')
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='metatourrecords')
    quantity = models.IntegerField()
    percentage = models.FloatField()
    note = models.TextField(null=True, blank=True)

    objects = MetaTourRecordManager()

    class Meta:
        ordering = ['tour', ]

    def __str__(self):
        return 'MetaTourRecord {}'.format(self.pk)

    def increase_quantity(self, amount):
        self.quantity += amount
        self.save()