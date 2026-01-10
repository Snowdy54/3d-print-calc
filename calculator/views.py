import requests
import plotly.express as px
from django.shortcuts import render
from django.db.models import Sum
from .models import PrintOrder

def get_usd_rate():
    try:
        response = requests.get("https://api.exchangerate-api.com/v4/latest/USD", timeout=5)
        return response.json()['rates']['RUB']
    except:
        return 80.50

def index(request):
    orders = PrintOrder.objects.all().order_by('-created_at')
    total_revenue = orders.aggregate(Sum('total_cost'))['total_cost__sum'] or 0
    usd_rate = get_usd_rate()

    chart_data = orders.values('printer__name').annotate(total=Sum('total_cost'))
    
    fig = px.pie(chart_data, names='printer__name', values='total', 
                 title="Распределение затрат", hole=0.4)
    
    chart_html = fig.to_html(full_html=False, include_plotlyjs='cdn')

    return render(request, 'calculator/index.html', {
        'orders': orders,
        'total_revenue': total_revenue,
        'usd_rate': usd_rate,
        'chart': chart_html 
    })