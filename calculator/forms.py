from django import forms
from .models import PrintOrder

class PrintOrderForm(forms.ModelForm):
    class Meta:
        model = PrintOrder
        fields = ['printer', 'filament', 'model_weight_g', 'print_time_hours']
        labels = {
            'printer': 'Принтер',
            'filament': 'Пластик',
            'model_weight_g': 'Вес (г)',
            'print_time_hours': 'Время (ч)',
        }
        widgets = {
            'printer': forms.Select(attrs={'class': 'form-select'}),
            'filament': forms.Select(attrs={'class': 'form-select'}),
            'model_weight_g': forms.NumberInput(attrs={'class': 'form-control'}),
            'print_time_hours': forms.NumberInput(attrs={'class': 'form-control'}),
        }