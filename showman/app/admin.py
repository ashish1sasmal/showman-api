from django.contrib import admin

# Register your models here.
from .models import Cities, Events

admin.site.register(Cities)
admin.site.register(Events)
