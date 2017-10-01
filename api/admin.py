from django.contrib import admin

# Register your models here.

from .models import Log, DataInfo

admin.site.register(Log)
admin.site.register(DataInfo)