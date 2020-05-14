# -*- coding: utf-8 -*-
import datetime

from rest_framework import serializers

from tours.models import Tour

from sows.models import Sow
from piglets.models import Piglets
from locations.models import Location
from sows_events.models import ( SowFarrow, Semination, Ultrasound, AbortionSow,
 CullingSow, MarkAsNurse, MarkAsGilt )
from piglets_events.models import CullingPiglets, WeighingPiglets
from transactions.models import SowTransaction, PigletsTransaction


class OperationsSerializer(serializers.ModelSerializer):
    oper_name = serializers.ReadOnlyField()


class OpSowEventSerializer(OperationsSerializer):
    sow = serializers.ReadOnlyField(source='sow.farm_id')
    tour = serializers.StringRelatedField()
    initiator = serializers.StringRelatedField()
    location = serializers.ReadOnlyField(source='location.get_full_loc')


class OpSeminationSerializer(OpSowEventSerializer):
    semination_employee = serializers.StringRelatedField()
    boar = serializers.ReadOnlyField(source='boar.birth_id')

    class Meta:
        model = Semination
        fields = ['date', 'sow', 'tour', 'initiator', 'semination_employee', 'boar',
        'oper_name']


class OpUsoundSerializer(OpSowEventSerializer):
    u_type = serializers.ReadOnlyField(source='u_type.days')

    class Meta:
        model = Ultrasound
        fields = ['oper_name', 'date', 'sow', 'tour', 'initiator', 'u_type', 'result',
            'location']


class OpAbortSerializer(OpSowEventSerializer):
    class Meta:
        model = AbortionSow
        fields = ['oper_name','date', 'sow', 'tour', 'initiator', 'location' ]


class OpCullingSowSerializer(OpSowEventSerializer):
    class Meta:
        model = CullingSow
        fields = ['oper_name','date', 'sow', 'tour', 'location', 'initiator',
         'culling_type', 'reason', ]


class OpSowFarrowSerializer(OpSowEventSerializer):
    class Meta:
        model = SowFarrow
        fields = ['oper_name', 'date', 'location', 'sow', 'alive_quantity', 'dead_quantity',
         'mummy_quantity', 'tour', 'initiator']


class OpSowTransactionSerializer(OpSowEventSerializer):
    from_location = serializers.ReadOnlyField(source='from_location.get_full_loc')
    to_location = serializers.ReadOnlyField(source='to_location.get_full_loc')

    class Meta:
        model = SowTransaction
        fields = ['oper_name', 'date', 'initiator', 'sow', 'tour', 'from_location', 
            'location', 'to_location']


class OpMarkAsNurseSerializer(OpSowEventSerializer):
    class Meta:
        model = MarkAsNurse
        fields = ['oper_name', 'date', 'initiator', 'sow', 'tour']


class OpMarkAsGiltSerializer(OpSowEventSerializer):
    gilt = serializers.ReadOnlyField(source='gilt.birth_id')

    class Meta:
        model = MarkAsGilt
        fields = ['oper_name', 'date', 'initiator', 'sow', 'tour', 'gilt']


class OperationsSerializer(serializers.ModelSerializer):
    oper_name = serializers.ReadOnlyField()


class OpPigletsEventSerializer(OperationsSerializer):
    week_tour = serializers.StringRelatedField()
    initiator = serializers.StringRelatedField()
    location = serializers.ReadOnlyField(source='location.get_full_loc')
    
    # Todo: 
    age = serializers.ReadOnlyField(source=None)


class OpPigletsCullingSerializer(OpPigletsEventSerializer):
    class Meta:
        model = CullingPiglets
        fields = ['oper_name', 'date', 'initiator', 'location', 'week_tour',
         'culling_type', 'reason', 'quantity', 'total_weight', 'age' ]


class OpPigletsTransactionSerializer(OpPigletsEventSerializer):
    from_location = serializers.ReadOnlyField(source='from_location.get_full_loc')
    to_location = serializers.ReadOnlyField(source='to_location.get_full_loc')

    class Meta:
        model = PigletsTransaction
        fields = ['oper_name', 'date', 'initiator', 'week_tour', 'age', 'from_location',
          'to_location', 'location']


class OpPigletsWeighingSerializer(OpPigletsEventSerializer):
    class Meta:
        model = WeighingPiglets
        fields = ['oper_name', 'date', 'initiator', 'location', 'week_tour',
         'place', 'average_weight', 'piglets_quantity', 'total_weight', 'age' ]