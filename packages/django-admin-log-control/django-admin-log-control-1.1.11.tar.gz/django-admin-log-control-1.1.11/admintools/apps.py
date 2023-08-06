from django.apps import AppConfig


class AdmintoolsConfig(AppConfig):
    name = 'admintools'

    def ready(self):
        import admintools.signals
