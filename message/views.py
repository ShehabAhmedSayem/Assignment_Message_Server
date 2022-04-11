from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from message.redis_connect import RedisClient
from message.tasks import task_send_new_and_reply_message
from message.helpers import (
    get_client_ip_address, get_receiver_client_address
)

@csrf_exempt
def connect_with_chat_server(request):
    if request.method == 'GET':
        client_ip_address = get_client_ip_address(request)
        client_list = RedisClient().add_new_client(client_ip_address)
        return JsonResponse({'client_list': client_list})
    else:
        return JsonResponse({'error': 'NOT ALLOWED'}, status=405)


@csrf_exempt
def incoming_message(request):
    if request.method == 'POST':
        sender_client_address = get_client_ip_address(request)
        message = request.POST.get('message', None)
        client_list = RedisClient().get_client_list()
        receiver_client_address = get_receiver_client_address(
                                    client_list, 
                                    sender_client_address
                                )
        if receiver_client_address:
            task_send_new_and_reply_message.delay(
                message, 
                sender_client_address,
                receiver_client_address
            )
        else:
            print("Cannot send message back to the sender!")
    return JsonResponse({'status': 'OK'})
