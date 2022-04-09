from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from message.redis_connect import RedisClient
from message.tasks import task_send_new_and_reply_message
from message.helpers import get_client_ip_address


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
        client_ip_address = get_client_ip_address(request)
        message = request.POST.get('message', None)
        client_list = RedisClient().add_new_client(client_ip_address)
        task_send_new_and_reply_message.delay(message, client_ip_address)
    return JsonResponse({'status': 'OK'})
