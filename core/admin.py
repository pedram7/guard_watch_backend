from django.contrib import admin

# Register your models here.
from .models import *


class GuardAdmin(admin.ModelAdmin):
    list_display = ('staff_id', 'name', 'date_joined',)
    search_fields = ('staff_id', 'name',)


class LogAdmin(admin.ModelAdmin):
    list_filter = ('guard', 'wristband')
    list_display = ('id', 'time', 'guard', 'wristband',)
    # search_fields = (,)


admin.site.register(Guard, GuardAdmin)
admin.site.register(MyUser)
admin.site.register(Wristband)
admin.site.register(LogInstance, LogAdmin)
