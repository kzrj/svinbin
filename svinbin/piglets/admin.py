from django.contrib import admin

from piglets.models import Piglets


@admin.register(Piglets)
class PigletsAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Piglets._meta.fields]
