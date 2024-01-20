import json

"""
Movement Class 1:

Movement type: 1 = Normal Move
Movement type: 2 = Artillery Move
Movement type: 3 = Converting Move
Movement type: 4 = -
Movement type: 5 = Spawn Pawn Move

Done
Movement class: 1 = Just Moving
Movement class: 2 = I9 placing
Movement class: 3 = Rikeren
Movement class: 4 = Transitioning
Movement class: 5 = Merging
Movement class: 6 = Sacraficing
Movement class: 7 = Channeling

To Do:
Lobby System for multiplayer
(Omdat roan klaagt): Main Menu "improvements"
"""


class Move:
    def __init__(self, position=(0, 0), movement_class=1, old_position=(0, 0), old_position2=(0, 0), movement_type=1,
                 french_revolution=False,
                 spawn_piece=None, spawn_god=False, pawns=False) -> None:
        self.movement_class = movement_class

        # movement class 1, 2, 4, 5, 6
        self.position = position

        # movement class 1, 5
        self.old_position = old_position

        # movement class 1
        self.french_revolution = french_revolution

        # movement class 1
        self.movement_type = movement_type

        # movement class 5
        self.old_position2 = old_position2
        self.spawn_god = spawn_god

        # movement class 7
        self.pawns = pawns

    def to_json(self):
        json_text = json.dumps(
            {"movement_class": self.movement_class, "new_posX": self.position[0], "new_posY": self.position[1],
             "old_posX": self.old_position[0], "old_posY": self.old_position[1],
             "old_pos2X": self.old_position2[0], "old_pos2Y": self.old_position2[1],
             "movement_type": self.movement_type,
             "french_revolution": self.french_revolution,
             "spawn_god": self.spawn_god,
             "pawns": self.pawns})

        return json_text

    def from_json(json_text: str):
        decoded_json = json.loads(json_text)

        old_pos = (decoded_json["old_posX"], decoded_json["old_posY"])
        old_pos2 = (decoded_json["old_pos2X"], decoded_json["old_pos2Y"])
        new_pos = (decoded_json["new_posX"], decoded_json["new_posY"])

        movement_type = decoded_json["movement_type"]
        french_revolution = decoded_json["french_revolution"]
        movement_class = decoded_json["movement_class"]
        spawn_god = decoded_json["spawn_god"]
        pawns = decoded_json["pawns"]

        move = Move(old_position=old_pos, old_position2=old_pos2, position=new_pos, movement_type=movement_type,
                    french_revolution=french_revolution, movement_class=movement_class, spawn_god=spawn_god,
                    pawns=pawns)

        return move

    def compare(self, move):
        old_pos_equal = move.old_position[0] == self.old_position[0] and move.old_position[1] == self.old_position[1]
        old_pos_equal = move.old_position2[0] == self.old_position2[0] and move.old_position2[1] == self.old_position2[
            1]
        pos_equal = move.position[0] == self.position[0] and move.position[1] == self.position[1]
        french_revolution_equal = move.french_revolution == self.french_revolution
        movement_type_equal = move.movement_type == self.movement_type
        movement_class_equal = move.movement_class == self.movement_class
        spawn_god_equal = move.spawn_god == self.spawn_god
        pawns_equal = move.pawns == self.pawns

        return old_pos_equal and pos_equal and french_revolution_equal and movement_type_equal and movement_class_equal and spawn_god_equal and pawns_equal


class Piece:
    def __init__(self, position, is_white):
        self.position = position
        self.is_white = is_white
        self.piece = 'none'
        self.notatie = ''
        self.hp = 0
        self.max_hp = 0
        self.damage1 = 1
        self.damage2 = 0.5
        self.boss_piece = False
        self.has_ai = False
        self.boss_damage_bonus = 0
        self.aoe = False
        self.building = False
        self.value = 0
        self.smoll_guy = False
        self.channel_cost = 1
        self.can_channel = False
        self.movement_type = 1

    def get_available_positions(self, board):
        return []

    def on_channel(self, pawns, board):
        return board, False, pawns


class Pion(Piece):
    def __init__(self, position, is_white):
        super().__init__(position, is_white)
        self.piece = 'pion'
        self.notatie = ''
        self.hp = 1
        self.max_hp = 1
        self.is_white = is_white
        self.value = 1

    def get_available_positions(self, board):
        moves = []
        if self.is_white:
            if self.position[1] <= 0:
                return moves
            if board[self.position[0]][self.position[1] - 1].piece == 'none':
                moves.append(Move(position=(self.position[0], self.position[1] - 1)))
            if not self.position[0] >= 7:
                if not board[self.position[0] + 1][self.position[1] - 1].piece == 'none':
                    if not board[self.position[0] + 1][self.position[1] - 1].is_white:
                        moves.append(Move(position=(self.position[0] + 1, self.position[1] - 1)))
            if not self.position[0] <= 0:
                if not board[self.position[0] - 1][self.position[1] - 1].piece == 'none':
                    if not board[self.position[0] - 1][self.position[1] - 1].is_white:
                        moves.append(Move(position=(self.position[0] - 1, self.position[1] - 1)))
        else:
            if self.position[1] >= 7:
                return moves
            if board[self.position[0]][self.position[1] + 1].piece == 'none':
                moves.append(Move(position=(self.position[0], self.position[1] + 1)))
            if not self.position[0] >= 7:
                if not board[self.position[0] + 1][self.position[1] + 1].piece == 'none':
                    if board[self.position[0] + 1][self.position[1] + 1].is_white:
                        moves.append(Move(position=(self.position[0] + 1, self.position[1] + 1)))
            if not self.position[0] <= 0:
                if not board[self.position[0] - 1][self.position[1] + 1].piece == 'none':
                    if board[self.position[0] - 1][self.position[1] + 1].is_white:
                        moves.append(Move(position=(self.position[0] - 1, self.position[1] + 1)))
        return moves


class PionT2(Pion):
    def __init__(self, position, is_white):
        super().__init__(position, is_white)
        self.piece = 'pionT2'
        self.notatie = ''
        self.max_hp = 2
        self.hp = 2
        self.movement_type = 1
        self.damage1 = 1.75
        self.value = 2


