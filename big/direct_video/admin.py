from django.contrib import admin

from direct_video.models import Direct_video, Category

# Register your models here.

admin.site.register(Category)
admin.site.register(Direct_video)


