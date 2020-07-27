from django.contrib import admin

from locations.models import Location, PigletsGroupCell


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Location._meta.fields]


@admin.register(PigletsGroupCell)
class PigletsGroupCellAdmin(admin.ModelAdmin):
    list_display = [f.name for f in PigletsGroupCell._meta.fields]