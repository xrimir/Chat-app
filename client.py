import threading
import socket


HEADER = 64
SERVER = "insert server ip"
PORT = 5050
ADDR = (SERVER, PORT)
ENCODING = 'utf-8'
DISCONNECT_MESSAGE = '$disconnect'
nickname = ""

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def set_nickname():
    global nickname
    nickname = input("[ENTER NICKNAME]: ")
    send(nickname)


def send(msg):
    message = msg.encode(ENCODING)
    msg_len = len(message)
    send_length = str(msg_len).encode(ENCODING)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)


def write():
    chat = True
    while chat:
        message = f"{nickname}: {input()}"
        send(message)
        if message == DISCONNECT_MESSAGE:
            client.close()
            break

def receive():
    while True:
        try:
            message_len = int(client.recv(HEADER).decode(ENCODING))
            message = client.recv(message_len).decode(ENCODING)
            print(message)
        except:
            print("Error has occured")
            client.close()
            break

def start_client():
    set_nickname()
    
    receive_thread = threading.Thread(target=receive)
    receive_thread.start()

    write_thread = threading.Thread(target=write)
    write_thread.start()



start_client()