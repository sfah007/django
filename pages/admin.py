from django.contrib import admin
from .models import Anime, AnimeClass, AnimeDate, AnimeDays, AnimeState, AnimeType, Episodes
from import_export import resources
from import_export.admin import ImportExportModelAdmin




@admin.register(Anime)
class AnimeAdmin(ImportExportModelAdmin):
    search_fields = ['name']
    pass


@admin.register(AnimeType)
class AnimeTypeAdmin(ImportExportModelAdmin):
    pass


@admin.register(AnimeDate)
class AnimeDateAdmin(ImportExportModelAdmin):
    pass


@admin.register(AnimeClass)
class AnimeClassAdmin(ImportExportModelAdmin):
    pass


@admin.register(AnimeState)
class AnimeStateAdmin(ImportExportModelAdmin):
    pass


@admin.register(AnimeDays)
class AnimeDaysAdmin(ImportExportModelAdmin):
    pass


@admin.register(Episodes)
class EpisodesAdmin(ImportExportModelAdmin):
    pass