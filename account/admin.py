from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *
# Register your models here.
    
@admin.register(UsersBack)
class AnimeAdmin(ImportExportModelAdmin):
    pass

@admin.register(done_show)
class AnimeAdmin(ImportExportModelAdmin):
    pass

@admin.register(want_show)
class AnimeAdmin(ImportExportModelAdmin):
    pass