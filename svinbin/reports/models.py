# -*- coding: utf-8 -*-
from operator import itemgetter
from collections import Counter

from datetime import timedelta, date, datetime

from django.db import models
from django.db.models import Subquery, OuterRef, F, ExpressionWrapper, Q, Sum, Avg, Count, Value
from django.db.models.functions import Coalesce, Greatest
from django.utils import timezone

from core.models import CoreModel, CoreModelManager
from sows.models import Sow, SowStatusRecord
from piglets.models import Piglets
from locations.models import Location
from sows_events.models import ( SowFarrow, Semination, Ultrasound, AbortionSow, CullingSow, MarkAsNurse,
 MarkAsGilt )
from piglets_events.models import CullingPiglets, WeighingPiglets
from transactions.models import SowTransaction, PigletsTransaction

from reports import operation_serializers


# https://stackoverflow.com/questions/1060279/iterating-through-a-range-of-dates-in-python
def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)


class ReportDateQuerySet(models.QuerySet):
    def gen_sow_culling_cnt_by_daterange_subquery(self, culling_type, start_date, end_date):
        return Coalesce(
                    Subquery(
                        CullingSow.objects.filter(
                            date__date__gte=start_date, date__date__lt=end_date, culling_type=culling_type) \
                                    .values('culling_type') \
                                    .annotate(cnt=Count('pk')) \
                                    .values('cnt')
                        ), 0
        )

    def gen_sow_culling_cnt_by_date_subquery(self, culling_type, target_date):
        return Coalesce(
                    Subquery(
                        CullingSow.objects.filter(
                            date__date=target_date, culling_type=culling_type) \
                                    .values('culling_type') \
                                    .annotate(cnt=Count('pk')) \
                                    .values('cnt')
                        ), 0
        )


    def gen_piglets_culling_cnt_by_daterange_subquery(self, culling_type, start_date, end_date):
        return Coalesce(
                    Subquery(
                        CullingPiglets.objects.filter(
                            date__date__gte=start_date, date__date__lt=end_date, culling_type=culling_type) \
                                    .values('culling_type') \
                                    .annotate(qnty=Sum('quantity')) \
                                    .values('qnty')
                        ), 0
        )

    def gen_piglets_culling_cnt_by_date_subquery(self, culling_type, target_date):
        return Coalesce(
                    Subquery(
                        CullingPiglets.objects.filter(
                            date__date=target_date, culling_type=culling_type) \
                                    .values('culling_type') \
                                    .annotate(qnty=Sum('quantity')) \
                                    .values('qnty')
                        ), 0
        )

    def gen_sowfarrow_alive_piglets_qnty_at_date(self, target_date):
        return Coalesce(
                        Subquery(SowFarrow.objects.filter(date__date=target_date) \
                                .values('date__date') \
                                .annotate(today_born_alive=Sum('alive_quantity')) \
                                .values('today_born_alive'), output_field=models.IntegerField()),
                        0 )

    def gen_sowfarrow_alive_piglets_qnty_at_daterange(self, start_date, end_date):
        return Coalesce(
                        Subquery(SowFarrow.objects.filter(date__date__gte=start_date, date__date__lt=end_date) \
                                .annotate(flag_group=Value(0)) \
                                .values('flag_group') \
                                .annotate(today_born_alive=Sum('alive_quantity')) \
                                .values('today_born_alive'), output_field=models.IntegerField()),
                        0 )

    def gen_ws_piglets_culling_qnt_subquery(self, culling_type, date, ws_locs):
        return Subquery(
                        CullingPiglets.objects.filter(
                            date__date=date, culling_type=culling_type,
                            location__in=ws_locs) \
                                    .values('culling_type') \
                                    .annotate(qnty=Sum('quantity')) \
                                    .values('qnty')
                        )

    def gen_ws_piglets_culling_total_weight_subquery(self, culling_type, date, ws_locs):
        return  Subquery(
                        CullingPiglets.objects.filter(
                            date__date=date, culling_type=culling_type,
                            location__in=ws_locs) \
                                    .values('culling_type') \
                                    .annotate(total_weight=Sum('total_weight')) \
                                    .values('total_weight')
                    )

    def gen_ws_piglets_culling_avg_weight_subquery(self, culling_type, date, ws_locs):
        return  Subquery(
                        CullingPiglets.objects.filter(
                            date__date=date, culling_type=culling_type,
                            location__in=ws_locs) \
                                    .values('culling_type') \
                                    .annotate(avg_weight=ExpressionWrapper(
                                            F('total_weight') / F('quantity'),
                                            output_field=models.FloatField())
                                    ) \
                                    .values('avg_weight')
                )

    def gen_weighing_qnty_subquery(self, date, place):
        return Subquery(WeighingPiglets.objects \
                        .filter(date__date=date, place=place) \
                        .values('place') \
                        .annotate(qnty=Sum('piglets_quantity')) \
                        .values('qnty'))

    def gen_weighing_total_subquery(self, date, place):
        return Subquery(WeighingPiglets.objects \
                        .filter(date__date=date, place=place) \
                        .values('place') \
                        .annotate(total=Sum('total_weight')) \
                        .values('total'))

    def gen_weighing_avg_subquery(self, date, place):
        return Subquery(WeighingPiglets.objects \
                        .filter(date__date=date, place=place) \
                        .values('place') \
                        .annotate(average=Avg('average_weight')) \
                        .values('average'))

    def add_today_sows_qnty(self):
        today = timezone.now().date()
        today_padej_subquery = self.gen_sow_culling_cnt_by_date_subquery('padej', today)
        today_vinuzhd_subquery = self.gen_sow_culling_cnt_by_date_subquery('vinuzhd', today)

        sows_subquery = Sow.objects.all() \
                        .values('alive') \
                        .annotate(cnt=Count('pk')) \
                        .values('cnt')

        gitls_to_sows_subquery = 0

        # substract today gilt to sow qnty
        today_sows_qnty = Coalesce(Subquery(sows_subquery, output_field=models.IntegerField()), 0) + \
                         today_padej_subquery + today_vinuzhd_subquery - gitls_to_sows_subquery

        return self.annotate(today_start_sows_qnty=today_sows_qnty, today_padej_subquery=today_padej_subquery,
         today_vinuzhd_subquery=today_vinuzhd_subquery)


    def add_sows_quantity_at_date_start(self):
        yesterday = timezone.now().date() - timedelta(1)
        today = timezone.now().date()

        cnt_padej_subquery = self.gen_sow_culling_cnt_by_daterange_subquery('padej', OuterRef('date'), today)
        cnt_vinuzhd_subquery = self.gen_sow_culling_cnt_by_daterange_subquery('vinuzhd', OuterRef('date'), today)

        cnt_gilts_to_sows = 0

        return self.annotate(
                sow_qnty_at_date_start=ExpressionWrapper(
                    F('today_start_sows_qnty') + cnt_padej_subquery + cnt_vinuzhd_subquery - cnt_gilts_to_sows,
                    output_field=models.IntegerField()
                    )
                )

    def add_sows_quantity_at_date_end(self):
        cnt_gilts_to_sows = 0

        return self.annotate(
                sows_quantity_at_date_end=ExpressionWrapper(
                    F('sow_qnty_at_date_start') - F('sow_padej_qnty') - F('sow_vinuzhd_qnty') + cnt_gilts_to_sows,
                    output_field=models.IntegerField()
                    )
                )

    def add_sow_padej_qnty(self):
        return self.annotate(sow_padej_qnty=self.gen_sow_culling_cnt_by_date_subquery('padej',  OuterRef('date')))

    def add_sow_vinuzhd_qnty(self):
        return self.annotate(sow_vinuzhd_qnty=self.gen_sow_culling_cnt_by_date_subquery('vinuzhd',  OuterRef('date')))
        
    def add_piglets_today_quantity(self):
        count_piglets = Piglets.objects.all() \
                    .values('active').annotate(sum_piglets=Sum('quantity')).values('sum_piglets')

        today = timezone.now().date()
        # today cullings
        piglets_today_padej_subquery = self.gen_piglets_culling_cnt_by_date_subquery('padej', today)
        piglets_today_prirezka_subquery = self.gen_piglets_culling_cnt_by_date_subquery('prirezka', today)
        piglets_today_vinuzhd_subquery = self.gen_piglets_culling_cnt_by_date_subquery('vinuzhd', today)
        piglets_today_spec_subquery = self.gen_piglets_culling_cnt_by_date_subquery('spec', today)

        # today born alive
        today_born_alive_subquery = Coalesce(
                                        Subquery(SowFarrow.objects.filter(date__date=today) \
                                                .values('date__date') \
                                                .annotate(today_born_alive=Sum('alive_quantity')) \
                                                .values('today_born_alive'), output_field=models.IntegerField()),
                                        0 )

        today_count_piglets = count_piglets + piglets_today_padej_subquery + piglets_today_prirezka_subquery + \
                piglets_today_vinuzhd_subquery + piglets_today_spec_subquery - today_born_alive_subquery

        # + cull qnty today - born today
        return self.annotate(piglets_today_qnty=today_count_piglets)

    def add_piglets_quantity_at_date_start(self):
        today = timezone.now().date()

        piglets_padej_subquery = self.gen_piglets_culling_cnt_by_daterange_subquery('padej', OuterRef('date'),
             today)
        piglets_prirezka_subquery = self.gen_piglets_culling_cnt_by_daterange_subquery('prirezka', OuterRef('date'),
             today)
        piglets_vinuzhd_subquery = self.gen_piglets_culling_cnt_by_daterange_subquery('vinuzhd', OuterRef('date'), 
             today)
        piglets_spec_subquery = self.gen_piglets_culling_cnt_by_daterange_subquery('spec', OuterRef('date'),
             today)

        born_alive = self.gen_sowfarrow_alive_piglets_qnty_at_daterange(OuterRef('date'), today)

        return self.annotate(piglets_qnty_start_date=ExpressionWrapper(
                        F('piglets_today_qnty') + piglets_padej_subquery + piglets_prirezka_subquery + \
                        piglets_vinuzhd_subquery + piglets_spec_subquery - born_alive,
                        output_field=models.IntegerField()
                    ))

    def add_piglets_quantity_at_date_end(self):
        return self.annotate(piglets_qnty_start_end=ExpressionWrapper(
                        F('piglets_qnty_start_date') - F('piglets_padej_qnty') - F('piglets_prirezka_qnty') - \
                        F('piglets_vinuzhd_qnty') - F('piglets_spec_qnty') + F('born_alive'),
                        output_field=models.IntegerField()
                    ))

    def add_born_alive(self):
        return self.annotate(born_alive=self.gen_sowfarrow_alive_piglets_qnty_at_date(OuterRef('date')))

    def add_piglets_padej_qnty(self):
        return self.annotate(
            piglets_padej_qnty=self.gen_piglets_culling_cnt_by_date_subquery('padej', OuterRef('date')))

    def add_piglets_prirezka_qnty(self):
        return self.annotate(
            piglets_prirezka_qnty=self.gen_piglets_culling_cnt_by_date_subquery('prirezka', OuterRef('date')))

    def add_piglets_vinuzhd_qnty(self):
        return self.annotate(
            piglets_vinuzhd_qnty=self.gen_piglets_culling_cnt_by_date_subquery('vinuzhd', OuterRef('date')))

    def add_piglets_spec_qnty(self):
        return self.annotate(
            piglets_spec_qnty=self.gen_piglets_culling_cnt_by_date_subquery('spec', OuterRef('date')))

    def add_piglets_spec_total_weight(self):
        total_weight = Coalesce(
                        Subquery(CullingPiglets.objects.filter(
                            date__date=OuterRef('date'), culling_type='spec') \
                                    .values('culling_type') \
                                    .annotate(all_total_weight=Sum('total_weight')) \
                                    .values('all_total_weight'), output_field=models.FloatField()),
                        0 )
        return self.annotate(piglets_spec_total_weight=total_weight)

    def add_priplod_by_sow(self):
        farrow_cnt = Coalesce(Subquery(SowFarrow.objects.filter(date__date=OuterRef('date')) \
            .values('date__date') \
            .annotate(cnt=Count('*')) \
            .values('cnt'), output_field=models.IntegerField()), 1)

        return self.annotate(priplod_by_sow=ExpressionWrapper(F('born_alive') / farrow_cnt,
         output_field=models.FloatField()))

    def add_piglets_qnty_in_transactions(self):
        total_qnty = Coalesce(
            Subquery(PigletsTransaction.objects.filter(date__date=OuterRef('date'))\
            .values('date__date') \
            .annotate(total_qnty=Sum('quantity')) \
            .values('total_qnty')), 0)

        return self.annotate(piglets_transfered=total_qnty)

    def dir_rep_aggregate_total_data(self):        
        return self.aggregate(
                total_priplod=Sum('born_alive'),
                total_sows_padej=Sum('piglets_padej_qnty'),
                total_piglets_padej=Sum('sow_padej_qnty'),
                total_sows_vinuzhd=Sum('sow_vinuzhd_qnty') ,
                total_piglets_vinuzhd=Sum('piglets_vinuzhd_qnty'),
                total_spec=Sum('piglets_spec_qnty'),
                total_prirezka=Sum('piglets_prirezka_qnty'),
                total_spec_weight=Sum('piglets_spec_total_weight'),
                avg_priplod=Avg('priplod_by_sow'),
                )

    def add_ws3_sow_cullings_data(self, ws_locs):
        data = dict()

        for culling_type in ['padej', 'vinuzhd']:
            data[f'{culling_type}_sup_count'] = CullingSow.objects \
                            .filter(date__date=OuterRef('date'), culling_type=culling_type) \
                            .filter(sow_status__title__in=['Супорос 35', 'Супорос 28',
                                 'Осеменена 1', 'Осеменена 2'], location__in=ws_locs) \
                            .values('date__date') \
                            .annotate(cnt=Count('*')) \
                            .values('cnt')

            data[f'{culling_type}_sup_weight'] = CullingSow.objects \
                            .filter(date__date=OuterRef('date'), culling_type=culling_type) \
                            .filter(sow_status__title__in=['Супорос 35', 'Супорос 28', 
                                'Осеменена 1', 'Осеменена 2'], location__in=ws_locs) \
                            .values('date__date') \
                            .annotate(total_weight=Sum('weight')) \
                            .values('total_weight')

            data[f'{culling_type}_podsos_count'] = CullingSow.objects \
                            .filter(date__date=OuterRef('date'), culling_type=culling_type) \
                            .filter(sow_status__title__in=['Опоросилась', 'Отъем', 'Кормилица', 'Аборт',],
                                location__in=ws_locs) \
                            .values('date__date') \
                            .annotate(cnt=Count('*')) \
                            .values('cnt')

            data[f'{culling_type}_podsos_weight'] = CullingSow.objects \
                            .filter(date__date=OuterRef('date'), culling_type=culling_type) \
                            .filter(sow_status__title__in=['Опоросилась', 'Отъем', 'Кормилица', 'Аборт',],
                                location__in=ws_locs) \
                            .values('date__date') \
                            .annotate(total_weight=Sum('weight')) \
                            .values('total_weight')

        return self.annotate(**data)

    def add_ws3_sow_trs_data(self, ws_locs):
        data = dict()
   
        data['tr_in_from_1_sup_count'] = SowTransaction.objects \
                        .filter(date__date=OuterRef('date'), 
                                to_location__workshop__number=3,
                                from_location__workshop__number=1,
                                sow_status__title__in=['Супорос 35', 'Супорос 28', 
                                    'Осеменена 1', 'Осеменена 2']) \
                        .values('to_location') \
                        .annotate(cnt=Count('*')) \
                        .values('cnt')

        data['tr_in_from_2_sup_count'] = SowTransaction.objects \
                        .filter(date__date=OuterRef('date'), 
                                to_location__workshop__number=3,
                                from_location__workshop__number=2,
                                sow_status__title__in=['Супорос 35', 'Супорос 28', 'Осеменена 1',
                                 'Осеменена 2']) \
                        .values('to_location') \
                        .annotate(cnt=Count('*')) \
                        .values('cnt')

        data['tr_in_podsos_count'] = SowTransaction.objects \
                        .filter(date__date=OuterRef('date'), 
                                to_location__workshop__number=3,
                                sow_status__title__in=['Опоросилась', 'Отъем', 'Кормилица', 'Аборт',
                                 'Ожидает осеменения']) \
                        .exclude(from_location__in=ws_locs) \
                        .values('date__date') \
                        .annotate(cnt=Count('*')) \
                        .values('cnt')

        data['tr_out_sup_count'] = SowTransaction.objects \
                        .filter(date__date=OuterRef('date'), 
                                from_location__in=ws_locs,
                                sow_status__title__in=['Супорос 35', 'Супорос 28','Осеменена 1',
                                 'Осеменена 2']) \
                        .exclude(to_location__in=ws_locs) \
                        .values('date__date') \
                        .annotate(cnt=Count('*')) \
                        .values('cnt')

        data['tr_out_podsos_count'] = SowTransaction.objects \
                        .filter(date__date=OuterRef('date'), 
                                from_location__in=ws_locs,
                                sow_status__title__in=['Опоросилась', 'Отъем', 'Кормилица', 'Аборт',
                                 'Ожидает осеменения']) \
                        .exclude(to_location__in=ws_locs) \
                        .values('date__date') \
                        .annotate(cnt=Count('*')) \
                        .values('cnt')
                        
        return self.annotate(**data)

    def add_ws3_sow_farrow_data(self):
        data = dict()
        data['count_oporos'] = SowFarrow.objects.filter(date__date=OuterRef('date')) \
                                .values('date__date') \
                                .annotate(cnt=Count('*')) \
                                .values('cnt')

        data['count_alive'] = SowFarrow.objects.filter(date__date=OuterRef('date')) \
                                .values('date__date') \
                                .annotate(count_alive=Sum('alive_quantity')) \
                                .values('count_alive')

        return self.annotate(**data)

    def add_ws3_count_piglets_start_day(self, ws_locs):
        # add date__date__gt 24\06
        total_alive = Coalesce(
                        Subquery(SowFarrow.objects \
                        .filter(date__date__lt=OuterRef('date')) \
                        .annotate(flag_group=Value(0)) \
                        .values('flag_group') \
                        .annotate(total_alive=Sum('alive_quantity')) \
                        .values('total_alive')), 0)

        trs_out_qnty = Coalesce(
                        Subquery(PigletsTransaction.objects \
                        .filter(date__date__lt=OuterRef('date'), from_location__in=ws_locs) \
                        .exclude(to_location__in=ws_locs) \
                        .annotate(flag_group=Value(0)) \
                        .values('flag_group') \
                        .annotate(trs_out_qnty=Sum('quantity')) \
                        .values('trs_out_qnty')), 0)

        trs_in_qnty = Coalesce(
                        Subquery(PigletsTransaction.objects \
                        .filter(date__date__lt=OuterRef('date'), to_location__in=ws_locs) \
                        .exclude(from_location__in=ws_locs) \
                        .annotate(flag_group=Value(0)) \
                        .values('flag_group') \
                        .annotate(trs_in_qnty=Sum('quantity')) \
                        .values('trs_in_qnty')), 0)

        culling_qnty = Coalesce(
                        Subquery(CullingPiglets.objects \
                        .filter(date__date__lt=OuterRef('date'), location__in=ws_locs) \
                        .annotate(flag_group=Value(0)) \
                        .values('flag_group') \
                        .annotate(culling_qnty=Sum('quantity')) \
                        .values('culling_qnty')), 0)

        # + count piglets at 24/06 
        # - count init piglets 3715
        return self.annotate(count_piglets_at_start=ExpressionWrapper(
            3715 + total_alive - trs_out_qnty + trs_in_qnty - culling_qnty, output_field=models.IntegerField()))

    def add_ws3_piglets_trs_out_aka_weighing(self):
        data = dict()
        data['tr_out_aka_weight_qnty'] = Subquery(WeighingPiglets.objects \
                            .filter(date__date=OuterRef('date'), place='3/4') \
                            .values('place') \
                            .annotate(qnty=Sum('piglets_quantity')) \
                            .values('qnty'))

        data['tr_out_aka_weight_total'] = Subquery(WeighingPiglets.objects \
                            .filter(date__date=OuterRef('date'), place='3/4') \
                            .values('place') \
                            .annotate(total=Sum('total_weight')) \
                            .values('total'))

        data['tr_out_aka_weight_avg'] = Subquery(WeighingPiglets.objects \
                            .filter(date__date=OuterRef('date'), place='3/4') \
                            .values('place') \
                            .annotate(average=Avg('average_weight')) \
                            .values('average'))

        return self.annotate(**data)

    def add_ws3_piglets_cullings(self, ws_locs):
        data = dict()
        data['piglets_padej_qnty'] = CullingPiglets.objects \
                    .filter(date__date=OuterRef('date'), culling_type__in=['padej', 'prirezka'],
                        location__in=ws_locs) \
                    .values('date__date') \
                    .annotate(qnty=Sum('quantity')) \
                    .values('qnty')

        data['piglets_vinuzhd_qnty'] = CullingPiglets.objects \
                    .filter(date__date=OuterRef('date'), culling_type__in=['vinuzhd'],
                        location__in=ws_locs) \
                    .values('date__date') \
                    .annotate(qnty=Sum('quantity')) \
                    .values('qnty')

        data['piglets_padej_weight'] = CullingPiglets.objects \
                    .filter(date__date=OuterRef('date'), culling_type__in=['padej', 'prirezka'],
                        location__in=ws_locs) \
                    .values('date__date') \
                    .annotate(weight=Sum('total_weight')) \
                    .values('weight')

        data['piglets_vinuzhd_weight'] = CullingPiglets.objects \
                    .filter(date__date=OuterRef('date'), culling_type__in=['vinuzhd'],
                        location__in=ws_locs) \
                    .values('date__date') \
                    .annotate(weight=Sum('total_weight')) \
                    .values('weight')

        return self.annotate(**data)

    def ws3_aggregate_total(self):
        return self.aggregate(
                total_tr_in_podsos_count=Sum('tr_in_podsos_count'),
                total_tr_in_from_1_sup_count=Sum('tr_in_from_1_sup_count'),
                total_tr_in_from_2_sup_count=Sum('tr_in_from_2_sup_count'),

                total_count_oporos=Sum('count_oporos') ,
                total_count_alive=Sum('count_alive'),

                total_tr_out_podsos_count=Sum('tr_out_podsos_count'),
                total_tr_out_sup_count=Sum('tr_out_sup_count'),

                total_padej_podsos_count=Sum('padej_podsos_count'),
                total_padej_podsos_weight=Sum('padej_podsos_weight'),

                total_padej_sup_count=Sum('padej_sup_count'),
                total_padej_sup_weight=Sum('padej_sup_weight'),

                total_vinuzhd_podsos_count=Sum('vinuzhd_podsos_count') ,
                total_vinuzhd_podsos_weight=Sum('vinuzhd_podsos_weight'),

                total_vinuzhd_sup_count=Sum('vinuzhd_sup_count'),
                total_vinuzhd_sup_weight=Sum('vinuzhd_sup_weight'),

                total_tr_out_aka_weight_qnty=Sum('tr_out_aka_weight_qnty'),
                total_tr_out_aka_weight_total=Sum('tr_out_aka_weight_total'),
                avg_tr_out_weight=Avg('tr_out_aka_weight_avg'),

                total_piglets_padej_qnty=Sum('piglets_padej_qnty'),
                total_piglets_padej_weight=Sum('piglets_padej_weight'),

                total_piglets_vinuzhd_qnty=Sum('piglets_vinuzhd_qnty'),
                total_piglets_vinuzhd_weight=Sum('piglets_vinuzhd_weight'),
                )

    def add_ws_count_piglets_start_day(self, ws_locs):
        trs_in_qnty = Coalesce(
                        Subquery(PigletsTransaction.objects \
                            .filter(date__date__lt=OuterRef('date'), to_location__in=ws_locs) \
                            .exclude(from_location__in=ws_locs) \
                            .annotate(flag_group=Value(0)) \
                            .values('flag_group') \
                            .annotate(trs_in_qnty=Sum('quantity')) \
                            .values('trs_in_qnty')), 0)

        trs_out_qnty = Coalesce(
                        Subquery(PigletsTransaction.objects \
                            .filter(date__date__lt=OuterRef('date'), from_location__in=ws_locs) \
                            .exclude(to_location__in=ws_locs) \
                            .annotate(flag_group=Value(0)) \
                            .values('flag_group') \
                            .annotate(trs_out_qnty=Sum('quantity')) \
                            .values('trs_out_qnty')), 0)

        culling_qnty = Coalesce(
                        Subquery(CullingPiglets.objects \
                            .filter(date__date__lt=OuterRef('date'), location__in=ws_locs) \
                            .annotate(flag_group=Value(0)) \
                            .values('flag_group') \
                            .annotate(culling_qnty=Sum('quantity')) \
                            .values('culling_qnty')), 0)

        return self.annotate(count_piglets_at_start=ExpressionWrapper(
          trs_in_qnty - trs_out_qnty - culling_qnty, output_field=models.IntegerField()))

    def add_ws_weighing_in(self, ws_number):
        place = None
        if ws_number == 4:
            place = '3/4'
        elif ws_number == 8:
            place = '4/8'
        elif ws_number == 5:
            place = '8/5'
        elif ws_number == 6:
            place = '8/6'
        elif ws_number == 7:
            place = '8/7'

        data = dict()
        data['tr_in_aka_weight_in_qnty'] = self.gen_weighing_qnty_subquery(date=OuterRef('date'),
            place=place)
        data['tr_in_aka_weight_in_total'] = self.gen_weighing_total_subquery(date=OuterRef('date'),
            place=place)
        data['tr_in_aka_weight_in_avg'] = self.gen_weighing_avg_subquery(date=OuterRef('date'),
            place=place)

        return self.annotate(**data)

    def add_ws_weighing_out(self, ws_number):
        place = None
        if ws_number == 4:
            place = ['4/8']
        elif ws_number == 8:
            place = ['8/5', '8/6', '8/7',]

        data = dict()
        data['tr_out_aka_weight_in_qnty'] = ExpressionWrapper(Value(0), output_field=models.IntegerField())
        data['tr_out_aka_weight_in_total'] = ExpressionWrapper(Value(0), output_field=models.IntegerField())
        data['tr_out_aka_weight_in_avg'] = ExpressionWrapper(Value(0), output_field=models.IntegerField())

        if place:           
            data['tr_out_aka_weight_in_qnty'] = Subquery(WeighingPiglets.objects \
                            .filter(date__date=OuterRef('date'), place__in=place) \
                            .annotate(flag_group=Value(0)) \
                            .values('flag_group') \
                            .annotate(qnty=Sum('piglets_quantity')) \
                            .values('qnty'))

            data['tr_out_aka_weight_in_total'] = Subquery(WeighingPiglets.objects \
                            .filter(date__date=OuterRef('date'), place__in=place) \
                            .annotate(flag_group=Value(0)) \
                            .values('flag_group') \
                            .annotate(total=Sum('total_weight')) \
                            .values('total'))

            data['tr_out_aka_weight_in_avg'] = Subquery(WeighingPiglets.objects \
                            .filter(date__date=OuterRef('date'), place__in=place) \
                            .annotate(flag_group=Value(0)) \
                            .values('flag_group') \
                            .annotate(average=Avg('average_weight')) \
                            .values('average'))

        return self.annotate(**data)

    def add_ws_piglets_culling_data(self, ws_locs):
        data = dict()
        for culling_type in ['padej', 'prirezka', 'vinuzhd', 'spec']:
            data[f'{culling_type}_qnty'] = Subquery(
                        CullingPiglets.objects.filter(
                            date__date=OuterRef('date'), culling_type=culling_type,
                            location__in=ws_locs) \
                                    .values('culling_type') \
                                    .annotate(qnty=Sum('quantity')) \
                                    .values('qnty')
                        )

            data[f'{culling_type}_total_weight'] = Subquery(
                        CullingPiglets.objects.filter(
                            date__date=OuterRef('date'), culling_type=culling_type,
                            location__in=ws_locs) \
                                    .values('culling_type') \
                                    .annotate(all_total_weight=Sum('total_weight')) \
                                    .values('all_total_weight')
                    )

            data[f'{culling_type}_avg_weight'] = Subquery(
                        CullingPiglets.objects.filter(
                            date__date=OuterRef('date'), culling_type=culling_type,
                            location__in=ws_locs) \
                                    .values('culling_type') \
                                    .annotate(avg_weight=ExpressionWrapper(
                                            F('total_weight') / F('quantity'),
                                            output_field=models.FloatField())
                                    ) \
                                    .values('avg_weight')
                )

        return self.annotate(**data)

    def add_ws_piglets_trs_in_out(self, ws_locs):
        data = dict()
        data['tr_in_qnty'] = Subquery(PigletsTransaction.objects \
                        .filter(date__date=OuterRef('date'), to_location__in=ws_locs) \
                        .exclude(from_location__in=ws_locs) \
                        .annotate(flag_group=Value(0)) \
                        .values('flag_group') \
                        .annotate(tr_in_qnty=Sum('quantity')) \
                        .values('tr_in_qnty'))

        data['tr_out_qnty'] = Subquery(PigletsTransaction.objects \
                        .filter(date__date=OuterRef('date'), from_location__in=ws_locs) \
                        .exclude(to_location__in=ws_locs) \
                        .annotate(flag_group=Value(0)) \
                        .values('flag_group') \
                        .annotate(trs_out_qnty=Sum('quantity')) \
                        .values('trs_out_qnty'))

        return self.annotate(**data)

    def ws_aggregate_total(self):
        return self.aggregate(
                total_tr_in_aka_weight_in_qnty=Sum('tr_in_aka_weight_in_qnty'),
                total_tr_in_aka_weight_in_total=Sum('tr_in_aka_weight_in_total'),
                total_tr_in_aka_weight_in_avg=Avg('tr_in_aka_weight_in_avg'),

                total_tr_out_aka_weight_in_qnty=Sum('tr_out_aka_weight_in_qnty'),
                total_tr_out_aka_weight_in_total=Sum('tr_out_aka_weight_in_total'),
                total_tr_out_aka_weight_in_avg=Avg('tr_out_aka_weight_in_avg'),

                total_tr_in_qnty=Sum('tr_in_qnty'),
                total_tr_out_qnty=Sum('tr_out_qnty'),

                total_padej_qnty=Sum('padej_qnty'),
                total_padej_total_weight=Sum('padej_total_weight'),
                total_padej_avg_weight=Avg('padej_avg_weight'),

                total_prirezka_qnty=Sum('prirezka_qnty'),
                total_prirezka_total_weight=Sum('prirezka_total_weight'),
                total_prirezka_avg_weight=Avg('prirezka_avg_weight'),

                total_vinuzhd_qnty=Sum('vinuzhd_qnty'),
                total_vinuzhd_total_weight=Sum('vinuzhd_total_weight'),
                total_vinuzhd_avg_weight=Avg('vinuzhd_avg_weight'),

                total_spec_qnty=Sum('spec_qnty'),
                total_spec_total_weight=Sum('spec_total_weight'),
                total_spec_avg_weight=Avg('spec_avg_weight'),
                )


