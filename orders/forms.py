from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'first_name', 
            'last_name', 
            'phone_number',  # Agregar teléfono del cliente
            'payment_method',  # Método de pago
            'special_instructions',  # Instrucciones especiales
            'service_type',  # Tipo de servicio (para llevar o comer en el lugar)
            'delivery_time'  # Hora de entrega (si aplica)
        ]
