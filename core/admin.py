from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Guard)
admin.site.register(MyUser)
admin.site.register(Wristband)
admin.site.register(LogInstance)
