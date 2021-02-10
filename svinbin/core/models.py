# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.utils import timezone


class CoreQuerySet(models.QuerySet):
    def add_missing_fields_for_union(self, fields=[]):
        data = dict()
        for field in fields:
            if field == 'result':
                data[field] = models.Value(False, output_field=models.BooleanField())
            else:
                data[field] = models.Value(0, output_field=models.IntegerField())

        return self.annotate(**data)

    def values_for_union(self, label):
        return self.values(
                op_date=models.F('date'),
                op_week=models.F('tour__week_number'),
                op_initiator=models.F('initiator__username'),
                op_uzi_result=models.F('result'),
                op_from_location=models.F('from_location'),
                op_to_location=models.F('to_location'),
                op_label=models.Value(label, output_field=models.CharField()),
                )

    def prepare_and_return_union_values(self, label, fields=[]):
        return self.add_missing_fields_for_union(fields=fields) \
                .values_for_union(label=label)


class CoreModelManager(models.Manager):
    def create(self, *args, **kwargs):
        if 'date' in kwargs and not kwargs['date']:
            kwargs['date'] = timezone.now()

        return super(CoreModelManager, self).create(*args, **kwargs)  


class CoreModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Event(CoreModel):
    date = models.DateTimeField(null=True)
    initiator = models.ForeignKey(settings.AUTH_USER_MODEL,
     on_delete=models.SET_NULL, null=True)
    
    class Meta:
        abstract = True
