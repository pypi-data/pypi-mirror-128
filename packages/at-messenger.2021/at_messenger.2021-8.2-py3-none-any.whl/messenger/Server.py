import select
import sys
from socket import *
import messenger.JIM
from messenger import JIM, security
# from Log.server_log import server_log
from messenger.common_def import send_json, get_json, CheckMeta
from messenger.db import MainStorage, ListClients, Client, History, ClientPass
from threading import Thread

# GUI
from PyQt5 import QtWidgets
from messenger.server_gui import Ui_MainWindow

# auth
import messenger.security
from messenger.decorators_all import login_required


class ServerGui(QtWidgets.QMainWindow):
    def __init__(self):
        self.server = None

        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.start_server)
        self.ui.pushButton_2.clicked.connect(self.stop_server)

    def start_server(self):
        server = Server()
        self.server = server
        self.ui.getUsers.clicked.connect(self.server.get_users)
        self.server.start_server()

    def stop_server(self):
        self.server.stop_server()
        self.server = None


class ServerCheck:
    def __init__(self, name_attr, default=7777):
        self.name = f'_{name_attr}'
        self.default = default

    def __get__(self, instance, owner):
        return getattr(instance, self.name, self.default)

    def __set__(self, instance, value):
        value = int(value)
        if 65000 < value < 0:
            setattr(instance, self.name, self.default)
        else:
            setattr(instance, self.name, value)


class ServerBase(metaclass=CheckMeta):
    pass


class Server(ServerBase, Thread):
    port = ServerCheck('parse_port', 7777)
    base_db = MainStorage()

    def __init__(self):
        self.clients = []
        self.server_connect_socket = socket(AF_INET, SOCK_STREAM)
        self.server_is_running = False
        Thread.__init__(self)

    def server_start(self):
        print(f'!!! Using port {self.port}')
        self.server_connect_socket.bind(('127.0.0.1', self.port))
        self.server_connect_socket.listen(JIM.default_attrs.get('default_max_connections'))
        self.server_connect_socket.settimeout(0.2)
        # server_log.info('Server has started.')
        print('Server has started.')

        while self.server_is_running:
            try:
                connect, addr = self.server_connect_socket.accept()
            except OSError as e:
                pass
            else:
                if connect not in self.clients:
                    # run auth proc
                    if not security.check(connect, JIM.secret_key_for_auth):
                        connect.close()
                        print(f'Del client ==>> {addr}')
                    else:
                        print(f'Add client ==>> {addr}')
                        self.clients.append(connect)
            from_users_msg = []
            to_users_msg = []
            dict_msg_from_users = {}
            try:
                from_users_msg, to_users_msg, err_user = select.select(self.clients, self.clients, [], 0)
            except Exception as e:
                print(f'Something went wrong {e}')
            list_msg_from_user = self.from_users(from_users_msg, dict_msg_from_users, to_users_msg)
            if list_msg_from_user:
                print(f'We have msg from users: {list_msg_from_user}')
                self.w_user(list_msg_from_user, to_users_msg)

    def from_users(self, from_users_msg, dict_msg_from_users, to_users_msg):
        for user in from_users_msg:
            try:
                msg_from_user = get_json(user.recv(JIM.default_attrs.get('default_file_size')).decode(
                    JIM.default_attrs.get('default_encoding')), is_server=True)
                dict_msg_from_users[user] = msg_from_user
            except Exception as e:
                self.clients.remove(user)
        return dict_msg_from_users

    @login_required
    def w_user(self, r, w_clients):
        serv_answer = JIM.serv_response
        for str_from_r in r:
            for w_client in w_clients:
                if r[str_from_r]['action'] == 'GET_CONTACTS':
                    li = []
                    db = ListClients(r[str_from_r]).get_list(r[str_from_r])
                    serv_answer['response'] = db[0]
                    for idx in db[1]:
                        li.append(idx.user_id)
                    serv_answer['alert'] = li
                    serv_answer['to'] = r[str_from_r]['user_login']
                    serv_answer['from'] = 'SERVER'
                elif r[str_from_r]['action'] == 'MESSAGE':
                    # add message  to db
                    History(r[str_from_r]).add_message()

                    serv_answer['response'] = 'MESSAGE'
                    serv_answer['alert'] = r[str_from_r]['msg']
                    serv_answer['to'] = r[str_from_r]['to']
                    serv_answer['from'] = r[str_from_r]['from']

                elif r[str_from_r]['action'] == 'ADD' or r[str_from_r]['action'] == 'DEL':
                    db = ListClients(r[str_from_r]).work_list(r[str_from_r])
                    serv_answer['response'] = db[0]
                    serv_answer['alert'] = db[1] + r[str_from_r]['action'] + '' + r[str_from_r]['user_id'] + ' to ' \
                                                                                                             'list of ' \
                                                                                                             'contacts'
                    serv_answer['to'] = r[str_from_r]['user_login']
                    serv_answer['from'] = 'SERVER'
                elif r[str_from_r]['action'] == 'PRESENCE':
                    db = Client(r[str_from_r]['user']['account_name'],
                                r[str_from_r]['user']['status']).get_client()
                    name = r[str_from_r]['user']['account_name']
                    psw = security.hash_pass(*r[str_from_r]['user']['pass'])
                    db_pass = ClientPass(name, psw).add_pss()
                    serv_answer['response'] = db[0]
                    serv_answer['alert'] = db[1]
                    serv_answer['to'] = r[str_from_r]['user']['account_name']
                    serv_answer['from'] = 'SERVER'
                try:
                    print(serv_answer)
                    w_client.send(send_json(serv_answer, is_server=True))
                except Exception as e:
                    w_client.close()
                    self.clients.remove(w_client)

    def run(self):
        self.server_start()

    def start_server(self):
        self.server_is_running = True
        self.port = '7778'
        self.start()

    def stop_server(self):
        self.server_is_running = False
        self.server_connect_socket.close()
        print('Server has stop.')

    def get_users(self):
        db = Client(login=None, info=None).get_query_filter_all_no()
        for idx in db:
            print(idx)

    def server_log(self, log):
        print('server log')


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = ServerGui()

    window.show()

    return app.exec_()


if __name__ == "__main__":
    sys.exit(main())
