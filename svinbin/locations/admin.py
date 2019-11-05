from django.contrib import admin

from locations.models import WorkShop, Section, SowSingleCell, SowGroupCell, PigletsGroupCell, \
		SowAndPigletsCell, Location


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Location._meta.fields]


@admin.register(WorkShop)
class WorkShopAdmin(admin.ModelAdmin):
    list_display = [f.name for f in WorkShop._meta.fields]

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Section._meta.fields]


@admin.register(SowAndPigletsCell)
class SowAndPigletsCellAdmin(admin.ModelAdmin):
    list_display = [f.name for f in SowAndPigletsCell._meta.fields]


@admin.register(PigletsGroupCell)
class PigletsGroupCellAdmin(admin.ModelAdmin):
    list_display = [f.name for f in PigletsGroupCell._meta.fields]
