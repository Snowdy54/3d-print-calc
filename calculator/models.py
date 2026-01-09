from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

class Printer(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название принтера")
    power_consumption = models.IntegerField(verbose_name="Мощность (Вт)")
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена покупки")
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Filament(models.Model):
    name = models.CharField(max_length=100, verbose_name="Тип пластика")
    price_per_spool = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена за катушку")
    weight_g = models.IntegerField(verbose_name="Вес катушки (г)")
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class PrintOrder(models.Model):
    printer = models.ForeignKey(Printer, on_delete=models.CASCADE, verbose_name="Принтер")
    filament = models.ForeignKey(Filament, on_delete=models.CASCADE, verbose_name="Пластик")
    model_weight_g = models.IntegerField(verbose_name="Вес модели (г)")
    print_time_hours = models.FloatField(verbose_name="Время печати (ч)")
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, editable=False, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Заказ {self.id} — {self.printer.name}"
    
    def save(self, *args, **kwargs):
        amortization = (self.printer.purchase_price / 2000) * Decimal(str(self.print_time_hours))
        
        electricity = (Decimal(str(self.printer.power_consumption)) / 1000) * Decimal(str(self.print_time_hours)) * Decimal('6.0')
        
        plastic = (self.filament.price_per_spool / self.filament.weight_g) * self.model_weight_g
        
        self.total_cost = amortization + electricity + plastic
        
        # Сохраняем результат в базу
        super().save(*args, **kwargs)