class Koning(Piece):
    def __init__(self, position, is_white):
        super().__init__(position, is_white)
        self.piece = 'koning'
        self.notatie = 'K'
        self.hp = 5
        self.max_hp = 5
        self.movement_type = 1
        self.damage1 = 2.25
        self.value = 5

    def get_available_positions(self, board):
        moves = []
        # up
        if self.position[1] != 7:
            if board[self.position[0]][self.position[1] + 1].is_white != self.is_white or board[self.position[0]][
                self.position[1] + 1].piece == 'none':
                moves.append(Move(position=(self.position[0], self.position[1] + 1)))
        # down
        if self.position[1] != 0:
            if board[self.position[0]][self.position[1] - 1].is_white != self.is_white or board[self.position[0]][
                self.position[1] - 1].piece == 'none':
                moves.append(Move(position=(self.position[0], self.position[1] - 1)))
        # left
        if self.position[0] != 0:
            if board[self.position[0] - 1][self.position[1]].is_white != self.is_white or board[self.position[0] - 1][
                self.position[1]].piece == 'none':
                moves.append(Move(position=(self.position[0] - 1, self.position[1])))
        # right
        if self.position[0] != 7:
            if board[self.position[0] + 1][self.position[1]].is_white != self.is_white or board[self.position[0] + 1][
                self.position[1]].piece == 'none':
                moves.append(Move(position=(self.position[0] + 1, self.position[1])))
        # right-up
        if self.position[0] != 7 and self.position[1] != 7:
            if board[self.position[0] + 1][self.position[1] + 1].is_white != self.is_white or \
                    board[self.position[0] + 1][self.position[1] + 1].piece == 'none':
                moves.append(Move(position=(self.position[0] + 1, self.position[1] + 1)))
        # right-down
        if self.position[0] != 7 and self.position[1] != 0:
            if board[self.position[0] + 1][self.position[1] - 1].is_white != self.is_white or \
                    board[self.position[0] + 1][self.position[1] - 1].piece == 'none':
                moves.append(Move(position=(self.position[0] + 1, self.position[1] - 1)))
        # left-up
        if self.position[0] != 0 and self.position[1] != 7:
            if board[self.position[0] - 1][self.position[1] + 1].is_white != self.is_white or \
                    board[self.position[0] - 1][self.position[1] + 1].piece == 'none':
                moves.append(Move(position=(self.position[0] - 1, self.position[1] + 1)))
        # left-down
        if self.position[0] != 0 and self.position[1] != 0:
            if board[self.position[0] - 1][self.position[1] - 1].is_white != self.is_white or \
                    board[self.position[0] - 1][self.position[1] - 1].piece == 'none':
                moves.append(Move(position=(self.position[0] - 1, self.position[1] - 1)))
        return moves


class PionT3(Koning):
    def __init__(self, position, is_white):
        super().__init__(position, is_white)
        self.piece = 'pionT3'
        self.notatie = ''
        self.max_hp = 4
        self.hp = 4
        self.movement_type = 1
        self.damage1 = 2.25
        self.value = 3


class PionT4(Piece):
    def __init__(self, position, is_white):
        super().__init__(position, is_white)
        self.piece = 'pionT4'
        self.notatie = ''
        self.hp = 8
        self.max_hp = 8
        self.damage1 = 3
        self.boss_piece = True
        self.value = 4

    def get_available_positions(self, board):

        moves = []

        for x in range(self.position[0] - 2, self.position[0] + 3):
            for y in range(self.position[1] - 2, self.position[1] + 3):
                if 0 <= x <= 7 and 0 <= y <= 7:
                    if board[x][y].is_white != self.is_white:
                        moves.append(Move(position=(x, y), movement_type=5, spawn_piece=Pion))

        return moves


class PionT5(Piece):
    def __init__(self, position, is_white):
        super().__init__(position, is_white)
        self.piece = 'pionT5'
        self.notatie = ''
        self.hp = 16
        self.max_hp = 16
        self.damage1 = 3.5
        self.boss_piece = True
        self.value = 5

    def get_available_positions(self, board):

        moves = []

        for x in range(self.position[0] - 2, self.position[0] + 3):
            for y in range(self.position[1] - 2, self.position[1] + 3):
                if 0 <= x <= 7 and 0 <= y <= 7:
                    if board[x][y].is_white != self.is_white:
                        moves.append(Move(position=(x, y), movement_type=5, spawn_piece=PionT2))

        return moves


class PionT128(Piece):
    def __init__(self, position, is_white):
        super().__init__(position, is_white)
        self.piece = 'pionT128'
        self.notatie = 'hacker'
        self.hp = 80000
        self.max_hp = 80000
        self.damage1 = 3000
        self.boss_piece = True
        self.value = 128

    def get_available_positions(self, board):
        moves = []
        for x in range(self.position[0] - 2, self.position[0] + 3):
            for y in range(self.position[1] - 2, self.position[1] + 3):
                if 0 <= x <= 7 and 0 <= y <= 7:
                    if board[x][y].is_white != self.is_white:
                        moves.append(Move(position=(x, y)))
        return moves


class Loper(Piece):
    def __init__(self, position, is_white) -> None:
        super().__init__(position, is_white)
        self.piece = 'loper'
        self.notatie = 'L'
        self.hp = 3
        self.max_hp = 3
        self.is_white = is_white
        self.value = 2
        self.can_channel = True
        self.channel_cost = 4

    def get_available_positions(self, board):
        moves = []
        for i in range(self.position[0] + 1, 8):
            if self.position[1] + (i - self.position[0]) < 0:
                break
            if self.position[1] + (i - self.position[0]) > 7:
                break
            if not board[i][self.position[1] + (i - self.position[0])].piece == 'none':
                if not board[i][self.position[1] + (i - self.position[0])].is_white == self.is_white:
                    moves.append(Move(position=(i, self.position[1] + (i - self.position[0]))))
                    # this looks like a bug but its called "passer du Loper"
                    break
            moves.append(Move(position=(i, self.position[1] + (i - self.position[0]))))
        for i in range(self.position[0] + 1, 8):
            if self.position[1] - (i - self.position[0]) > 7:
                break
            if self.position[1] - (i - self.position[0]) < 0:
                break
            if not board[i][self.position[1] - (i - self.position[0])].piece == 'none':
                if not board[i][self.position[1] - (i - self.position[0])].is_white == self.is_white:
                    moves.append(Move(position=(i, self.position[1] - (i - self.position[0]))))
                break
            moves.append(Move(position=(i, self.position[1] - (i - self.position[0]))))
        for i in range(self.position[0] - 1, -1, -1):
            if self.position[1] + (i - self.position[0]) < 0:
                break
            if self.position[1] + (i - self.position[0]) > 7:
                break
            if not board[i][self.position[1] + (i - self.position[0])].piece == 'none':
                if not board[i][self.position[1] + (i - self.position[0])].is_white == self.is_white:
                    moves.append(Move(position=(i, self.position[1] + (i - self.position[0]))))
                break
            moves.append(Move(position=(i, self.position[1] + (i - self.position[0]))))
        for i in range(self.position[0] - 1, -1, -1):
            if self.position[1] - (i - self.position[0]) > 7:
                break
            if self.position[1] - (i - self.position[0]) < 0:
                break
            if not board[i][self.position[1] - (i - self.position[0])].piece == 'none':
                if not board[i][self.position[1] - (i - self.position[0])].is_white == self.is_white:
                    moves.append(Move(position=(i, self.position[1] - (i - self.position[0]))))
                break
            moves.append(Move(position=(i, self.position[1] - (i - self.position[0]))))

        return moves

    def on_channel(self, pawns, board):
        if pawns > 4:
            board[self.position[0]][self.position[1]] = Renner(self)

            return board, False, 0

        return board, False, pawns


