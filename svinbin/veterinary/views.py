# # -*- coding: utf-8 -*-
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from locations.models import Section
from locations.serializers import SectionFilterSerializer

from tours.models import Tour
from tours.serializers import TourSimpleSerializer
from piglets.models import Piglets

from veterinary.models import PigletsVetEvent, Recipe, Drug
from veterinary.serializers import RecipeSerializer, DrugSerializer, PigletsVetEventSerializer
from veterinary.filters import RecipeFilter
from core.permissions import VeterinarPermissions


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [VeterinarPermissions]
    filter_class = RecipeFilter

    def destroy(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        super().destroy(*args, **kwargs)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DrugViewSet(viewsets.ModelViewSet):
    queryset = Drug.objects.all()
    serializer_class = DrugSerializer
    permission_classes = [VeterinarPermissions]

    def destroy(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        super().destroy(*args, **kwargs)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PigletsVetEventViewSet(viewsets.ModelViewSet):
    queryset = PigletsVetEvent.objects.all().select_related('location__pigletsGroupCell',
        'location__section', 'recipe__drug')
    serializer_class = PigletsVetEventSerializer
    permission_classes = [VeterinarPermissions]
    # filter_class = RecipeFilter

    def create(self, *args, **kwargs):
        pass

    def destroy(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        super().destroy(*args, **kwargs)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False)
    def get_filters_data(self, request):
        data = dict()
        data['sections'] = SectionFilterSerializer(Section.objects.exclude(workshop__number__in=[1, 2]),
             many=True)

        tours = Tour.objects.get_tours_by_piglets(piglets=Piglets.objects.all())
        data['tours'] = TourSimpleSerializer(tours, many=True)

        return Response(data)