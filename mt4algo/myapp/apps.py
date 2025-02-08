from django.apps import AppConfig


class MyappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapp'

    # def ready(self):
    #     from .utils import start_monitoring
    #     start_monitoring()  # मॉनिटरिंग सर्वर स्टार्ट होते ही शुरू हो जाएगी
