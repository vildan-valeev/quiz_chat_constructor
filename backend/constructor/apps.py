from django.apps import AppConfig


class ConstructorConfig(AppConfig):
    name = 'constructor'
    verbose_name = "Конструктор"

    def ready(self):
        import constructor.signals
