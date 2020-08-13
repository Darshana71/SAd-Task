#!/usr/bin/python3
import socket
import sys
import threading
import select

host = socket.gethostname()
port = 1234
buffer = 4096
socket_list = {}

ARMY = ["ArmyGeneral", "ChiefCommander"]
NAVY = ["NavyMarshal", "ChiefCommander"]
AIRFORCE = ["AirForceChief", "ChiefCommander"]
HEADS = ["ArmyGeneral", "NavyMarshal", "AirForceChief", "ChiefCommander"]
CHATS = ["army_chat", "navy_chat", "airforce_chat", "heads_chat"]

army_chat = []
navy_chat = []
airforce_chat = []
heads_chat = []

# Adding each of the troop members to their respective groups
for i in range(1, 50):
    ARMY.append(f'Army{i}')
    NAVY.append(f'Navy{i}')
    AIRFORCE.append(f'AirForce{i}')


def clientthread(conn, addr, user):
    while True:
        try:
            msg = conn.recv(buffer)
            msg = msg.decode()
            words = msg.split()
            # Sending messages to the respective groups based on the client
            if user in ARMY:
                if "<ArmyGeneral>:" in words:
                    broadcast(conn, msg, army_chat)
                    broadcast(conn, msg, heads_chat)
                else:
                    broadcast(conn, msg, army_chat)

            if user in NAVY:
                if "<NavyMarshal>:" in words:
                    broadcast(conn, msg, navy_chat)
                    broadcast(conn, msg, heads_chat)
                else:
                    broadcast(conn, msg, navy_chat)

            if user in AIRFORCE:
                if "<ArmyGeneral>:" in words:
                    broadcast(conn, msg, airforce_chat)
                    broadcast(conn, msg, heads_chat)
                else:
                    broadcast(conn, msg, airforce_chat)

            elif user == "ChiefCommander":
                broadcast(conn, msg, heads_chat)

        except:
            conn.send("Couldn't send your message!".encode())


def broadcast(conn, msg, chat):
    for client in chat:
            try:
                client.send(msg.encode())
            except:
                client.close()
                socket_list.remove(client)


if __name__ == "__main__":
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as msg:
        print("Could not create socket. Error code: ", str(msg[0]), "Error: ", msg[1])
        sys.exit()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ip = socket.gethostbyname(host)
    try:
        server_socket.bind((ip, port))
    except socket.error as msg:
        print("Bind failed. Error code: {} Error: {}".format(str(msg[0]), msg[1]))
        sys.exit()

    socket_list = [server_socket]
    server_socket.listen(200)
    print("Server is waiting for connections!")
    while True:
        read_sockets, _, exception_socket = select.select(socket_list, [], socket_list)

        for notified_socket in read_sockets:
            if notified_socket == server_socket:
                # Accepting connections from clients
                conn, addr = server_socket.accept()
                user = conn.recv(buffer).decode()
                socket_list.append(conn)
                print("Client(%s, %s) has connected! Username: " % addr, user)

                if user in ARMY:
                    if user == "ArmyGeneral":
                        heads_chat.append(conn)
                    army_chat.append(conn)

                if user in NAVY:
                    if user == "NavyMarshal":
                        heads_chat.append(conn)
                    navy_chat.append(conn)

                if user in AIRFORCE:
                    if user == "AirForceChief":
                        heads_chat.append(conn)
                    airforce_chat.append(conn)

                elif user == "ChiefCommander":
                    heads_chat.append(conn)
                    army_chat.append(conn)
                    navy_chat.append(conn)
                    airforce_chat.append(conn)

            t = threading.Thread(target=clientthread, args=(conn, addr, user))
            t.start()
