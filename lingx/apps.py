from django.apps import AppConfig


class LingxConfig(AppConfig):
    name = 'lingx'
    
    def ready(self):
        import lingx.signals