class Toren(Piece):
    def __init__(self, position, is_white):
        super().__init__(position, is_white)
        self.piece = 'toren'
        self.is_white = is_white
        self.notatie = 'T'
        self.hp = 4
        self.max_hp = 4
        self.movement_type = 1
        self.damage1 = 1.5
        self.value = 2

    def get_available_positions(self, board):
        moves = []
        for i in range(self.position[0] + 1, 8):
            if not board[i][self.position[1]].piece == 'none':
                if not board[i][self.position[1]].is_white == self.is_white:
                    moves.append(Move(position=(i, self.position[1])))
                break
            moves.append(Move(position=(i, self.position[1])))
        for i in range(self.position[0] - 1, -1, -1):
            if not board[i][self.position[1]].piece == 'none':
                if not board[i][self.position[1]].is_white == self.is_white:
                    moves.append(Move(position=(i, self.position[1])))
                break
            moves.append(Move(position=(i, self.position[1])))
        for i in range(self.position[1] + 1, 8):
            if not board[self.position[0]][i].piece == 'none':
                if not board[self.position[0]][i].is_white == self.is_white:
                    moves.append(Move(position=(self.position[0], i)))
                break
            moves.append(Move(position=(self.position[0], i)))
        for i in range(self.position[1] - 1, -1, -1):
            if not board[self.position[0]][i].piece == 'none':
                if not board[self.position[0]][i].is_white == self.is_white:
                    moves.append(Move(position=(self.position[0], i)))
                break
            moves.append(Move(position=(self.position[0], i)))
        if not self.position[0] <= 0 and not self.position[1] <= 0:
            if not board[self.position[0] - 1][self.position[1] - 1].piece == 'none':
                if board[self.position[0] - 1][self.position[1] - 1].is_white == self.is_white:
                    moves.append(Move(position=(self.position[0] - 1, self.position[1] - 1)))
        return moves


class Dame(Piece):
    def __init__(self, position, is_white):
        super().__init__(position, is_white)
        self.piece = 'dame'
        self.notatie = 'D'
        self.hp = 5
        self.max_hp = 5
        self.is_white = is_white
        self.movement_type = 1
        self.damage1 = 1.25
        self.value = 5

    def get_available_positions(self, board):
        moves = []
        for i in range(self.position[0] + 1, 8):
            if not board[i][self.position[1]].piece == 'none':
                if not board[i][self.position[1]].is_white == self.is_white:
                    moves.append(Move(position=(i, self.position[1])))
                break
            moves.append(Move(position=(i, self.position[1])))
        for i in range(self.position[0] - 1, -1, -1):
            if not board[i][self.position[1]].piece == 'none':
                if not board[i][self.position[1]].is_white == self.is_white:
                    moves.append(Move(position=(i, self.position[1])))
                break
            moves.append(Move(position=(i, self.position[1])))
        for i in range(self.position[1] + 1, 8):
            if not board[self.position[0]][i].piece == 'none':
                if not board[self.position[0]][i].is_white == self.is_white:
                    moves.append(Move(position=(self.position[0], i)))
                break
            moves.append(Move(position=(self.position[0], i)))
        for i in range(self.position[1] - 1, -1, -1):
            if not board[self.position[0]][i].piece == 'none':
                if not board[self.position[0]][i].is_white == self.is_white:
                    moves.append(Move(position=(self.position[0], i)))
                break
            moves.append(Move(position=(self.position[0], i)))
        if not self.position[0] <= 0 and not self.position[1] <= 0:
            if not board[self.position[0] - 1][self.position[1] - 1].piece == 'none':
                if board[self.position[0] - 1][self.position[1] - 1].is_white == self.is_white:
                    moves.append(Move(position=(self.position[0] - 1, self.position[1] - 1)))
        for i in range(self.position[0] + 1, 8):
            if self.position[1] + (i - self.position[0]) < 0:
                break
            if self.position[1] + (i - self.position[0]) > 7:
                break
            if not board[i][self.position[1] + (i - self.position[0])].piece == 'none':
                if not board[i][self.position[1] + (i - self.position[0])].is_white == self.is_white:
                    moves.append(Move(position=(i, self.position[1] + (i - self.position[0]))))
                    # this looks like a bug but its called "passer de la Dame"
                    break
            moves.append(Move(position=(i, self.position[1] + (i - self.position[0]))))
        for i in range(self.position[0] + 1, 8):
            if self.position[1] - (i - self.position[0]) > 7:
                break
            if self.position[1] - (i - self.position[0]) < 0:
                break
            if not board[i][self.position[1] - (i - self.position[0])].piece == 'none':
                if not board[i][self.position[1] - (i - self.position[0])].is_white == self.is_white:
                    moves.append(Move(position=(i, self.position[1] - (i - self.position[0]))))
                break
            moves.append(Move(position=(i, self.position[1] - (i - self.position[0]))))
        for i in range(self.position[0] - 1, -1, -1):
            if self.position[1] + (i - self.position[0]) < 0:
                break
            if self.position[1] + (i - self.position[0]) > 7:
                break
            if not board[i][self.position[1] + (i - self.position[0])].piece == 'none':
                if not board[i][self.position[1] + (i - self.position[0])].is_white == self.is_white:
                    moves.append(Move(position=(i, self.position[1] + (i - self.position[0]))))
                break
            moves.append(Move(position=(i, self.position[1] + (i - self.position[0]))))
        for i in range(self.position[0] - 1, -1, -1):
            if self.position[1] - (i - self.position[0]) > 7:
                break
            if self.position[1] - (i - self.position[0]) < 0:
                break
            if not board[i][self.position[1] - (i - self.position[0])].piece == 'none':
                if not board[i][self.position[1] - (i - self.position[0])].is_white == self.is_white:
                    moves.append(Move(position=(i, self.position[1] - (i - self.position[0]))))
                break
            moves.append(Move(position=(i, self.position[1] - (i - self.position[0]))))
        return moves


class Paard(Piece):
    def __init__(self, position, is_white):
        super().__init__(position, is_white)
        self.piece = 'paard'
        self.notatie = 'P'
        self.hp = 2.5
        self.max_hp = 2.5
        self.is_white = is_white
        self.movement_type = 1
        self.damage1 = 1
        self.value = 2
        self.snor = False

    def get_available_positions(self, board):
        moves = []
        x = self.position[0]
        y = self.position[1]
        n, m = len(board), len(board[0])

        for i, j in [(x + 2, y + 1), (x + 2, y - 1), (x - 2, y + 1), (x - 2, y - 1),
                     (x + 1, y + 2), (x + 1, y - 2), (x - 1, y + 2), (x - 1, y - 2)]:
            if 0 <= i < n and 0 <= j < m:
                if not board[i][j].piece == "none":
                    if not board[i][j].is_white == self.is_white:
                        moves.append(Move(position=(i, j)))
                    continue
                moves.append(Move(position=(i, j)))
        return moves


class HIMAR(Piece):
    def __init__(self, position, is_white):
        super().__init__(position, is_white)
        self.movement_type = 2
        self.hp = 2.5
        self.max_hp = 2.5
        self.piece = "HIMAR"
        self.notatie = "HIMAR"
        self.is_white = is_white
        self.damage1 = 1
        self.damage2 = 0.75
        self.value = 3

    def get_available_positions(self, board):
        moves = []

        # up
        if self.position[1] != 7:
            if board[self.position[0]][self.position[1] + 1].piece == 'none':
                moves.append(Move(position=(self.position[0], self.position[1] + 1), movement_type=1))
        # down
        if self.position[1] != 0:
            if board[self.position[0]][self.position[1] - 1].piece == 'none':
                moves.append(Move(position=(self.position[0], self.position[1] - 1), movement_type=1))
        # left
        if self.position[0] != 0:
            if board[self.position[0] - 1][self.position[1]].piece == 'none':
                moves.append(Move(position=(self.position[0] - 1, self.position[1]), movement_type=1))
        # right
        if self.position[0] != 7:
            if board[self.position[0] + 1][self.position[1]].piece == 'none':
                moves.append(Move(position=(self.position[0] + 1, self.position[1]), movement_type=1))

        for i in range(0, 8):
            for j in range(0, 8):
                piece = board[i][j]
                if piece.piece != 'none' and piece.piece != 'koning' and piece.piece != 'HIMAR' and piece.piece != 'NBRF':
                    if not piece.is_white == self.is_white:
                        moves.append(Move(position=(i, j), movement_type=2))
        return moves


