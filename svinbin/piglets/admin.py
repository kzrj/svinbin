from django.contrib import admin
from django.db.models import Q

from piglets.models import Piglets, PigletsStatus


@admin.register(Piglets)
class PigletsAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Piglets._meta.fields] + ['metatour']
    list_filter = ('active', 'modified_at',)
    search_fields = ['id',]

    def get_queryset(self, request):
        qs = super(PigletsAdmin, self).get_queryset(request)
        return Piglets.objects.get_all()


@admin.register(PigletsStatus)
class PigletsStatusAdmin(admin.ModelAdmin):
    list_display = [f.name for f in PigletsStatus._meta.fields]
