import os
import socket
import threading
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
buffer = 4096
port = 1234
ip = socket.gethostbyname(socket.gethostname())
print("CLIENT SERVER STARTED!")

try:
    s.connect((ip, port))
    print("Connected to the server!")
except:
    print("Could not connect!")
s.setblocking(False)

# Gets the username of the User
name = os.environ.get('USERNAME')
'''
flag = 0
if name == 'ArmyGeneral' or name == 'NavyMarshal' or name == 'AirForceChief':
    flag = 1

for i in range(1, 51):
    if name == "Army%d" % i or name == "Navy%d" % i or name == "AirForce%d" % i:
        flag = 1

if flag == 0:
    print("You cannot access this chatroom!")
    sys.exit()
'''
# Sending the username of the client to the server
s.send(name.encode())


def send_msg():
    while True:
        msg = input(str())
        msg = "<" + name + ">: " + msg
        s.send(msg.encode())

        if msg == '[exit]':
            msg = "Left the chat room"
            s.send(msg.encode())
            s.close()


def recv_msg():
    while True:
        message = s.recv(buffer)
        if not message:
            sys.exit()
        msg = message.decode()
        print(msg)


# Send and receive messages continuously
t = threading.Thread(target=recv_msg)
t.start()
send_msg()
