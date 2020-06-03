from django.apps import AppConfig
from django.conf import settings


class ServerConfig(AppConfig):
    name = 'server'

    def ready(self):
        from server.v1.alarm import scheduler
        if settings.SCHEDULER_AUTOSTART:
            scheduler.start()
