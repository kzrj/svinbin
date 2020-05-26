# -*- coding: utf-8 -*-
from operator import itemgetter

from datetime import timedelta, date, datetime

from django.db import models
from django.db.models import Subquery, OuterRef, F, ExpressionWrapper, Q, Sum, Avg, Count, Value
from django.db.models.functions import Coalesce, Greatest
from django.utils import timezone

from core.models import CoreModel, CoreModelManager
from sows.models import Sow
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
        last_date = self.order_by('-date').first()
        pigs_count = 0
        if last_date:
            sows_quantity_at_date_end = last_date.sows_quantity_at_date_end \
                if last_date.sows_quantity_at_date_end else 0
            piglets_qnty_start_end = last_date.piglets_qnty_start_end \
                if last_date.piglets_qnty_start_end else 0
            pigs_count = sows_quantity_at_date_end + piglets_qnty_start_end

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

    operations_data['ws3_sow_culling'] = {'qs':  CullingSow.objects.filter(location__workshop__number=3)\
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

    operations_data['ws3_piglets_inner_trs'] = {'qs': PigletsTransaction.objects
            .filter(from_location__in=ws3_locs_exclude_ws, to_location__in=ws3_locs_exclude_ws)\
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

        if ws_number == 4:
            operations_data[f'ws{ws_number}_piglets_prirezka'] = {'qs': CullingPiglets.objects
                    .filter(location__in=ws_locs, culling_type='prirezka')\
                    .select_related('initiator',  'week_tour',
                        'location__pigletsGroupCell__workshop',
                        'location__pigletsGroupCell__section', 'piglets_group') \
                    .annotate(oper_name=Value(f'ws{ws_number}_piglets_prirezka', output_field=models.CharField())),
                'serializer': operation_serializers.OpPigletsCullingSerializer,
                'target': 'piglets' }

        else:
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


def gen_megalist(request_json):
    megalist = list()
    operations_data = gen_operations_dict()

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
            
            for i in data:
                megalist.append(i)

    megalist = sorted(megalist, key=lambda x: datetime.strptime(x['date'], '%d-%m-%Y %M:%S'),
     reverse=True)
    
    return megalist