class ReportDateManager(CoreModelManager):
    def get_queryset(self):
        return ReportDateQuerySet(self.model, using=self._db)

    def get_exist_from_range(self, start_date, end_date):
        return self.get_queryset().filter(date__in=daterange(start_date, end_date)).values_list('date', flat=True)

    def create_bulk_if_none_from_range(self, start_date, end_date):
        exist = list(self.get_exist_from_range(start_date, end_date))
        input_dates = list(daterange(start_date, end_date))
        not_exist_dates = [date for date in input_dates if date not in exist]

        return self.bulk_create([ReportDate(date=date) for date in not_exist_dates])

    def gen_list_for_create(self, start_date, end_date):
        for single_date in daterange(start_date, end_date):
            yield ReportDate(date=single_date)

    def create_by_year(self, year):
        start_date = date(year, 1, 1)
        end_date = timezone.now().date()
        dates = self.gen_list_for_create(start_date, end_date)        
        return self.bulk_create(dates)


class ReportDate(CoreModel):
    date = models.DateField()

    objects = ReportDateManager()

    def __str__(self):
        return f'{self.date}'

    def substract_qs_values_lists(self, qs1_values_list, qs2_values_list):
        return list((Counter(qs1_values_list) - Counter(qs2_values_list)).elements())

    def count_sows_ws3(self, day=None, start_date=None):
        if not day:
            day = self.date

        ws_locs = Location.objects.all().get_workshop_location_by_number(workshop_number=3)
        sows_in = SowTransaction.objects.trs_in_ws(ws_number=3, ws_locs=ws_locs, end_date=day)\
            .values_list('sow__farm_id', flat=True)
        sows_out = SowTransaction.objects.trs_out_ws(ws_locs=ws_locs, end_date=day)\
            .values_list('sow__farm_id', flat=True)

        sows_dead = CullingSow.objects.in_ws(ws_locs=ws_locs, end_date=day) \
            .values_list('sow__farm_id', flat=True)

        result = self.substract_qs_values_lists(qs1_values_list=sows_in,
             qs2_values_list=sows_out)
        result = self.substract_qs_values_lists(qs1_values_list=result,
             qs2_values_list=sows_dead)

        sows = Sow.objects.get_queryset_with_not_alive() \
                        .filter(farm_id__in=result) \
                        .select_related('status') \
                        .add_status_at_date(date=day) \
                        .count_sows_by_statuses_at_date(date=day)
        return sows
    
    @property
    def count_sows_ws3_start_date(self):
        sow = self.count_sows_ws3(day=self.date - timedelta(1)).first()
        return {
            'suporos': sow.count_status_sup35 + sow.count_status_abort, # + count sup at 25/06
            'suporos2': sow.count_status_sup35,
            'podsos': sow.count_status_oporos + sow.count_status_otiem + sow.count_status_korm, # + count podsos at 25/06
            'podsos2': f'{sow.count_status_oporos} , {sow.count_status_otiem} , {sow.count_status_korm}',
        }

    @property
    def count_sows_ws3_end_date(self):
        sow = self.count_sows_ws3(day=self.date + timedelta(1)).first()
        return {
            'suporos': sow.count_status_sup35 + sow.count_status_abort,
            'podsos': sow.count_status_oporos + sow.count_status_otiem + sow.count_status_korm,
        }

    # def count_all_pigs_ws3(self):

        

