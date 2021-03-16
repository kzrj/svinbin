from django.contrib import admin

from sows_events import models
from piglets.models import Piglets
from sows.models import Sow, Boar


class SowsEventFormMixin(object):
    def render_change_form(self, request, context, *args, **kwargs):
        if context['adminform'].form.fields.get('sow'):
            context['adminform'].form.fields['sow'].queryset = \
                Sow.objects.get_queryset_with_not_alive()

        if context['adminform'].form.fields.get('piglets_group'):
            context['adminform'].form.fields['piglets_group'].queryset = \
                Piglets.objects.get_all()

        if context['adminform'].form.fields.get('piglets'):
            context['adminform'].form.fields['piglets'].queryset = \
                Piglets.objects.get_all()

        return super(SowsEventFormMixin, self).render_change_form(request, context, *args, **kwargs)


@admin.register(models.Semination)
class SeminationAdmin(SowsEventFormMixin, admin.ModelAdmin):
    list_display = [f.name for f in models.Semination._meta.fields]
    search_fields = ['sow__farm_id']


@admin.register(models.Ultrasound)
class UltrasoundAdmin(SowsEventFormMixin, admin.ModelAdmin):
    list_display = [f.name for f in models.Ultrasound._meta.fields]
    search_fields = ['sow__farm_id']


@admin.register(models.SowFarrow)
class SowFarrowAdmin(SowsEventFormMixin, admin.ModelAdmin):
    list_display = [f.name for f in models.SowFarrow._meta.fields]
    search_fields = ['sow__farm_id']

    def render_change_form(self, request, context, *args, **kwargs):
        context['adminform'].form.fields['piglets_group'].queryset = \
            Piglets.objects.get_all()
        context['adminform'].form.fields['sow'].queryset = \
            Sow.objects.get_queryset_with_not_alive()
        return super(SowFarrowAdmin, self).render_change_form(request, context, *args, **kwargs)


@admin.register(models.CullingSow)
class CullingSowAdmin(SowsEventFormMixin, admin.ModelAdmin):
    list_display = [f.name for f in models.CullingSow._meta.fields]
    search_fields = ['sow__farm_id']


@admin.register(models.AbortionSow)
class AbortionSowAdmin(SowsEventFormMixin, admin.ModelAdmin):
    list_display = [f.name for f in models.AbortionSow._meta.fields]
    search_fields = ['sow__farm_id']


@admin.register(models.MarkAsGilt)
class MarkAsGiltAdmin(SowsEventFormMixin, admin.ModelAdmin):
    list_display = [f.name for f in models.MarkAsGilt._meta.fields]
    search_fields = ['sow__farm_id']


@admin.register(models.AssingFarmIdEvent)
class AssingFarmIdEventAdmin(SowsEventFormMixin, admin.ModelAdmin):
    list_display = [f.name for f in models.AssingFarmIdEvent._meta.fields]
    search_fields = ['sow__farm_id']


@admin.register(models.PigletsToSowsEvent)
class PigletsToSowsEventAdmin(SowsEventFormMixin, admin.ModelAdmin):
    list_display = [f.name for f in models.PigletsToSowsEvent._meta.fields]
    search_fields = ['piglets__pk']


@admin.register(models.SemenBoar)
class SemenBoarAdmin(SowsEventFormMixin, admin.ModelAdmin):
    list_display = [f.name for f in models.SemenBoar._meta.fields]
    search_fields = ['boar__farm_id']


@admin.register(models.CullingBoar)
class CullingBoarAdmin(SowsEventFormMixin, admin.ModelAdmin):
    list_display = [f.name for f in models.CullingBoar._meta.fields]
    search_fields = ['boar__farm_id']
