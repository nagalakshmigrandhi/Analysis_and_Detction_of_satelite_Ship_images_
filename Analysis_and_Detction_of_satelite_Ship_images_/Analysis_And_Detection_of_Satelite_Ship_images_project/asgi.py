import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Analysis_And_Detection_of_Satelite_Ship_images.settings')

application = get_asgi_application()