class Paus(Loper):
    def __init__(self, position, is_white) -> None:
        super().__init__(position, is_white)
        self.hp = 4
        self.max_hp = 4
        self.piece = "paus"
        self.notatie = "PAUS"
        self.is_white = is_white
        self.damage1 = 0.75
        self.boss_damage_bonus = 0.25
        self.value = 3

    def get_available_positions(self, board):
        moves = super().get_available_positions(board)
        for move in moves:
            move.movemnent_type = 3
        return moves


class Ruiter(Paard):
    def __init__(self, position, is_white):
        super().__init__(position, is_white)
        self.hp = 3.5
        self.max_hp = 3.5
        self.piece = "ruiter"
        self.notatie = "R"
        self.is_white = is_white
        self.damage1 = 1.25
        self.value = 3

    def get_available_positions(self, board):
        moves = super().get_available_positions(board)
        for i in [(self.position[0] + 2, self.position[1]), (self.position[0] - 2, self.position[1]),
                  (self.position[0], self.position[1] + 2), (self.position[0], self.position[1] - 2)]:
            if 0 <= i[0] <= 7 and 0 <= i[1] <= 7:
                if not board[i[0]][i[1]].piece == 'none' and not board[i[0]][i[1]].is_white == self.is_white:
                    moves.append(Move(position=i))
        return moves


class NBRF(Dame):
    def __init__(self, position, is_white) -> None:
        super().__init__(position, is_white)
        self.hp = 10
        self.max_hp = 10
        self.piece = "NBRF"
        self.notatie = "NBRF"
        self.is_white = is_white
        self.damage1 = 2.25
        self.boss_piece = True
        self.value = 5

    def get_available_positions(self, board):
        return super().get_available_positions(board)


class Kasteel(Piece):
    def __init__(self, position, is_white):
        super().__init__(position, is_white)
        self.boss_piece = True
        self.hp = 10
        self.max_hp = 10
        self.piece = "Kasteel"
        self.notatie = "T□T"
        self.is_white = is_white
        self.damage1 = 1.75
        self.damage2 = 1.5
        self.value = 4

    def get_available_positions(self, board):
        moves = []
        for i in range(self.position[0] + 1, 8):
            if not board[i][self.position[1]].piece == 'none':
                if not board[i][self.position[1]].is_white == self.is_white:
                    moves.append(Move(position=(i, self.position[1])))
                break
            moves.append(Move(position=(i, self.position[1])))
        for i in range(self.position[0] - 1, -1, -1):
            if not board[i][self.position[1]].piece == 'none':
                if not board[i][self.position[1]].is_white == self.is_white:
                    moves.append(Move(position=(i, self.position[1])))
                break
            moves.append(Move(position=(i, self.position[1])))
        for i in range(self.position[1] + 1, 8):
            if not board[self.position[0]][i].piece == 'none':
                if not board[self.position[0]][i].is_white == self.is_white:
                    moves.append(Move(position=(self.position[0], i)))
                break
            moves.append(Move(position=(self.position[0], i)))
        for i in range(self.position[1] - 1, -1, -1):
            if not board[self.position[0]][i].piece == 'none':
                if not board[self.position[0]][i].is_white == self.is_white:
                    moves.append(Move(position=(self.position[0], i)))
                break
            moves.append(Move(position=(self.position[0], i)))
        if not self.position[0] <= 0 and not self.position[1] <= 0:
            if not board[self.position[0] - 1][self.position[1] - 1].piece == 'none':
                if board[self.position[0] - 1][self.position[1] - 1].is_white:
                    moves.append(Move(position=(self.position[0] - 1, self.position[1] - 1)))
        for x in range(self.position[0] - 2, self.position[0] + 3):
            for y in range(self.position[1] - 2, self.position[1] + 3):
                if 0 <= x <= 7 and 0 <= y <= 7:
                    if board[x][y].piece != 'none' and board[x][y].is_white != self.is_white:
                        moves.append(Move(position=(x, y), movement_type=2))
        return moves


class BewoondKasteel(Kasteel):
    def __init__(self, position, is_white):
        super().__init__(position, is_white)
        self.hp = 12
        self.max_hp = 12
        self.damage1 = 1.75
        self.damage2 = 1.5
        self.piece = 'bewoond kasteel'
        self.notatie = 'TkT'
        self.value = 5


class Dameskasteel(Kasteel):
    def __init__(self, position, is_white):
        super().__init__(position, is_white)
        self.hp = 9
        self.max_hp = 9
        self.damage1 = 2.25
        self.damage2 = 2
        self.piece = 'dameskasteel'
        self.notatie = 'TdT'
        self.value = 5


class LGBTQIA2SplusKasteel(Kasteel):
    def __init__(self, position, is_white):
        super().__init__(position, is_white)
        self.hp = 12
        self.max_hp = 12
        self.damage1 = 2.25
        self.damage2 = 2
        self.piece = 'LGBTQIA2S+Kasteel'
        self.notatie = 'TnbrfT'
        self.value = 5


class Tank(Piece):
    def __init__(self, position, is_white) -> None:
        super().__init__(position, is_white)
        self.piece = "Tank"
        self.notatie = "TANK"
        self.hp = 5
        self.max_hp = 5
        self.damage1 = 2
        self.damage2 = 1.5
        self.boss_damage_bonus = 1
        self.movement_type = 2
        self.value = 3

    def get_available_positions(self, board):
        moves = []
        for x in range(self.position[0] - 2, self.position[0] + 3):
            for y in range(self.position[1] - 2, self.position[1] + 3):
                if 0 <= x <= 7 and 0 <= y <= 7:
                    if board[x][y].is_white != self.is_white:
                        moves.append(Move(position=(x, y)))
        for x in range(self.position[0] - 3, self.position[0] + 4):
            for y in range(self.position[1] - 3, self.position[1] + 4):
                if 0 <= x <= 7 and 0 <= y <= 7:
                    if board[x][y].is_white != self.is_white and board[x][y].piece != 'none' and board[x][
                        y].piece != 'koning':
                        moves.append(Move(position=(x, y), movement_type=2))
        return moves


class Apostel(Paus):
    def __init__(self, position, is_white) -> None:
        super().__init__(position, is_white)
        self.hp = 5
        self.max_hp = 5
        self.piece = "Apostel"
        self.notatie = "A"
        self.is_white = is_white
        self.damage1 = 1.25
        self.boss_damage_bonus = 0.25
        self.value = 3

    def get_available_positions(self, board):
        return super().get_available_positions(board)


class Jezus(Apostel):
    def __init__(self, position, is_white) -> None:
        super().__init__(position, is_white)
        self.hp = 6
        self.max_hp = 6
        self.piece = "Jezus"
        self.notatie = "J"
        self.is_white = is_white
        self.damage1 = 1.75
        self.boss_damage_bonus = 0.25
        self.value = 4

    def get_available_positions(self, board):
        return super().get_available_positions(board)


