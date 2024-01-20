import pieces
from pieces import Move
import movement
import merging
import sacrifice

def coord_to_notation(coord):
    hashmap = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}
    return f'{hashmap[coord[0]]}{8 - coord[1]}'


class Game:
    def __init__(self):

        self.last_move = ''

        # Create a 2D list to represent the chess board

        self.board = [[pieces.Piece((x, y), None) for x in range(8)] for y in range(8)]

        for i in range(0, 8):
            self.board[i][1] = pieces.Pion((i, 1), False)
        for i in range(0, 8):
            self.board[i][6] = pieces.Pion((i, 6), True)

        self.i9_piece = None

        self.board[0][7] = pieces.Toren((0, 7), True)
        self.board[7][7] = pieces.Toren((7, 7), True)
        self.board[2][7] = pieces.Loper((2, 7), True)
        self.board[5][7] = pieces.Loper((5, 7), True)
        self.board[4][7] = pieces.Koning((4, 7), True)
        self.board[3][7] = pieces.Dame((3, 7), True)
        self.board[1][7] = pieces.Paard((1, 7), True)
        self.board[6][7] = pieces.Paard((6, 7), True)

        self.board[0][0] = pieces.Toren((0, 0), False)
        self.board[7][0] = pieces.Toren((7, 0), False)
        self.board[2][0] = pieces.Loper((2, 0), False)
        self.board[5][0] = pieces.Loper((5, 0), False)
        self.board[4][0] = pieces.Koning((4, 0), False)
        self.board[3][0] = pieces.Dame((3, 0), False)
        self.board[1][0] = pieces.Paard((1, 0), False)
        self.board[6][0] = pieces.Paard((6, 0), False)
        self.zet_nummer = 1
        self.wit_aan_de_buurt = True

        self.event = ""

        self.has_rikeerd = False

        self.stage = 1
        self.captured_pieces = []

        self.running = True

        self.show_i9 = False
        self.i9_piece = None

        self.wit_sacraficial_pawns = 0
        self.zwart_sacraficial_pawns = 0

        self.zet_nummer = 0
        self.zet_aantal = 0

    def get_piece(self, position) -> pieces.Piece:
        return self.board[position[0]][position[1]]

    def white_turn(self) -> bool:
        return self.wit_aan_de_buurt

    def is_valid_move(self, move: Move) -> bool:

        if move.movement_class == 1:

            print("oi")

            if self.get_piece(move.old_position) != self.white_turn():
                return False

            for row in self.board:
                for piece in row:

                    moves: list = piece.get_available_positions(self.board)

                    for available_move in moves:
                        if move.compare(available_move):
                            return True

        if move.movement_class == 2:

            if self.i9_piece is not None:
                if self.i9_piece.is_white == self.white_turn():
                    if self.get_piece(move.position).piece != "none":
                        return True

        if move.movement_class == 3:
            if self.has_rikeerd:
                return False

            n_k = 0
            n_q = 0
            for x in range(8):
                for y in range(8):
                    if self.board[x][y].is_white == self.white_turn():
                        if self.board[x][y].piece == "koning":
                            n_k += 1
                        if self.board[x][y].piece == "dame":
                            n_q += 1
            if n_k == 1 and n_q == 1:
                return True
        if move.movement_class == 4:
            if self.get_piece(move.position).piece == "koning":
                return True
            if self.get_piece(move.position).piece == "dame":
                return True
            if self.get_piece(move.position).piece == "dameskasteel":
                return True
            if self.get_piece(move.position).piece == "bewoond kasteel":
                return True
        if move.movement_class == 5:
            # Check for merge needs to be updated to use second piece argument instead of mouse x and y

            return True

        return False

    def make_move(self, move: Move):

        # if self.isValidMove(move):
        if True:
            if move.movement_class == 1:
                self.board, last_move, captured_piece, has_moved = movement.move(move, self.board, self.zet_aantal,
                                                                                 self.zet_nummer)
            if move.movement_class == 2:
                self.board[move.position[0]][move.position[1]] = self.i9_piece
                self.board[move.position[0]][move.position[1]].position = move.position
                self.i9_piece = None
            if move.movement_class == 3:
                n_k = 0
                n_q = 0
                king_pos = (-1, -1)
                queen_pos = (-1, -1)
                for x in range(8):
                    for y in range(8):
                        if self.board[x][y].is_white == self.white_turn():
                            if self.board[x][y].piece == "koning":
                                n_k += 1
                                king_pos = (x, y)
                            if self.board[x][y].piece == "dame":
                                n_q += 1
                                queen_pos = (x, y)
                if n_k == 1 and n_q == 1:
                    hp_king = self.board[king_pos[0]][king_pos[1]].hp
                    self.board[king_pos[0]][king_pos[1]].piece = "dame"
                    self.board[king_pos[0]][king_pos[1]].hp = self.board[queen_pos[0]][queen_pos[1]].hp
                    self.board[queen_pos[0]][queen_pos[1]].piece = "koning"
                    self.board[queen_pos[0]][queen_pos[1]].hp = hp_king
                    self.has_rikeerd = True
            if move.movement_class == 4:
                selected_piece = self.get_piece(move.position)
                match selected_piece.piece:
                    case "dame":
                        new_piece = pieces.Koning(selected_piece.position, selected_piece.is_white)
                        new_piece.hp = selected_piece.hp
                        self.board[selected_piece.position[0]][selected_piece.position[1]] = new_piece
                        last_move = f"D{coord_to_notation(new_piece.position)} transitioned K{coord_to_notation(new_piece.position)}"
                        self.zet_nummer += 1
                        print(last_move)
                    case "koning":
                        new_piece = pieces.Dame(selected_piece.position, selected_piece.is_white)
                        new_piece.hp = selected_piece.hp
                        self.board[selected_piece.position[0]][selected_piece.position[1]] = new_piece
                        last_move = f"K{coord_to_notation(new_piece.position)} transitioned D{coord_to_notation(new_piece.position)}"
                        self.zet_nummer += 1
                        print(last_move)
                    case "dameskasteel":
                        new_piece = pieces.BewoondKasteel(selected_piece.position, selected_piece.is_white)
                        new_piece.hp = selected_piece.hp + 3
                        self.board[selected_piece.position[0]][selected_piece.position[1]] = new_piece
                        last_move = f"TQT{coord_to_notation(new_piece.position)} transitioned K{coord_to_notation(new_piece.position)}"
                        self.zet_nummer += 1
                        print(last_move)
                    case "bewoond kasteel":
                        new_piece = pieces.Dameskasteel(selected_piece.position, selected_piece.is_white)
                        new_piece.hp = selected_piece.hp - 3
                        self.board[selected_piece.position[0]][selected_piece.position[1]] = new_piece
                        last_move = f"K{coord_to_notation(new_piece.position)} transitioned Q{coord_to_notation(new_piece.position)}"
                        self.zet_nummer += 1
                        print(last_move)
            if move.movement_class == 5:
                if self.wit_aan_de_buurt:

                    if move.spawn_god:
                        self.i9_piece = pieces.God((-1, -1), True)
                    else:
                        show_god, self.board, merge_text = merging.merge_white(self.board, selected_piece=self.get_piece(
                            move.old_position), second_piece=self.get_piece(move.old_position2))

                else:

                    if move.spawn_god:
                        self.i9_piece = pieces.God((-1, -1), False)
                    else:
                        show_god, self.board, merge_text = merging.merge_black(self.board, selected_piece=self.get_piece(
                            move.old_position), second_piece=self.get_piece(move.old_position2))

            if move.movement_class == 6:
                if self.white_turn():

                    self.board, self.wit_sacraficial_pawns = sacrifice.sacrafice(
                        self.board, self.get_piece(move.position), self.wit_sacraficial_pawns)
                else:
                    self.board, self.zwart_sacraficial_pawns = sacrifice.sacrafice(
                        self.board, self.get_piece(move.position), self.zwart_sacraficial_pawns)

            if move.movement_class == 7:

                if self.white_turn():

                    self.board, self.wit_sacraficial_pawns = sacrifice.channel(
                        self.board, self.get_piece(move.position), self.wit_sacraficial_pawns)
                else:
                    self.board, self.zwart_sacraficial_pawns = sacrifice.channel(
                        self.board, self.get_piece(move.position), self.zwart_sacraficial_pawns)