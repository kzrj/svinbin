from django.contrib import admin

from sows.models import Sow, Gilt, Boar, SowStatus


admin.site.register(Sow)
admin.site.register(SowStatus)
admin.site.register(Gilt)
admin.site.register(Boar)
