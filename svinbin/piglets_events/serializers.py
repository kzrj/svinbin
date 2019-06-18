# -*- coding: utf-8 -*-
from rest_framework import serializers

from piglets_events.models import NewBornPigletsGroupRecount, NewBornPigletsMerger


class NewBornPigletsGroupRecountSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewBornPigletsGroupRecount
        fields = "__all__"


class NewBornPigletsGroupMerger(serializers.ModelSerializer):
    class Meta:
        model = NewBornPigletsMerger
        fields = "__all__"    