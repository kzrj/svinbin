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

    # add_count_tour_sow
    ws1_count_tour_sow = serializers.ReadOnlyField()
    ws2_count_tour_sow = serializers.ReadOnlyField()
    ws3_count_tour_sow = serializers.ReadOnlyField()

    # farrow_data
    total_born_alive = serializers.ReadOnlyField()
    total_born_dead = serializers.ReadOnlyField()
    total_born_mummy = serializers.ReadOnlyField()
    gilt_count = serializers.ReadOnlyField()

    # add_weight_date
    weight_date_3_4 = serializers.ReadOnlyField()
    weight_date_4_8 = serializers.ReadOnlyField()
    weight_date_8_5 = serializers.ReadOnlyField()
    weight_date_8_6 = serializers.ReadOnlyField()
    weight_date_8_7 = serializers.ReadOnlyField()

    # add_week_weight
    week_weight_avg_3_4 = serializers.ReadOnlyField()
    week_weight_avg_4_8 = serializers.ReadOnlyField()
    week_weight_avg_8_5 = serializers.ReadOnlyField()
    week_weight_avg_8_6 = serializers.ReadOnlyField()
    week_weight_avg_8_7 = serializers.ReadOnlyField()

    week_weight_qnty_3_4 = serializers.ReadOnlyField()
    week_weight_qnty_4_8 = serializers.ReadOnlyField()
    week_weight_qnty_8_5 = serializers.ReadOnlyField()
    week_weight_qnty_8_6 = serializers.ReadOnlyField()
    week_weight_qnty_8_7 = serializers.ReadOnlyField()

    # add_week_weight_ws8_v2
    week_weight_qnty_ws8 = serializers.ReadOnlyField()
    week_weight_avg_ws8 = serializers.ReadOnlyField()

    # add_culling_data_by_week_tour
    ws3_padej_quantity = serializers.ReadOnlyField()
    ws4_padej_quantity = serializers.ReadOnlyField()
    ws8_padej_quantity = serializers.ReadOnlyField()
    ws5_padej_quantity = serializers.ReadOnlyField()
    ws6_padej_quantity = serializers.ReadOnlyField()
    ws7_padej_quantity = serializers.ReadOnlyField()

    ws3_prirezka_quantity = serializers.ReadOnlyField()
    ws4_prirezka_quantity = serializers.ReadOnlyField()
    ws8_prirezka_quantity = serializers.ReadOnlyField()

    ws4_vinuzhd_quantity = serializers.ReadOnlyField()
    ws8_vinuzhd_quantity = serializers.ReadOnlyField()
    ws5_vinuzhd_quantity = serializers.ReadOnlyField()
    ws6_vinuzhd_quantity = serializers.ReadOnlyField()
    ws7_vinuzhd_quantity = serializers.ReadOnlyField()

    ws5_spec_quantity = serializers.ReadOnlyField()
    ws6_spec_quantity = serializers.ReadOnlyField()
    ws7_spec_quantity = serializers.ReadOnlyField()

    ws5_spec_avg_weight = serializers.ReadOnlyField()
    ws6_spec_avg_weight = serializers.ReadOnlyField()
    ws7_spec_avg_weight = serializers.ReadOnlyField()

    # add_piglets_count_by_ws_week_tour
    ws5_piglets_qnty_now = serializers.ReadOnlyField()
    ws6_piglets_qnty_now = serializers.ReadOnlyField()
    ws7_piglets_qnty_now = serializers.ReadOnlyField()

    # add_piglets_count_by_ws_week_tour
    ws3_gilts_qnty_now = serializers.ReadOnlyField()
    ws4_gilts_qnty_now = serializers.ReadOnlyField()
    ws5_gilts_qnty_now = serializers.ReadOnlyField()
    ws6_gilts_qnty_now = serializers.ReadOnlyField()
    ws7_gilts_qnty_now = serializers.ReadOnlyField()
    ws8_gilts_qnty_now = serializers.ReadOnlyField()

    class Meta:
        model = Tour
        fields = '__all__'

