import pieces


def coord_to_notation(coord):
    hashmap = {0: 'h', 1: 'g', 2: 'f', 3: 'e', 4: 'd', 5: 'c', 6: 'b', 7: 'a'}
    return f'{hashmap[coord[0]]}{8 - coord[1]}'


def move(move: pieces.Move, board, zet_aantal, zet_nummer):
    has_moved = False
    initial_position = move.old_position
    last_move = ""
    captured_piece = None
    has_moved = True
    selected_piece = board[initial_position[0]][initial_position[1]]
    match move.movement_type:
        case 1:
            board, last_move, captured_piece = attack_position_type1(selected_piece, board, last_move, captured_piece,
                                                                     move.position[0], move.position[1])
        case 2:
            board, last_move, captured_piece = attack_position_type2(selected_piece, board, last_move, captured_piece,
                                                                     move.position[0], move.position[1])
        case 3:
            board, last_move, captured_piece = attack_position_type3(selected_piece, board, last_move, captured_piece,
                                                                     move.position[0], move.position[1])
        case 5:
            board, last_move, captured_piece = attack_position_type5(selected_piece, board, last_move, captured_piece,
                                                                     move.position[0], move.position[1])

    if has_moved:
        if zet_aantal == 0 and zet_nummer == 0:
            if type(board[0][5]) == pieces.Paard:
                for i in range(0, 8):
                    board[i][1] = pieces.PionT2((i, 1), False)
                for i in range(0, 8):
                    board[i][6] = pieces.PionT2((i, 6), True)
                board[0][7] = pieces.Tank((0, 7), True)
                board[7][7] = pieces.Tank((7, 7), True)
                board[2][7] = pieces.HIMAR((2, 7), True)
                board[5][7] = pieces.HIMAR((5, 7), True)
                board[4][7] = pieces.NBRF((4, 7), True)
                board[3][7] = pieces.Dameskasteel((3, 7), True)
                board[0][5] = pieces.Ruiter((0, 5), True)
                board[6][7] = pieces.Ruiter((6, 7), True)

                board[0][0] = pieces.Tank((0, 0), False)
                board[7][0] = pieces.Tank((7, 0), False)
                board[2][0] = pieces.HIMAR((2, 0), False)
                board[5][0] = pieces.HIMAR((5, 0), False)
                board[4][0] = pieces.NBRF((4, 0), False)
                board[3][0] = pieces.Dameskasteel((3, 0), False)
                board[1][0] = pieces.Ruiter((1, 0), False)
                board[6][0] = pieces.Ruiter((6, 0), False)
                last_move = "Secret Move: Sodium Attack : Militairy Game"
        if zet_aantal == 0 and zet_nummer == 0:
            if type(board[2][6]) == pieces.Dame:
                for i in range(0, 8):
                    board[i][7] = pieces.Peasant((i, 7), True)
                for i in range(0, 8):
                    board[i][6] = pieces.Peasant((i, 6), True)
                board[4][7] = pieces.Lenin((4, 7), True)
                board[4][0] = pieces.JoeBiden((4, 0), False)

                last_move = "Secret Move: Communist Revolution Lenin variation"
        if move.french_revolution:
            for i in range(0, 8):
                for j in range(0, 8):
                    if board[i][j].is_white == selected_piece.is_white:
                        if board[i][j].piece == "pion":
                            board[i][j] = pieces.Bagguette((i, j), selected_piece.is_white)
                        if board[i][j].piece == "paard":
                            board[i][j].snor = True
            board[initial_position[0]][initial_position[1]] = pieces.Napoleon(
                (initial_position[0], initial_position[1]), selected_piece.is_white)
            last_move = "Secrect Move: French Revolution"

        if zet_aantal == 1 and zet_nummer == 0:
            if type(board[4][1]) is pieces.Dame and piece_on_board(board, pieces.Lenin):
                board[2][0] = pieces.ICBM_Missle_Launcher((2, 0), False)
                board[5][0] = pieces.ICBM_Missle_Launcher((2, 0), False)
                board[2][7] = pieces.ICBM_Missle_Launcher((2, 7), True)
                board[5][7] = pieces.ICBM_Missle_Launcher((5, 7), True)

                lenin_location = find_piece(board, pieces.Lenin)

                board[lenin_location[0]][lenin_location[1]] = pieces.Stalin((lenin_location[0], lenin_location[1]),
                                                                            True)

                joe_biden_location = find_piece(board, pieces.JoeBiden)

                board[joe_biden_location[0]][joe_biden_location[1]] = pieces.Obama((joe_biden_location[0],
                                                                                    joe_biden_location[1]), False)

                last_move = "Secret Move: American Cold War Nuclear Arms Race"
    return board, last_move, captured_piece, has_moved


