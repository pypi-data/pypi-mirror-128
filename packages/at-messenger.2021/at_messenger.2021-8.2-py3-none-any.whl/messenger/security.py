import hashlib
import hmac
import os

from messenger import JIM


def server_auth(connection, secret_key):
    message = os.urandom(32)
    connection.send(message)
    # calc mhash
    msg_hash = hmac.new(secret_key, message, digestmod=hashlib.sha256)
    digest = msg_hash.digest()

    response = connection.recv(len(digest))
    return hmac.compare_digest(digest, response)


def check(connect, s_key):
    if not server_auth(connect, s_key):
        return False
    else:
        return True


def auth_client_msg(connect, s_key):
    message = connect.recv(32)
    msg_hash = hmac.new(s_key, message, digestmod=hashlib.sha256)
    digest = msg_hash.digest()
    connect.send(digest)


def hash_pass(*args):
    return hashlib.pbkdf2_hmac('sha256', b'args[0]', JIM.ha_so_pss, 10000)
