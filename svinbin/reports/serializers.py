# -*- coding: utf-8 -*-
import datetime

from rest_framework import serializers

from tours.models import Tour
from reports.models import ReportDate

from core.models import CoreModel, CoreModelManager
from sows.models import Sow
from piglets.models import Piglets
from locations.models import Location
from sows_events.models import ( SowFarrow, Semination, Ultrasound, AbortionSow, CullingSow, MarkAsNurse,
 MarkAsGilt )
from piglets_events.models import CullingPiglets, WeighingPiglets
from transactions.models import SowTransaction, PigletsTransaction


class AnnotateFieldsModelSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(AnnotateFieldsModelSerializer, self).__init__(*args, **kwargs)
        if len(args) > 0 and len(args[0]) > 0:
            for field_name in args[0][0].__dict__.keys():
                if field_name[0] == '_' or field_name in self.fields.keys():
                    continue
                self.fields[field_name] = serializers.ReadOnlyField()


class ReportDateSerializer(AnnotateFieldsModelSerializer, serializers.ModelSerializer):
    class Meta:
        model = ReportDate
        fields = '__all__'


class ReportTourSerializer(AnnotateFieldsModelSerializer, serializers.ModelSerializer):
    class Meta:
        model = Tour
        fields = '__all__'


class ReportDateWs3Serializer(AnnotateFieldsModelSerializer, serializers.ModelSerializer):
    count_sows_ws3_start_date = serializers.ReadOnlyField()

    class Meta:
        model = ReportDate
        fields = '__all__'


class StartDateEndDateSerializer(serializers.Serializer):
    start_date = serializers.DateField(format="%Y-%m-%d")
    end_date = serializers.DateField(format="%Y-%m-%d")

    
class TotalWeightsSerializer(serializers.Serializer):
    total_quantity = serializers.IntegerField()
    total_avg = serializers.DecimalField(max_digits=10, decimal_places=2, coerce_to_string=False)
    total_total_weight = serializers.DecimalField(max_digits=10, decimal_places=2, coerce_to_string=False)
    total_avg_age = serializers.DecimalField(max_digits=10, decimal_places=2, coerce_to_string=False)
