import datetime
from django.db import models
from django.db.models import Subquery, OuterRef, F, ExpressionWrapper, Q, Sum, Avg, Count, Value, Func, \
    Case, When
from django.db.models.functions import Coalesce, Greatest
from django.utils import timezone
from django.core.exceptions import ValidationError as DjangoValidationError

from core.models import CoreModel, CoreModelManager
from sows_events import models as events_models
from sows import models as sows_models
from piglets import models as piglets_models
import piglets_events
import transactions


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

    def add_week_weight(self):
        data = dict()

        for place in ['3/4', '4/8', '8/5', '8/6', '8/7']:
            place_formatted = place.replace('/', '_')
            weights_subquery = piglets_events.models.WeighingPiglets.objects.filter(
                                    week_tour__pk=OuterRef('pk'), place=place,) \
                                .values('place') 

            # total weights
            weights_subquery_total_weight = weights_subquery.annotate(weight=Sum('total_weight')) \
                .values('weight')
            data[f'week_weight_{place_formatted}'] = Coalesce(Subquery(weights_subquery_total_weight,
                 output_field=models.FloatField()), 0)

            # avg weights
            weights_subquery_avg_weight = weights_subquery.annotate(avg_weight=Avg('average_weight')) \
                .values('avg_weight')
            data[f'week_weight_avg_{place_formatted}'] = Coalesce(Subquery(weights_subquery_avg_weight,
                 output_field=models.FloatField()), 0)

            # qnty weights
            weights_subquery_qnty_weight = weights_subquery.annotate(qnty_weight=Sum('piglets_quantity')) \
                .values('qnty_weight')
            data[f'week_weight_qnty_{place_formatted}'] = Coalesce(Subquery(weights_subquery_qnty_weight,
                 output_field=models.FloatField()), 0)

        return self.annotate(**data)

    def add_week_weight_ws8_v2(self):
        # avg by week_tour
        weights_subquery = piglets_events.models.WeighingPiglets.objects.filter(
                                    week_tour__pk=OuterRef('pk'),
                                    place__in=['8/5', '8/6', '8/7']) \
                                .values('week_tour')

        weights_subquery_avg_weight = weights_subquery.annotate(avg_weight=Avg('average_weight')) \
                .values('avg_weight')

        return self.annotate(
            week_weight_qnty_ws8=F('week_weight_qnty_8_5') + F('week_weight_qnty_8_6') + \
                F('week_weight_qnty_8_7'),
            week_weight_avg_ws8=Coalesce(Subquery(weights_subquery_avg_weight,
                 output_field=models.FloatField()), 0)
            )

    def add_culling_data_by_week_tour(self):
        data = dict()

        for ws_number in [3, 4, 5, 6, 7, 8]:
            for c_type in ['padej', 'prirezka', 'vinuzhd', 'spec']:
                culling_subquery = piglets_events.models.CullingPiglets.objects \
                    .filter(
                        Q(
                            Q(location__workshop__number=ws_number) |
                            Q(location__section__workshop__number=ws_number) |
                            Q(location__pigletsGroupCell__workshop__number=ws_number) |
                            Q(location__sowAndPigletsCell__workshop__number=ws_number)
                        )
                    ) \
                    .filter(
                        culling_type=c_type,
                        week_tour__pk=OuterRef('pk')
                    )
                        
                culling_subquery_qnty = culling_subquery \
                    .values('culling_type') \
                    .annotate(qnty=Sum('quantity')) \
                    .values('qnty')

                data[f'ws{ws_number}_{c_type}_quantity'] = Subquery(culling_subquery_qnty,
                     output_field=models.IntegerField())

                if ws_number in [5, 6, 7]:
                    if c_type == 'prirezka':
                        continue

                    if c_type == 'spec':
                        culling_subquery_avg_weight = culling_subquery \
                            .values('culling_type') \
                            .annotate(avg_weight=Avg(F('total_weight') / F('quantity'), output_field=models.FloatField())) \
                            .values('avg_weight')

                        data[f'ws{ws_number}_{c_type}_avg_weight'] = Subquery(culling_subquery_avg_weight,
                         output_field=models.FloatField())

        return self.annotate(**data)

    def add_count_transfer_to_7_5(self):
        data = dict()

        for ws_number in [5, 6, 7]:
            trs_subquery = transactions.models.PigletsTransaction.objects \
                .filter(to_location__workshop__number=11, week_tour=OuterRef('pk')) \
                .filter(Q(
                        Q(from_location__workshop__number=ws_number) |
                        Q(from_location__section__workshop__number=ws_number) |
                        Q(from_location__pigletsGroupCell__workshop__number=ws_number) |
                        Q(from_location__sowAndPigletsCell__workshop__number=ws_number)
                    )) \
                .values('week_tour') \
                .annotate(qnty=models.Sum('quantity')) \
                .values('qnty')

            data[f'ws{ws_number}_qnty_to_7_5'] = Subquery(trs_subquery, output_field=models.IntegerField())

        return self.annotate(**data)

    def add_culling_percentage(self):
        data = dict()

        data['ws3_padej_percentage'] = Case(
                When(Q(total_born_alive__isnull=True) | Q(total_born_alive=0), then=0.0),
                When(total_born_alive__gt=0, 
                        then=ExpressionWrapper(
                            F('ws3_padej_quantity') * 100.0 / F('total_born_alive'),
                            output_field=models.FloatField())
                    ), output_field=models.FloatField()
                )

        data['ws3_prirezka_percentage'] = Case(
                When(Q(total_born_alive__isnull=True) | Q(total_born_alive=0), then=0.0),
                When(total_born_alive__gt=0, 
                        then=ExpressionWrapper(
                            F('ws3_prirezka_quantity') * 100.0 / F('total_born_alive'),
                            output_field=models.FloatField())
                    ), output_field=models.FloatField()
                )

        for ws_number, place_number in zip([4, 8, 5, 6, 7], ['3_4', '4_8', '8_5', '8_6', '8_7']):
            padej_lookup1 = {f'week_weight_qnty_{place_number}__isnull': True, }
            padej_lookup2 = {f'week_weight_qnty_{place_number}': 0, }
            padej_lookup3 = {f'week_weight_qnty_{place_number}__gt': 0, }

            data[f'ws{ws_number}_padej_percentage'] = Case(
                When(Q(**padej_lookup1) | Q(**padej_lookup2), then=0.0),
                When(**padej_lookup3, 
                        then=ExpressionWrapper(
                            F(f'ws{ws_number}_padej_quantity') * 100.0 / F(f'week_weight_qnty_{place_number}'),
                            output_field=models.FloatField())
                    ), output_field=models.FloatField()
                )

            # ws4_prirezka_percentage=Case(
            #     When(Q(week_weight_qnty_3_4__isnull=True) | Q(week_weight_qnty_3_4=0), then=0.0),
            #     When(week_weight_qnty_3_4__gt=0, 
            #             then=ExpressionWrapper(
            #                 F('ws4_prirezka_quantity') * 100.0 / F('week_weight_qnty_3_4'),
            #                 output_field=models.FloatField())
            #         ), output_field=models.FloatField()
            #     ),
            # ws4_vinuzhd_percentage=Case(
            #     When(Q(week_weight_qnty_3_4__isnull=True) | Q(week_weight_qnty_3_4=0), then=0.0),
            #     When(week_weight_qnty_3_4__gt=0, 
            #             then=ExpressionWrapper(
            #                 F('ws4_vinuzhd_quantity') * 100.0 / F('week_weight_qnty_3_4'),
            #                 output_field=models.FloatField())
            #         ), output_field=models.FloatField()
            #     ),



        return self.annotate(**data
            # ws3_padej_percentage=test,
            # ws3_prirezka_percentage=Case(
            #     When(Q(total_born_alive__isnull=True) | Q(total_born_alive=0), then=0.0),
            #     When(total_born_alive__gt=0, 
            #             then=ExpressionWrapper(
            #                 F('ws3_prirezka_quantity') * 100.0 / F('total_born_alive'),
            #                 output_field=models.FloatField())
            #         ), output_field=models.FloatField()
            #     ),

            # ws4_padej_percentage=Case(
            #     When(Q(week_weight_qnty_3_4__isnull=True) | Q(week_weight_qnty_3_4=0), then=0.0),
            #     When(week_weight_qnty_3_4__gt=0, 
            #             then=ExpressionWrapper(
            #                 F('ws4_padej_quantity') * 100.0 / F('week_weight_qnty_3_4'),
            #                 output_field=models.FloatField())
            #         ), output_field=models.FloatField()
            #     ),
            # ws4_prirezka_percentage=Case(
            #     When(Q(week_weight_qnty_3_4__isnull=True) | Q(week_weight_qnty_3_4=0), then=0.0),
            #     When(week_weight_qnty_3_4__gt=0, 
            #             then=ExpressionWrapper(
            #                 F('ws4_prirezka_quantity') * 100.0 / F('week_weight_qnty_3_4'),
            #                 output_field=models.FloatField())
            #         ), output_field=models.FloatField()
            #     ),
            # ws4_vinuzhd_percentage=Case(
            #     When(Q(week_weight_qnty_3_4__isnull=True) | Q(week_weight_qnty_3_4=0), then=0.0),
            #     When(week_weight_qnty_3_4__gt=0, 
            #             then=ExpressionWrapper(
            #                 F('ws4_vinuzhd_quantity') * 100.0 / F('week_weight_qnty_3_4'),
            #                 output_field=models.FloatField())
            #         ), output_field=models.FloatField()
            #     ),


            # ws8_padej_percentage=ExpressionWrapper(
            #     F('ws8_padej_quantity') * 100.0 / F('week_weight_qnty_4_8'), output_field=models.FloatField()),
            # ws8_vinuzhd_percentage=ExpressionWrapper(
            #     F('ws8_vinuzhd_quantity') * 100.0 / F('week_weight_qnty_4_8'), output_field=models.FloatField()),

            # ws5_padej_percentage=ExpressionWrapper(
            #     F('ws5_padej_quantity') * 100.0 / F('week_weight_qnty_8_5'), output_field=models.FloatField()),
            # ws5_vinuzhd_percentage=ExpressionWrapper(
            #     F('ws5_vinuzhd_quantity') * 100.0 / F('week_weight_qnty_8_5'), output_field=models.FloatField()),

            # ws6_padej_percentage=ExpressionWrapper(
            #     F('ws6_padej_quantity') * 100.0 / F('week_weight_qnty_8_6'), output_field=models.FloatField()),
            # ws6_vinuzhd_percentage=ExpressionWrapper(
            #     F('ws6_vinuzhd_quantity') * 100.0 / F('week_weight_qnty_8_6'), output_field=models.FloatField()),   

            # ws7_padej_percentage=ExpressionWrapper(
            #     F('ws7_padej_quantity') * 100.0 / F('week_weight_qnty_8_7'), output_field=models.FloatField()),
            # ws7_vinuzhd_percentage=ExpressionWrapper(
            #     F('ws7_vinuzhd_quantity') * 100.0 / F('week_weight_qnty_8_7'), output_field=models.FloatField())
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

    # for Import_From_Farm mechanism
    def create_or_return_by_raw(self, raw_tour, start_date=None):
        week_number = int(raw_tour[2:])
        year = int('20' + raw_tour[:2])
        if not start_date:
            start_date = self.get_monday_date_by_week_number(week_number, year)
        return self.get_or_create_by_week(week_number, year, start_date)

    def create_tour_from_farrow_date_string(self, farrow_date, days=135):
        semination_date = datetime.datetime.strptime(farrow_date, '%Y-%m-%d') \
            - datetime.timedelta(days)
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
    week_tour = models.ForeignKey(Tour, on_delete=models.SET_NULL, null=True)

    objects = MetaTourManager()

    def __str__(self):
        return 'Piglets {} MetaTour {}'.format(self.piglets, self.pk)

    def records_repr(self):
        return [{
                    'tour': record.tour.week_number, 
                    'percentage': round(record.percentage, 2),
                    'quantity': round(record.quantity, 2),
                    'days_left_from_farrow_approx': str((record.tour.days_left_from_farrow_approx).days),
                    'days_left_from_farrow': str((record.tour.days_left_from_farrow).days) 
                        if record.tour.days_left_from_farrow else None
                } 
            for record in self.records.all()]

    def set_week_tour(self):
        record = self.records.all().order_by('-percentage', 'tour__year', 'tour__week_number').first()
        if record:
            self.week_tour = record.tour
            self.save()


class MetaTourRecordQuerySet(models.QuerySet):
    def sum_quantity_by_tour(self, tour):
        return self.filter(tour=tour).aggregate(models.Sum('quantity'))['quantity__sum']

    def get_set_of_tours(self):
        return Tour.objects.filter(metatourrecords__in=self).distinct()


class MetaTourRecordManager(CoreModelManager):
    def get_queryset(self):
        return MetaTourRecordQuerySet(self.model, using=self._db)

    def create_record(self, metatour, tour, quantity, total_quantity, percentage=None):
        # total quantity is quantity by all metatour records
        # if total_quantity <= 0:
        #     total_quantity = 1
        
        if not percentage:
            percentage = (quantity * 100) / total_quantity

        note = None
        if percentage > 100:
            percentage = 100
            note = f'Новая версия. Неверно подсчитались проценты {percentage}, \
                 у группы с количеством {metatour.piglets.quantity}, \
                 Данные : тур={tour.week_number}, quantity={quantity}, total_quantity={total_quantity}, \
                 percentage={percentage}. Проценты изменены на 100. \
                 ID piglets {metatour.piglets.pk}, piglets.quantty={metatour.piglets.quantity}, \
                 piglets.quantty={metatour.piglets.start_quantity},'

        return self.create(metatour=metatour, tour=tour, quantity=quantity,
            percentage=percentage, note=note)

    def recount_records_by_total_quantity(self, new_total_quantity):
        self.get_queryset().update(quantity=(models.F('percentage') * new_total_quantity / 100))


class MetaTourRecord(CoreModel):
    metatour = models.ForeignKey(MetaTour, on_delete=models.CASCADE, related_name='records')
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='metatourrecords')
    quantity = models.FloatField()
    percentage = models.FloatField()
    note = models.TextField(null=True, blank=True)

    objects = MetaTourRecordManager()

    class Meta:
        ordering = ['tour', ]

    def __str__(self):
        return 'MetaTourRecord {}  {}'.format(self.pk, self.tour)

    def increase_quantity(self, amount):
        self.quantity += amount
        self.save()