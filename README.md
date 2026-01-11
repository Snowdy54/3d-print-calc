# 3D-Print Calc

Профессиональный сервис для расчета экономики 3D-печати. Позволяет точно оценивать себестоимость заказов и анализировать эффективность работы печатной фермы.

**Ссылка на работающий проект:** [https://snowdy54.pythonanywhere.com](https://snowdy54.pythonanywhere.com)

## Технологии
* **Core:** Python 3.13, Django 6.0
* **Analysis:** Pandas, Plotly (интерактивные графики)
* **UI:** Bootstrap 5 (адаптивная верстка), Django Templates
* **DB:** SQLite (локально), PythonAnywhere (Production)

## Скриншоты интерфейса

![Дашборд аналитики](screenshots/dashboard.png)
*Интерактивная аналитика выручки по принтерам (Plotly)*

![Панель управления](screenshots/admin_panel.png)
*Управление заказами и ресурсами студии*

## Функционал
* **Автоматизированный расчет:** Учет стоимости грамма пластика и потребляемой электроэнергии в каждом заказе.
* **Data Science интеграция:** Использование Pandas для обработки статистики и Plotly для визуализации данных.
* **Архитектура:** Чистый код с соблюдением стандартов PEP8 и DRY.
* **Мобильность:** Адаптивный интерфейс для работы с мобильных устройств.

## Локальное развертывание

1.  **Клонируйте репозиторий:**
    ```bash
    git clone [https://github.com/Snowdy54/3D-print-calc.git](https://github.com/Snowdy54/3D-print-calc.git)
    cd 3D-print-calc
    ```
2.  **Настройте окружение:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Для Windows: venv\Scripts\activate
    ```
3.  **Установите зависимости:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Подготовьте базу данных:**
    ```bash
    python manage.py migrate
    python manage.py createsuperuser
    ```
5.  **Запустите проект:**
    ```bash
    python manage.py runserver
    ```
    Перейдите по адресу: `http://127.0.0.1:8000/`
