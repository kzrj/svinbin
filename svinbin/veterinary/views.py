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

    def destroy(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        super().destroy(*args, **kwargs)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DrugViewSet(viewsets.ModelViewSet):
    queryset = Drug.objects.all()
    serializer_class = DrugSerializer
    permission_classes = [VeterinarPermissions]