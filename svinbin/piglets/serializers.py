# # -*- coding: utf-8 -*-
# from rest_framework import serializers, status

# from core.utils import CustomValidation
# from sows.models import Sow, Gilt
# from piglets.models import NomadPigletsGroup, NewBornPigletsGroup
# from piglets_events.models import NewBornPigletsMerger
# from piglets_events.serializers import WeighingPigletsSerializer
# from locations.models import Location


# class NomadPigletsGroupPkSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = NomadPigletsGroup
#         fields = ('pk',)


# class NomadPigletsGroupSerializer(serializers.ModelSerializer):
#     merger_part_number = serializers.ReadOnlyField()
#     cells_numbers_from_merger = serializers.ReadOnlyField()
#     status = serializers.StringRelatedField()
#     weighing_records = WeighingPigletsSerializer(many=True)

#     class Meta:
#         model = NomadPigletsGroup        
#         fields = '__all__'


# class NewBornPigletsGroupSerializer(serializers.ModelSerializer):
#     tour = serializers.StringRelatedField()
    
#     class Meta:
#         model = NewBornPigletsGroup
#         fields = "__all__"


# class NewBornPigletsGroupPkSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = NewBornPigletsGroup
#         fields = ('pk',)


# class NewBornPigletsGetSerializer(serializers.Serializer):
#     new_born_group = serializers.IntegerField()


# class MoveFromCellToCellSerializer(serializers.Serializer):
#     from_location = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all())
#     to_location = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all())
#     quantity = serializers.IntegerField()
#     gilts_quantity = serializers.IntegerField(default=0)


# class MoveToSerializer(serializers.Serializer):
#     to_location = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all())
#     quantity = serializers.IntegerField()
#     gilts_quantity = serializers.IntegerField(default=0)


# # class MoveOneToCellSerializer(serializers.Serializer):
# #     to_location = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all())
# #     quantity = serializers.IntegerField()
# #     gilts_quantity = serializers.IntegerField(default=0)


# class NewBornGroupsToMerge(serializers.ModelSerializer):
#     class Meta:
#         model = NewBornPigletsMerger
#         fields = ['piglets_groups', ]