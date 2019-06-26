from django.db import models

from core.models import CoreModel, CoreModelManager
from piglets.models import NewBornPigletsGroup, NomadPigletsGroup, PigletsStatus



class GiltMergerManager(CoreModelManager):
    def create_gilt_merger(self, gilts):
        merger = self.create()

        # if queryset
        gilts.update(merger=merger)

    def create_nomad_group(self):
        pass
        


class GiltMerger(CoreModel):
    nomad_group = models.OneToOneField(NomadPigletsGroup, on_delete=models.SET_NULL, null=True,
     related_name='creating_gilt_merger')

    objects = GiltMergerManager()