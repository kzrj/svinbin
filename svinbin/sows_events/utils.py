# -*- coding: utf-8 -*-
from sows_events.models import UltrasoundType


def create_types():
    if UltrasoundType.objects.all().count() == 0:
        UltrasoundType.objects.bulk_create([
            UltrasoundType(days=30),
            UltrasoundType(days=60, final=True),
            ])