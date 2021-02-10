from django.contrib import admin

from veterinary.models import Recipe, Drug


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Recipe._meta.fields]


@admin.register(Drug)
class DrugAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Drug._meta.fields]