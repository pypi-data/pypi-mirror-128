import sys
import threading
from threading import Thread
from socket import *

from messenger import JIM
from messenger import security

# from Log.client_log import client_log
from messenger.common_def import parser, get_json, send_json, CheckMeta

# GUI
from PyQt5 import QtWidgets
from messenger.client_gui import Ui_MainWindow


class ClientGui(QtWidgets.QMainWindow):
    def __init__(self):
        self.client = None

        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.connect_client.clicked.connect(self.client_connect)

    def client_connect(self):
        client_name = input('what is your nick:  ')
        client_pss = input('what is your password:  ')
        client = ClientC(client_name, client_pss)
        self.client = client
        # self.ui.getUsers.clicked.connect(self.client.get_users)
        # self.ui.getUsers.clicked.connect(self.client.get_clients)
        # self.ui.send_message.clicked.connect(self.client.send_msg)
        self.client.start_client()


class ClientBase(metaclass=CheckMeta):
    pass


class ClientC(ClientBase, Thread):
    def __init__(self, client_name, client_pss):
        self.client_name = client_name
        self.client_pss = client_pss
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.server = threading.Thread(target=self.server_msg, args=(self.client_socket, self.client_name))
        self.user = threading.Thread(target=self.client_msg, args=(self.client_socket, self.client_name))
        self.auth = False
        Thread.__init__(self)

    def client_start(self):
        attr_from_parser = parser(is_server=False)
        try:
            if attr_from_parser.address is None:
                raise AttributeError('Client stopped. Argument -address of CLI is missing.')
            elif attr_from_parser.port is None:
                raise AttributeError('Client stopped. Argument -port of CLI is missing.')
            # client_socket = socket(AF_INET, SOCK_STREAM)
            self.client_socket.connect((attr_from_parser.address, attr_from_parser.port))
        except AttributeError as ae:
            pass
            # client_log.error(ae)
        else:
            security.auth_client_msg(self.client_socket, JIM.secret_key_for_auth)
            if self.client_socket:
                print('Connection is ready')
                self.server.start()
                self.user.start()
                # if new user add to db
                jim = JIM.presence
                jim['action'], jim['user'] = 'PRESENCE', {'account_name': self.client_name, 'status': 'add user',
                                                          'pass': self.client_pss}
                self.client_socket.send(send_json(jim, is_server=True))

    def client_msg(self, client_socket, client_name):
        jim_body = ''
        while True:
            user_input = input('enter command ')
            if user_input == 'q':
                break
            elif user_input == 'm':
                jim_body = JIM.body_of_msg
                msg_to = input('message to client: ')
                msg = input('enter a text: ')
                jim_body['from'], jim_body['to'], jim_body['msg'], jim_body['action'] = client_name, \
                                                                                        msg_to, \
                                                                                        msg, \
                                                                                        'MESSAGE'
            elif user_input == 'get':
                jim_body = JIM.request_clients
                jim_body['action'], jim_body['time'], jim_body['user_login'], jim_body['user_id'] = 'GET_CONTACTS', \
                                                                                                    'get_time', \
                                                                                                    client_name, \
                                                                                                    None
            elif user_input.lower() == 'add' or user_input.lower() == 'del':
                jim_body = JIM.add_del_clients
                user_id = input('enter nickname: ')
                jim_body['action'], jim_body['time'], jim_body['user_login'], jim_body['user_id'] = user_input.upper(), \
                                                                                                    'get_time', \
                                                                                                    client_name, \
                                                                                                    user_id

            else:
                pass

            client_socket.send(send_json(jim_body, is_server=False))

    def server_msg(self, client_socket, client_name):
        while True:
            msg = get_json(client_socket.recv(JIM.default_attrs.get(
                'default_file_size')).decode(
                JIM.default_attrs.get('default_encoding')), is_server=True)
            if msg['to'] == client_name:
                print(f'\nReceived a message from {msg["from"]}\n{msg["alert"]} {msg["response"]}\n')

    def run(self):
        self.client_start()

    def start_client(self):
        self.start()


def main():
    app = QtWidgets.QApplication(sys.argv)
    window_client = ClientGui()

    window_client.show()

    return app.exec_()


if __name__ == "__main__":
    sys.exit(main())
