from django.contrib import admin

from piglets_events import models


@admin.register(models.WeighingPiglets)
class WeighingPigletsAdmin(admin.ModelAdmin):
    list_display = [f.name for f in models.WeighingPiglets._meta.fields]


@admin.register(models.CullingPiglets)
class CullingPigletsAdmin(admin.ModelAdmin):
    list_display = [f.name for f in models.CullingPiglets._meta.fields]


@admin.register(models.PigletsSplit)
class PigletsSplitAdmin(admin.ModelAdmin):
    list_display = [f.name for f in models.PigletsSplit._meta.fields]


@admin.register(models.PigletsMerger)
class PigletsMergerAdmin(admin.ModelAdmin):
    list_display = [f.name for f in models.PigletsMerger._meta.fields]