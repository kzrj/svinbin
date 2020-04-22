from django.contrib import admin
from django.db.models import Q

from piglets.models import Piglets, PigletsStatus


@admin.register(Piglets)
class PigletsAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Piglets._meta.fields]

    def get_queryset(self, request):
        qs = super(PigletsAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs.filter(Q(Q(active=True) | Q(active=False)))
        return qs.filter(Q(Q(active=True) | Q(active=False)))


@admin.register(PigletsStatus)
class PigletsStatusAdmin(admin.ModelAdmin):
    list_display = [f.name for f in PigletsStatus._meta.fields]
