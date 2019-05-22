# -*- coding: utf-8 -*-
from django.db import models

from transactions.models import Location, SowTransaction, GiltTransaction


class SowStatus(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title


class GiltStatus(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title


class Pig(models.Model):
    birth_id = models.CharField(max_length=10, unique=True)
    location = models.OneToOneField("transactions.Location", on_delete=models.SET_NULL, null=True)

    class Meta:
        abstract = True

    # def move_to_workshop(self, location, initiator):
    #     pass


class Sow(Pig):
    status = models.ForeignKey(SowStatus, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return 'Sow #%s' % self.birth_id

    # def move_to_workshop(self, location, initiator):
    #     SowTransaction.objects.create(sow=self, from_location=self.location,
    #      to_location=location, initiator=initiator)


class Gilt(Pig):
    status = models.ForeignKey(SowStatus, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return 'Gilt #%s' % self.birth_id


class PigletsGroup(models.Model):
    # location = models.OneToOneField('transactions.Location', on_delete=models.SET_NULL, null=True)
    location = models.ForeignKey('transactions.Location', on_delete=models.SET_NULL, null=True)
    birth_date = models.DateTimeField(null=True)
    quantity = models.IntegerField()
    # parent_group = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)
    parent_groups = models.ManyToManyField('self', related_name="parent_groups")
    tours = models.ManyToManyField('tours.Tour', related_name="tours")

    # add oporos on other side of OneToOne

    def __str__(self):
        return 'Piglets group #%s' % self.pk