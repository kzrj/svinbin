# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings


class CoreModelManager(models.Manager):
    pass


class CoreModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Event(CoreModel):
    date = models.DateTimeField(auto_now_add=True)
    initiator = models.ForeignKey(settings.AUTH_USER_MODEL,
     on_delete=models.SET_NULL, null=True)
    
    class Meta:
        abstract = True
