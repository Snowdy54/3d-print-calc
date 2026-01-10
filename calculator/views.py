import requests
import plotly.express as px
from django.shortcuts import render, redirect
from django.db.models import Sum
from .models import PrintOrder 
from .forms import PrintOrderForm

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
    
    if request.method == 'POST':
        form = PrintOrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.save(usd_rate=usd_rate)
            return redirect('index')
    else:
        form = PrintOrderForm()

    chart_data = orders.values('printer__name').annotate(total=Sum('total_cost'))
    fig = px.pie(chart_data, names='printer__name', values='total', hole=0.4)
    chart_html = fig.to_html(full_html=False, include_plotlyjs='cdn')

    return render(request, 'calculator/index.html', {
        'orders': orders,
        'total_revenue': total_revenue,
        'usd_rate': usd_rate,
        'chart': chart_html,
        'form': form,
        'markup': 2.5
    })