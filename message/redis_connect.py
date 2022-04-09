import redis

from django.conf import settings


class RedisClient():
    
    def __init__(self):
        if settings.REDIS_INSTANCE:
            self.redis_instance = settings.REDIS_INSTANCE
        else:
            self.redis_instance = settings.REDIS_INSTANCE = (
                redis.Redis.from_url(
                    url=settings.REDIS_CONNECTION_URL,
                    retry_on_timeout=True,
                    retry_on_error=[redis.exceptions.ConnectionError]
                )
            )

    def get_client_list(self):
        client_list_byte = self.redis_instance.lrange('client_list', 0, -1)
        client_list = []
        for client in client_list_byte:
            client = client.decode('utf-8')
            client_list.append(client)
        return client_list

    def append_client(self, client):
        self.redis_instance.rpush('client_list', client)
    
    def add_new_client(self, client):
        client_list = self.get_client_list()
        if client not in client_list:
            self.append_client(client)
        return client_list

    def remove_client(self, client):
        self.redis_instance.lrem('client_list', 1, client)
    