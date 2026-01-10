from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

class Printer(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название принтера")
    power_consumption = models.IntegerField(verbose_name="Мощность (Вт)")
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена покупки (руб)")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Владелец")

    class Meta:
        verbose_name = "Принтер"
        verbose_name_plural = "Принтеры"

class Filament(models.Model):
    name = models.CharField(max_length=100, verbose_name="Тип пластика")
    price_per_spool = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена за катушку (USD)")
    weight_g = models.IntegerField(verbose_name="Вес катушки (г)")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Владелец")

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

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

class StudioSettings(models.Model):
    electricity_tariff = models.DecimalField(max_digits=5, decimal_places=2, default=6.0, verbose_name="Тариф (руб/кВт)")
    markup_coefficient = models.DecimalField(max_digits=4, decimal_places=2, default=2.5, verbose_name="Коэффициент наценки")

    class Meta:
        verbose_name = "Настройки"
        verbose_name_plural = "Настройки"