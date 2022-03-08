import socket
import threading

HEADER = 64
SERVER = socket.gethostbyname(socket.gethostname())
PORT = 5050
ADDR = (SERVER, PORT)
ENCODING = "utf-8"
DISCONNECT_MESSAGE = "$disconnect"
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
clients = []

def broadcast_message(message, sender_conn):
    for client in clients:
        #if client == sender_conn:
        #    continue
        #else:
        client.send(message)

def handle_client_nickname(conn, addr):
    msg_length = conn.recv(HEADER).decode(ENCODING)
    if msg_length:
        msg_length = int(msg_length)
        msg = conn.recv(msg_length).decode(ENCODING)
        clients.append(conn)
        return conn


def handle_client(conn, addr):
    nick = handle_client_nickname(conn, addr)
    connected = True
    while connected:
        
        msg_length = conn.recv(HEADER)
        temp_msg_len = int(msg_length.decode(ENCODING))
        
        if msg_length:
            msg = conn.recv(temp_msg_len)

            broadcast_message(msg_length, conn)
            broadcast_message(msg, conn)

            if msg == DISCONNECT_MESSAGE:
                connected = False
    conn.close()


def start():
    server.listen()
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
start()
