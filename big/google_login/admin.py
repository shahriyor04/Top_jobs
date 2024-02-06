from django.contrib import admin

from google_login.models import User


class UserAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)


admin.site.register(User, UserAdmin)
