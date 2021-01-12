from django.contrib import admin

from piglets_events import models
from piglets.models import Piglets


class PigletsEventFormMixin(object):
    def render_change_form(self, request, context, *args, **kwargs):
        if context['adminform'].form.fields.get('piglets_group'):
            context['adminform'].form.fields['piglets_group'].queryset = \
                Piglets.objects.get_all()

        if context['adminform'].form.fields.get('parent_piglets'):
            context['adminform'].form.fields['parent_piglets'].queryset = \
                Piglets.objects.get_all()

        if context['adminform'].form.fields.get('created_piglets'):
            context['adminform'].form.fields['created_piglets'].queryset = \
                Piglets.objects.get_all()

        return super(PigletsEventFormMixin, self).render_change_form(request, context, *args, **kwargs)


@admin.register(models.WeighingPiglets)
class WeighingPigletsAdmin(PigletsEventFormMixin, admin.ModelAdmin):
    search_fields = ['piglets_group__id']
    list_display = [f.name for f in models.WeighingPiglets._meta.fields]


@admin.register(models.CullingPiglets)
class CullingPigletsAdmin(PigletsEventFormMixin, admin.ModelAdmin):
    search_fields = ['piglets_group__id']
    list_display = [f.name for f in models.CullingPiglets._meta.fields]


@admin.register(models.PigletsSplit)
class PigletsSplitAdmin(PigletsEventFormMixin, admin.ModelAdmin):
    # search_fields = ['sow__farm_id']
    list_display = [f.name for f in models.PigletsSplit._meta.fields]


@admin.register(models.PigletsMerger)
class PigletsMergerAdmin(PigletsEventFormMixin, admin.ModelAdmin):
    # search_fields = ['piglets__id']
    list_display = [f.name for f in models.PigletsMerger._meta.fields]


@admin.register(models.Recount)
class RecountAdmin(PigletsEventFormMixin, admin.ModelAdmin):
    search_fields = ['piglets__id']
    list_display = [f.name for f in models.Recount._meta.fields]


@admin.register(models.PigletsMedEvent)
class PigletsMedEventAdmin(PigletsEventFormMixin, admin.ModelAdmin):
    search_fields = ['piglets__id']
    list_display = [f.name for f in models.PigletsMedEvent._meta.fields]