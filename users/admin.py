import django
from django.contrib import admin
from .models import Security, Verification


admin.site.register(Security)
admin.site.register(Verification)
