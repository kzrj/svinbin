# -*- coding: utf-8 -*-
from django.db import models

# from transactions.models import Location


class SowStatus(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title


class GiltStatus(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title


class Pig(models.Model):
    birth_id = models.CharField(max_length=10)
    location = models.OneToOneField("transactions.Location", on_delete=models.SET_NULL, null=True)

    class Meta:
        abstract = True


class Sow(Pig):
    status = models.ForeignKey(SowStatus, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return 'Sow #%s' % self.birth_id


class Gilt(Pig):
    status = models.ForeignKey(SowStatus, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return 'Gilt #%s' % self.birth_id