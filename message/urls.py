from django.urls import path

from message.views import connect_with_chat_server, incoming_message

urlpatterns = [
    path('connect/', connect_with_chat_server, name='connect_with_chat_server'),
    path('incoming-message/', incoming_message, name='incoming_message'),
]
