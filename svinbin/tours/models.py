import datetime
from django.db import models
from django.db.models import Subquery, OuterRef, F, ExpressionWrapper, Q, Sum, Avg, Count, Value, Func, \
    Case, When, Prefetch
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
        subquery_seminated = self.filter(semination__tour__pk=OuterRef('pk')) \
                            .values('semination__tour') \
                            .annotate(cnt_seminated=Count('semination__sow', distinct=True)) \
                            .values('cnt_seminated')

        subquery_usound28_suporos = self.filter(
                                ultrasound__tour__pk=OuterRef('pk'), ultrasound__u_type__days=30,
                                ultrasound__result=True) \
                            .values('ultrasound__tour') \
                            .annotate(cnt_usound28_sup=Count('ultrasound__sow', distinct=True)) \
                            .values('cnt_usound28_sup')

        subquery_usound28_proholost = self.filter(
                                ultrasound__tour__pk=OuterRef('pk'), ultrasound__u_type__days=30,
                                ultrasound__result=False) \
                            .values('ultrasound__tour') \
                            .annotate(cnt_usound28_proh=Count('ultrasound__sow', distinct=True)) \
                            .values('cnt_usound28_proh')

        subquery_usound35_suporos = self.filter(
                                ultrasound__tour__pk=OuterRef('pk'), ultrasound__u_type__days=60,
                                ultrasound__result=True) \
                            .values('ultrasound__tour') \
                            .annotate(cnt_usound35_sup=Count('ultrasound__sow', distinct=True)) \
                            .values('cnt_usound35_sup')

        subquery_usound35_proholost = self.filter(
                                ultrasound__tour__pk=OuterRef('pk'), ultrasound__u_type__days=60,
                                ultrasound__result=False) \
                            .values('ultrasound__tour') \
                            .annotate(cnt_usound35_proh=Count('ultrasound__sow', distinct=True)) \
                            .values('cnt_usound35_proh')

        subquery_abort = self.filter(abortionsow__tour__pk=OuterRef('pk')) \
                            .values('abortionsow__tour') \
                            .annotate(cnt_abort=Count('abortionsow__sow', distinct=True)) \
                            .values('cnt_abort')

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
                self.filter(sowfarrow__tour__pk=OuterRef('pk')) \
                    .values('sowfarrow__tour') \
                    .annotate(total_born=Sum(f'sowfarrow__{born_type}_quantity')) \
                    .values('total_born')
                ,output_field=models.IntegerField())

        data['gilt_count'] = Subquery(self.filter(gilt__tour__pk=OuterRef('pk')) \
                                .values('gilt__tour') \
                                .annotate(cnt_gilt=Count('gilt')) \
                                .values('cnt_gilt'),
                output_field=models.IntegerField())

        data['count_farrows'] = Subquery(
                self.filter(sowfarrow__tour__pk=OuterRef('pk'))
                .values('sowfarrow__tour') \
                .annotate(farrow_cnt=Count('sowfarrow__sow')) \
                .values('farrow_cnt'))

        return self.annotate(**data)

    def add_farrow_percentage(self):
        return self.annotate(farrow_percentage=ExpressionWrapper(
            (F('count_farrows') * 100 ) / F('count_seminated'), output_field=models.FloatField()))

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
                        .annotate(cnt_tour_sow=Count('*')) \
                        .values('cnt_tour_sow'),
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

    def add_weighing_first_dates(self):
        data = dict()

        for place in ['3/4', '4/8', '8/5', '8/6', '8/7']:
            place_formatted = place.replace('/', '_')
            first_date_weights_subquery = Subquery(piglets_events.models.WeighingPiglets.objects.filter(
                                        week_tour__pk=OuterRef('pk'),
                                        place=place) \
                                    .order_by('date') \
                                    .values('date__date')[:1], output_field=models.DateTimeField())

            data[f'first_date_{place_formatted}'] = first_date_weights_subquery

        data['first_date_spec'] = Subquery(piglets_events.models.CullingPiglets.objects.filter(
                                        week_tour__pk=OuterRef('pk'),
                                        culling_type='spec') \
                                    .order_by('date') \
                                    .values('date__date')[:1], output_field=models.DateTimeField())

        return self.annotate(**data)

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
                    .annotate(culling_qnty=Sum('quantity')) \
                    .values('culling_qnty')

                data[f'ws{ws_number}_{c_type}_quantity'] = Subquery(culling_subquery_qnty,
                     output_field=models.IntegerField())

                if ws_number in [5, 6, 7]:
                    if c_type == 'prirezka':
                        continue

                    if c_type == 'spec':
                        culling_subquery_avg_weight = culling_subquery \
                            .values('culling_type') \
                            .annotate(culling_avg_weight=Avg(F('total_weight') / F('quantity'), output_field=models.FloatField())) \
                            .values('culling_avg_weight')

                        data[f'ws{ws_number}_{c_type}_avg_weight'] = Subquery(culling_subquery_avg_weight,
                         output_field=models.FloatField())

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
            lookup1 = {f'week_weight_qnty_{place_number}__isnull': True, }
            lookup2 = {f'week_weight_qnty_{place_number}': 0, }
            lookup3 = {f'week_weight_qnty_{place_number}__gt': 0, }

            data[f'ws{ws_number}_padej_percentage'] = Case(
                When(Q(**lookup1) | Q(**lookup2), then=0.0),
                When(**lookup3, 
                        then=ExpressionWrapper(
                            F(f'ws{ws_number}_padej_quantity') * 100.0 / F(f'week_weight_qnty_{place_number}'),
                            output_field=models.FloatField())
                    ), output_field=models.FloatField()
                )

            if ws_number != 4:
                data[f'ws{ws_number}_vinuzhd_percentage'] = Case(
                    When(Q(**lookup1) | Q(**lookup2), then=0.0),
                    When(**lookup3, 
                            then=ExpressionWrapper(
                                F(f'ws{ws_number}_vinuzhd_quantity') * 100.0 / F(f'week_weight_qnty_{place_number}'),
                                output_field=models.FloatField())
                        ), output_field=models.FloatField()
                    )

            if ws_number in [4, 8]:
                data[f'ws{ws_number}_prirezka_percentage'] = Case(
                    When(Q(**lookup1) | Q(**lookup2), then=0.0),
                    When(**lookup3, 
                            then=ExpressionWrapper(
                                F(f'ws{ws_number}_prirezka_quantity') * 100.0 / F(f'week_weight_qnty_{place_number}'),
                                output_field=models.FloatField())
                        ), output_field=models.FloatField()
                    )

        return self.annotate(**data)

    def add_sow_events(self, sow):
        return self.prefetch_related(
            Prefetch(
                'semination_set',
                queryset=events_models.Semination.objects.filter(sow=sow),
                to_attr='sow_semination'
                ),
            Prefetch(
                'ultrasound_set',
                queryset=events_models.Ultrasound.objects.filter(sow=sow),
                to_attr='sow_ultrasound'
                ),
            Prefetch(
                'sowfarrow_set',
                queryset=events_models.SowFarrow.objects.filter(sow=sow),
                to_attr='sow_farrow'
                ),
            Prefetch(
                'weaningsow_set',
                queryset=events_models.WeaningSow.objects.filter(sow=sow),
                to_attr='sow_weaning'
                ),
            )

    def add_weight_data_by_place(self, place):
        data = dict()
        subquery_weight_quantity = self.filter(
                                    piglets_weights__week_tour__pk=OuterRef('pk'),
                                    piglets_weights__place=place) \
                            .values('piglets_weights__place') \
                            .annotate(weight_quantity=Sum('piglets_weights__piglets_quantity'))\
                            .values('weight_quantity')
        data['weight_quantity'] = Subquery(subquery_weight_quantity)

        subquery_weight_avg = self.filter(
                                    piglets_weights__week_tour__pk=OuterRef('pk'),
                                    piglets_weights__place=place) \
                            .values('piglets_weights__place') \
                            .annotate(weight_avg=Avg('piglets_weights__average_weight'))\
                            .values('weight_avg')
        data['weight_avg'] = Subquery(subquery_weight_avg)

        subquery_weight_total = self.filter(
                                    piglets_weights__week_tour__pk=OuterRef('pk'),
                                    piglets_weights__place=place) \
                            .values('piglets_weights__place') \
                            .annotate(weight_total=Sum('piglets_weights__total_weight'))\
                            .values('weight_total')
        data['weight_total'] = Subquery(subquery_weight_total)

        return self.annotate(**data)

    def add_culling_data_by_ws(self, ws_number, culling_type):
        data = dict()
        subquery_quantity = self.filter(
                                piglets_culling__week_tour__pk=OuterRef('pk'),
                                piglets_culling__culling_type=culling_type,
                                piglets_culling__location__pigletsGroupCell__workshop__number=ws_number,
                                    ) \
                            .values('piglets_culling__culling_type') \
                            .annotate(culling_by_ws_qnty=Sum('piglets_culling__quantity'))\
                            .values('culling_by_ws_qnty')
        data[f'{culling_type}_quantity'] = Subquery(subquery_quantity)

        subquery_avg = self.filter(
                                piglets_culling__week_tour__pk=OuterRef('pk'),
                                piglets_culling__culling_type=culling_type,
                                piglets_culling__location__pigletsGroupCell__workshop__number=ws_number,
                                    ) \
                            .values('piglets_culling__culling_type') \
                            .annotate(culling_by_ws_avg=Avg('piglets_culling__avg_weight'))\
                            .values('culling_by_ws_avg')
        data[f'{culling_type}_avg'] = Subquery(subquery_avg)

        subquery_total = self.filter(
                                piglets_culling__week_tour__pk=OuterRef('pk'),
                                piglets_culling__culling_type=culling_type,
                                piglets_culling__location__pigletsGroupCell__workshop__number=ws_number)\
                            .values('piglets_culling__culling_type') \
                            .annotate(culling_by_ws_total=Sum('piglets_culling__total_weight'))\
                            .values('culling_by_ws_total')
        data[f'{culling_type}_total'] = Subquery(subquery_total)

        return self.annotate(**data)

    def add_remont_trs_out(self):
        data = dict()
        for ws_number in [5, 6, 7]:
            data[f'ws{ws_number}_remont'] = Subquery(
                    self.filter(
                        piglets_transactions__week_tour__pk=OuterRef('pk'),
                        piglets_transactions__to_location__workshop__number=2,
                        piglets_transactions__from_location__pigletsGroupCell__workshop__number=ws_number,
                        ) \
                    .values('piglets_transactions__week_tour') \
                    .annotate(ws_remont_total=Sum('piglets_transactions__quantity'))
                    .values('ws_remont_total'))

        data['count_remont_total'] = Subquery(
                self.filter(piglets_transactions__week_tour__pk=OuterRef('pk'),
                    piglets_transactions__to_location__workshop__number=2) \
                .values('piglets_transactions__week_tour') \
                .annotate(remont_total=Sum('piglets_transactions__quantity'))
                .values('remont_total'))

        return self.annotate(**data)

    def gen_subquery_sv_age_at_place(self, places):
        return Subquery(self.filter(
                    piglets_weights__week_tour__pk=OuterRef('pk'),
                    piglets_weights__place__in=places,
                    ) \
                .values('piglets_weights__week_tour') \
                .annotate(weight_sv_avg_age=ExpressionWrapper(
                    Sum(
                        ExpressionWrapper(
                            F('piglets_weights__piglets_age') 
                            * F('piglets_weights__piglets_quantity'),
                            output_field=models.FloatField())
                        )
                     / Sum('piglets_weights__piglets_quantity'),
                    output_field=models.FloatField()
                    )) \
                .values('weight_sv_avg_age'))

    def gen_subquery_total2_place(self, places):
        return Subquery(self.filter(
                    piglets_weights__week_tour__pk=OuterRef('pk'),
                    piglets_weights__place__in=places,
                    ) \
                .values('piglets_weights__week_tour') \
                .annotate(total2=Sum('piglets_weights__total_weight')) \
                .values('total2'))

    def add_prives_prepare(self):
        data = dict()

        def subquery_sv_age_at_place(self, places):
            return Subquery(self.filter(
                    piglets_weights__week_tour__pk=OuterRef('pk'),
                    piglets_weights__place__in=places,
                    ) \
                .values('piglets_weights__week_tour') \
                .annotate(weight_sv_avg_age=ExpressionWrapper(
                    Sum(
                        ExpressionWrapper(
                            F('piglets_weights__piglets_age') 
                            * F('piglets_weights__piglets_quantity'),
                            output_field=models.FloatField())
                        )
                     / Sum('piglets_weights__piglets_quantity'),
                    output_field=models.FloatField()
                    )) \
                .values('weight_sv_avg_age'))

        def subquery_total1_place(self, places):
            return Subquery(self.filter(
                    piglets_weights__week_tour__pk=OuterRef('pk'),
                    piglets_weights__place__in=places,
                    ) \
                .values('piglets_weights__week_tour') \
                .annotate(total1=
                    Sum(
                        ExpressionWrapper(
                            F('piglets_weights__piglets_quantity') 
                            * F('piglets_weights__average_weight'),
                            output_field=models.FloatField())
                        )
                    ) \
                .values('total1'))

        def subquery_total2_place(self, places):
            return Subquery(self.filter(
                    piglets_weights__week_tour__pk=OuterRef('pk'),
                    piglets_weights__place__in=places,
                    ) \
                .values('piglets_weights__week_tour') \
                .annotate(total2=Sum('piglets_weights__total_weight')) \
                .values('total2'))

        for place in ['3/4', '4/8', '8/5', '8/6', '8/7']:
            place_formatted = place.replace('/', '_')
            # data[f'sv_age_{place_formatted}']  = self.gen_subquery_sv_age_at_place(places=[place])
            data[f'sv_age_{place_formatted}']  = subquery_sv_age_at_place(self, [place])
            # data[f'total1_{place_formatted}']  = subquery_total1_place(self, [place])
            data[f'total2_{place_formatted}']  = subquery_total2_place(self, [place])
            # data[f'total2_{place_formatted}']  = self.gen_subquery_total2_place(places=[place])

        # data['sv_age_ws8'] = self.gen_subquery_sv_age_at_place(places=['8/5', '8/6', '8/7'])
        # data['total1_ws8'] = subquery_total1_place(self, ['8/5', '8/6', '8/7'])
        # data['total2_ws8'] = self.gen_subquery_total2_place(places=['8/5', '8/6', '8/7'])

        data['sv_age_ws8'] = subquery_sv_age_at_place(self, ['8/5', '8/6', '8/7'])
        # data['total1_ws8'] = subquery_total1_place(self, ['8/5', '8/6', '8/7'])
        data['total2_ws8'] = subquery_total2_place(self, ['8/5', '8/6', '8/7'])

        return self.annotate(**data)

    def add_prives_prepare_spec(self):
        data = dict()

        for ws_number in [5, 6, 7]:
            subquery_age = Subquery(self.filter(
                        piglets_culling__week_tour__pk=OuterRef('pk'),
                        piglets_culling__culling_type='spec',
                        piglets_culling__location__pigletsGroupCell__workshop__number=ws_number,
                        ) \
                    .values('piglets_culling__week_tour') \
                    .annotate(spec_sv_avg_age=ExpressionWrapper(
                        Sum(
                            ExpressionWrapper(
                                F('piglets_culling__piglets_age') 
                                * F('piglets_culling__quantity'),
                                output_field=models.FloatField())
                            )
                         / Sum('piglets_culling__quantity'),
                        output_field=models.FloatField()
                        )) \
                    .values('spec_sv_avg_age'))

            subquery_weight_total = Subquery(self.filter(
                        piglets_culling__week_tour__pk=OuterRef('pk'),
                        piglets_culling__culling_type='spec',
                        piglets_culling__location__pigletsGroupCell__workshop__number=ws_number,
                        ) \
                    .values('piglets_culling__week_tour') \
                    .annotate(spec_total_weight=Sum('piglets_culling__total_weight')) \
                    .values('spec_total_weight'))

            data[f'spec_sv_avg_age_ws{ws_number}'] = subquery_age
            data[f'spec_weight_total_ws{ws_number}'] = subquery_weight_total

        return self.annotate(**data)

    def add_prives(self):
        data = dict()
        data['prives_4'] = (F('total2_4_8') - F('total2_3_4')) / (F('sv_age_4_8') - F('sv_age_3_4'))
        data['prives_8'] = (F('total2_ws8') - F('total2_4_8'))  / (F('sv_age_ws8') - F('sv_age_4_8'))
        data['prives_5'] = (F('spec_weight_total_ws5') - F('total2_8_5')) / \
                             (F('spec_sv_avg_age_ws5') - F('sv_age_8_5'))
        data['prives_6'] = (F('spec_weight_total_ws6') - F('total2_8_6')) / \
                             (F('spec_sv_avg_age_ws6') - F('sv_age_8_6'))
        data['prives_7'] = (F('spec_weight_total_ws7') - F('total2_8_7')) / \
                             (F('spec_sv_avg_age_ws7') - F('sv_age_8_7'))

        return self.add_prives_prepare().add_prives_prepare_spec().annotate(**data)
        # return self.annotate(**data)



class TourManager(CoreModelManager):
    def get_queryset(self):
        return TourQuerySet(self.model, using=self._db)

    def get_monday_date_by_week_number(self, week_number, year):
        start_week_number_pre = str(year) + '-W' + str(week_number)
        return datetime.datetime.strptime(start_week_number_pre + '-1', "%Y-W%W-%w")

    def get_or_create_by_week(self, week_number, year, start_date=None):
        if not start_date:
            start_date=timezone.now()
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