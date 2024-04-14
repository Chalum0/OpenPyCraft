import socket
import threading
import ast

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind(('', 8080))
FORMAT = "UTF-8"
all_players = []

connected_ip = {}


class Player:
    def __init__(self, username, id):
        self.username = username
        self.id = id
        self.pos = [0, 0, 0]

    def get_pos(self):
        return self.pos

    def set_pos(self, pos):
        self.pos = pos


def handle_client(conn, addr):
    global all_players
    global connected_ip
    try:
        username = conn.recv(255).decode(FORMAT)
        if username not in connected_ip:
            connected_ip[username] = 0
        connected_ip[username] += 1
        instance = Player(username, connected_ip[username])
        all_players.append(instance)
    except ConnectionResetError:
        conn.close()
        exit()

    try:
        connected = True
        while connected:
            data = conn.recv(1024).decode(FORMAT)
            if data == "quit":
                connected = False
                all_players.remove(instance)
                conn.close()
            else:
                instance.set_pos(ast.literal_eval(data))
                poses = {}
                for player in all_players:
                    if not player.username == instance.username:
                        poses[f'{player.username}:{player.id}'] = player.get_pos()
                conn.send(str(poses).encode(FORMAT))
    except ConnectionResetError:
        all_players.remove(instance)
        connected_ip[username] -= 1
        conn.close()


while True:
    socket.listen(5)
    connection, address = socket.accept()
    print(f"address {address} is connected")
    my_thread = threading.Thread(target=handle_client, args=(connection, address))
    my_thread.start()
