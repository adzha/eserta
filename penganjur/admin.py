# from django.contrib import admin
# from .models import Aktiviti

# # Register your models here.
# admin.site.register(Aktiviti)


from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import Aktiviti

@admin.register(Aktiviti)
class AktivitiAdmin(ImportExportModelAdmin):
    pass