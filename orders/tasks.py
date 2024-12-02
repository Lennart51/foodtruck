from celery import shared_task
from django.core.mail import send_mail
from .models import Order

@shared_task
def order_created(order_id):
    """ Task to send an e-mail notification when an order is successfully created. """
    
    # Get the order from the database
    order = Order.objects.get(id=order_id)
    
    # Define the subject for the email
    subject = f'Order nr. {order.id}'
    
    # Create the email message
    message = (
        f'Dear {order.first_name},\n\n'
        f'You have successfully placed an order.\n'
        f'Your order ID is {order.id}.'
    )
    
    # Send the email
    mail_sent = send_mail(
        subject, 
        message, 
        'admin@myshop.com', 
        [order.email]
    )
    
    return mail_sent
