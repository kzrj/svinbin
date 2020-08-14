# -*- coding: utf-8 -*-
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from transactions.models import SowTransaction, PigletsTransaction
from transactions import serializers
from core.permissions import ReadOrAdminOnlyPermissions


class SowTransactionsViewSet(viewsets.ModelViewSet):
    queryset = SowTransaction.objects.all()
    serializer_class = serializers.SowTransactionSerializer
    permission_classes = [ReadOrAdminOnlyPermissions]


class PigletsTransactionsViewSet(viewsets.ModelViewSet):
    queryset = PigletsTransaction.objects.all()
    serializer_class = serializers.PigletsTransactionSerializer
    permission_classes = [ReadOrAdminOnlyPermissions]
