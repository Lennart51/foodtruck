from django.db import models

class Order(models.Model):
    # Datos del cliente
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)  # Teléfono del cliente

    # Fecha de creación y actualización
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # Método de pago
    PAYMENT_CHOICES = [
        ('CASH', 'Efectivo'),
        ('CARD', 'Tarjeta'),
        ('MOBILE', 'Pago Móvil'),
    ]
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='CASH')
    paid = models.BooleanField(default=False)  # Si la orden ha sido pagada

    # Instrucciones especiales y tipo de servicio
    special_instructions = models.TextField(blank=True, null=True)  # Alergias, preferencias
    service_type = models.CharField(max_length=20, choices=[('TAKEAWAY', 'Para llevar'), ('DINEIN', 'Para consumir en el lugar')], default='TAKEAWAY')

    # Hora de entrega (si aplica)
    delivery_time = models.TimeField(blank=True, null=True)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
        ]

    def __str__(self):
        return f'Order {self.id} - {self.first_name} {self.last_name}'

    def get_total_cost(self):
        # Sumar el costo total de todos los items
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey('shop.Product', related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.quantity} x {self.product.name}'

    def get_cost(self):
        # Calcular el costo total para ese item (precio unitario * cantidad)
        return self.price * self.quantity
