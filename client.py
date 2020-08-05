import socket, time
import threading

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
buffer = 4096
#ip = socket.gethostbyname(socket.gethostname())
print("This is the client server.")
ip = input(str("Enter the ip address of the server to connect to: "))
time.sleep(1)
s.connect((ip, 1234))
print("Connected to the server!")
#name = os.environ.get('USER')

def send_msg():
    while True:
        msg = input(str())
        #msg = sys.stdin.readline()
        s.send(msg.encode())

        if msg == '[exit]':
            msg = "Left the chat room"
            s.send(msg.encode())
            s.close()

def recv_msg():
    while True:
        message = s.recv(buffer)
        if not message:
            sys.exit(0)
        msg = message.decode()
        print(msg)

t = threading.Thread(target=recv_msg)
t.start()

send_msg()
