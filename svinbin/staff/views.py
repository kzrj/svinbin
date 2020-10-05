# -*- coding: utf-8 -*-
from django.contrib.auth.models import User

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from staff.serializers import UserSerializer
from staff.filters import UserFilter
from core.permissions import ReadOrAdminOnlyPermissions


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_class = UserFilter
    permission_classes = [ReadOrAdminOnlyPermissions]
    