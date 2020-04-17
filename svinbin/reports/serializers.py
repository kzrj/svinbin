# -*- coding: utf-8 -*-
import datetime

from rest_framework import serializers

from tours.models import Tour


class AnnotateFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Instantiate the superclass normally
        super(AnnotateFieldsModelSerializer, self).__init__(*args, **kwargs)
        # print(self.fields)
        # print(type(self.fields))
        # print(kwargs)
        # print(args)
        # # print(args[0].piglets_age)
        # print(args[0])
        # print(type(args[0]))
        # print(args[0].__dict__.keys())

        # TODO: args[0] - object or queryset

        fields = args[0].__dict__.keys()
        fields = args[0].__dict__.keys()
        if fields:
            for field_name in fields:
                if field_name[0] == '_' or field_name in self.fields.keys():
                    continue
                self.fields[field_name] = serializers.ReadOnlyField()


class ReportTourSerializer2(AnnotateFieldsModelSerializer, serializers.ModelSerializer):
    class Meta:
        model = Tour
        fields = '__all__'



class ReportTourSerializer(serializers.ModelSerializer):
    piglets_age = serializers.ReadOnlyField()

    # sow data
    count_sow = serializers.ReadOnlyField()
    count_seminated = serializers.ReadOnlyField()
    count_usound28_suporos = serializers.ReadOnlyField()
    count_usound28_proholost = serializers.ReadOnlyField()
    count_usound35_suporos = serializers.ReadOnlyField()
    count_usound35_proholost = serializers.ReadOnlyField()
    count_abort = serializers.ReadOnlyField()

    ws1_count_tour_sow = serializers.ReadOnlyField()
    ws2_count_tour_sow = serializers.ReadOnlyField()
    ws3_count_tour_sow = serializers.ReadOnlyField()

    # farrow_data
    total_born_alive = serializers.ReadOnlyField()
    total_born_dead = serializers.ReadOnlyField()
    total_born_mummy = serializers.ReadOnlyField()
    gilt_count = serializers.ReadOnlyField()

    # current_not_mixed_piglets_quantity
    total_not_mixed_piglets = serializers.ReadOnlyField()
    ws3_qnty_not_mixed = serializers.ReadOnlyField()
    ws4_qnty_not_mixed = serializers.ReadOnlyField()
    ws8_qnty_not_mixed = serializers.ReadOnlyField()
    ws5_qnty_not_mixed = serializers.ReadOnlyField()
    ws6_qnty_not_mixed = serializers.ReadOnlyField()
    ws7_qnty_not_mixed = serializers.ReadOnlyField()

    # current_mixed_piglets_quantity
    total_mixed_piglets = serializers.ReadOnlyField()
    ws3_qnty_mixed = serializers.ReadOnlyField()
    ws4_qnty_mixed = serializers.ReadOnlyField()
    ws8_qnty_mixed = serializers.ReadOnlyField()
    ws5_qnty_mixed = serializers.ReadOnlyField()
    ws6_qnty_mixed = serializers.ReadOnlyField()
    ws7_qnty_mixed = serializers.ReadOnlyField()

    # weight_data_not_mixed
    total_weight_not_mixed_3_4 = serializers.ReadOnlyField()
    total_weight_not_mixed_4_8 = serializers.ReadOnlyField()
    total_weight_not_mixed_8_5 = serializers.ReadOnlyField()
    total_weight_not_mixed_8_6 = serializers.ReadOnlyField()
    total_weight_not_mixed_8_7 = serializers.ReadOnlyField()

    # weight_data_mixed
    total_weight_mixed_3_4 = serializers.ReadOnlyField()
    total_weight_mixed_4_8 = serializers.ReadOnlyField()
    total_weight_mixed_8_5 = serializers.ReadOnlyField()
    total_weight_mixed_8_6 = serializers.ReadOnlyField()
    total_weight_mixed_8_7 = serializers.ReadOnlyField()

    # avg_weight_data (?mixed)
    avg_weight_data_3_4 = serializers.ReadOnlyField()
    avg_weight_data_4_8 = serializers.ReadOnlyField()
    avg_weight_data_8_5 = serializers.ReadOnlyField()
    avg_weight_data_8_6 = serializers.ReadOnlyField()
    avg_weight_data_8_7 = serializers.ReadOnlyField()

    # weight_date
    weight_date_3_4 = serializers.ReadOnlyField()
    weight_date_4_8 = serializers.ReadOnlyField()
    weight_date_8_5 = serializers.ReadOnlyField()
    weight_date_8_6 = serializers.ReadOnlyField()
    weight_date_8_7 = serializers.ReadOnlyField()

    # age_at_weight_date
    age_at_3_4 = serializers.ReadOnlyField()
    age_at_4_8 = serializers.ReadOnlyField()
    age_at_8_5 = serializers.ReadOnlyField()
    age_at_8_6 = serializers.ReadOnlyField()
    age_at_8_7 = serializers.ReadOnlyField()

    # culling_weight_not_mixed_piglets
    padej_weight = serializers.ReadOnlyField()
    prirezka_weight = serializers.ReadOnlyField()
    vinuzhd_weight = serializers.ReadOnlyField()
    spec_weight = serializers.ReadOnlyField()

    # culling_qnty_not_mixed_piglets
    padej_quantity = serializers.ReadOnlyField()
    prirezka_quantity = serializers.ReadOnlyField()
    vinuzhd_quantity = serializers.ReadOnlyField()
    spec_quantity = serializers.ReadOnlyField()

    # culling_avg_weight_not_mixed_piglets
    padej_avg_weight = serializers.ReadOnlyField()
    prirezka_avg_weight = serializers.ReadOnlyField()
    vinuzhd_avg_weight = serializers.ReadOnlyField()
    spec_avg_weight = serializers.ReadOnlyField()

    padej_avg_weight_mixed = serializers.ReadOnlyField()
    prirezka_avg_weight_mixed = serializers.ReadOnlyField()
    vinuzhd_avg_weight_mixed = serializers.ReadOnlyField()
    spec_avg_weight_mixed = serializers.ReadOnlyField()

    # culling_percentage_not_mixed_piglets
    padej_percentage = serializers.ReadOnlyField()
    prirezka_percentage = serializers.ReadOnlyField()
    vinuzhd_percentage = serializers.ReadOnlyField()
    spec_percentage = serializers.ReadOnlyField()

    class Meta:
        model = Tour
        fields = '__all__'

