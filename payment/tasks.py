from io import BytesIO
import weasyprint
from celery import shared_task
from django.contrib.staticfiles import finders
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from orders.models import Order

@shared_task
def payment_completed(order_id):
    """ Task to send an e-mail notification when an order is successfully paid. """
    # Retrieve the order by ID
    order = Order.objects.get(id=order_id)

    # Create the email subject and message
    subject = f'My Shop - Invoice no. {order.id}'
    message = 'Please, find attached the invoice for your recent purchase.'
    
    # Create the email message
    email = EmailMessage(subject, message, 'admin@myshop.com', [order.email])

    # Generate the PDF from the order HTML
    html = render_to_string('orders/order/pdf.html', {'order': order})
    out = BytesIO()

    # Load the CSS and generate the PDF
    stylesheets = [weasyprint.CSS(finders.find('css/pdf.css'))]
    weasyprint.HTML(string=html).write_pdf(out, stylesheets=stylesheets)

    # Attach the PDF to the email
    email.attach(f'order_{order.id}.pdf', out.getvalue(), 'application/pdf')

    # Send the email
    email.send()
