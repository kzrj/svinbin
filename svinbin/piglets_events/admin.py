from django.contrib import admin

from piglets_events import models
from piglets.models import Piglets


class PigletsEventFormMixin(object):
    def render_change_form(self, request, context, *args, **kwargs):
        context['adminform'].form.fields['piglets_group'].queryset = \
            Piglets.objects.get_all()
        context['adminform'].form.fields['parent_piglets'].queryset = \
            Piglets.objects.get_all()
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

    # def get_queryset(self, request):
    #     qs = super(CullingPigletsAdmin, self).get_queryset(request)
    #     if request.user.is_superuser:
    #         return qs
    #     return qs.filter(author=request.user)


@admin.register(models.PigletsSplit)
class PigletsSplitAdmin(admin.ModelAdmin):
    # search_fields = ['sow__farm_id']
    list_display = [f.name for f in models.PigletsSplit._meta.fields]


@admin.register(models.PigletsMerger)
class PigletsMergerAdmin(admin.ModelAdmin):
    # search_fields = ['piglets__id']
    list_display = [f.name for f in models.PigletsMerger._meta.fields]


@admin.register(models.Recount)
class RecountAdmin(PigletsEventFormMixin, admin.ModelAdmin):
    search_fields = ['piglets__id']
    list_display = [f.name for f in models.Recount._meta.fields]