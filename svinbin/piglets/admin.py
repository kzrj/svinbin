from django.contrib import admin
from django.db.models import Q

from piglets.models import Piglets, PigletsStatus


@admin.register(Piglets)
class PigletsAdmin(admin.ModelAdmin):
    my_fields = [
        'location',
        'status',
        'start_quantity',
        'quantity',
        'gilts_quantity',
        'merger_as_parent',
        'split_as_child',  
        'transfer_part_number',
        'active',
        'birthday',
        'metatour.week_tour'
    ]
    list_display = my_fields
    list_filter = ('active', 'modified_at',)
    search_fields = ['location__id',]

    def get_queryset(self, request):
        qs = super(PigletsAdmin, self).get_queryset(request)
        return Piglets.objects.get_all()


@admin.register(PigletsStatus)
class PigletsStatusAdmin(admin.ModelAdmin):
    list_display = [f.name for f in PigletsStatus._meta.fields]
