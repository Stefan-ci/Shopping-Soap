from django.apps import AppConfig


class ProfilsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'profils'

    def ready(self):
        import profils.signals
