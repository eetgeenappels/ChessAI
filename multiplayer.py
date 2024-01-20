import pygame
import game
import render
import control
import socket
import pieces
import json
import assets

nathan_chess_game = game.Game()

running = True
merge_mode = False

is_client_white = True

move_made: pieces.Move
made_move = False

in_queue = False
in_game = False
in_lobby_select = False

font = pygame.font.SysFont('arial', size=40)
font_small = pygame.font.SysFont('arial', size=20)

lobbies_json = []

ip = "ip"
name = " "

action = 0
lobby_id = ""


def connect():
    global made_move, in_game, is_client_white, move_made, in_queue, in_lobby_select, lobbies_json, lobby_id

    while ip == "ip":
        pass

    print("Connecting to " + ip)

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (ip, 10203)
    client_socket.connect(server_address)

    print("Connected to " + ip)

    client_socket.send(json.dumps({"name": name}).encode('utf-8'))

    lobbies = client_socket.recv(1024)

    print("in lobby select")

    lobbies_json = json.loads(lobbies.decode('utf-8'))["lobbies"]

    print(lobbies_json)

    width = 400
    height = 50
    offset = 100

    def on_click(button: render.Button):
        global in_lobby_select, lobby_id

        lobby_id = button.text

        in_lobby_select = False

    for lobby in enumerate(lobbies_json):
        player_name = lobby[1]["player_name"]
        id = lobby[1]["id"]

        # render squared
        button = render.Button(100, 100 + offset * lobby[0], width, height, text=id)

        button.on_click = on_click

        buttons.append(button)

    in_lobby_select = True

    while in_lobby_select:
        pass

    if action == 1:
        client_socket.send(json.dumps({"type": "create lobby"}).encode('utf-8'))
        in_queue = True

        client_socket.recv(1024)

        in_queue = False
    if action == 2:
        client_socket.send(json.dumps({"type": "join lobby", "id": lobby_id}).encode('utf-8'))

        client_socket.recv(1024)

    while running:

        message = json.loads(client_socket.recv(1024).decode())

        print(message)

        if message["type"] == "move_request":

            nathan_chess_game.wit_aan_de_buurt = is_client_white

            while not made_move:
                pass

            payload = move_made.to_json()

            client_socket.send(payload.encode())

            nathan_chess_game.wit_aan_de_buurt = not is_client_white

            made_move = False

        if message["type"] == "enemy_move":
            move = pieces.Move.from_json(json.dumps(message["move"]))

            nathan_chess_game.make_move(move)


textfield = render.InputBox(100, 100, 400, 50)
textfield2 = render.InputBox(100, 20, 400, 50)

add_lobby_button = render.ImageButton(900, 0, 100, 100, assets.plus)

textfield2.reset_on_return = False


def on_return_ip(text):
    global ip, textfield2, name
    name = textfield2.text
    print(textfield2.text)
    ip = text


textfield.return_event = on_return_ip


def add_lobby(button):
    global in_lobby_select, action
    in_lobby_select = False
    action = 1
    print("oi")


add_lobby_button.on_click = add_lobby

buttons = []


def tick(screen: pygame.Surface):
    global running, merge_mode, is_client_white, move_made, made_move

    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            running = False
        if not in_queue and not in_game and not in_lobby_select:
            textfield.handle_event(event)
            textfield2.handle_event(event)
        if in_lobby_select:
            add_lobby_button.handle_event(event)
            for button in buttons:
                button.handle_event(event)

    if in_lobby_select:

        add_lobby_button.render(screen)

        for button in buttons:
            button.render(screen)

    elif in_queue:

        screen.blit(font.render("Waiting in Lobby...", False, (0, 0, 0)), (100, 100))

    elif in_game:

        if is_client_white == nathan_chess_game.white_turn():
            running, move_made, merge_mode = control.get_input(nathan_chess_game=nathan_chess_game,
                                                               merge_mode=merge_mode, events=events)

            if move_made is not None:
                nathan_chess_game.make_move(move_made)

                made_move = True

        render.render_board(screen=screen, nathan_chess_game=nathan_chess_game, selected_piece=control.selected_piece,
                            merge_mode=merge_mode,
                            render_move_highlights=is_client_white == nathan_chess_game.white_turn())

    else:

        textfield.draw(screen)
        textfield2.draw(screen)

    return running
