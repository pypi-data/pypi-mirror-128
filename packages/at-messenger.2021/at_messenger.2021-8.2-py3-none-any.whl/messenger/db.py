# from pprint import pprint
from sqlalchemy import Column, Integer, String, DATETIME, create_engine, and_, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

BaseDb = declarative_base()


class MainStorage:
    def __init__(self):
        self.EngineDB = create_engine('sqlite:///server_db.sqlite', echo=False)
        self.BaseDB = BaseDb.metadata.create_all(self.EngineDB)
        SessionDb = sessionmaker(bind=self.EngineDB)
        self.sess = SessionDb()

    # def __repr__(self):
    #     return f'{self.__class__.__name__}' \
    #            f'({self.id}, {self.login})'
    #
    # def delete(self):
    #     self.sess.

    def add_commit(self, *kwargs):
        self.sess.add(self)
        if self.sess.commit() is not None:
            return f'Session {self.sess} uncommitted. Using rollback'
            self.sess.rollback()
            return False
        else:
            return True

    def get_query_filter_all(self, *args):
        return self.sess.query(self.__class__).filter(args[0]).all()

    def get_query_filter_one(self, *args):
        return self.sess.query(self.__class__).filter(and_(args[0], args[1])).one_or_none()

    def get_query_filter_all_no(self):
        return self.sess.query(self.__class__).all()


class Client(MainStorage, BaseDb):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True)
    login = Column(String(32), unique=True)
    info = Column(String(128))

    def __init__(self, login, info):
        super().__init__()
        self.login = login
        self.info = info

    def get_client(self):
        condition_1 = self.__class__.login == self.login
        req = self.get_query_filter_all(condition_1)
        if not req:
            self.add_commit()
            return True, 'create user '
        else:
            return False, 'create user '

    def get_all_clients(self):
        req = self.get_query_filter_all()
        print(req)


class History(MainStorage, BaseDb):
    __tablename__ = 'history_of_clients'

    id = Column(Integer, primary_key=True)
    to_user = Column(String(32))
    user_name = Column(ForeignKey('clients.id'))
    message = Column(String(256))

    def __init__(self, msg):
        super().__init__()
        self.to_user = msg['to']
        self.user_name = msg['from']
        self.message = msg['msg']

    def get_history(self):
        # looking for existing login
        req = self.get_query_filter_all(self.__class__.login, self.login)
        if not req:
            return 'No records '
        return f'{req[0].login}     {req[0].ip}'

    def add_message(self):
        self.add_commit()
        pass


class ListClients(MainStorage, BaseDb):
    __tablename__ = 'list_of_contacts'

    id = Column(Integer, primary_key=True)
    user_login = Column(ForeignKey('clients.id'))
    user_id = Column(Integer)

    def __init__(self, msg):
        super().__init__()
        self.user_login = msg['user_login']
        self.user_id = msg['user_id']

    def get_list(self, msg):
        condition_1 = self.__class__.user_login == msg['user_login']
        req = self.get_query_filter_all(condition_1)
        if req is not None:
            return '202', req
        return '500', 'The list is empty'

    def work_list(self, msg):
        condition_1 = self.__class__.user_login == msg['user_login']
        condition_2 = self.__class__.user_id == msg['user_id']
        req = self.get_query_filter_one(condition_1, condition_2)
        if req is None:
            if msg['action'] == 'ADD':
                if self.add_commit():
                    return '200 ', 'Successful '
        else:
            if msg['action'] == 'DEL':
                self.sess.delete(req)
                self.sess.commit()
                return '200 ', 'Successful '
        return '500 ', 'Unsuccessful '


class ClientPass(MainStorage, BaseDb):
    __tablename__ = 'clients_pss'

    id = Column(Integer, primary_key=True)
    pss = Column(String(256))
    client = Column(ForeignKey('clients.id'))

    def __init__(self, client, pss):
        super().__init__()
        self.pss = pss
        self.client = client

    def add_pss(self):
        condition_1 = self.__class__.client == self.client
        req = self.get_query_filter_all(condition_1)
        if not req:
            self.add_commit()

    # def del_record(self, msg):
    #     condition_1 = self.__class__.user_login == msg['user_login']

# if __name__ == "__main__":
#     pass
# history of user activity
# request = History(datetime.now(), '10.1.1.3', 'Mark')
# print(request.get_history())
#
# # add new client
# request = Client('Black widow', 'adding new client')
# print(request.get_client())

# list of contacts
# request = ListClients(context)
