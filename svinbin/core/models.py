# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings


class CoreModelManager(models.Manager):
    pass
    # def create(self, *args, **kwargs):
    #     last_pk = self.all().order_by('-pk').first().pk
    #     kwargs['id'] = last_pk + 1
    #     print(kwargs)
    #     return super(CoreModelManager, self).create(*args, **kwargs)


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
