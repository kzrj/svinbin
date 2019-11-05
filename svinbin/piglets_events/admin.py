from django.contrib import admin

from piglets_events import models


@admin.register(models.NewBornPigletsMerger)
class NewBornPigletsMergerAdmin(admin.ModelAdmin):
    list_display = [f.name for f in models.NewBornPigletsMerger._meta.fields]


@admin.register(models.SplitNomadPigletsGroup)
class SplitNomadPigletsGroupAdmin(admin.ModelAdmin):
    list_display = [f.name for f in models.SplitNomadPigletsGroup._meta.fields]


@admin.register(models.NewBornPigletsGroupRecount)
class NewBornPigletsGroupRecountAdmin(admin.ModelAdmin):
    list_display = [f.name for f in models.NewBornPigletsGroupRecount._meta.fields]


@admin.register(models.NomadPigletsGroupRecount)
class NomadPigletsGroupRecountAdmin(admin.ModelAdmin):
    list_display = [f.name for f in models.NomadPigletsGroupRecount._meta.fields]


@admin.register(models.CullingNewBornPiglets)
class CullingNewBornPigletsAdmin(admin.ModelAdmin):
    list_display = [f.name for f in models.CullingNewBornPiglets._meta.fields]


@admin.register(models.CullingNomadPiglets)
class CullingNomadPigletsAdmin(admin.ModelAdmin):
    list_display = [f.name for f in models.CullingNomadPiglets._meta.fields]


@admin.register(models.WeighingPiglets)
class WeighingPigletsAdmin(admin.ModelAdmin):
    list_display = [f.name for f in models.WeighingPiglets._meta.fields]
    