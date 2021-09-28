from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *
# Register your models here.
    
@admin.register(UsersBack)
class AnimeAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['user', 'email']
    search_fields = ['username']
    pass
