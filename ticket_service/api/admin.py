from django.contrib import admin
from .models import Printer, Check


class PrinterAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'api_key', 'check_type', 'point_id',)
    search_fields = ('name',)


class CheckAdmin(admin.ModelAdmin):
    list_display = ('id', 'printer_id', 'type', 'order', 'status',)
    list_filter = ('printer_id', 'type', 'status',)


admin.site.register(Printer, PrinterAdmin),
admin.site.register(Check, CheckAdmin)
