from django.contrib import admin

from tours.models import Tour, MetaTour, MetaTourRecord

@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Tour._meta.fields]


@admin.register(MetaTour)
class MetaTourAdmin(admin.ModelAdmin):
    list_display = [f.name for f in MetaTour._meta.fields]
    search_fields = ['id', 'week_tour__pk']


@admin.register(MetaTourRecord)
class MetaTourRecordAdmin(admin.ModelAdmin):
    list_display = [f.name for f in MetaTourRecord._meta.fields]