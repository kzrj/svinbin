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
        event_pk = int(request.POST.get('event_pk')) if request.POST.get('event_pk') else None
        print(operation_name, event_pk, type(event_pk))

        rollback = None

        if 'weighing' in operation_name:
            rollback = Rollback.objects.create_piglets_weighing_rollback(event_pk=event_pk,
              initiator=request.user, operation_name=operation_name)

        if 'piglets_padej' in operation_name or 'prirezka' in operation_name \
           or 'piglets_vinuzhd' in operation_name or 'piglets_spec' in operation_name:
            rollback = Rollback.objects.create_piglets_culling_rollback(event_pk=event_pk,
              initiator=request.user, operation_name=operation_name)

        if 'piglets_inner_trs' in operation_name or 'piglets_rassadka' in operation_name \
           or operation_name == 'ws4_piglets_outer_trs' or operation_name == 'ws8_piglets_outer_trs':
            rollback = Rollback.objects.create_piglets_transactions_rollback(event_pk=event_pk,
              initiator=request.user, operation_name=operation_name)

        if 'remont_to_2' in operation_name:
            rollback = Rollback.objects.create_piglets_to_sows_event_rollback(event_pk=event_pk,
              initiator=request.user, operation_name=operation_name)

        if operation_name == 'ws3_mark_as_gilt':
            rollback = Rollback.objects.create_mark_as_gilt_rollback(event_pk=event_pk,
              initiator=request.user, operation_name=operation_name)

        if operation_name == 'ws3_piglets_outer_trs':
            rollback = Rollback.objects.create_ws3_weaning_piglets_rollback(event_pk=event_pk,
              initiator=request.user, operation_name=operation_name)

        if operation_name == 'ws3_mark_as_nurse':
            rollback = Rollback.objects.create_mark_as_nurse_rollback(event_pk=event_pk,
              initiator=request.user, operation_name=operation_name)

        if operation_name == 'ws3_farrow':
            rollback = Rollback.objects.create_farrow_rollback(event_pk=event_pk,
              initiator=request.user, operation_name=operation_name)

        if 'abort' in operation_name:
            rollback = Rollback.objects.create_abort_rollback(event_pk=event_pk,
              initiator=request.user, operation_name=operation_name)

        if operation_name == 'ws1_culling' or operation_name == 'ws2_culling' \
           or operation_name == 'ws3_culling':
            rollback = Rollback.objects.create_sow_culling_rollback(event_pk=event_pk,
              initiator=request.user, operation_name=operation_name)

        if operation_name == 'ws1_usound' or operation_name == 'ws2_usound':
            rollback = Rollback.objects.create_ultrasound_rollback(event_pk=event_pk,
              initiator=request.user, operation_name=operation_name)

        if operation_name == 'ws1_semination':
            rollback = Rollback.objects.create_semination_rollback(event_pk=event_pk,
              initiator=request.user, operation_name=operation_name)

        if operation_name == 'w1_peregon_sow' or operation_name == 'w2_peregon_sow' \
           or operation_name == 'ws3_sow_rassadka' or operation_name == 'ws3_sow_otiem' \
           or operation_name == 'ws3_sow_inner':
            rollback = Rollback.objects.create_sow_transaction_rollback(event_pk=event_pk,
              initiator=request.user, operation_name=operation_name)

        return Response({'message': f'Операция отменена.'})