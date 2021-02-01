# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models

from core.models import CoreModel, CoreModelManager, Event
from piglets_events.models import ( WeighingPiglets, CullingPiglets )
from sows_events.models import ( PigletsToSowsEvent, MarkAsGilt, MarkAsNurse, WeaningSow, SowFarrow,
    CullingSow, Ultrasound, Semination )
from transactions.models import PigletsTransaction, SowTransaction


class RollbackManager(CoreModelManager):
    def create(self, *args, **kwargs):
        if 'date' in kwargs and not kwargs['date']:
            kwargs['date'] = timezone.now()
        return super(RollbackManager, self).create(*args, **kwargs)  

    def create_piglets_weighing_rollback(self, event_pk, operation_name, initiator=None, date=None):
        wp = WeighingPiglets.objects.get(pk=event_pk)
        wp.piglets_group.change_status_to('Готовы ко взвешиванию')
        wp.delete()

        return self.create(initiator=initiator, date=date, operation_name=operation_name,
            workshop=wp.initiator.employee.workshop, user_employee=wp.initiator)

    def create_piglets_culling_rollback(self, event_pk, operation_name, initiator=None, date=None):
        cp = CullingPiglets.objects.get(pk=event_pk)
        cp.piglets_group.add_piglets(quantity=cp.quantity)
        cp.delete()

        return self.create(initiator=initiator, date=date, operation_name=operation_name,
            workshop=cp.initiator.employee.workshop, user_employee=cp.initiator)

    def create_piglets_transactions_rollback(self, event_pk, operation_name, initiator=None, date=None):
        transaction = PigletsTransaction.objects.get(pk=event_pk)
        transacted_piglets = transaction.piglets_group

        if transacted_piglets.merger_as_parent:
            # priority is important
            transacted_piglets.change_location(location=transaction.from_location)
            transacted_piglets.merger_as_parent.restore_parent_piglets_and_delete_created()
            transacted_piglets.merger_as_parent.delete()
            
        if transaction.split_event:
            transaction.split_event.restore_parent_and_delete_children()
            transaction.split_event.delete()

        if not transacted_piglets.merger_as_parent and not transaction.split_event:
            transacted_piglets.change_location(location=transaction.from_location)

        transaction.delete()

        return self.create(initiator=initiator, date=date, operation_name=operation_name,
            workshop=transaction.initiator.employee.workshop,
            user_employee=transaction.initiator)

    def create_piglets_to_sows_event_rollback(self, event_pk, operation_name, initiator=None, date=None):
        pts_event = PigletsToSowsEvent.objects.get(pk=event_pk)
        piglets = pts_event.piglets
        piglets.weighing_records.filter(place='o/2').delete()

        if piglets.split_as_child and not piglets.split_as_child.transaction:
            piglets.split_as_child.restore_parent_and_delete_children()
            piglets.split_as_child.delete()
        else:
            piglets.activate()

        pts_event.delete_event_sows_transactions()

        return self.create(initiator=initiator, date=date, operation_name=operation_name,
            workshop=pts_event.initiator.employee.workshop,
            user_employee=pts_event.initiator)

    def create_mark_as_gilt_rollback(self, event_pk, operation_name, initiator=None, date=None):
        mag_event = MarkAsGilt.objects.get(pk=event_pk)
        mag_event.delete_gilt_and_event()

        return self.create(initiator=initiator, date=date, operation_name=operation_name,
            workshop=mag_event.initiator.employee.workshop,
            user_employee=mag_event.initiator)

    def create_ws3_weaning_piglets_rollback(self, event_pk, operation_name, initiator=None, date=None):
        transaction = PigletsTransaction.objects.get(pk=event_pk)
        transacted_big_group = transaction.piglets_group

        transacted_big_group.change_location(location=transaction.from_location)
        transaction.delete()

        merger = transacted_big_group.merger_as_child
        merger.restore_parent_piglets_and_delete_created()
        piglets_as_parents = merger.piglets_as_parents.get_all().filter(merger_as_parent=merger)

        WeaningSow.objects.filter(piglets__in=piglets_as_parents).restore_tour_status_delete_events()

        for piglets in piglets_as_parents:
            if piglets.split_as_child:
                piglets.split_as_child.restore_parent_and_delete_children()
                piglets.split_as_child.delete()

        merger.delete()

        return self.create(initiator=initiator, date=date, operation_name=operation_name,
            workshop=transaction.initiator.employee.workshop,
            user_employee=transaction.initiator)

    def create_mark_as_nurse_rollback(self, event_pk, operation_name, initiator=None, date=None):
        mas_event = MarkAsNurse.objects.get(pk=event_pk)
        mas_event.sow.tour = mas_event.tour
        mas_event.sow.change_status_to_previous_delete_current_status_record()
        mas_event.delete()

        return self.create(initiator=initiator, date=date, operation_name=operation_name,
            workshop=mas_event.initiator.employee.workshop,
            user_employee=mas_event.initiator)

    def create_farrow_rollback(self, event_pk, operation_name, initiator=None, date=None):
        farrow = SowFarrow.objects.get(pk=event_pk)

        if farrow.piglets_group.merger_as_parent:
            farrow.piglets_group.merger_as_parent.restore_parent_piglets_and_delete_created()
            farrow.piglets_group.merger_as_parent.delete()

        farrow.piglets_group.delete()
        farrow.sow.change_status_to_previous_delete_current_status_record()
        farrow.delete()

        return self.create(initiator=initiator, date=date, operation_name=operation_name,
            workshop=farrow.initiator.employee.workshop,
            user_employee=farrow.initiator)

    def create_abort_rollback(self, event_pk, operation_name, initiator=None, date=None):
        abort = AbortionSow.objects.get(pk=event_pk)
        abort.sow.tour = abort.tour
        abort.sow.change_status_to_previous_delete_current_status_record()
        abort.delete()

        return self.create(initiator=initiator, date=date, operation_name=operation_name,
            workshop=abort.initiator.employee.workshop,
            user_employee=abort.initiator)

    def create_sow_culling_rollback(self, event_pk, operation_name, initiator=None, date=None):
        culling = CullingSow.objects.get(pk=event_pk)
        culling.sow.alive = True
        culling.sow.change_status_to_previous_delete_current_status_record()
        culling.delete()

        return self.create(initiator=initiator, date=date, operation_name=operation_name,
            workshop=culling.initiator.employee.workshop,
            user_employee=culling.initiator)

    def create_ultrasound_rollback(self, event_pk, operation_name, initiator=None, date=None):
        usound = Ultrasound.objects.get(pk=event_pk)
        if not usound.result:
            usound.sow.tour = usound.tour
        usound.sow.change_status_to_previous_delete_current_status_record()
        usound.delete()

        return self.create(initiator=initiator, date=date, operation_name=operation_name,
            workshop=usound.initiator.employee.workshop,
            user_employee=usound.initiator)

    def create_semination_rollback(self, event_pk, operation_name, initiator=None, date=None):
        semination = Semination.objects.get(pk=event_pk)
        if semination.sow.status.title == 'Осеменена 1':
            semination.sow.tour = None

        semination.sow.change_status_to_previous_delete_current_status_record()
        semination.delete()

        return self.create(initiator=initiator, date=date, operation_name=operation_name,
            workshop=semination.initiator.employee.workshop,
            user_employee=semination.initiator)

    def create_sow_transaction_rollback(self, event_pk, operation_name, initiator=None, date=None):
        transaction = SowTransaction.objects.get(pk=event_pk)

        if transaction.is_weaning_transaction_from_ws3_to_ws1():
            transaction.sow.tour = transaction.tour
            transaction.sow.change_status_to_previous_delete_current_status_record()

        transaction.sow.change_sow_current_location(to_location=transaction.from_location)
        transaction.delete()

        return self.create(initiator=initiator, date=date, operation_name=operation_name,
            workshop=transaction.initiator.employee.workshop,
            user_employee=transaction.initiator)


class Rollback(Event):
    operation_name = models.CharField(max_length=100)
    workshop = models.ForeignKey('locations.WorkShop', on_delete=models.CASCADE, null=True,
     blank=True, related_name='rollbacks')
    user_employee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
     related_name='rollbacks')

    objects = RollbackManager()

    def __str__(self):
        return f'Rollback {self.operation_name} pk {self.pk}'