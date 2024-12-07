from django.contrib import admin
from django.http import HttpResponse
import csv
import datetime
from .models import Order, OrderItem
from django.urls import reverse
from django.utils.safestring import mark_safe

# Inline para mostrar los items de la orden en la vista de la orden
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']  # Usar un campo de búsqueda para 'product' en lugar de un desplegable

# Función para exportar a CSV
def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    content_disposition = f'attachment; filename={opts.verbose_name}.csv'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = content_disposition
    writer = csv.writer(response)

    fields = [
        field for field in opts.get_fields() 
        if not field.many_to_many and not field.one_to_many
    ]
    
    # Escribir una primera fila con los nombres de las columnas
    writer.writerow([field.verbose_name for field in fields])
    
    # Escribir las filas de datos para cada objeto en el queryset
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')  # Formatear campos datetime
            data_row.append(value)
        writer.writerow(data_row)
    
    return response

export_to_csv.short_description = 'Exportar a CSV'

# Usando el decorador para registrar el modelo
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # Campos para mostrar en la lista de órdenes
    list_display = [
        'id', 'first_name', 'last_name', 'phone_number', 'payment_method','special_instructions',  'created', 'updated',
    ]
    
    # Filtros para las órdenes
    list_filter = ['paid', 'created', 'updated']
    
    # Inline para mostrar los items de la orden
    inlines = [OrderItemInline]
    
    # Campos para buscar en el admin
    search_fields = ['first_name', 'last_name', 'phone_number']
    
    # Agregar la acción de exportación a CSV
    actions = [export_to_csv]
