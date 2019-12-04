# -*- coding: utf-8 -*-
from rest_framework import viewsets

from transactions.models import SowTransaction, PigletsTransaction
from transactions import serializers


class SowTransactionsViewSet(viewsets.ModelViewSet):
    queryset = SowTransaction.objects.all()
    serializer_class = serializers.SowTransactionSerializer


class PigletsTransactionsViewSet(viewsets.ModelViewSet):
    queryset = PigletsTransaction.objects.all()
    serializer_class = serializers.PigletsTransactionSerializer
