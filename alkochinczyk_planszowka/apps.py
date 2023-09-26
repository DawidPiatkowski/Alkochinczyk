from django.apps import AppConfig


class AlkochinczykPlanszowkaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'alkochinczyk_planszowka'

    def ready(self):
        from alkochinczyk_planszowka import signals
