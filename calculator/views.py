from django.shortcuts import render
from .models import PrintOrder
from django.db.models import Sum

def index(request):
    # Получаем все заказы, от новых к старым
    orders = PrintOrder.objects.all().order_by('-created_at')
    
    # Считаем общую выручку/стоимость всех заказов для аналитики
    total_revenue = orders.aggregate(Sum('total_cost'))['total_cost__sum'] or 0
    
    return render(request, 'calculator/index.html', {
        'orders': orders,
        'total_revenue': total_revenue
    })