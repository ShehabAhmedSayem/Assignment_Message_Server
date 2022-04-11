import requests

from message.redis_connect import RedisClient


def send_request_to_chat_server(url, data=None, timeout=5):
    status_code = 200
    response_text = ''
    try:
        if data:
            r = requests.post(url=url, data=data, timeout=timeout)
        else:
            r = requests.get(url=url, timeout=timeout)
        status_code = r.status_code
        response_text = r.text
    except requests.exceptions.Timeout:
        status_code = 408
    except requests.exceptions.ConnectionError:
        status_code = 503
    except:
        status_code = 500
    return status_code, response_text


def send_new_message_to_client_address(
    receiver_client_address, 
    sender_client_address, 
    message,
    timeout=10
):
    url = "http://" + receiver_client_address + "/new-message/"
    data = {
        'message': message, 
        'sender_client_address': sender_client_address
    }
    return send_request_to_chat_server(url, data=data, timeout=timeout)


def send_reply_to_client_address(
    receiver_client_address, 
    sender_client_address, 
    message,
    reply,
    timeout=10
):
    url = "http://" + sender_client_address + "/reply-message/"
    data = {
        'message': message, 
        'reply': reply,
        'sender_client_address': receiver_client_address
    }
    return send_request_to_chat_server(url, data=data, timeout=timeout)


def get_receiver_client_address(client_list, sender_client_address):
    receiver_client_address = None
    if len(client_list) > 1:
        if client_list[0] == sender_client_address:
            receiver_client_address = client_list[1]
        else:
            receiver_client_address = client_list[0]
        RedisClient().pop_client(receiver_client_address)
        RedisClient().append_client(receiver_client_address)
    return receiver_client_address


def visitor_ip_address(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_client_ip_address(request):
    client_port = request.headers.get('Client-Port', None)
    client_address = visitor_ip_address(request)
    if client_port:
        client_address = client_address + ':' + str(client_port)
    return client_address


def ping(client):
    url = "http://" + client + "/ping/"
    status_code, _ = send_request_to_chat_server(url)
    if status_code == 200:
        return True
    return False