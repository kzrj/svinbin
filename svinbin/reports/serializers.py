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

from core.serializers import AnnotateFieldsModelSerializer


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
