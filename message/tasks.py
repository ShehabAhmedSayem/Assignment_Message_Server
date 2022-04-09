import json

from celery import shared_task

from message.redis_connect import RedisClient
from message.helpers import (
    get_to_client_address_by_round_robin, 
    send_new_message_to_client_address,
    send_reply_to_client_address
)

@shared_task
def task_send_new_and_reply_message(message, from_client_address):
    to_client_address = get_to_client_address_by_round_robin(from_client_address)
    if to_client_address:
        print(f"\n{from_client_address} -> {message}")
        status_code, response = send_new_message_to_client_address(
                                    to_client_address, 
                                    from_client_address, 
                                    message
                                )
        if status_code == 200:
            reply = json.loads(response)["reply"]
            print(f"{reply} -> {to_client_address}\n")
            status_code, reply = send_reply_to_client_address(
                                    to_client_address,
                                    from_client_address, 
                                    message,
                                    reply
                                )
        else:
            RedisClient().remove_client(to_client_address)
            print("Couldn't send message!")
        
        