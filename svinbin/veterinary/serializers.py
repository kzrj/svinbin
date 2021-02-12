# -*- coding: utf-8 -*-
from rest_framework import serializers

from veterinary.models import PigletsVetEvent, Recipe, Drug
from piglets.models import Piglets


class CreatePigletsVetEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = PigletsVetEvent
        fields = ['recipe', 'date']


class ChoiceField(serializers.ChoiceField):

    def to_representation(self, obj):
        if obj == '' and self.allow_blank:
            return obj
        return self._choices[obj]

    def to_internal_value(self, data):
        # To support inserts with the value
        if data == '' and self.allow_blank:
            return ''

        for key, val in self._choices.items():
            if val == data:
                return key
        self.fail('invalid_choice', input=data)


class RecipeSerializer(serializers.ModelSerializer):
    drug_name = serializers.StringRelatedField(source='drug', read_only=True)
    ru_type = ChoiceField(source='med_type', read_only=True, choices=Recipe.MED_TYPES)
    ru_method = ChoiceField(source='med_method', read_only=True, choices=Recipe.MED_METHODS)

    class Meta:
        model = Recipe
        fields = '__all__'


class DrugSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drug
        fields = '__all__'


class PigletsVetEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = PigletsVetEvent
        fields = '__all__'


class PigletsVetEventsSerializer(serializers.ModelSerializer):
    # metatour_repr = serializers.ReadOnlyField()
    week_tour = serializers.StringRelatedField(source='metatour.week_tour')
    age = serializers.DurationField()
    tagret_vet_events = serializers.StringRelatedField(source='piglets_vet_events_as_target',
         many=True)

    class Meta:
        model = Piglets
        fields = ['id', 'quantity', 'gilts_quantity', 'transfer_part_number', 
            'birthday', 'week_tour', 'age', 'tagret_vet_events']