class God(Jezus):
    def __init__(self, position, is_white) -> None:
        super().__init__(position, is_white)
        self.hp = 10
        self.max_hp = 10
        self.piece = "God"
        self.notatie = "G"
        self.is_white = is_white
        self.damage1 = 2.25
        self.boss_damage_bonus = 0.25
        self.boss_piece = True
        self.value = 5

    def get_available_positions(self, board):
        moves = []

        # up
        if self.position[1] != 7:
            if board[self.position[0]][self.position[1] + 1].is_white != self.is_white or board[self.position[0]][
                self.position[1] + 1].piece == 'none':
                moves.append(Move(position=(self.position[0], self.position[1] + 1), movement_type=3))
        # down
        if self.position[1] != 0:
            if board[self.position[0]][self.position[1] - 1].is_white != self.is_white or board[self.position[0]][
                self.position[1] - 1].piece == 'none':
                moves.append(Move(position=(self.position[0], self.position[1] - 1), movement_type=3))
        # left
        if self.position[0] != 0:
            if board[self.position[0] - 1][self.position[1]].is_white != self.is_white or board[self.position[0] - 1][
                self.position[1]].piece == 'none':
                moves.append(Move(position=(self.position[0] - 1, self.position[1]), movement_type=3))
        # right
        if self.position[0] != 7:
            if board[self.position[0] + 1][self.position[1]].is_white != self.is_white or board[self.position[0] + 1][
                self.position[1]].piece == 'none':
                moves.append(Move(position=(self.position[0] + 1, self.position[1]), movement_type=3))
        # right-up
        if self.position[0] != 7 and self.position[1] != 7:
            if board[self.position[0] + 1][self.position[1] + 1].is_white != self.is_white or \
                    board[self.position[0] + 1][self.position[1] + 1].piece == 'none':
                moves.append(Move(position=(self.position[0] + 1, self.position[1] + 1), movement_type=3))
        # right-down
        if self.position[0] != 7 and self.position[1] != 0:
            if board[self.position[0] + 1][self.position[1] - 1].is_white != self.is_white or \
                    board[self.position[0] + 1][self.position[1] - 1].piece == 'none':
                moves.append(Move(position=(self.position[0] + 1, self.position[1] - 1), movement_type=3))
        # left-up
        if self.position[0] != 0 and self.position[1] != 7:
            if board[self.position[0] - 1][self.position[1] + 1].is_white != self.is_white or \
                    board[self.position[0] - 1][self.position[1] + 1].piece == 'none':
                moves.append(Move(position=(self.position[0] - 1, self.position[1] + 1), movement_type=3))
        # left-down
        if self.position[0] != 0 and self.position[1] != 0:
            if board[self.position[0] - 1][self.position[1] - 1].is_white != self.is_white or \
                    board[self.position[0] - 1][self.position[1] - 1].piece == 'none':
                moves.append(Move(position=(self.position[0] - 1, self.position[1] - 1), movement_type=3))
        return moves + super().get_available_positions(board)


class ICBM_Missle_Launcher(HIMAR):
    def __init__(self, position, is_white):
        super().__init__(position, is_white)
        self.max_hp = 3
        self.hp = 3
        self.damage1 = 1
        self.damage2 = 2.0
        self.boss_damage_bonus = 1
        self.piece = 'ICBM missle launcher'
        self.notatie = 'ICBMml'
        self.movement_type = 2
        self.value = 4


class Railgun(HIMAR):
    def __init__(self, position, is_white):
        super().__init__(position, is_white)
        self.hp = 3
        self.max_hp = 3
        self.damage1 = 1.25
        self.damage2 = 1.5
        self.boss_damage_bonus = 0.5
        self.piece = 'Railgun'
        self.notatie = 'RG'
        self.value = 3


class Soldier(PionT3):
    def __init__(self, position, is_white):
        super().__init__(position, is_white)
        self.notatie = "Sol"
        self.piece = "soldier"
        self.value = 1
        self.hp = 3
        self.max_hp = 3
        self.damage1 = 1.5


class SecretAgent(PionT4):
    def __init__(self, position, is_white):
        super().__init__(position, is_white)

        self.hp = 4
        self.max_hp = 4
        self.piece = "secret agent"
        self.notatie = "S E"
        self.value = 3
        self.damage1 = 1.75
        self.boss_piece = False

        self.value = 1


class AttackHelikopter(Piece):
    def __init__(self, position, is_white):
        super().__init__(position, is_white)
        self.damage1 = 2
        self.damage2 = 2
        self.hp = 4
        self.max_hp = 4
        self.piece = "helicopter"
        self.notatie = "He"
        self.boss_damage_bonus = 1
        self.value = 3

    def get_available_positions(self, board):

        moves = []

        for x in range(self.position[0] - 3, self.position[0] + 4):
            for y in range(self.position[1] - 3, self.position[1] + 4):
                if 0 <= x <= 7 and 0 <= y <= 7:
                    if board[x][y].piece == 'none':
                        moves.append(Move(position=(x, y), movement_type=1))

        for x in range(self.position[0] - 3, self.position[0] + 4):
            for y in range(self.position[1] - 3, self.position[1] + 4):
                if 0 <= x <= 7 and 0 <= y <= 7:
                    if board[x][y].piece != 'none' and board[x][y].is_white != self.is_white:
                        moves.append(Move(position=(x, y), movement_type=2))

        return moves


