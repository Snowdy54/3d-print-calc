from django.contrib import admin
from .models import Printer, Filament, PrintOrder

@admin.register(Printer)
class PrinterAdmin(admin.ModelAdmin):
    list_display = ('name', 'power_consumption', 'purchase_price', 'owner')

@admin.register(Filament)
class FilamentAdmin(admin.ModelAdmin):
    list_display = ('name', 'price_per_spool', 'weight_g', 'owner')

@admin.register(PrintOrder)
class PrintOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'printer', 'filament', 'model_weight_g', 'total_cost', 'created_at')