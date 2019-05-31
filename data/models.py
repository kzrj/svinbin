# -*- coding: utf-8 -*-
from django.db import models

from transactions.models import Location, SowTransaction, GiltTransaction
from workshops.models import Section, SowGroupCell, WorkShop


class SowStatus(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title


class GiltStatus(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title


class Pig(models.Model):
    birth_id = models.CharField(max_length=10, unique=True, null=True)
    location = models.OneToOneField("transactions.Location", on_delete=models.SET_NULL, null=True)

    class Meta:
        abstract = True

    # def move_to_workshop(self, location, initiator):
    #     pass


class SowManager(models.Manager):
    def create_new_from_gilt_and_put_in_workshop_one(self, farm_id):
        # DECREASE GILT QUANTITY!!!
        
        return self.create(farm_id=farm_id,
            location=Location.objects.create_location(pre_location=WorkShop.objects.get(number=1)))

    def get_or_create_by_farm_id(self, farm_id):
        sow = Sow.objects.filter(farm_id=farm_id).first()
        if not sow:
            return self.create_new_from_gilt_and_put_in_workshop_one(farm_id)
        return sow

    def get_by_farm_id(self, farm_id):
        sow = Sow.objects.filter(farm_id=farm_id).first()
        # if not sow:
        #     raise error
        return sow



class Sow(Pig):
    farm_id = models.IntegerField(null=True, unique=True)
    status = models.ForeignKey(SowStatus, on_delete=models.SET_NULL, null=True)

    objects = SowManager()

    def __str__(self):
        return 'Sow #%s' % self.farm_id

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
    # parent_groups = models.ManyToManyField('self', related_name="parent_groups")
    # tours = models.ManyToManyField('tours.Tour', related_name="tours")

    # add oporos on other side of OneToOne

    def __str__(self):
        return 'Piglets group #%s' % self.pk