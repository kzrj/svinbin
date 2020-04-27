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


# https://stackoverflow.com/questions/1060279/iterating-through-a-range-of-dates-in-python
def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)


class ReportDateQuerySet(models.QuerySet):
    def gen_sow_culling_cnt_by_daterange_subquery(self, culling_type, start_date, end_date, *args, **kwargs):
        return Coalesce(
                    Subquery(
                        CullingSow.objects.filter(
                            date__date__gte=start_date, date__date__lt=end_date, culling_type=culling_type) \
                            # date__date__range=(start_date, end_date), culling_type=culling_type) \
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

    def gen_piglets_culling_cnt_by_date_subquery(self, culling_type, target_date):
        return Coalesce(
                    Subquery(
                        CullingPiglets.objects.filter(
                            date__date=target_date, culling_type=culling_type) \
                                    .values('culling_type') \
                                    .annotate(cnt=Count('pk')) \
                                    .values('cnt')
                        ), 0
        )

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
                cnt_padej_subquery_from_date=cnt_padej_subquery,
                cnt_vinuzhd_subquery_from_date=cnt_vinuzhd_subquery,
                sow_qnty_at_date_start=ExpressionWrapper(
                    F('today_start_sows_qnty') + cnt_padej_subquery + cnt_vinuzhd_subquery - cnt_gilts_to_sows,
                    output_field=models.IntegerField()
                    )
                )

    def add_sows_quantity_at_date_end(self):
        today = timezone.now().date()
        end_date = date(2020, 1, 2)

        cnt_padej_subquery = self.gen_sow_culling_cnt_by_date_subquery('padej', OuterRef('date'))

        cnt_vinuzhd_subquery = self.gen_sow_culling_cnt_by_date_subquery('vinuzhd', OuterRef('date'))

        cnt_gilts_to_sows = 0

        return self.annotate(
                cnt_padej_subquery_at_end_date=cnt_padej_subquery,
                cnt_vinuzhd_subquery_at_end_date=cnt_vinuzhd_subquery,
                sows_quantity_at_date_end=ExpressionWrapper(
                    F('sow_qnty_at_date_start') - cnt_padej_subquery - cnt_vinuzhd_subquery + cnt_gilts_to_sows,
                    output_field=models.IntegerField()
                    )
                )

    def add_piglets_today_quantity(self):
        count_piglets = Piglets.objects.all().count()

        today = timezone.now().date()
        # today cullings
        piglets_today_padej_subquery = self.gen_piglets_culling_cnt_by_date_subquery('padej', today)
        piglets_today_prirezka_subquery = self.gen_piglets_culling_cnt_by_date_subquery('prirezka', today)
        piglets_today_vinuzhd_subquery = self.gen_piglets_culling_cnt_by_date_subquery('vinuzhd', today)
        piglets_today_spec_subquery = self.gen_piglets_culling_cnt_by_date_subquery('spec', today)

        # today born alive
        SowFarrow.objects.filter()


        # + cull qnty today - born today
        return self.annotate(piglets_today_qnty=count_piglets)


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
    