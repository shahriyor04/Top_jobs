from django.contrib import admin

from singin.models import Verification, MyProfile


class VerificationAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)


admin.site.register(Verification, VerificationAdmin)
admin.site.register(MyProfile)
