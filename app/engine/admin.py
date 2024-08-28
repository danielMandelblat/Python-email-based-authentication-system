from django.contrib import admin
from .models import *
# Register your models here.

models = [
    SiteSettings,
    Email,
    Authentication,
    Log
]

for model in models:
    admin.site.register(model)
