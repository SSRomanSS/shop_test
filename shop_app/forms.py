from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    """Form for new order"""
    class Meta:
        model = Order
        fields = ('name', 'price',)
