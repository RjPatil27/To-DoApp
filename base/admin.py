from django.contrib import admin
from .models import Task
# Register your models here.

# admin.site.register(Task)


class CountryAdmin(admin.ModelAdmin):
    list_display = ['id','title']

admin.site.register(Task,CountryAdmin)