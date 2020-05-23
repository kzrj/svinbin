from django.contrib import admin


from sows.models import Sow, Gilt, Boar, SowStatus

@admin.register(Sow)
class SowAdmin(admin.ModelAdmin):
    list_display =  [f.name for f in Sow._meta.fields]
    list_filter = ('status', 'tour', 'location',)
    search_fields = ['farm_id']

    def get_queryset(self, request):
        qs = super(SowAdmin, self).get_queryset(request)
        return Sow.objects.get_queryset_with_not_alive()


@admin.register(SowStatus)
class SowStatusAdmin(admin.ModelAdmin):
    list_display = [f.name for f in SowStatus._meta.fields]


@admin.register(Gilt)
class GiltAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Gilt._meta.fields]


@admin.register(Boar)
class BoarAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Boar._meta.fields]
