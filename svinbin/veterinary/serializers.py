# -*- coding: utf-8 -*-
from rest_framework import serializers

from veterinary.models import PigletsVetEvent, Recipe, Drug


class CreatePigletsVetEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = PigletsVetEvent
        fields = ['recipe', 'date']


class RecipeSerializer(serializers.ModelSerializer):
    drug_name = serializers.StringRelatedField(source='drug', read_only=True)
    ru_type = serializers.ChoiceField(source='med_type', read_only=True, choices=Recipe.MED_TYPES)
    ru_method = serializers.ChoiceField(source='med_method', read_only=True, choices=Recipe.MED_METHODS)

    class Meta:
        model = Recipe
        fields = '__all__'


class DrugSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drug
        fields = '__all__'
