from django.contrib import admin

from locations.models import Location


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Location._meta.fields]