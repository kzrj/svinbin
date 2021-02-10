# -*- coding: utf-8 -*-
from rest_framework import serializers

from veterinary.models import PigletsVetEvent, Recipe, Drug


class CreatePigletsVetEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = PigletsVetEvent
        fields = ['recipe', 'date']


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = '__all__'


class DrugSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drug
        fields = '__all__'
