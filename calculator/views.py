import requests
import plotly.express as px
from django.shortcuts import render, redirect
from django.db.models import Sum, Count
from .models import PrintOrder, StudioSettings
from .forms import PrintOrderForm
from decimal import Decimal

def get_usd_rate():
    try:
        response = requests.get("https://api.exchangerate-api.com/v4/latest/USD", timeout=5)
        return response.json()['rates']['RUB']
    except:
        return 85.00

def index(request):
    orders = PrintOrder.objects.all().order_by('-created_at')
    total_revenue = orders.aggregate(Sum('total_cost'))['total_cost__sum'] or 0
    usd_rate = get_usd_rate()
    
    settings = StudioSettings.objects.first()
    markup = settings.markup_coefficient if settings else Decimal('2.5')
    
    if request.method == 'POST':
        form = PrintOrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.save(usd_rate=usd_rate)
            return redirect('index')
    else:
        form = PrintOrderForm()

    filament_stats = orders.values('filament__name').annotate(
        total_orders=Count('id'),
        total_weight=Sum('model_weight_g'),
        total_turnover=Sum('total_cost')
    ).order_by('-total_orders')

    printer_data = orders.values('printer__name').annotate(total=Sum('total_cost'))
    fig_printer = px.pie(printer_data, names='printer__name', values='total', 
                         hole=0.4, title="Выручка по принтерам (₽)")
    fig_printer.update_layout(margin=dict(l=10, r=10, t=40, b=10), showlegend=False)
    chart_printer_html = fig_printer.to_html(full_html=False, include_plotlyjs='cdn')

    filament_chart_data = orders.values('filament__name').annotate(total_g=Sum('model_weight_g'))
    fig_filament = px.pie(filament_chart_data, names='filament__name', values='total_g', 
                          hole=0.4, title="Расход пластика (г)")
    fig_filament.update_layout(margin=dict(l=10, r=10, t=40, b=10), showlegend=False)
    chart_filament_html = fig_filament.to_html(full_html=False, include_plotlyjs='cdn')

    for order in orders:
        order.recommended_price = order.total_cost * markup
        order.profit = order.total_cost * (markup - Decimal('1.0'))

    return render(request, 'calculator/index.html', {
        'orders': orders,
        'total_revenue': total_revenue,
        'usd_rate': usd_rate,
        'chart': chart_printer_html,
        'filament_chart': chart_filament_html,
        'form': form,
        'markup': markup,
        'filament_stats': filament_stats
    })