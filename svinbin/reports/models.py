# -*- coding: utf-8 -*-
from datetime import timedelta, date

from django.db import models
from django.db.models import Subquery, OuterRef, F, ExpressionWrapper, Q, Sum, Avg, Count, Value, Func
from django.db.models.functions import Coalesce, Greatest
from django.utils import timezone

from core.models import CoreModel, CoreModelManager
from sows.models import Sow
from sows_events.models import CullingSow, SowFarrow
from piglets.models import Piglets
from piglets_events.models import CullingPiglets
from transactions.models import PigletsTransaction


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

    def add_today_rep_sows_count(self):
        data = dict()
        for ws_number in [1, 2, 3]:
            data[f'ws{ws_number}_count_sow'] = Subquery(
                Sow.objects.filter(
                         Q(
                            Q(location__workshop__number=ws_number) |
                            Q(location__section__workshop__number=ws_number) |
                            Q(location__sowAndPigletsCell__workshop__number=ws_number)
                        )) \
                        .annotate(flag=Value(0))
                        .values('flag') \
                        .annotate(cnt=Count('*')) \
                        .values('cnt'),
                 output_field=models.IntegerField())

        return self.annotate(**data)

    def add_today_rep_piglets_count(self):
        data = dict()
        for ws_number in [3, 4, 8, 5, 6, 7]:
            data[f'ws{ws_number}_count_piglets'] = Subquery(
                Piglets.objects.filter(
                         Q(
                            Q(location__workshop__number=ws_number) |
                            Q(location__section__workshop__number=ws_number) |
                            Q(location__sowAndPigletsCell__workshop__number=ws_number)
                        )) \
                        .annotate(flag=Value(0))
                        .values('flag') \
                        .annotate(cnt=Count('*')) \
                        .values('cnt'),
                 output_field=models.IntegerField())

        return self.annotate(**data)

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
                )



class ReportDateManager(CoreModelManager):
    def get_queryset(self):
        # start_date = date(2020, 1, 1)
        # end_date = timezone.now().date() + timedelta(1)
        # ReportDate.objects.create_bulk_if_none_from_range(start_date, end_date)
        
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
    