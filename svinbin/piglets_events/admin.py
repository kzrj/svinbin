from django.contrib import admin

from piglets_events import models


@admin.register(models.WeighingPiglets)
class WeighingPigletsAdmin(admin.ModelAdmin):
	search_fields = ['piglets_group__id']
    list_display = [f.name for f in models.WeighingPiglets._meta.fields]


@admin.register(models.CullingPiglets)
class CullingPigletsAdmin(admin.ModelAdmin):
	search_fields = ['piglets_group__id']
    list_display = [f.name for f in models.CullingPiglets._meta.fields]


@admin.register(models.PigletsSplit)
class PigletsSplitAdmin(admin.ModelAdmin):
	# search_fields = ['sow__farm_id']
    list_display = [f.name for f in models.PigletsSplit._meta.fields]


@admin.register(models.PigletsMerger)
class PigletsMergerAdmin(admin.ModelAdmin):
	# search_fields = ['sow__farm_id']
    list_display = [f.name for f in models.PigletsMerger._meta.fields]