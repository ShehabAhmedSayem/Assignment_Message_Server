import json

from celery import shared_task

from message.redis_connect import RedisClient
from message.helpers import (
    send_new_message_to_client_address,
    send_reply_to_client_address
)

@shared_task
def task_send_new_and_reply_message(
    message, 
    sender_client_address, 
    receiver_client_address
):
    print(f"\n{sender_client_address} -> {message}\n")
    status_code, response = send_new_message_to_client_address(
                                receiver_client_address, 
                                sender_client_address, 
                                message
                            )
    if status_code == 200:
        reply = json.loads(response)["reply"]
        print(f"{reply} -> {receiver_client_address}\n")
        status_code, reply = send_reply_to_client_address(
                                receiver_client_address,
                                sender_client_address, 
                                message,
                                reply
                            )
        if status_code != 200:
            print(f"Couldn't send reply to {sender_client_address}!\n")
    else:
        RedisClient().remove_client(receiver_client_address)
        print(f"Couldn't send message to {receiver_client_address}!\n")
        