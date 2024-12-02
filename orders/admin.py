from django.contrib import admin
from django.http import HttpResponse
import csv
import datetime
from .models import Order, OrderItem
from django.urls import reverse
from django.utils.safestring import mark_safe

# Inline to show order items within the order view
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']  # Use a search field for 'product' instead of a dropdown

# Export to CSV function
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
    
    # Write a first row with header information
    writer.writerow([field.verbose_name for field in fields])
    
    # Write data rows for each object in the queryset
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')  # Format datetime fields
            data_row.append(value)
        writer.writerow(data_row)
    
    return response

export_to_csv.short_description = 'Export to CSV'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # Fields to display in the list of orders
    list_display = [
        'id', 'first_name', 'last_name', 'phone_number', 'payment_method', 'paid', 'created', 'updated',
    ]
    
    # Filters for orders
    list_filter = ['paid', 'created', 'updated']
    
    # Inline for showing order items
    inlines = [OrderItemInline]
    
    # Fields to search in the admin
    search_fields = ['first_name', 'last_name', 'phone_number']
    
    # Adding the CSV export action
    actions = [export_to_csv]