def get_selected_move(selected_piece: pieces.Piece, x, y, board):
    moves = selected_piece.get_available_positions(board)
    for move in moves:
        if (x, y) == move.position:
            move.old_position = selected_piece.position
            return move


def check_move(moves, position):
    for move in moves:
        if moves == position:
            return True
    return False


def piece_on_board(board, piece_type):
    for collumn in board:
        for piece in collumn:
            if type(piece) == piece_type:
                return True
    return False


def find_piece(board, piece_type):
    for collumn in range(8):
        for piece in range(8):
            if type(board[piece][collumn]) == piece_type:
                return (piece, collumn)
    return False


def attack_position_type1(selected_piece, board, last_move, captured_piece, x, y):
    original_pos = selected_piece.position
    new_pos = (x, y)
    board[x][y].hp -= calculate_damage_type1(selected_piece, board[x][y])
    if board[new_pos[0]][new_pos[1]].hp <= 0:
        captured_piece = board[new_pos[0]][new_pos[1]]
        if board[new_pos[0]][new_pos[1]].piece == 'none':
            print(f"{selected_piece.notatie}{coord_to_notation(original_pos)} -> {coord_to_notation(new_pos)}")
            last_move = f"{selected_piece.notatie}{coord_to_notation(original_pos)} -> {coord_to_notation(new_pos)}"
        else:
            last_move = f"{selected_piece.notatie}{coord_to_notation(original_pos)} kill {board[new_pos[0]][new_pos[1]].notatie}{coord_to_notation(new_pos)}"
            print(
                f"{selected_piece.notatie}{coord_to_notation(original_pos)} kill {board[new_pos[0]][new_pos[1]].notatie}{coord_to_notation(new_pos)}")
        board[new_pos[0]][new_pos[1]] = selected_piece
        board[original_pos[0]][original_pos[1]] = pieces.Piece(original_pos, None)
        board[new_pos[0]][new_pos[1]].position = new_pos
    else:
        if board[new_pos[0]][new_pos[1]].piece == 'none':
            print(f"{selected_piece.notatie}{coord_to_notation(original_pos)} -> {coord_to_notation(new_pos)}")
            last_move = f"{selected_piece.notatie}{coord_to_notation(original_pos)} -> {coord_to_notation(new_pos)}"
        else:
            last_move = f"{selected_piece.notatie}{coord_to_notation(original_pos)} hit {board[new_pos[0]][new_pos[1]].notatie}{coord_to_notation(new_pos)}"
            print(
                f"{selected_piece.notatie}{coord_to_notation(original_pos)} hit {board[new_pos[0]][new_pos[1]].notatie}{coord_to_notation(new_pos)}")
    selected_piece = None
    return board, last_move, captured_piece


def attack_position_type2(selected_piece, board, last_move, captured_piece, x, y):
    original_pos = selected_piece.position
    new_pos = (x, y)
    board[x][y].hp -= calculate_damage_type2(selected_piece, board[x][y])
    if board[new_pos[0]][new_pos[1]].hp <= 0:
        last_move = f"{selected_piece.notatie}{coord_to_notation(original_pos)} pew pewed {board[new_pos[0]][new_pos[1]].notatie}{coord_to_notation(new_pos)}"
        print(
            f"{selected_piece.notatie}{coord_to_notation(original_pos)} pew pewed {board[new_pos[0]][new_pos[1]].notatie}{coord_to_notation(new_pos)}")
        board[new_pos[0]][new_pos[1]] = pieces.Piece(original_pos, None)
    else:
        last_move = f"{selected_piece.notatie}{coord_to_notation(original_pos)} shoot {board[new_pos[0]][new_pos[1]].notatie}{coord_to_notation(new_pos)}"
        print(
            f"{selected_piece.notatie}{coord_to_notation(original_pos)} shoot {board[new_pos[0]][new_pos[1]].notatie}{coord_to_notation(new_pos)}")
    selected_piece = None
    return board, last_move, captured_piece