class Lenin(Piece):
    def __init__(self, position, is_white):
        super().__init__(position, is_white)

        self.hp = 15
        self.max_hp = 15
        self.boss_piece = True
        self.damage1 = 2.25
        self.notatie = "Le"
        self.piece = "Lenin"
        self.value = 5
        self.channel_cost = 2
        self.can_channel = True
        self.upgrade_level = 0

    def get_available_positions(self, board):
        moves = []
        for i in range(self.position[0] + 1, 8):
            if not board[i][self.position[1]].piece == 'none':
                if not board[i][self.position[1]].is_white == self.is_white:
                    moves.append(Move(position=(i, self.position[1])))
                break
            moves.append(Move(position=(i, self.position[1])))
        for i in range(self.position[0] - 1, -1, -1):
            if not board[i][self.position[1]].piece == 'none':
                if not board[i][self.position[1]].is_white == self.is_white:
                    moves.append(Move(position=(i, self.position[1])))
                break
            moves.append(Move(position=(i, self.position[1])))
        for i in range(self.position[1] + 1, 8):
            if not board[self.position[0]][i].piece == 'none':
                if not board[self.position[0]][i].is_white == self.is_white:
                    moves.append(Move(position=(self.position[0], i)))
                break
            moves.append(Move(position=(self.position[0], i)))
        for i in range(self.position[1] - 1, -1, -1):
            if not board[self.position[0]][i].piece == 'none':
                if not board[self.position[0]][i].is_white == self.is_white:
                    moves.append(Move(position=(self.position[0], i)))
                break
            moves.append(Move(position=(self.position[0], i)))
        if not self.position[0] <= 0 and not self.position[1] <= 0:
            if not board[self.position[0] - 1][self.position[1] - 1].piece == 'none':
                if board[self.position[0] - 1][self.position[1] - 1].is_white == self.is_white:
                    moves.append(Move(position=(self.position[0] - 1, self.position[1] - 1)))
        for i in range(self.position[0] + 1, 8):
            if self.position[1] + (i - self.position[0]) < 0:
                break
            if self.position[1] + (i - self.position[0]) > 7:
                break
            if not board[i][self.position[1] + (i - self.position[0])].piece == 'none':
                if not board[i][self.position[1] + (i - self.position[0])].is_white == self.is_white:
                    moves.append(Move(position=(i, self.position[1] + (i - self.position[0]))))
                    # this looks like a bug but its called "passer de la Dame"
                    break
            moves.append(Move(position=(i, self.position[1] + (i - self.position[0]))))
        for i in range(self.position[0] + 1, 8):
            if self.position[1] - (i - self.position[0]) > 7:
                break
            if self.position[1] - (i - self.position[0]) < 0:
                break
            if not board[i][self.position[1] - (i - self.position[0])].piece == 'none':
                if not board[i][self.position[1] - (i - self.position[0])].is_white == self.is_white:
                    moves.append(Move(position=(i, self.position[1] - (i - self.position[0]))))
                break
            moves.append(Move(position=(i, self.position[1] - (i - self.position[0]))))
        for i in range(self.position[0] - 1, -1, -1):
            if self.position[1] + (i - self.position[0]) < 0:
                break
            if self.position[1] + (i - self.position[0]) > 7:
                break
            if not board[i][self.position[1] + (i - self.position[0])].piece == 'none':
                if not board[i][self.position[1] + (i - self.position[0])].is_white == self.is_white:
                    moves.append(Move(position=(i, self.position[1] + (i - self.position[0]))))
                break
            moves.append(Move(position=(i, self.position[1] + (i - self.position[0]))))
        for i in range(self.position[0] - 1, -1, -1):
            if self.position[1] - (i - self.position[0]) > 7:
                break
            if self.position[1] - (i - self.position[0]) < 0:
                break
            if not board[i][self.position[1] - (i - self.position[0])].piece == 'none':
                if not board[i][self.position[1] - (i - self.position[0])].is_white == self.is_white:
                    moves.append(Move(position=(i, self.position[1] - (i - self.position[0]))))
                break
            moves.append(Move(position=(i, self.position[1] - (i - self.position[0]))))
        x = self.position[0]
        y = self.position[1]
        n, m = len(board), len(board[0])

        for i, j in [(x + 2, y + 1), (x + 2, y - 1), (x - 2, y + 1), (x - 2, y - 1),
                     (x + 1, y + 2), (x + 1, y - 2), (x - 1, y + 2), (x - 1, y - 2)]:
            if 0 <= i < n and 0 <= j < m:
                if not board[i][j].piece == "none":
                    if not board[i][j].is_white == self.is_white:
                        moves.append(Move(position=(i, j)))
                    continue
                moves.append(Move(position=(i, j)))
        return moves

    def on_channel(self, pawns, board: list[list[Piece]]):

        if self.upgrade_level > 4:
            return board, False, pawns

        match self.upgrade_level:
            case 0:
                if pawns < 2:
                    return board, False, pawns
                else:
                    self.channel_cost = 2
                    pawns -= 2
            case 1:
                if pawns < 2:
                    return board, False, pawns
                else:
                    self.channel_cost = 4
                    pawns -= 2
            case 2:
                if pawns < 4:
                    return board, False, pawns
                else:
                    self.channel_cost = 5
                    pawns -= 4
            case 3:
                if pawns < 5:
                    return board, False, pawns
                else:
                    self.channel_cost = 4
                    pawns -= 5
            case 4:
                if pawns < 4:
                    return board, False, pawns
                else:
                    pawns -= 4

        self.upgrade_level += 1

        match self.upgrade_level:

            case 1:
                for i in range(8):
                    for j in range(8):
                        if board[i][j].piece == "peasant":
                            new_piece = Soldier((i, j), self.is_white)
                            new_piece.hp = board[i][j].hp / board[i][j].max_hp * new_piece.max_hp
                            board[i][j] = new_piece
            case 2:
                for i in range(8):
                    for j in range(8):
                        if board[i][j].piece == "soldier":
                            new_piece = SecretAgent((i, j), self.is_white)
                            new_piece.hp = board[i][j].hp / board[i][j].max_hp * new_piece.max_hp
                            board[i][j] = new_piece
            case 3:
                for i in range(8):
                    for j in range(8):
                        if board[i][j].piece == "secret agent":
                            new_piece = Tank((i, j), self.is_white)
                            new_piece.hp = board[i][j].hp / board[i][j].max_hp * new_piece.max_hp
                            new_piece.value = 1
                            board[i][j] = new_piece
            case 4:
                for i in range(8):
                    for j in range(8):
                        if board[i][j].piece == "Tank":
                            new_piece = AttackHelikopter((i, j), self.is_white)
                            new_piece.hp = board[i][j].hp / board[i][j].max_hp * new_piece.max_hp
                            new_piece.value = 1
                            board[i][j] = new_piece
            case 5:
                board = self.upgrade_self(board)
                self.can_channel = False

        return board, True, pawns

    def upgrade_self(self, board):

        self.piece = "Lenin Prime"
        self.notatie = "LePr"
        self.hp += 4
        self.max_hp += 4
        self.damage1 += 0.5

        return board


class Peasant(PionT2):
    def __init__(self, position, is_white):
        super().__init__(position, is_white)
        self.notatie = "Pea"
        self.piece = "peasant"
        self.value = 1


class Stalin(Lenin):
    def __init__(self, position, is_white):
        super().__init__(position, is_white)
        self.hp = 18
        self.max_hp = 18
        self.boss_piece = True
        self.damage1 = 2.5
        self.notatie = "St"
        self.piece = "Stalin"

    def upgrade_self(self, board):
        self.piece = "Stalin Prime"
        self.hp += 4
        self.max_hp += 4
        self.damage1 += 0.5
        self.notatie = "StPr"

        return board


class JoeBiden(Piece):
    def __init__(self, position, is_white):
        super().__init__(position, is_white)
        self.hp = 14
        self.max_hp = 14
        self.boss_piece = True
        self.damage1 = 2.25
        self.notatie = "Jb"
        self.piece = "Joe Biden"
        self.value = 5

    def get_available_positions(self, board):
        moves = []
        for i in range(self.position[0] + 1, 8):
            if not board[i][self.position[1]].piece == 'none':
                if not board[i][self.position[1]].is_white == self.is_white:
                    moves.append(Move(position=(i, self.position[1])))
                break
            moves.append(Move(position=(i, self.position[1])))
        for i in range(self.position[0] - 1, -1, -1):
            if not board[i][self.position[1]].piece == 'none':
                if not board[i][self.position[1]].is_white == self.is_white:
                    moves.append(Move(position=(i, self.position[1])))
                break
            moves.append(Move(position=(i, self.position[1])))
        for i in range(self.position[1] + 1, 8):
            if not board[self.position[0]][i].piece == 'none':
                if not board[self.position[0]][i].is_white == self.is_white:
                    moves.append(Move(position=(self.position[0], i)))
                break
            moves.append(Move(position=(self.position[0], i)))
        for i in range(self.position[1] - 1, -1, -1):
            if not board[self.position[0]][i].piece == 'none':
                if not board[self.position[0]][i].is_white == self.is_white:
                    moves.append(Move(position=(self.position[0], i)))
                break
            moves.append(Move(position=(self.position[0], i)))
        return moves


class Obama(JoeBiden):
    def __init__(self, position, is_white):
        super().__init__(position, is_white)
        self.hp = 16
        self.max_hp = 16
        self.boss_piece = True
        self.damage1 = 2.5
        self.notatie = "Obama"
        self.piece = "Obama"

    def get_available_positions(self, board):
        return super().get_available_positions(board)


