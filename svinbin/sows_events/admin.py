from django.contrib import admin

from sows_events import models
from piglets.models import Piglets


@admin.register(models.Semination)
class SeminationAdmin(admin.ModelAdmin):
    list_display = [f.name for f in models.Semination._meta.fields]
    search_fields = ['sow__farm_id']


@admin.register(models.Ultrasound)
class UltrasoundAdmin(admin.ModelAdmin):
    list_display = [f.name for f in models.Ultrasound._meta.fields]
    search_fields = ['sow__farm_id']


@admin.register(models.SowFarrow)
class SowFarrowAdmin(admin.ModelAdmin):
    list_display = [f.name for f in models.SowFarrow._meta.fields]
    search_fields = ['sow__farm_id']

    def render_change_form(self, request, context, *args, **kwargs):
        context['adminform'].form.fields['piglets__group'].queryset = \
            Piglets.objects.get_all()
        return super(SowFarrowAdmin, self).render_change_form(request, context, *args, **kwargs)


@admin.register(models.CullingSow)
class CullingSowAdmin(admin.ModelAdmin):
    list_display = [f.name for f in models.CullingSow._meta.fields]
    search_fields = ['sow__farm_id']


@admin.register(models.AbortionSow)
class AbortionSowAdmin(admin.ModelAdmin):
    list_display = [f.name for f in models.AbortionSow._meta.fields]
    search_fields = ['sow__farm_id']


@admin.register(models.MarkAsGilt)
class MarkAsGiltAdmin(admin.ModelAdmin):
    list_display = [f.name for f in models.MarkAsGilt._meta.fields]
    search_fields = ['sow__farm_id']


@admin.register(models.AssingFarmIdEvent)
class AssingFarmIdEventAdmin(admin.ModelAdmin):
    list_display = [f.name for f in models.AssingFarmIdEvent._meta.fields]
    search_fields = ['sow__farm_id']


@admin.register(models.PigletsToSowsEvent)
class PigletsToSowsEventAdmin(admin.ModelAdmin):
    list_display = [f.name for f in models.PigletsToSowsEvent._meta.fields]
    search_fields = ['piglets__pk']


@admin.register(models.SemenBoar)
class SemenBoarAdmin(admin.ModelAdmin):
    list_display = [f.name for f in models.SemenBoar._meta.fields]
    search_fields = ['boar__far_id']
