# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings


class CoreModelManager(models.Manager):
	pass


class CoreModel(models.Model):
	class Meta:
		abstract = True


class Event(CoreModel):
    date = models.DateTimeField(null=True)
    initiator = models.ForeignKey(settings.AUTH_USER_MODEL,
     on_delete=models.SET_NULL, null=True)
    
    class Meta:
        abstract = True
