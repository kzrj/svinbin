from django.contrib import admin

from staff.models import WorkShopEmployee

@admin.register(WorkShopEmployee)
class WorkShopEmployeeAdmin(admin.ModelAdmin):
    list_display = [f.name for f in WorkShopEmployee._meta.fields]
