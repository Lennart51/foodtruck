import os
from celery import Celery

# Establecer el módulo de configuración predeterminado de Django para el programa 'celery'.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myshop.settings')

app = Celery('myshop')

# Cargar la configuración desde el módulo de configuración de Django.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Autodescubrimiento de tareas definidas en los `tasks.py` de las aplicaciones registradas.
app.autodiscover_tasks()
