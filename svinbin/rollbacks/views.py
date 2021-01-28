# -*- coding: utf-8 -*-
from rest_framework.permissions import IsAuthenticated

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from rollbacks.models import Rollback
from rollbacks.serializers import RollbackSerializer

from core.permissions import OfficerOnlyPermissions


class RollbackViewSet(viewsets.ModelViewSet):
    queryset = Rollback.objects.all() 
    serializer_class = RollbackSerializer
    permission_classes = [OfficerOnlyPermissions]

    def create(self, request, serializer_class=None):
        operation_name = request.POST.get('operation_name')
        event_pk = request.POST.get('event_pk')

        rollback = None

        if operation_name == 'piglets_weighing':
            rollback = Rollback.objects.create_piglets_weighing_rollback(event_pk=event_pk,
              initiator=request.user)

        if operation_name == 'piglets_culling':
            rollback = Rollback.objects.create_piglets_culling_rollback(event_pk=event_pk,
              initiator=request.user)

        if operation_name == 'piglets_transaction':
            rollback = Rollback.objects.create_piglets_transactions_rollback(event_pk=event_pk,
              initiator=request.user)

        if operation_name == 'piglets_to_sows_event':
            rollback = Rollback.objects.create_piglets_to_sows_event_rollback(event_pk=event_pk,
              initiator=request.user)

        if operation_name == 'mark_as_gilt':
            rollback = Rollback.objects.create_ws3_weaning_piglets_rollback(event_pk=event_pk,
              initiator=request.user)

        if operation_name == 'ws3_piglets_weaning':
            rollback = Rollback.objects.create_piglets_weighing_rollback(event_pk=event_pk,
              initiator=request.user)

        if operation_name == 'mark_as_nurse':
            rollback = Rollback.objects.create_piglets_weighing_rollback(event_pk=event_pk,
              initiator=request.user)

        if operation_name == 'create_mark_as_nurse_rollback':
            rollback = Rollback.objects.create_piglets_weighing_rollback(event_pk=event_pk,
              initiator=request.user)

        if operation_name == 'farrow':
            rollback = Rollback.objects.create_farrow_rollback(event_pk=event_pk,
              initiator=request.user)

        if operation_name == 'abort':
            rollback = Rollback.objects.create_abort_rollback(event_pk=event_pk,
              initiator=request.user)

        if operation_name == 'culling_sow':
            rollback = Rollback.objects.create_sow_culling_rollback(event_pk=event_pk,
              initiator=request.user)

        if operation_name == 'usound':
            rollback = Rollback.objects.create_ultrasound_rollback(event_pk=event_pk,
              initiator=request.user)

        if operation_name == 'semination':
            rollback = Rollback.objects.create_semination_rollback(event_pk=event_pk,
              initiator=request.user)

        if operation_name == 'sow_transaction':
            rollback = Rollback.objects.create_sow_transaction_rollback(event_pk=event_pk,
              initiator=request.user)

        return Response({'message': f'Операция отменена.'})