class Guillotine(Piece):

    def __init__(self, position, is_white):

        super().__init__(position, is_white)
        self.hp = 4
        self.max_hp = 4
        self.building = True
        self.piece = "guillotine"
        self.notatie = "Gu"
        self.value = 3
        self.damage1 = 20

    def get_available_positions(self, board):

        moves = []
        # up
        if self.position[1] != 7:
            french_revolution = board[self.position[0]][self.position[1] + 1].piece in ["koning", "Obama", "Joe Biden"]
            if french_revolution:
                moves.append(
                    Move(position=(self.position[0], self.position[1] + 1), french_revolution=french_revolution))
        # down
        if self.position[1] != 0:
            french_revolution = board[self.position[0]][self.position[1] - 1].piece in ["koning", "Obama", "Joe Biden"]
            if french_revolution:
                moves.append(
                    Move(position=(self.position[0], self.position[1] - 1), french_revolution=french_revolution))
        # left
        if self.position[0] != 0:
            french_revolution = board[self.position[0] - 1][self.position[1]].piece in ["koning", "Obama", "Joe Biden"]
            if french_revolution:
                moves.append(
                    Move(position=(self.position[0] - 1, self.position[1]), french_revolution=french_revolution))
        # right
        if self.position[0] != 7:
            french_revolution = board[self.position[0] + 1][self.position[1]].piece in ["koning", "Obama", "Joe Biden"]
            if french_revolution:
                moves.append(
                    Move(position=(self.position[0] + 1, self.position[1]), french_revolution=french_revolution))
        # right-up
        if self.position[0] != 7 and self.position[1] != 7:
            french_revolution = board[self.position[0] + 1][self.position[1] + 1].piece in ["koning", "Obama",
                                                                                            "Joe Biden"]
            if french_revolution:
                moves.append(
                    Move(position=(self.position[0] + 1, self.position[1] + 1), french_revolution=french_revolution))
        # right-down
        if self.position[0] != 7 and self.position[1] != 0:
            french_revolution = board[self.position[0] + 1][self.position[1] - 1].piece in ["koning", "Obama",
                                                                                            "Joe Biden"]
            if french_revolution:
                moves.append(
                    Move(position=(self.position[0] + 1, self.position[1] - 1), french_revolution=french_revolution))
        # left-up
        if self.position[0] != 0 and self.position[1] != 7:
            french_revolution = board[self.position[0] - 1][self.position[1] + 1].piece in ["koning", "Obama",
                                                                                            "Joe Biden"]
            if french_revolution:
                moves.append(
                    Move(position=(self.position[0] - 1, self.position[1] + 1), french_revolution=french_revolution))
        # left-down
        if self.position[0] != 0 and self.position[1] != 0:
            french_revolution = board[self.position[0] - 1][self.position[1] - 1].piece in ["koning", "Obama",
                                                                                            "Joe Biden"]
            if french_revolution:
                moves.append(
                    Move(position=(self.position[0] - 1, self.position[1] - 1), french_revolution=french_revolution))
        return moves


class Bagguette(Pion):

    def __init__(self, position, is_white):
        super().__init__(position, is_white)
        self.piece = "bagguette"
        self.notatie = "Bag"
        self.damage1 = 1.5


class Napoleon(Piece):

    def __init__(self, position, is_white):

        super().__init__(position, is_white)

        self.piece = "napoleon"
        self.notatie = "Na"
        self.hp = 10
        self.max_hp = 10
        self.damage1 = 2.5
        self.smoll_guy = True
        self.value = 5
        self.boss_damage_bonus = 0.75

    def get_available_positions(self, board):

        moves = []

        for x in range(self.position[0] - 2, self.position[0] + 3):
            for y in range(self.position[1] - 2, self.position[1] + 3):
                if 0 <= x <= 7 and 0 <= y <= 7:
                    if board[x][y].is_white != self.is_white:
                        moves.append(Move(position=(x, y)))

        return moves


class Crossiant(Paard):
    def __init__(self, position, is_white):
        super().__init__(position, is_white)

        self.piece = "crossiant"
        self.notatie = "Cr"
        self.damage1 = 1.5


class Furry(Paard):
    def __init__(self, position, is_white):
        super().__init__(position, is_white)
        self.piece = "furry"
        self.notatie = "Fu"
        self.max_hp = 5
        self.hp = 5
        self.value = 3
        self.damage1 = 2


class Renner(Loper):
    def __init__(self, loper: Loper):
        super().__init__(loper.position, loper.is_white)

        self.piece = "renner"
        self.notatie = "Re"
        self.max_hp = loper.max_hp + 2
        self.hp = loper.hp + 2
        self.value = loper.value - 1
        self.damage1 = loper.damage1 + 0.75


class Paardatron(Paard):

    def __init__(self, position, is_white):
        super().__init__(position, is_white)

        self.piece = "paardatron"
        self.notatie = "P-tron"

        self.max_hp = 6
        self.hp = 6
        self.value = 2

        self.damage1 = 1.75
        self.has_upgraded = False

        self.can_channel = True
        self.channel_cost = 5

    def on_channel(self, pawns, board):

        if self.has_upgraded or pawns < 5:
            return board, False, pawns

        self.piece = "paardatron2000"
        self.notatie = "P-tron-2000"

        self.damage1 = 2.25
        self.hp *= 2
        self.max_hp = 12

        self.can_channel = False

        self.boss_piece = True
        self.boss_damage_bonus = -0.5

        return board, True, 0

    def get_available_positions(self, board):
        moves = []
        x = self.position[0]
        y = self.position[1]
        n, m = len(board), len(board[0])

        for i, j in [(x + 2, y + 1), (x + 2, y - 1), (x - 2, y + 1), (x - 2, y - 1),
                     (x + 1, y + 2), (x + 1, y - 2), (x - 1, y + 2), (x - 1, y - 2)]:
            if 0 <= i < n and 0 <= j < m:
                if not board[i][j].piece == "none":
                    if not board[i][j].is_white == self.is_white:
                        moves.append(Move(position=(i, j)))
                    continue
                moves.append(Move(position=(i, j)))

        for move in list(moves):

            x = move.position[0]
            y = move.position[1]

            for i, j in [(x + 2, y + 1), (x + 2, y - 1), (x - 2, y + 1), (x - 2, y - 1),
                         (x + 1, y + 2), (x + 1, y - 2), (x - 1, y + 2), (x - 1, y - 2)]:
                if 0 <= i < n and 0 <= j < m:
                    if not board[i][j].piece == "none":
                        if not board[i][j].is_white == self.is_white:
                            moves.append(Move(position=(i, j)))
                        continue
                    moves.append(Move(position=(i, j)))

        if self.has_upgraded:

            # up
            if self.position[1] != 7:
                if board[self.position[0]][self.position[1] + 1].is_white != self.is_white or board[self.position[0]][
                    self.position[1] + 1].piece == 'none':
                    moves.append(Move(position=(self.position[0], self.position[1] + 1)))
            # down
            if self.position[1] != 0:
                if board[self.position[0]][self.position[1] - 1].is_white != self.is_white or board[self.position[0]][
                    self.position[1] - 1].piece == 'none':
                    moves.append(Move(position=(self.position[0], self.position[1] - 1)))
            # left
            if self.position[0] != 0:
                if board[self.position[0] - 1][self.position[1]].is_white != self.is_white or \
                        board[self.position[0] - 1][self.position[1]].piece == 'none':
                    moves.append(Move(position=(self.position[0] - 1, self.position[1])))
            # right
            if self.position[0] != 7:
                if board[self.position[0] + 1][self.position[1]].is_white != self.is_white or \
                        board[self.position[0] + 1][self.position[1]].piece == 'none':
                    moves.append(Move(position=(self.position[0] + 1, self.position[1])))
            # right-up
            if self.position[0] != 7 and self.position[1] != 7:
                if board[self.position[0] + 1][self.position[1] + 1].is_white != self.is_white or \
                        board[self.position[0] + 1][self.position[1] + 1].piece == 'none':
                    moves.append(Move(position=(self.position[0] + 1, self.position[1] + 1)))
            # right-down
            if self.position[0] != 7 and self.position[1] != 0:
                if board[self.position[0] + 1][self.position[1] - 1].is_white != self.is_white or \
                        board[self.position[0] + 1][self.position[1] - 1].piece == 'none':
                    moves.append(Move(position=(self.position[0] + 1, self.position[1] - 1)))
            # left-up
            if self.position[0] != 0 and self.position[1] != 7:
                if board[self.position[0] - 1][self.position[1] + 1].is_white != self.is_white or \
                        board[self.position[0] - 1][self.position[1] + 1].piece == 'none':
                    moves.append(Move(position=(self.position[0] - 1, self.position[1] + 1)))
            # left-down
            if self.position[0] != 0 and self.position[1] != 0:
                if board[self.position[0] - 1][self.position[1] - 1].is_white != self.is_white or \
                        board[self.position[0] - 1][self.position[1] - 1].piece == 'none':
                    moves.append(Move(position=(self.position[0] - 1, self.position[1] - 1)))

        moves = list(set(moves))

        return moves


