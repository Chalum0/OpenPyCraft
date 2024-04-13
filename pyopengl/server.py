import socket
import threading
import json

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind(('', 8080))
FORMAT = "UTF-8"
all_players = []


class Player:
    def __init__(self, username):
        self.username = username
        self.pos = [0, 0, 0]

    def get_pos(self):
        return self.pos

    def set_pos(self, pos):
        self.pos = pos


def handle_client(conn, addr):
    global all_players
    username = conn.recv(255).decode(FORMAT)
    instance = Player(username)
    all_players.append(instance)

    connected = True
    while connected:
        data = conn.recv(1024).decode(FORMAT)
        print(data == "quit")
        if data == "quit":
            connected = False
            all_players.remove(instance)
            conn.close()
        else:
            instance.set_pos(json.loads(data))
            poses = []
            for player in all_players:
                if not player.username == instance.username:
                    poses.append(player.get_pos())
            conn.send(str(poses).encode(FORMAT))


while True:
    print("running")
    socket.listen(5)
    connection, address = socket.accept()
    my_thread = threading.Thread(target=handle_client, args=(connection, address))
    my_thread.start()
