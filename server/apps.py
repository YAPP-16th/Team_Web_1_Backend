from django.apps import AppConfig


class ServerConfig(AppConfig):
    name = 'server'

    def ready(self):
        from server.v1.alarm import scheduler
        scheduler.start()