# For operations view
def gen_operations_dict():
    operations_data = dict()

    operations_data['ws1_semination'] = \
        {'qs': Semination.objects.all() \
            .select_related('sow', 'tour', 'initiator', 'semination_employee', 'boar') \
            .annotate(
                oper_name=Value('ws1_semination', output_field=models.CharField())),
         'serializer': operation_serializers.OpSeminationSerializer,
         'target': 'sow'
        }

    operations_data['ws1_usound'] = { 
        'qs': Ultrasound.objects.filter(location__workshop__number=1) \
            .select_related('sow', 'tour', 'initiator', 'u_type', 'location__workshop') \
            .annotate(oper_name=Value('ws1_usound',  output_field=models.CharField())), 
        'serializer': operation_serializers.OpUsoundSerializer,
        'target': 'sow'
        }

    operations_data['ws1_abort'] = {'qs':  AbortionSow.objects.filter(location__workshop__number=1) \
            .select_related('sow', 'tour', 'initiator', 'location__workshop') \
            .annotate(oper_name=Value('ws1_abort',  output_field=models.CharField())),
        'serializer': operation_serializers.OpAbortSerializer,
        'target': 'sow'  } 

    operations_data['ws1_culling'] = {'qs':  CullingSow.objects.filter(location__workshop__number=1) \
            .select_related('sow', 'tour', 'initiator', 
                'location__workshop', 
                'location__sowAndPigletsCell__section', 
                'location__sowAndPigletsCell__workshop') \
            .annotate(oper_name=Value('ws1_culling',  output_field=models.CharField())),
        'serializer': operation_serializers.OpCullingSowSerializer,
        'target': 'sow' }

    operations_data['w1_peregon_sow'] = {'qs':  SowTransaction.objects \
            .filter(from_location__workshop__number=1)\
            .select_related('sow', 'tour', 'initiator', 
                'from_location__workshop', 
                'to_location__workshop') \
            .annotate(oper_name=Value('w1_peregon_sow',  output_field=models.CharField())),
        'serializer': operation_serializers.OpSowTransactionSerializer,
        'target': 'sow' }

    operations_data['ws2_usound'] = {'qs':  Ultrasound.objects.filter(location__workshop__number=2) \
            .select_related('sow', 'tour', 'initiator', 'u_type', 'location__workshop') \
            .annotate(oper_name=Value('ws2_usound',  output_field=models.CharField())),
        'serializer': operation_serializers.OpUsoundSerializer,
        'target': 'sow'  }

    operations_data['ws2_abort'] = {'qs':  AbortionSow.objects.filter(location__workshop__number=2) \
            .select_related('sow', 'tour', 'initiator', 'location__workshop') \
            .annotate(oper_name=Value('ws2_abort',  output_field=models.CharField())),
        'serializer': operation_serializers.OpAbortSerializer,
        'target': 'sow' }

    operations_data['ws2_culling'] = {'qs':  CullingSow.objects.filter(location__workshop__number=2) \
            .select_related('sow', 'tour', 'initiator', 
                'location__workshop', 
                'location__sowAndPigletsCell__section', 
                'location__sowAndPigletsCell__workshop') \
            .annotate(oper_name=Value('ws2_culling',  output_field=models.CharField())),
        'serializer': operation_serializers.OpCullingSowSerializer,
        'target': 'sow' }

    operations_data['w2_peregon_sow'] = {'qs':  SowTransaction.objects \
            .filter(from_location__workshop__number=2)\
            .select_related('sow', 'tour', 'initiator', 
                'from_location__workshop', 'to_location__workshop') \
            .annotate(oper_name=Value('w2_peregon_sow',  output_field=models.CharField())),
        'serializer': operation_serializers.OpSowTransactionSerializer,
        'target': 'sow' }

    ws3_locs = Location.objects.all().get_workshop_location_by_number(workshop_number=3)
    ws3_locs_exclude_ws = Location.objects.all().get_workshop_location_by_number(workshop_number=3) \
        .exclude(workshop__number=3)
    not_ws3_locs = Location.objects.all().get_locations_exclude_workshop_locations(workshop_number=3)

    operations_data['ws3_farrow'] = {'qs':  SowFarrow.objects.all()\
            .select_related('sow', 'location__sowAndPigletsCell__section', 'tour', 'initiator',
             'location__sowAndPigletsCell__workshop') \
            .annotate(
                oper_name=Value('ws3_farrow',output_field=models.CharField())),
        'serializer': operation_serializers.OpSowFarrowSerializer,
        'target': 'sow' }

    operations_data['ws3_abort'] = {'qs':  AbortionSow.objects \
            .filter(location__in=ws3_locs) \
            .select_related('sow', 'tour', 'initiator', 'location__workshop', 
                'location__sowAndPigletsCell__section', 'location__sowAndPigletsCell__workshop') \
            .annotate(oper_name=Value('ws3_abort',  output_field=models.CharField())),
        'serializer': operation_serializers.OpAbortSerializer,
        'target': 'sow' }

    operations_data['ws3_sow_culling'] = {'qs':  CullingSow.objects.filter(location__in=ws3_locs)\
            .select_related('sow', 'tour', 'initiator', 
                'location__workshop', 
                'location__sowAndPigletsCell__section',
                'location__sowAndPigletsCell__workshop') 
            .annotate(oper_name=Value('ws3_sow_culling',  output_field=models.CharField())),
        'serializer': operation_serializers.OpCullingSowSerializer,
        'target': 'sow' }

    operations_data['ws3_sow_rassadka'] = {'qs':  SowTransaction.objects \
            .filter(from_location__workshop__number=3, to_location__in=ws3_locs)\
            .select_related('sow', 'tour', 'initiator', 
                'from_location__workshop',
                'to_location__sowAndPigletsCell__section',
                'to_location__sowAndPigletsCell__workshop') \
            .annotate(oper_name=Value('ws3_sow_rassadka',  output_field=models.CharField())),
        'serializer': operation_serializers.OpSowTransactionSerializer,
        'target': 'sow' }

    operations_data['ws3_sow_otiem'] = {'qs':  SowTransaction.objects \
            .filter(from_location__in=ws3_locs, to_location__in=not_ws3_locs) \
            .select_related('sow', 'tour', 'initiator', 
                'to_location__workshop',
                'from_location__sowAndPigletsCell__section', 
                'from_location__sowAndPigletsCell__workshop') \
            .annotate(oper_name=Value('ws3_sow_otiem',  output_field=models.CharField())),
        'serializer': operation_serializers.OpSowTransactionSerializer,
        'target': 'sow' }

    operations_data['ws3_sow_inner'] = {'qs':  SowTransaction.objects
            .filter(from_location__in=ws3_locs_exclude_ws, to_location__in=ws3_locs_exclude_ws)\
            .select_related('sow', 'tour', 'initiator', 
                'from_location__workshop',
                'from_location__sowAndPigletsCell__section', 
                'from_location__sowAndPigletsCell__workshop',
                'to_location__workshop', 
                'to_location__sowAndPigletsCell__section',
                'to_location__sowAndPigletsCell__workshop') \
            .annotate(oper_name=Value('ws3_sow_inner',  output_field=models.CharField())),
        'serializer': operation_serializers.OpSowTransactionSerializer,
        'target': 'sow' }

    operations_data['ws3_mark_as_nurse'] = {'qs':  MarkAsNurse.objects.all() \
            .select_related('sow', 'tour', 'initiator') \
            .annotate(oper_name=Value('ws3_mark_as_nurse', output_field=models.CharField())),
        'serializer': operation_serializers.OpMarkAsNurseSerializer,
        'target': 'sow' }

    operations_data['ws3_mark_as_gilt'] = {'qs': MarkAsGilt.objects.all()\
            .select_related('sow', 'tour', 'initiator', 'gilt') \
            .annotate(oper_name=Value('ws3_mark_as_gilt', output_field=models.CharField())),
        'serializer': operation_serializers.OpMarkAsGiltSerializer,
        'target': 'piglets' }

    operations_data['ws3_piglets_padej'] = {'qs': CullingPiglets.objects \
            .filter(location__in=ws3_locs, culling_type='padej')\
            .select_related('initiator', 'week_tour',
                'location__sowAndPigletsCell__workshop',
                'location__sowAndPigletsCell__section','piglets_group') \
            .annotate(oper_name=Value('ws3_piglets_padej', output_field=models.CharField())),
        'serializer': operation_serializers.OpPigletsCullingSerializer,
        'target': 'piglets' }

    operations_data['ws3_piglets_prirezka'] = {'qs': CullingPiglets.objects
            .filter(location__in=ws3_locs, culling_type='prirezka')\
            .select_related('initiator',  'week_tour',
                'location__sowAndPigletsCell__workshop',
                'location__sowAndPigletsCell__section','piglets_group') \
            .annotate(oper_name=Value('ws3_piglets_prirezka', output_field=models.CharField())),
        'serializer': operation_serializers.OpPigletsCullingSerializer,
        'target': 'piglets' }

    operations_data['ws3_piglets_vinuzhd'] = {'qs': CullingPiglets.objects
                .filter(location__in=ws3_locs, culling_type='vinuzhd')\
                .select_related('initiator',  'week_tour',
                    'location__pigletsGroupCell__workshop',
                    'location__pigletsGroupCell__section', 'piglets_group') \
                .annotate(oper_name=Value('ws3_piglets_vinuzhd', output_field=models.CharField())),
            'serializer': operation_serializers.OpPigletsCullingSerializer,
            'target': 'piglets' }

    operations_data['ws3_piglets_inner_trs'] = {'qs': PigletsTransaction.objects
            .filter(from_location__in=ws3_locs_exclude_ws, to_location__in=ws3_locs)\
            .select_related('initiator', 'week_tour',
                'from_location__workshop',
                'from_location__sowAndPigletsCell__workshop',
                'from_location__sowAndPigletsCell__section', 
                'to_location__sowAndPigletsCell__workshop',
                'to_location__sowAndPigletsCell__section', 'piglets_group') \
            .annotate(oper_name=Value('ws3_piglets_inner_trs', output_field=models.CharField())),
        'serializer': operation_serializers.OpPigletsTransactionSerializer,
        'target': 'piglets' }

    operations_data['ws3_piglets_outer_trs'] = {'qs': PigletsTransaction.objects \
            .filter(from_location__in=ws3_locs, to_location__in=not_ws3_locs)\
            .select_related('initiator', 'week_tour',
                'from_location__workshop',
                'from_location__sowAndPigletsCell__workshop',
                'from_location__sowAndPigletsCell__section',
                'to_location__workshop',
                'piglets_group'
                ) \
            .annotate(oper_name=Value('ws3_piglets_outer_trs', output_field=models.CharField())),
        'serializer': operation_serializers.OpPigletsTransactionSerializer,
        'target': 'piglets' }

    ws75_locs = Location.objects.all().get_workshop_location_by_number(workshop_number=11)
    
    for ws_number in [4, 8, 5, 6, 7]:
        ws_locs = Location.objects.all().get_workshop_location_by_number(workshop_number=ws_number)
        ws_locs_exclude_ws = ws_locs.exclude(workshop__number=ws_number)
        not_ws_locs = Location.objects.all() \
            .get_locations_exclude_workshop_locations(workshop_number=ws_number)\
            .exclude(Q(
                Q(workshop__number=11) |
                Q(pigletsGroupCell__workshop__number=11) | 
                Q(section__workshop__number=11) |
                Q(sowAndPigletsCell__workshop__number=11)
                )
            )

        place = '4/8' 

        if ws_number == 4:
            place = '3/4'
        
        if ws_number == 8:
            place = '4/8' 
        
        if ws_number == 5:
            place = '8/5' 
        
        if ws_number == 6:
            place = '8/6' 
        
        if ws_number == 7:
            place = '8/7' 

        operations_data[f'ws{ws_number}_weighing'] = {'qs': WeighingPiglets.objects
                .filter(place=place)\
                .select_related('initiator', 'week_tour') \
                .annotate(oper_name=Value(f'ws{ws_number}_weighing', output_field=models.CharField())),
            'serializer': operation_serializers.OpPigletsWeighingSerializer,
            'target': 'piglets' }

        operations_data[f'ws{ws_number}_piglets_padej'] = {'qs': CullingPiglets.objects
                .filter(location__in=ws_locs, culling_type='padej')\
                .select_related('initiator',  'week_tour',
                    'location__pigletsGroupCell__workshop',
                    'location__pigletsGroupCell__section', 'piglets_group') \
                .annotate(oper_name=Value(f'ws{ws_number}_piglets_padej', output_field=models.CharField())),
            'serializer': operation_serializers.OpPigletsCullingSerializer,
            'target': 'piglets' }

        if ws_number in [4, 8]:
            operations_data[f'ws{ws_number}_piglets_prirezka'] = {'qs': CullingPiglets.objects
                    .filter(location__in=ws_locs, culling_type='prirezka')\
                    .select_related('initiator',  'week_tour',
                        'location__pigletsGroupCell__workshop',
                        'location__pigletsGroupCell__section', 'piglets_group') \
                    .annotate(oper_name=Value(f'ws{ws_number}_piglets_prirezka', output_field=models.CharField())),
                'serializer': operation_serializers.OpPigletsCullingSerializer,
                'target': 'piglets' }

        operations_data[f'ws{ws_number}_piglets_vinuzhd'] = {'qs': CullingPiglets.objects
                .filter(location__in=ws_locs, culling_type='vinuzhd')\
                .select_related('initiator',  'week_tour',
                    'location__pigletsGroupCell__workshop',
                    'location__pigletsGroupCell__section', 'piglets_group') \
                .annotate(oper_name=Value(f'ws{ws_number}_piglets_vinuzhd', output_field=models.CharField())),
            'serializer': operation_serializers.OpPigletsCullingSerializer,
            'target': 'piglets' }

        operations_data[f'ws{ws_number}_piglets_rassadka'] = {'qs': PigletsTransaction.objects
                .filter(from_location__workshop__number=ws_number, to_location__in=ws_locs)\
                .select_related('initiator', 'week_tour',
                    'from_location__workshop',
                    'to_location__pigletsGroupCell__workshop',
                    'to_location__pigletsGroupCell__section',
                    'piglets_group'
                ) \
                .annotate(oper_name=Value(f'ws{ws_number}_piglets_rassadka', output_field=models.CharField())),
            'serializer': operation_serializers.OpPigletsTransactionSerializer,
            'target': 'piglets' }

        operations_data[f'ws{ws_number}_piglets_inner_trs'] = {'qs': PigletsTransaction.objects
                .filter(from_location__in=ws_locs.exclude(workshop__number=ws_number),
                         to_location__in=ws_locs_exclude_ws)\
                .select_related('initiator', 'week_tour',
                    'from_location__pigletsGroupCell__workshop',
                    'from_location__pigletsGroupCell__section',
                    'to_location__pigletsGroupCell__workshop',
                    'to_location__pigletsGroupCell__section',
                    'piglets_group'
                ) \
                .annotate(oper_name=Value(f'ws{ws_number}_piglets_inner_trs', output_field=models.CharField())),
            'serializer': operation_serializers.OpPigletsTransactionSerializer,
            'target': 'piglets' }

        operations_data[f'ws{ws_number}_piglets_outer_trs'] = {'qs': PigletsTransaction.objects
                .filter(from_location__in=ws_locs, to_location__in=not_ws_locs)\
                .select_related('initiator', 'week_tour',
                    'from_location__pigletsGroupCell__workshop',
                    'from_location__pigletsGroupCell__section',
                    'to_location__workshop',
                    'piglets_group'
                ) \
                .annotate(oper_name=Value(f'ws{ws_number}_piglets_outer_trs', output_field=models.CharField())),
            'serializer': operation_serializers.OpPigletsTransactionSerializer,
            'target': 'piglets' }

        if ws_number in [5, 6, 7]:
            operations_data[f'ws{ws_number}_piglets_spec'] = {'qs': CullingPiglets.objects
                        .filter(location__in=ws_locs, culling_type='spec')\
                        .select_related('initiator',  'week_tour',
                            'location__pigletsGroupCell__workshop',
                            'location__pigletsGroupCell__section',
                            'piglets_group'
                             ) \
                        .annotate(oper_name=Value(f'ws{ws_number}_piglets_spec', output_field=models.CharField())),
                    'serializer': operation_serializers.OpPigletsSpecSerializer,
                    'target': 'piglets' }

            operations_data[f'ws{ws_number}_piglets_to_75'] = {'qs': PigletsTransaction.objects
                .filter(from_location__in=ws_locs, to_location__in=ws75_locs)\
                .select_related('initiator', 'week_tour',
                    'from_location__pigletsGroupCell__workshop',
                    'from_location__pigletsGroupCell__section',
                    'to_location__workshop',
                    'piglets_group'
                ) \
                .annotate(oper_name=Value(f'ws{ws_number}_piglets_to_75', output_field=models.CharField())),
            'serializer': operation_serializers.OpPigletsTransactionSerializer,
            'target': 'piglets' }

    return operations_data


