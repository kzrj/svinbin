from django.contrib import admin

from transactions.models import SowTransaction, PigletsTransaction


@admin.register(SowTransaction)
class SowTransactionAdmin(admin.ModelAdmin):
    list_display =  [f.name for f in SowTransaction._meta.fields]
    search_fields = ['sow__farm_id']


@admin.register(PigletsTransaction)
class PigletsTransactionAdmin(admin.ModelAdmin):
    list_display =  [f.name for f in PigletsTransaction._meta.fields]
    search_fields = ['date',]