import argparse
import json
import sys
from functools import wraps
import dis

from messenger import JIM
# from Log.client_log import client_log
# from Log.server_log import server_log


class CheckMeta(type):
    def __init__(self, clsname, bases, clsdict):
        super().__init__(clsname, bases, clsdict)

        used = set()
        prohibited_words = ''
        permitted_words = ''

        if clsname == 'Server':
            prohibited_words = ['connect']
            permitted_words = ['AF_INET', 'SOCK_STREAM', 'socket']
        elif clsname == 'Client':
            prohibited_words = ['accept', 'listen']
            permitted_words = ['AF_INET', 'SOCK_STREAM', 'socket']

        for key, value in clsdict.items():
            if hasattr(value, '__call__'):
                get_parse = dis.get_instructions(value)
                for idx in get_parse:
                    if idx.opname == 'LOAD_GLOBAL':
                        used.add(idx.argval)
        for search_word in prohibited_words:
            if search_word in used:
                raise TypeError(f'Use prohibited words {search_word}')
        for search_word in permitted_words:
            if not (search_word in used):
                raise TypeError(f'Do not use permitted methods {search_word}')


class LogClass:
    def __call__(self, some_func):
        @wraps(some_func)
        def wrapper(is_server, **kwargs):
            msg = f'\nFunction: {some_func.__name__} , it runs from {sys._getframe(1).f_code.co_name}'
            # if is_server:
            #     # server_log.debug(msg)
            # else:
            #     # client_log.debug(msg)
            run_func = some_func(is_server, **kwargs)
            return run_func

        return wrapper


# def log_def(some_func):
#     @wraps(some_func)
#     def wrapper(is_server, **kwargs):
#         msg = f'\nFunction: {some_func.__name__} , it runs from {sys._getframe(1).f_code.co_name}'
#         if is_server:
#             server_log.debug(msg)
#         else:
#             client_log.debug(msg)
#         run_func = some_func(is_server, **kwargs)
#         return run_func
#
#     return wrapper


def send_json(msg, is_server):
    # if is_server:
    #     # server_log.info(f'Sent message to client.\n{msg}')
    # else:
    #     # client_log.info(f'Sent message to server.\n{msg}')
    return json.dumps(msg).encode(JIM.default_attrs.get('default_encoding'))


def get_json(msg, is_server):
    # if is_server:
    # server_log.info(f'Received message from client\n{msg}')
    return json.loads(msg)


# @log_def
@LogClass()
def parser(is_server):
    pars_string = argparse.ArgumentParser()
    pars_string.add_argument('-p', '--port', type=int, default=JIM.default_attrs.get('default_port'))
    pars_string.add_argument('-a', '--address', default=JIM.default_attrs.get('default_address'))
    pars_attr = pars_string.parse_args()
    return pars_attr


def check_status(msg_from_client):
    if msg_from_client['action'] == 'presence':
        status = '200'
        msg = 'OK'
    else:
        status = '500'
        msg = 'Error'
    res = JIM.serv_response['response'], JIM.serv_response['alert'] = status, msg
    # server_log.info(f'Prepare answer to client\n{res}')
    return res