def gen_megadict(request_json):
    final_dict = {'additional_data': {}, 'results': []}
    megalist = list()
    operations_data = gen_operations_dict()
    culling_piglets_padej_qss = CullingPiglets.objects.none()
    culling_piglets_prirezka_qss = CullingPiglets.objects.none()
    culling_piglets__qss = CullingPiglets.objects.none()
    culling_sow_padej_qss = CullingSow.objects.none()
    sow_farrow_qss = SowFarrow.objects.none()
    sow_nurse_qss = MarkAsNurse.objects.none()
    mark_gilt_qss = MarkAsGilt.objects.none()

    for operation_key in request_json['operations'].keys():
        if request_json['operations'][operation_key]:
            qs = operations_data[operation_key]['qs']
            
            if request_json['filters']['farm_id']:
                if operations_data[operation_key]['target'] != 'sow':
                    continue
                else:
                    qs = qs.filter(sow__farm_id=request_json['filters']['farm_id'])

            if request_json['filters']['start_date']:
                qs = qs.filter(date__date__gte=request_json['filters']['start_date'])
            if request_json['filters']['end_date']:
                qs = qs.filter(date__date__lte=request_json['filters']['end_date'])

            # if request_json['filters']['week_tour']:
            #     qs = qs.filter(=request_json['filters']['week_tour'])

            serializer = operations_data[operation_key]['serializer']
            data = serializer(qs, many=True).data

            if 'piglets_padej' in operation_key:
                culling_piglets_padej_qss = culling_piglets_padej_qss | qs

            if 'ws1_culling' in operation_key or 'ws2_culling' in operation_key \
                or 'ws3_sow_culling' in operation_key:
                culling_sow_padej_qss = culling_sow_padej_qss | qs

            if 'piglets_prirezka' in operation_key:
                culling_piglets_prirezka_qss = culling_piglets_prirezka_qss | qs    

            if 'ws3_farrow' in operation_key:
                sow_farrow_qss = sow_farrow_qss | qs

            if 'ws3_mark_as_nurse' in operation_key:
                sow_nurse_qss = sow_nurse_qss | qs

            if 'ws3_mark_as_gilt' in operation_key:
                mark_gilt_qss = mark_gilt_qss | qs
            
            for i in data:
                megalist.append(i)

    megalist = sorted(megalist, key=lambda x: (datetime.strptime(x['date'], '%d-%m-%Y %H:%M:%S'),
     datetime.strptime(x['created_at'], '%d-%m-%Y %H:%M:%S')), reverse=True)
    
    final_dict['additional_data'] = {
        'piglets_padej_data': culling_piglets_padej_qss.aggregate(total_qnty=models.Sum('quantity'), 
                total_weight=models.Sum('total_weight')),

        'piglets_prirezka_data': culling_piglets_prirezka_qss.aggregate(total_qnty=models.Sum('quantity'), 
                total_weight=models.Sum('total_weight')),

        'sow_padej_data': culling_sow_padej_qss.aggregate(total_qnty=models.Count('*'), 
                total_weight=models.Sum('weight')),

        'sow_nurse': sow_nurse_qss.aggregate(total_qnty=models.Count('*')),

        'mark_as_gilt': mark_gilt_qss.aggregate(total_qnty=models.Count('*')),

        'farrow_data': sow_farrow_qss.aggregate(
            total_count=models.Count('*'), 
            total_alive_quantity=models.Sum('alive_quantity'),
            total_dead_quantity=models.Sum('dead_quantity'),
            total_mummy_quantity=models.Sum('mummy_quantity')
        ),
    } 
    final_dict['results'] = megalist

    return final_dict


# to do: Refract to class
class OperationsData():
    def __init__(self, operations_init_dict, request_operations):
        self.operations_to_show = dict()

        for operation_key in request_operations.keys():
            if request_operations[operation_key]:
                self.operations_to_show[operation_key] = operations_init_dict[operation_key]

        self.megalist = []
        self.additional_data = {}

    def filter_qs(self, request_filters):
        pass
