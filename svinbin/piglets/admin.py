from django.contrib import admin

from piglets.models import Piglets, PigletsStatus


@admin.register(Piglets)
class PigletsAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Piglets._meta.fields]


@admin.register(PigletsStatus)
class PigletsStatusAdmin(admin.ModelAdmin):
    list_display = [f.name for f in PigletsStatus._meta.fields]
