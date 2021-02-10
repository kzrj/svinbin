# # -*- coding: utf-8 -*-
from rest_framework import status, viewsets
from rest_framework.response import Response

from veterinary.models import PigletsVetEvent, Recipe, Drug
from veterinary.serializers import RecipeSerializer, DrugSerializer
from core.permissions import VeterinarPermissions


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [VeterinarPermissions]


class DrugViewSet(viewsets.ModelViewSet):
    queryset = Drug.objects.all()
    serializer_class = DrugSerializer
    permission_classes = [VeterinarPermissions]