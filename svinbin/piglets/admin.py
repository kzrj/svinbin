from django.contrib import admin

from piglets.models import NewBornPigletsGroup, NomadPigletsGroup


@admin.register(NewBornPigletsGroup)
class NewBornPigletsGroupAdmin(admin.ModelAdmin):
    list_display = [f.name for f in NewBornPigletsGroup._meta.fields]


@admin.register(NomadPigletsGroup)
class NomadPigletsGroupAdmin(admin.ModelAdmin):
    list_display = [f.name for f in NomadPigletsGroup._meta.fields]