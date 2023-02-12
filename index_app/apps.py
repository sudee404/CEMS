from django.apps import AppConfig


class IndexAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'index_app'

    def ready(self):
        import index_app.signals