class Bastille(Kasteel):
    def __init__(self, position, is_white):
        super().__init__(position, is_white)

        self.piece = "bastille"
        self.notatie = "Ba"
        self.damage2 = 2.5

        self.max_hp = 15
        self.hp = 15

    def get_available_positions(self, board):

        moves = []
        for i in range(self.position[0] + 1, 8):
            if not board[i][self.position[1]].piece == 'none':
                if not board[i][self.position[1]].is_white == self.is_white:
                    moves.append(Move(position=(i, self.position[1])))
                break
            moves.append(Move(position=(i, self.position[1])))
        for i in range(self.position[0] - 1, -1, -1):
            if not board[i][self.position[1]].piece == 'none':
                if not board[i][self.position[1]].is_white == self.is_white:
                    moves.append(Move(position=(i, self.position[1])))
                break
            moves.append(Move(position=(i, self.position[1])))
        for i in range(self.position[1] + 1, 8):
            if not board[self.position[0]][i].piece == 'none':
                if not board[self.position[0]][i].is_white == self.is_white:
                    moves.append(Move(position=(self.position[0], i)))
                break
            moves.append(Move(position=(self.position[0], i)))
        for i in range(self.position[1] - 1, -1, -1):
            if not board[self.position[0]][i].piece == 'none':
                if not board[self.position[0]][i].is_white == self.is_white:
                    moves.append(Move(position=(self.position[0], i)))
                break
            moves.append(Move(position=(self.position[0], i)))
        if not self.position[0] <= 0 and not self.position[1] <= 0:
            if not board[self.position[0] - 1][self.position[1] - 1].piece == 'none':
                if board[self.position[0] - 1][self.position[1] - 1].is_white:
                    moves.append(Move(position=(self.position[0] - 1, self.position[1] - 1)))
        for x in range(self.position[0] - 3, self.position[0] + 4):
            for y in range(self.position[1] - 3, self.position[1] + 4):
                if 0 <= x <= 7 and 0 <= y <= 7:
                    if board[x][y].piece != 'none' and board[x][y].is_white != self.is_white:
                        moves.append(Move(position=(x, y), movement_type=2))

        return moves


class Bass(Pion):

    def __init__(self, position, is_white):
        super().__init__(position, is_white)

        self.piece = "bass"
        self.notatie = "bass"
        self.damage1 = 0.25
        self.hp = 0.5
        self.max_hp = 0.5


class Mimespeler(Piece):

    def __init__(self, position, is_white):
        super().__init__(position, is_white)

        self.piece = "mimespeler"
        self.notatie = "Mi"
        self.damage1 = 1.5
        self.hp = 5
        self.max_hp = 5

    def get_available_positions(self, board):
        moves = []

        x = self.position[0]
        y = self.position[1]
        n, m = len(board), len(board[0])

        for i, j in [(x + 2, y + 1), (x + 2, y - 1), (x - 2, y + 1), (x - 2, y - 1),
                     (x + 1, y + 2), (x + 1, y - 2), (x - 1, y + 2), (x - 1, y - 2)]:
            if 0 <= i < n and 0 <= j < m:
                if not board[i][j].piece == "none":
                    if not board[i][j].is_white == self.is_white:
                        moves.append(Move(position=(i, j)))
                    continue
                moves.append(Move(position=(i, j)))

        # up
        if self.position[1] != 7:
            if board[self.position[0]][self.position[1] + 1].is_white != self.is_white or board[self.position[0]][
                self.position[1] + 1].piece == 'none':
                moves.append(Move(position=(self.position[0], self.position[1] + 1)))
        # down
        if self.position[1] != 0:
            if board[self.position[0]][self.position[1] - 1].is_white != self.is_white or board[self.position[0]][
                self.position[1] - 1].piece == 'none':
                moves.append(Move(position=(self.position[0], self.position[1] - 1)))
        # left
        if self.position[0] != 0:
            if board[self.position[0] - 1][self.position[1]].is_white != self.is_white or board[self.position[0] - 1][
                self.position[1]].piece == 'none':
                moves.append(Move(position=(self.position[0] - 1, self.position[1])))
        # right
        if self.position[0] != 7:
            if board[self.position[0] + 1][self.position[1]].is_white != self.is_white or board[self.position[0] + 1][
                self.position[1]].piece == 'none':
                moves.append(Move(position=(self.position[0] + 1, self.position[1])))
        # right-up
        if self.position[0] != 7 and self.position[1] != 7:
            if board[self.position[0] + 1][self.position[1] + 1].is_white != self.is_white or \
                    board[self.position[0] + 1][self.position[1] + 1].piece == 'none':
                moves.append(Move(position=(self.position[0] + 1, self.position[1] + 1)))
        # right-down
        if self.position[0] != 7 and self.position[1] != 0:
            if board[self.position[0] + 1][self.position[1] - 1].is_white != self.is_white or \
                    board[self.position[0] + 1][self.position[1] - 1].piece == 'none':
                moves.append(Move(position=(self.position[0] + 1, self.position[1] - 1)))
        # left-up
        if self.position[0] != 0 and self.position[1] != 7:
            if board[self.position[0] - 1][self.position[1] + 1].is_white != self.is_white or \
                    board[self.position[0] - 1][self.position[1] + 1].piece == 'none':
                moves.append(Move(position=(self.position[0] - 1, self.position[1] + 1)))
        # left-down
        if self.position[0] != 0 and self.position[1] != 0:
            if board[self.position[0] - 1][self.position[1] - 1].is_white != self.is_white or \
                    board[self.position[0] - 1][self.position[1] - 1].piece == 'none':
                moves.append(Move(position=(self.position[0] - 1, self.position[1] - 1)))

        return moves
