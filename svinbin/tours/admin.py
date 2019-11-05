from django.contrib import admin

from tours.models import Tour

@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Tour._meta.fields]