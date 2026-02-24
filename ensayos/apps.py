from django.apps import AppConfig


class EnsayosConfig(AppConfig):
    name = 'ensayos'

    def ready(self):
        import ensayos.signals
