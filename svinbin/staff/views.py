# -*- coding: utf-8 -*-
from django.contrib.auth.models import User

from rest_framework import viewsets

from staff.serializers import UserSerializer
from staff.filters import UserFilter


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_class = UserFilter
    