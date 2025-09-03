from django.contrib import admin
from .models import Tool,RequestLog,Content

# Register your models here.

admin.site.register(Tool)
admin.site.register(Content)
admin.site.register(RequestLog)