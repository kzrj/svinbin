# -*- coding: utf-8 -*-
from django.db import models

from core.models import CoreModel, CoreModelManager, Event
from piglets.models import NewBornPigletsGroup, NomadPigletsGroup, PigletsStatus
from sows.models import Gilt
from locations.models import Location


class GiltMergerManager(CoreModelManager):
    def create_gilt_merger(self, gilts, initiator=None): # test +
        merger = self.create(initiator=initiator) 
        if isinstance(gilts, list):
            gilts = Gilt.objects.from_list_to_queryset(gilts)
        gilts.update(merger=merger)

        return merger

    def _get_gilts_from_group_update_group(self, new_born_groups): # test +
        if isinstance(new_born_groups, list):
            new_born_groups = NewBornPigletsGroup.objects.from_list_to_queryset(new_born_groups)

        gilts = Gilt.objects.filter(new_born_group__in=new_born_groups)
        gilts.update(new_born_group=None)
        new_born_groups.remove_gilts_and_update_quantity()
        
        return gilts

    def create_merger_and_return_nomad_group(self, new_born_groups): # test +
        gilts = self._get_gilts_from_group_update_group(new_born_groups)
        merger = self.creating_gilt_merger(gilt)
        return merger.create_nomad_group()


class GiltMerger(Event):
    nomad_group = models.OneToOneField(NomadPigletsGroup, on_delete=models.SET_NULL, null=True,
     related_name='creating_gilt_merger')

    objects = GiltMergerManager()

    def create_nomad_group(self): # test +
        gilts_count = self.gilts.all().count()
        location = Location.objects.create_workshop_location(workshop_number=3)
        nomad_group = NomadPigletsGroup.objects.create(start_quantity=gilts_count, quantity=gilts_count,
            gilts_quantity=gilts_count, location=location)
        self.nomad_group = nomad_group
        self.save()
        return nomad_group


class CastingListToSevenFiveManager(CoreModelManager):
    def create_casting_list(self, nomad_groups_list_of_dicts, initiator=None):
        event = self.create(initiator=initiator)

        # input dict should be {'nomad_group': 1, 'gilts': [1,2]}
        for input_dict in nomad_groups_list_of_dicts:
            gilts = Gilt.objects.from_list_to_queryset(input_dict['gilts'])
            gilts.update(casting_list_to_seven_five=event)
            nomad_group = input_dict['nomad_group']
            nomad_group.remove_gilts(len(input_dict['gilts']))    

        return event


class CastingListToSevenFiveEvent(Event):
    objects = CastingListToSevenFiveManager()
