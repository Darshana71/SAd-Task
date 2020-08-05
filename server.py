#!/usr/bin/python3

import tkinter as tk
window = tk.Tk()
window.title("Chat application - Server")

topFrame = tk.Frame(window)
btnStart = tk.Button(topFrame, text="Start", command=lambda : start())
btnStart.pack(side=tk.LEFT)
btnStop = tk.Button(topFrame, text="Stop", command=lambda: stop())
btnStop.pack(side=tk.LEFT)
topFrame.pack(side=tk.TOP, pady=(5, 0))


middleFrame = tk.Frame(window)
lblHost = tk.Label(middleFrame, text = "Host: X.X.X.X")
lblHost.pack(side=tk.LEFT)
lblPort = tk.Label(middleFrame, text = "Port:XXXX")
lblPort.pack(side=tk.LEFT)
middleFrame.pack(side=tk.TOP, pady=(5, 0))


import socket, select, sys
import threading

host = socket.gethostname()
Port = 1234
clients_list=[]
buffer = 4096

def start():
    global server, host, Port
    while True:
        btnStart.config(state=tk.DISABLED)
        btnStop.config(state=tk.NORMAL)

        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except:
            print("Could not create socket. Error code: ", str(msg[0]), "Error: ", msg[1])
            sys.exit()
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        ip = socket.gethostbyname(host)
        try:
            server.bind((ip, Port))
        except socket.error as msg:
            print("Bind failed. Error code: {} Error: {}".format(str(msg[0]), msg[1]))
            sys.exit()
        
        server.listen(200)

        print("Server is waiting for connections!")
   
        threading._start_new_thread(target=accept_clients, args=(server,),)

        lblHost["text"] = "IP: " + ip
        lblPort["text"] = "Port: " + str(Port)


def stop():
    global server
    btnStart.config(state=tk.NORMAL)
    btnStop.config(state=tk.DISABLED)
    server.close()
    print("Server has been closed!")

def clientthread(conn, addr):
    while True:
        try:
            msg = conn.recv(buffer)
            msg = msg.decode()
            if msg:
                print(msg)
                broadcast(msg, conn)

            else:
                remove(conn)
        except:
            continue
    
def broadcast(msg, conn):
    for clients in clients_list:
        if clients!=conn:
            try:
                clients.send(msg.encode())
            except:
                clients.close()
                remove(clients)

def remove(conn):
    if conn in clients_list:
        clients_list.remove(conn)


def accept_clients(server):
    while True:
        conn, addr = server.accept()
        clients_list.append(conn)
        print("Client(%s, %s) has connected!" % addr)
        broadcast("Client(%s, %s) has connected!" % addr, conn)

        threading._start_new_thread(target=clientthread, args=(conn, addr))
    


window.mainloop()
