from django.contrib import admin
from .models import Printer, Filament, PrintOrder, StudioSettings

@admin.register(Printer)
class PrinterAdmin(admin.ModelAdmin):
    list_display = ('name', 'power_consumption', 'purchase_price') 
    search_fields = ('name',)

@admin.register(Filament)
class FilamentAdmin(admin.ModelAdmin):
    list_display = ('name', 'price_per_spool', 'weight_g')
    list_filter = ('name',)

@admin.register(PrintOrder)
class PrintOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'printer', 'filament', 'model_weight_g', 'total_cost', 'created_at')
    list_filter = ('printer', 'filament', 'created_at')
    search_fields = ('printer__name',)

@admin.register(StudioSettings)
class StudioSettingsAdmin(admin.ModelAdmin):
    list_display = ('electricity_tariff', 'markup_coefficient')