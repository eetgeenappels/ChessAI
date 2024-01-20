import random
import socket
import threading
import time
import uuid
import game
import json
from pieces import Move

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
server_address = ('0.0.0.0', 10203)
server_socket.bind(server_address)

white_player_queue: socket.socket = None
black_player_queue: socket.socket = None

matches = []

lobbies = []


class Match:

    def __init__(self, white_player: socket.socket, black_player: socket.socket):
        self.white_player = white_player
        self.black_player = black_player

        self.nathan_chess_game = game.Game()
        self.ongoing = True

    def round(self):
        self.nathan_chess_game.make_move(self.request_move_white())
        self.nathan_chess_game.make_move(self.request_move_white())
        self.nathan_chess_game.make_move(self.request_move_black())
        self.nathan_chess_game.make_move(self.request_move_black())

    def request_move_white(self):
        self.white_player.send(json.dumps({'type': 'move_request'}).encode('utf-8'))
        move_data = self.white_player.recv(1024)
        move_json = json.loads(move_data.decode('utf-8'))
        self.black_player.send(json.dumps({'type': 'enemy_move', 'move': move_json}).encode('utf-8'))
        return Move.from_json(json.dumps(move_json))

    def request_move_black(self):
        self.black_player.send(json.dumps({'type': 'move_request'}).encode('utf-8'))
        move_data = self.black_player.recv(1024)
        move_json = json.loads(move_data.decode('utf-8'))
        self.white_player.send(json.dumps({'type': 'enemy_move', 'move': move_json}).encode('utf-8'))
        return Move.from_json(json.dumps(move_json))


class Lobby:
    def __init__(self, player: socket.socket, player_name: str) -> None:
        self.player2 = None
        self.player2_name = None
        self.player = player
        self.lobby_uuid = uuid.uuid4().hex
        self.player_name = player_name

    def join(self, player2_socket: socket.socket, player2_name: str) -> None:
        self.player2 = player2_socket
        self.player2_name = player2_name

    def match(self):
        match = Match(self.player, self.player2)

        matches.append(match)

        while match.ongoing:
            match.round()

        self.player2.close()
        self.player2.close()


def handle_client(sock: socket.socket):
    player_info = json.loads(sock.recv(1024).decode('utf-8'))

    player_name = player_info['name']

    if player_name == "":
        with open("assets/names_if_user_puts_in_no_names.txt", "r") as f:
            player_name = random.choice(f.readlines())

    lobbies_payload = {
        "lobbies": []
    }

    for lobby in lobbies:
        lobby_payload = lobby.lobby_uuid
        lobbies_payload['lobbies'].append({"id": lobby_payload, "player_name": lobby.player_name})

    sock.send(json.dumps(lobbies_payload).encode("UTF-8"))

    time.sleep(0.1)

    request = json.loads(sock.recv(1024).decode("UTF-8"))

    time.sleep(0.1)

    if request["type"] == 'create lobby':
        new_lobby = Lobby(sock, player_name=player_name)

        lobbies.append(new_lobby)

    if request['type'] == "join lobby":
        lobby_id = request["uuid"]

        for lobby in lobbies:
            if lobby.uuid == lobby_id:
                lobby.join_lobby(sock, player_name)

                lobby.player.send(json.dumps({"type": "game starting"}).encode("UTF-8"))
                lobby.player2.send(json.dumps({"type": "game starting"}).encode("UTF-8"))
                lobby.match()


server_socket.listen(5)

while True:
    try:
        client_socket, client_address = server_socket.accept()

        thread = threading.Thread(target=handle_client, args=[client_socket])
        thread.daemon = True
        thread.start()
    except KeyboardInterrupt:
        print('Server shutting down...')
        server_socket.close()