def attack_position_type3(selected_piece, board, last_move, captured_piece, x, y):
    original_pos = selected_piece.position
    new_pos = (x, y)
    board[new_pos[0]][new_pos[1]].hp -= calculate_damage_type1(selected_piece, board[new_pos[0]][new_pos[1]])
    if board[new_pos[0]][new_pos[1]].hp <= 0:
        captured_piece = board[new_pos[0]][new_pos[1]]
        if board[new_pos[0]][new_pos[1]].piece == 'none':
            print(f"{selected_piece.notatie}{coord_to_notation(original_pos)} -> {coord_to_notation(new_pos)}")
            last_move = f"{selected_piece.notatie}{coord_to_notation(original_pos)} -> {coord_to_notation(new_pos)}"

            board[new_pos[0]][new_pos[1]] = selected_piece
            board[original_pos[0]][original_pos[1]] = pieces.Piece(original_pos, None)
            board[new_pos[0]][new_pos[1]].position = new_pos
        else:
            last_move = f"{selected_piece.notatie}{coord_to_notation(original_pos)} converted {board[new_pos[0]][new_pos[1]].notatie}{coord_to_notation(new_pos)}"
            print(
                f"{selected_piece.notatie}{coord_to_notation(original_pos)} converted {board[new_pos[0]][new_pos[1]].notatie}{coord_to_notation(new_pos)}")
            board[new_pos[0]][new_pos[1]].is_white = selected_piece.is_white
    else:
        if board[new_pos[0]][new_pos[1]].piece == 'none':
            print(f"{selected_piece.notatie}{coord_to_notation(original_pos)} -> {coord_to_notation(new_pos)}")
            last_move = f"{selected_piece.notatie}{coord_to_notation(original_pos)} -> {coord_to_notation(new_pos)}"
            board[new_pos[0]][new_pos[1]] = selected_piece
            board[original_pos[0]][original_pos[1]] = pieces.Piece(original_pos, None)
            board[new_pos[0]][new_pos[1]].position = new_pos
        else:
            last_move = f"{selected_piece.notatie}{coord_to_notation(original_pos)} hit {board[new_pos[0]][new_pos[1]].notatie}{coord_to_notation(new_pos)}"
            print(
                f"{selected_piece.notatie}{coord_to_notation(original_pos)} hit {board[new_pos[0]][new_pos[1]].notatie}{coord_to_notation(new_pos)}")
    selected_piece = None
    return board, last_move, captured_piece


def attack_position_type5(selected_piece, board, last_move, captured_piece, x, y):
    new_pos = (x, y)
    original_pos = selected_piece.position
    board[new_pos[0]][new_pos[1]].hp -= calculate_damage_type1(selected_piece, board[new_pos[0]][new_pos[1]])
    if board[new_pos[0]][new_pos[1]].hp <= 0:
        captured_piece = board[new_pos[0]][new_pos[1]]
        if board[new_pos[0]][new_pos[1]].piece == 'none':
            print(f"{selected_piece.notatie}{coord_to_notation(original_pos)} -> {coord_to_notation(new_pos)}")
            last_move = f"{selected_piece.notatie}{coord_to_notation(original_pos)} -> {coord_to_notation(new_pos)}"
        else:
            last_move = f"{selected_piece.notatie}{coord_to_notation(original_pos)} kill {board[new_pos[0]][new_pos[1]].notatie}{coord_to_notation(new_pos)}"
            print(
                f"{selected_piece.notatie}{coord_to_notation(original_pos)} kill {board[new_pos[0]][new_pos[1]].notatie}{coord_to_notation(new_pos)}")
        board[new_pos[0]][new_pos[1]] = selected_piece
        board[original_pos[0]][original_pos[1]] = pieces.Pion(original_pos, selected_piece.is_white)
        board[new_pos[0]][new_pos[1]].position = new_pos
    else:
        if board[new_pos[0]][new_pos[1]].piece == 'none':
            print(f"{selected_piece.notatie}{coord_to_notation(original_pos)} -> {coord_to_notation(new_pos)}")
            last_move = f"{selected_piece.notatie}{coord_to_notation(original_pos)} -> {coord_to_notation(new_pos)}"
        else:
            last_move = f"{selected_piece.notatie}{coord_to_notation(original_pos)} hit {board[new_pos[0]][new_pos[1]].notatie}{coord_to_notation(new_pos)}"
            print(
                f"{selected_piece.notatie}{coord_to_notation(original_pos)} hit {board[new_pos[0]][new_pos[1]].notatie}{coord_to_notation(new_pos)}")
    selected_piece = None
    return board, last_move, captured_piece


def calculate_damage_type1(attacking_piece: pieces.Piece, recieving_piece):
    damage = attacking_piece.damage1
    if recieving_piece.boss_piece:
        damage += attacking_piece.boss_damage_bonus
    return damage


def calculate_damage_type2(attacking_piece: pieces.Piece, recieving_piece):
    damage = attacking_piece.damage2
    if recieving_piece.boss_piece:
        damage += attacking_piece.boss_damage_bonus
    return damage


class AOE_Move:
    def __init__(self, positions, movement_type=1) -> None:
        self.positions = positions
        self.movement_type = movement_type
