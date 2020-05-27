from django.contrib import admin

from tours.models import Tour, MetaTour

@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Tour._meta.fields]


@admin.register(MetaTour)
class MetaTourAdmin(admin.ModelAdmin):
    list_display = [f.name for f in MetaTour._meta.fields]