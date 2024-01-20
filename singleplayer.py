import pygame
import game
import pieces
import render
import control

nathan_chess_game = game.Game()

running = True
merge_mode = False


def tick(screen: pygame.Surface):
    global running, merge_mode

    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            print("quitting...")

            pygame.quit()
            quit()

    running, move_made, merge_mode = control.get_input(nathan_chess_game=nathan_chess_game, merge_mode=merge_mode,
                                                       events=events)

    if move_made is not None:
        json_move = move_made.to_json()

        nathan_chess_game.make_move(pieces.Move.from_json(json_move))

        nathan_chess_game.zet_nummer += 1
        if nathan_chess_game.zet_nummer > 1:
            nathan_chess_game.zet_nummer = 0
            nathan_chess_game.zet_aantal += 1
            nathan_chess_game.wit_aan_de_buurt = not nathan_chess_game.wit_aan_de_buurt

        #nathan_chess_game.wit_aan_de_buurt = True

    render.render_board(screen=screen, nathan_chess_game=nathan_chess_game, selected_piece=control.selected_piece,
                        merge_mode=merge_mode)

    return running
