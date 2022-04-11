from django.apps import AppConfig
from django.conf import settings
import redis


class MessageConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'message'

    def ready(self):
        settings.REDIS_INSTANCE = redis.Redis.from_url(
            url=settings.REDIS_CONNECTION_URL,
            retry_on_timeout=True,
            retry_on_error=[redis.exceptions.ConnectionError]
        )
