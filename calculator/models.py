from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

class Printer(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название принтера")
    power_consumption = models.IntegerField(verbose_name="Мощность (Вт)")
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена покупки (руб)")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Владелец")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Принтер"
        verbose_name_plural = "Принтеры"

class Filament(models.Model):
    name = models.CharField(max_length=100, verbose_name="Тип пластика")
    price_per_spool = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена за катушку (USD)")
    weight_g = models.IntegerField(verbose_name="Вес катушки (г)")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Владелец")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Пластик"
        verbose_name_plural = "Пластик"

class PrintOrder(models.Model):
    printer = models.ForeignKey(Printer, on_delete=models.CASCADE, verbose_name="Принтер")
    filament = models.ForeignKey(Filament, on_delete=models.CASCADE, verbose_name="Пластик")
    model_weight_g = models.IntegerField(verbose_name="Вес модели (г)")
    print_time_hours = models.FloatField(verbose_name="Время печати (ч)")
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Себестоимость", editable=False, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def save(self, *args, **kwargs):
        usd_rate = kwargs.pop('usd_rate', Decimal('80.5')) # 80.5 как запасной вариант
        
        settings = StudioSettings.objects.first()
        tariff = settings.electricity_tariff if settings else Decimal('6.0')
        
        price_per_gram_usd = Decimal(str(self.filament.price_per_spool)) / Decimal(str(self.filament.weight_g))
        filament_cost_rub = price_per_gram_usd * Decimal(str(self.model_weight_g)) * Decimal(str(usd_rate))
        
        power_kw = Decimal(str(self.printer.power_consumption)) / Decimal('1000.0')
        electricity_cost_rub = power_kw * Decimal(str(self.print_time_hours)) * tariff
        
        self.total_cost = filament_cost_rub + electricity_cost_rub
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Заказ №{self.id} ({self.printer.name})"

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

class StudioSettings(models.Model):
    electricity_tariff = models.DecimalField(max_digits=5, decimal_places=2, default=6.0, verbose_name="Тариф (руб/кВт)")
    markup_coefficient = models.DecimalField(max_digits=4, decimal_places=2, default=2.5, verbose_name="Коэффициент наценки")

    def __str__(self):
        return "Глобальные настройки студии"

    class Meta:
        verbose_name = "Настройки"
        verbose_name_plural = "Настройки"