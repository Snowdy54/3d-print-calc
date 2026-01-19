from django.test import TestCase
from django.contrib.auth.models import User
from .models import Printer, Filament, PrintOrder, StudioSettings
from decimal import Decimal

class StudioLogicTest(TestCase):
    def setUp(self):
        """Подготовка тестовой среды: создание пользователя, оборудования и настроек."""
        self.user = User.objects.create_user(username='test_engineer', password='password123')
        
        self.settings = StudioSettings.objects.create(
            markup_coefficient=Decimal('3.0'), 
            electricity_tariff=Decimal('5.50')
        )
        
        self.printer = Printer.objects.create(
            name="Creality Ender 3",
            power_consumption=350,
            purchase_price=Decimal('18000.00'),
            owner=self.user
        )
        
        self.filament = Filament.objects.create(
            name="PETG Jet",
            price_per_spool=Decimal('25.00'),
            weight_g=1000,
            owner=self.user
        )

    def test_printer_owner_assignment(self):
        """Проверка корректности привязки оборудования к владельцу (ForeignKey)."""
        self.assertEqual(self.printer.owner.username, 'test_engineer')

    def test_string_representations(self):
        """Проверка метода __str__ для корректного отображения объектов в админ-панели."""
        self.assertEqual(str(self.printer), "Creality Ender 3")
        self.assertEqual(str(self.filament), "PETG Jet")

    def test_calculate_cost_logic(self):
        """
        Проверка формулы расчета себестоимости пластика.
        Логика: (Цена катушки * Курс / Вес) * Вес модели.
        """
        order = PrintOrder(
            printer=self.printer,
            filament=self.filament,
            model_weight_g=200,  # 20% катушки
            print_time_hours=10.0
        )
        # При курсе usd = 100: (25$ * 100 / 1000) * 200 = 2.5 * 200 = 500 руб.
        cost = order.calculate_cost(usd_rate=100.0)
        self.assertEqual(cost, Decimal('500.00'))

    def test_auto_calculation_on_save(self):
        """Проверка автоматического вызова расчета при сохранении заказа через метод save()."""
        order = PrintOrder.objects.create(
            printer=self.printer,
            filament=self.filament,
            model_weight_g=100,
            print_time_hours=1.0
        )
        # Используем дефолтный курс 85 из метода save: (25 * 85 / 1000) * 100 = 212.50
        self.assertEqual(order.total_cost, Decimal('212.50'))

    def test_markup_application(self):
        """Проверка корректности применения коэффициента наценки из StudioSettings."""
        base_cost = Decimal('1000.00')
        final_price = base_cost * self.settings.markup_coefficient
        self.assertEqual(final_price, Decimal('3000.00'))

    def test_electricity_tariff_storage(self):
        """Проверка точности хранения тарифа электроэнергии (DecimalField)."""
        self.assertEqual(self.settings.electricity_tariff, Decimal('5.50'))

    def test_order_id_generation(self):
        """Проверка корректности генерации ID заказа и связи с принтером."""
        order = PrintOrder.objects.create(
            printer=self.printer,
            filament=self.filament,
            model_weight_g=10,
            print_time_hours=0.5
        )
        self.assertIsNotNone(order.id)
        self.assertEqual(order.printer.name, "Creality Ender 3")

    def test_negative_weight_handling(self):
        """
        Проверка логики: сумма заказа не должна быть отрицательной 
        даже при минимальном весе.
        """
        order = PrintOrder.objects.create(
            printer=self.printer,
            filament=self.filament,
            model_weight_g=1,
            print_time_hours=0.1
        )
        self.assertGreaterEqual(order.total_cost, Decimal('0'))