import pygame
from game import Game
import sacrifice
import pieces
import merging
import math
import movement

selected_piece = None


def get_input(nathan_chess_game: Game, merge_mode, events):
    global selected_piece

    running = True
    move_made = None

    for event in events:
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                if not selected_piece is None:
                    if not selected_piece.piece == 'none':
                        merge_mode = True
            if event.key == pygame.K_s:

                if not selected_piece is None:

                    if nathan_chess_game.white_turn():
                        move_made = pieces.Move(position=selected_piece.position, movement_class=6, pawns = nathan_chess_game.wit_sacraficial_pawns)
                    else:
                        move_made = pieces.Move(position=selected_piece.position, movement_class=6, pawns=nathan_chess_game.zwart_sacraficial_pawns)
                pass
            if event.key == pygame.K_c:

                if selected_piece is not None:

                    if selected_piece.can_channel:
                        if nathan_chess_game.white_turn():
                            if selected_piece.channel_cost >= nathan_chess_game.wit_sacraficial_pawns:
                                move_made = pieces.Move(position=selected_piece.position, movement_class=7)
                        else:
                            if selected_piece.channel_cost >= nathan_chess_game.zwart_sacraficial_pawns:
                                move_made = pieces.Move(position=selected_piece.position, movement_class=7)

            if event.key == pygame.K_r:
                if not nathan_chess_game.has_rikeerd:
                    n_k = 0
                    n_q = 0
                    for x in range(8):
                        for y in range(8):
                            if nathan_chess_game.board[x][y].is_white == nathan_chess_game.white_turn():
                                if nathan_chess_game.board[x][y].piece == "koning":
                                    n_k += 1
                                if nathan_chess_game.board[x][y].piece == "dame":
                                    n_q += 1
                    if n_k == 1 and n_q == 1:
                        move_made = pieces.Move((-1, -1), movement_class=3)
            if event.key == pygame.K_t:
                if not selected_piece == None:
                    potential_move = pieces.Move(selected_piece.position, movement_class=4)
                    if nathan_chess_game.is_valid_move(potential_move):
                        move_made = potential_move
        if event.type == pygame.MOUSEBUTTONDOWN:
            m1 = pygame.mouse.get_pressed(3)

            if m1[0]:
                if nathan_chess_game.i9_piece != None:
                    if nathan_chess_game.i9_piece.is_white == nathan_chess_game.white_turn():
                        x, y = pygame.mouse.get_pos()
                        x, y = math.floor(x / 100), math.floor(y / 100)
                        if 0 <= x <= 7 and 0 <= y <= 7:
                            if nathan_chess_game.board[x][y].piece == 'none':
                                move_made = pieces.Move((x, y), movement_class=2)

                if merge_mode:
                    if nathan_chess_game.white_turn:
                        x, y = pygame.mouse.get_pos()
                        x, y = math.floor(x / 100), math.floor(y / 100)
                        if 0 <= x <= 7 and 0 <= y <= 7:
                            if nathan_chess_game.board[x][y].piece != 'none':

                                if nathan_chess_game.white_turn():
                                    can_merge, move = merging.check_merge_white(nathan_chess_game.board, selected_piece,
                                                                                nathan_chess_game.board[x][y])
                                    if can_merge:
                                        move_made = move
                                else:
                                    can_merge, move = merging.check_merge_black(nathan_chess_game.board, selected_piece,
                                                                                nathan_chess_game.board[x][y])
                                    if can_merge:
                                        move_made = move

                    merge_mode = None
                    selected_piece = None

                elif selected_piece == None:
                    x, y = pygame.mouse.get_pos()
                    x, y = math.floor(x / 100), math.floor(y / 100)
                    if 0 <= x <= 7 and 0 <= y <= 7:
                        if nathan_chess_game.board[x][y].is_white == nathan_chess_game.white_turn():
                            if not nathan_chess_game.board[x][y].piece == 'none':
                                selected_piece = nathan_chess_game.board[x][y]
                else:
                    x, y = pygame.mouse.get_pos()
                    x, y = math.floor(x / 100), math.floor(y / 100)
                    if 0 <= x <= 7 and 0 <= 7 <= 7:
                        # Convert

                        move_made = movement.get_selected_move(selected_piece, x, y, nathan_chess_game.board)
            elif m1[2]:
                selected_piece = None
                merge_mode = False
    if move_made:
        selected_piece = None

    return running, move_made, merge_mode
