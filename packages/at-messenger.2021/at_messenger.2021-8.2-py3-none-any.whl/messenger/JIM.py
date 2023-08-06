presence = {
    "action": "presence",
    "type": "status",
    "user": {
        "account_name": '',
        "status": "Online",
        "pass": ''
    }
}

default_attrs = {
    "default_address": '127.0.0.1',
    "default_port": 7778,
    "default_encoding": 'utf-8',
    "default_max_connections": 5,
    "default_file_size": 1024
}

active_users_request = {
    'type_of_request': None,
    'from_who': None
}

body_of_msg = {
    # 'id_session': None,
    'action': None,
    'from': None,
    'to': None,
    'msg': None
}

request_clients = {
    "action": "get_contacts",
    "time": None,
    "user_login": None,
    "user_id": None
}

serv_response = {
    "response": None,
    "alert": None,
    "to": None,
    "from": None
}

add_del_clients = {
    "action": None,  # "add_contact" | "del_contact",
    "user_id": None,  # "nickname",
    "time": None,  # now
    "user_login": None
}

prohibited_words_server = ['connect']
prohibited_words_client = ['accept', 'listen']
permitted_words = ['AF_INET', 'SOCK_STREAM', 'socket']


secret_key_for_auth = b'Geek_keY'
ha_so_pss = b'BrainS$GeeK'
