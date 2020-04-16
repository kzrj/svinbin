import datetime
from django.db import models
from django.db.models import Subquery, OuterRef, F, ExpressionWrapper, Q, Sum, Avg, Count, Value, Func
from django.utils import timezone
from django.apps import apps
from django.core.exceptions import ValidationError as DjangoValidationError

from core.models import CoreModel, CoreModelManager
from sows_events import models as events_models
from sows import models as sows_models
from piglets import models as piglets_models
import piglets_events


class TourQuerySet(models.QuerySet):
    def add_sow_data(self):
        subquery_seminated = events_models.Semination.objects.filter(tour__pk=OuterRef('pk')) \
                            .values('tour') \
                            .annotate(cnt=Count('sow', distinct=True)) \
                            .values('cnt')

        subquery_usound28_suporos = events_models.Ultrasound.objects.filter(
                                            tour__pk=OuterRef('pk'), u_type__days=30, result=True) \
                            .values('tour') \
                            .annotate(cnt=Count('sow', distinct=True)) \
                            .values('cnt')

        subquery_usound28_proholost = events_models.Ultrasound.objects.filter(
                                            tour__pk=OuterRef('pk'), u_type__days=30, result=False) \
                            .values('tour') \
                            .annotate(cnt=Count('sow', distinct=True)) \
                            .values('cnt')

        subquery_usound35_suporos = events_models.Ultrasound.objects.filter(
                                            tour__pk=OuterRef('pk'), u_type__days=60, result=True) \
                            .values('tour') \
                            .annotate(cnt=Count('sow', distinct=True)) \
                            .values('cnt')

        subquery_usound35_proholost = events_models.Ultrasound.objects.filter(
                                            tour__pk=OuterRef('pk'), u_type__days=60, result=False) \
                            .values('tour') \
                            .annotate(cnt=Count('sow', distinct=True)) \
                            .values('cnt')

        subquery_abort = events_models.AbortionSow.objects.filter(tour__pk=OuterRef('pk')) \
                            .values('tour') \
                            .annotate(cnt=Count('sow', distinct=True)) \
                            .values('cnt')

        return self.annotate(
            count_sow=Count('sows'),
            count_seminated=Subquery(subquery_seminated),
            count_usound28_suporos=Subquery(subquery_usound28_suporos),
            count_usound28_proholost=Subquery(subquery_usound28_proholost),
            count_usound35_suporos=Subquery(subquery_usound35_suporos),
            count_usound35_proholost=Subquery(subquery_usound35_proholost),
            count_abort=Subquery(subquery_abort),
            )

    def add_farrow_data(self):
        data = dict()
        for born_type in ['alive', 'dead', 'mummy']:
            data[f'total_born_{born_type}'] = Subquery(
                events_models.SowFarrow.objects.filter(tour__pk=OuterRef('pk')) \
                            .values('tour') \
                            .annotate(total=models.Sum(f'{born_type}_quantity')) \
                            .values('total')
                ,output_field=models.IntegerField())

        data['gilt_count'] = Subquery(sows_models.Gilt.objects.filter(tour__pk=OuterRef('pk')) \
                                .values('tour') \
                                .annotate(cnt=Count('*')) \
                                .values('cnt'),
                output_field=models.IntegerField())

        return self.annotate(**data)

    def add_count_tour_sow(self):
        data = dict()
        for ws_number in [1, 2, 3]:
            data[f'ws{ws_number}_count_tour_sow'] = Subquery(
                sows_models.Sow.objects.filter(tour__pk=OuterRef('pk')).filter(
                         Q(
                            Q(location__workshop__number=ws_number) |
                            Q(location__section__workshop__number=ws_number) |
                            Q(location__sowAndPigletsCell__workshop__number=ws_number)
                        )) \
                        .values('tour') \
                        .annotate(cnt=Count('*')) \
                        .values('cnt'),
                 output_field=models.IntegerField())

        return self.annotate(**data)        

    def add_current_not_mixed_piglets_quantity(self):
        data = dict()

        data['total_not_mixed_piglets'] = Subquery(
                    piglets_models.Piglets.objects.all() \
                            .filter(metatour__records__tour__pk=OuterRef('pk'), metatour__records__percentage=100) \
                            .values('metatour__records__tour') \
                            .annotate(qnty=Sum('quantity')) \
                            .values('qnty'),\
                    output_field=models.FloatField())
        
        # for ws_number in [3, 4, 5, 6, 7, 8]:
        #     data[f'ws{ws_number}_qnty_not_mixed'] = Subquery(
        #             piglets_models.Piglets.objects.all() \
        #                                 .filter(metatour__records__tour__pk=OuterRef('pk'), metatour__records__percentage=100) \
        #                                 .all_in_workshop(workshop_number=ws_number) \
        #                                 .values('metatour__records__tour') \
        #                                 .annotate(qnty=Sum('quantity')) \
        #                                 .values('qnty'),
        #             output_field=models.FloatField())

        return self.annotate(**data)

    def add_current_mixed_piglets_quantity(self):
        data = dict()
        data['total_mixed_piglets'] = Subquery(
                    MetaTourRecord.objects.filter(tour__pk=OuterRef('pk'),
                                                 percentage__lt=100,
                                                 metatour__piglets__active=True
                                                 ) \
                                        .values('tour') \
                                        .annotate(qnty=Sum('quantity')) \
                                        .values('qnty'),\
                    output_field=models.FloatField())

        for ws_number in [3, 4, 5, 6, 7, 8]:
            data[f'ws{ws_number}_qnty_mixed'] = Subquery(
                MetaTourRecord.objects.filter(
                         tour__pk=OuterRef('pk'),
                         percentage__lt=100,
                         metatour__piglets__active=True) \
                        .filter(
                         Q(
                            Q(metatour__piglets__location__workshop__number=ws_number) |
                            Q(metatour__piglets__location__section__workshop__number=ws_number) |
                            Q(metatour__piglets__location__pigletsGroupCell__workshop__number=ws_number) |
                            Q(metatour__piglets__location__sowAndPigletsCell__workshop__number=ws_number)
                        )) \
                    .values('tour') \
                    .annotate(qnty=Sum('quantity')) \
                    .values('qnty'),\
                output_field=models.FloatField())

        return self.annotate(**data)

    def gen_not_mixed_piglets_subquery(self, ws_number=None):
        queryset = MetaTourRecord.objects.filter(tour__pk=OuterRef(OuterRef('pk')), percentage=100)

        if ws_number:
            queryset = queryset.filter(
                Q(
                    Q(metatour__piglets__location__workshop__number=ws_number) |
                    Q(metatour__piglets__location__section__workshop__number=ws_number) |
                    Q(metatour__piglets__location__pigletsGroupCell__workshop__number=ws_number) |
                    Q(metatour__piglets__location__sowAndPigletsCell__workshop__number=ws_number)
                ))

        return queryset.values('metatour__piglets')

    def gen_mixed_piglets_subquery(self, ws_number=None):
        queryset = MetaTourRecord.objects.filter(tour__pk=OuterRef(OuterRef('pk')), percentage__lt=100)
        if ws_number:
            queryset = queryset.filter(
                Q(
                    Q(metatour__piglets__location__workshop__number=ws_number) |
                    Q(metatour__piglets__location__section__workshop__number=ws_number) |
                    Q(metatour__piglets__location__pigletsGroupCell__workshop__number=ws_number) |
                    Q(metatour__piglets__location__sowAndPigletsCell__workshop__number=ws_number)
                ))

        return queryset.values('metatour__piglets')

    def gen_weight_subquery(self, piglets_subquery, place):
        return piglets_events.models.WeighingPiglets.objects.filter(
                                piglets_group__in=Subquery(piglets_subquery), place=place) \
                            .values('piglets_group__metatour__records__tour') \
                            .annotate(weight=Sum('total_weight')) \
                            .values('weight')

    def add_weight_data_not_mixed(self):
        subquery_piglets = self.gen_not_mixed_piglets_subquery()

        data = dict()
        for place in ['3/4', '4/8', '8/5', '8/6', '8/7']:
            subquery = Subquery(self.gen_weight_subquery(subquery_piglets, place), output_field=models.FloatField())
            place = place.replace('/', '_')
            data[f'total_weight_not_mixed_{place}'] = subquery

        return self.annotate(**data)

    def gen_weight_mixed_subquery(self, subquery_mixed_piglets, subquery_percent, place):
        return piglets_events.models.WeighingPiglets.objects.filter(
                                piglets_group__in=Subquery(subquery_mixed_piglets), place=place) \
                            .values('piglets_group__metatour__records__tour') \
                            .annotate(weight=ExpressionWrapper(
                                (F('total_weight')  * Subquery(subquery_percent,
                                                                 output_field=models.FloatField()) / 100),
                                output_field=models.FloatField())) \
                            .values('piglets_group__metatour__records__tour') \
                            .annotate(all_weight=Sum('weight')) \
                            .values('all_weight')[:1]

    def add_weight_data_mixed(self):
        subquery_mixed_piglets = self.gen_mixed_piglets_subquery()

        subquery_percent = MetaTourRecord.objects.filter(metatour__piglets=OuterRef('piglets_group'),
                 tour=OuterRef(OuterRef('pk'))) \
            .annotate(percentages=Sum('percentage')) \
            .values('percentages')

        data = dict()
        for place in ['3/4', '4/8', '8/5', '8/6', '8/7']:
            subquery = Subquery(self.gen_weight_mixed_subquery(subquery_mixed_piglets, subquery_percent, place), \
                output_field=models.FloatField())
            place = place.replace('/', '_')
            data[f'total_weight_mixed_{place}'] = subquery

        return self.annotate(**data)

    def gen_avg_weight_subquery(self, piglets_subquery, place):
        return piglets_events.models.WeighingPiglets.objects.filter(
                                piglets_group__in=Subquery(piglets_subquery), place=place) \
                            .values('place') \
                            .annotate(weight=Avg('average_weight')) \
                            .values('weight')

    def add_avg_weight_data(self):
        subquery_piglets = MetaTourRecord.objects \
            .filter(tour__pk=OuterRef(OuterRef('pk'))) \
            .values('metatour__piglets')

        data = dict()
        for place in ['3/4', '4/8', '8/5', '8/6', '8/7']:
            subquery = Subquery(self.gen_avg_weight_subquery(subquery_piglets, place), \
                output_field=models.FloatField())
            place = place.replace('/', '_')
            data[f'avg_weight_{place}'] = subquery
       
        return self.annotate(**data)

    def add_weight_date(self):
        subquery_piglets = self.gen_not_mixed_piglets_subquery()

        data = dict()
        for place in ['3/4', '4/8', '8/5', '8/6', '8/7']:
            subquery = Subquery(
                piglets_events.models.WeighingPiglets.objects.filter(
                                    piglets_group__in=Subquery(subquery_piglets), place=place) \
                                .values('date')[:1]

                ,output_field=models.DateTimeField())
            place = place.replace('/', '_')
            data[f'weight_date_{place}'] = subquery

        return self.annotate(**data)

    def add_age_at_weight_date(self):
        # use after add_weight_date
        subquery_piglets = self.gen_not_mixed_piglets_subquery()

        data = dict()
        for place in ['3/4', '4/8', '8/5', '8/6', '8/7']:
            subquery = self.gen_piglets_age_at_date_subquery(OuterRef('weight_date_3_4'))
            place = place.replace('/', '_')
            data[f'age_at_{place}'] = subquery

        return self.annotate(**data)

    def gen_culling_weight_subquery(self, subquery_piglets, culling_type, ws_number=None):
        queryset =  piglets_events.models.CullingPiglets.objects.filter(
            piglets_group__in=Subquery(subquery_piglets), culling_type=culling_type)

        if ws_number:
            queryset = queryset.filter(
                        Q(
                            Q(location__workshop__number=ws_number) |
                            Q(location__section__workshop__number=ws_number) |
                            Q(location__pigletsGroupCell__workshop__number=ws_number) |
                            Q(location__sowAndPigletsCell__workshop__number=ws_number)
                        )
                    )

        return queryset.values('culling_type') \
                        .annotate(all_weight=Sum('total_weight')) \
                        .values('all_weight')

    def add_culling_weight_not_mixed_piglets(self):
        subquery_piglets = self.gen_not_mixed_piglets_subquery()

        data = dict()
        for c_type in ['padej', 'prirezka', 'vinuzhd', 'spec']:
            subquery = Subquery(self.gen_culling_weight_subquery(subquery_piglets, c_type), \
                output_field=models.FloatField())
            data[f'{c_type}_weight'] = subquery

        return self.annotate(**data)

    def gen_culling_qnty_subquery(self, subquery_piglets, culling_type, ws_number=None):
        queryset =  piglets_events.models.CullingPiglets.objects.filter(
            piglets_group__in=Subquery(subquery_piglets), culling_type=culling_type)

        if ws_number:
            queryset = queryset.filter(
                        Q(
                            Q(location__workshop__number=ws_number) |
                            Q(location__section__workshop__number=ws_number) |
                            Q(location__pigletsGroupCell__workshop__number=ws_number) |
                            Q(location__sowAndPigletsCell__workshop__number=ws_number)
                        )
                    )

        return queryset.values('culling_type') \
                        .annotate(all_qnty=Sum('quantity')) \
                        .values('all_qnty')

    def add_culling_qnty_not_mixed_piglets(self):
        subquery_piglets = self.gen_not_mixed_piglets_subquery()

        data = dict()
        for c_type in ['padej', 'prirezka', 'vinuzhd', 'spec']:
            subquery = Subquery(self.gen_culling_qnty_subquery(subquery_piglets, c_type), \
                output_field=models.FloatField())
            data[f'{c_type}_quantity'] = subquery

        return self.annotate(**data)

    def gen_culling_avg_weight_subquery(self, subquery_piglets, culling_type, ws_number=None):
        queryset =  piglets_events.models.CullingPiglets.objects.filter(
            piglets_group__in=Subquery(subquery_piglets), culling_type=culling_type)

        if ws_number:
            queryset = queryset.filter(
                        Q(
                            Q(location__workshop__number=ws_number) |
                            Q(location__section__workshop__number=ws_number) |
                            Q(location__pigletsGroupCell__workshop__number=ws_number) |
                            Q(location__sowAndPigletsCell__workshop__number=ws_number)
                        )
                    )

        return queryset.values('culling_type') \
                        .annotate(padej_avg_weight=Avg(F('total_weight') / F('quantity'),
                                                            output_field=models.FloatField())) \
                        .values('padej_avg_weight')

    def add_culling_avg_weight_not_mixed_piglets(self):
        subquery_piglets = self.gen_not_mixed_piglets_subquery()
        subquery_mixed_piglets = self.gen_mixed_piglets_subquery()

        data = dict()
        for c_type in ['padej', 'prirezka', 'vinuzhd', 'spec']:
            subquery_not_mixed = Subquery(self.gen_culling_avg_weight_subquery(subquery_piglets, c_type), \
                output_field=models.FloatField())
            data[f'{c_type}_avg_weight'] = subquery_not_mixed

            subquery_mixed = Subquery(self.gen_culling_avg_weight_subquery(subquery_mixed_piglets, c_type), \
                output_field=models.FloatField())
            data[f'{c_type}_avg_weight_mixed'] = subquery_mixed

        return self.annotate(**data)

    def add_culling_percentage_not_mixed_piglets(self):
        # use only after add_farrow_data, add_culling_qnty_not_mixed_piglets
        data = dict()
        for c_type in ['padej', 'prirezka', 'vinuzhd', 'spec']:
            data[f'{c_type}_percentage'] = ExpressionWrapper(
                    F(f'{c_type}_quantity') * 100.0 / F('total_born_alive'), \
                    output_field=models.FloatField())

        return self.annotate(**data)

    def gen_piglets_age_at_date_subquery(self, date_at=timezone.now()): 
        return events_models.SowFarrow.objects.filter(tour__pk=OuterRef('pk')) \
                                    .values('tour') \
                                    .annotate(age=Avg(Func(
                                        date_at, F('date'), function='age')
                                        )
                                    ) \
                                    .values('age')

    def add_current_piglets_age(self, date_at=timezone.now()):
        subquery = self.gen_piglets_age_at_date_subquery(date_at)

        return self.annotate(piglets_age=Subquery(subquery, output_field=models.DateTimeField()))

    def add_culling_data_by_ws(self):      
        subquery_piglets = self.gen_not_mixed_piglets_subquery()
        subquery_mixed_piglets = self.gen_mixed_piglets_subquery()

        data = dict()
        for ws_number in [3, 4, 5, 6, 7, 8]:
            for c_type in ['padej', 'prirezka', 'vinuzhd', 'spec']:
                subquery_weight = Subquery(self.gen_culling_weight_subquery(subquery_piglets, c_type, ws_number), \
                    output_field=models.FloatField())
                data[f'ws{ws_number}_{c_type}_weight'] = subquery_weight

                subquery_qnty = Subquery(self.gen_culling_qnty_subquery(subquery_piglets, c_type, ws_number), \
                    output_field=models.FloatField())
                data[f'ws{ws_number}_{c_type}_quantity'] = subquery_qnty

                subquery_avg = Subquery(self.gen_culling_avg_weight_subquery(subquery_piglets, c_type, ws_number), \
                    output_field=models.FloatField())
                data[f'ws{ws_number}_{c_type}_avg_weight'] = subquery_avg

                subquery_mixed_avg = Subquery(self.gen_culling_avg_weight_subquery(subquery_mixed_piglets,
                     c_type, ws_number), \
                    output_field=models.FloatField())
                data[f'ws{ws_number}_{c_type}_avg_weight_mixed'] = subquery_mixed_avg

        return self.annotate(**data)


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