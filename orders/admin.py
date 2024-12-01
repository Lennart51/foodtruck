from django.contrib import admin
from .models import Order, OrderItem

# Inline para mostrar los ítems de la orden dentro de la vista de la orden
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']  # Para hacer que el campo 'product' use un campo de búsqueda en vez de un desplegable

# Personalización de la vista de la administración para la orden
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # Campos que se mostrarán en la lista de órdenes
    list_display = [
        'id', 'first_name', 'last_name', 'phone_number', 'payment_method', 'paid', 'created', 'updated'
    ]
    
    # Filtros para las órdenes
    list_filter = ['paid', 'created', 'updated']
    
    # Inline para los ítems de la orden (para mostrar los productos de cada orden)
    inlines = [OrderItemInline]
    
    # Campos para la búsqueda rápida en la administración
    search_fields = ['first_name', 'last_name', 'phone_number']

# Para el modelo OrderItem, ya que el inline lo gestiona, no es necesario un administrador separado.
