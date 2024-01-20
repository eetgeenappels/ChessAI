import pieces


def coord_to_notation(coord):
    hashmap = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}
    return f'{hashmap[coord[0]]}{8 - coord[1]}'


can_merge: bool = False


def can_merge_fun(can_merge_piece):
    global can_merge
    if can_merge_piece:
        can_merge = True


# convert to detection script
def check_merge_white(board_in, selected_piece, second_piece):
    board = board_in
    spawn_god = False
    if second_piece.is_white:
        original_pos = selected_piece.position
        if not second_piece.piece == 'none':
            can_merge_fun(doMergeStuff(board=board, selected_piece=selected_piece, second_piece=second_piece,
                                       merge_piece_name1="loper", merge_piece_name2="pion",
                                       rank=5))
            can_merge_fun(doMergeStuff(board=board, selected_piece=selected_piece, second_piece=second_piece,
                                       merge_piece_name1="loper", merge_piece_name2="loper",
                                       rank=5))

            can_merge_fun(doMergeStuff(board=board, selected_piece=selected_piece, second_piece=second_piece,
                                       merge_piece_name1="paard", merge_piece_name2="pion",
                                       rank=5))

            can_merge_fun(doMergeStuff(board=board, selected_piece=selected_piece, second_piece=second_piece,
                                       merge_piece_name1="koning", merge_piece_name2="dame",
                                       rank=5))

            can_merge_fun(doMergeStuff(board=board, selected_piece=selected_piece, second_piece=second_piece,
                                       merge_piece_name1="toren", merge_piece_name2="toren",
                                       rank=5))
            can_merge_fun(doMergeStuff(board=board, selected_piece=selected_piece, second_piece=second_piece,
                                       merge_piece_name1="toren", merge_piece_name2="pion",
                                       rank=5))

            can_merge_fun(doMergeStuff(board=board, selected_piece=selected_piece, second_piece=second_piece,
                                       merge_piece_name1="paus", merge_piece_name2="pion",
                                       rank=5))

            can_merge_fun(doMergeStuff(board=board, selected_piece=selected_piece, second_piece=second_piece,
                                       merge_piece_name1="HIMAR", merge_piece_name2="pionT2",
                                       rank=5))

            can_merge_fun(doMergeStuff(board=board, selected_piece=selected_piece, second_piece=second_piece,
                                       merge_piece_name1="Apostel", merge_piece_name2="pion",
                                       rank=5))

            if selected_piece.piece == "Jezus":
                if board[selected_piece.position[0]][5].piece == 'none':
                    if second_piece.piece == "dame":
                        spawn_god = True
                        second_piece = pieces.Piece(original_pos, None)
                        board[original_pos[0]][original_pos[1]] = pieces.Piece(original_pos, None)

            can_merge_fun(doMergeStuff(board=board, selected_piece=selected_piece, second_piece=second_piece,
                                       merge_piece_name1="pion", merge_piece_name2="pion",
                                       rank=5))
            can_merge_fun(doMergeStuff(board=board, selected_piece=selected_piece, second_piece=second_piece,
                                       merge_piece_name1="pionT2", merge_piece_name2="pionT2",
                                       rank=4))
            can_merge_fun(doMergeStuff(board=board, selected_piece=selected_piece, second_piece=second_piece,
                                       merge_piece_name1="pionT3", merge_piece_name2="pionT3",
                                       rank=5))
            can_merge_fun(doMergeStuff(board=board, selected_piece=selected_piece, second_piece=second_piece,
                                       merge_piece_name1="pionT4", merge_piece_name2="pionT4",
                                       rank=5))
            can_merge_fun(doMergeStuff(board=board, selected_piece=selected_piece, second_piece=second_piece,
                                       merge_piece_name1="Kasteel", merge_piece_name2="koning",
                                       rank=5))
            can_merge_fun(doMergeStuff(board=board, selected_piece=selected_piece, second_piece=second_piece,
                                       merge_piece_name1="Kasteel", merge_piece_name2="dame",
                                       rank=5))
            can_merge_fun(doMergeStuff(board=board, selected_piece=selected_piece, second_piece=second_piece,
                                       merge_piece_name1="Kasteel", merge_piece_name2="NBRF",
                                       rank=5))

            can_merge_fun(doMergeStuff(board=board, selected_piece=selected_piece, second_piece=second_piece,
                                       merge_piece_name1="bewoond kasteel", merge_piece_name2="dame",
                                       rank=5))

            can_merge_fun(doMergeStuff(board=board, selected_piece=selected_piece, second_piece=second_piece,
                                       merge_piece_name1="dameskasteel", merge_piece_name2="koning",
                                       rank=5))
            can_merge_fun(doMergeStuff(board=board, selected_piece=selected_piece, second_piece=second_piece,
                                       merge_piece_name1="dame", merge_piece_name2="pion",
                                       rank=5))
            can_merge_fun(doMergeStuff(board=board, selected_piece=selected_piece, second_piece=second_piece,
                                       merge_piece_name1="ruiter", merge_piece_name2="ruiter",
                                       rank=5))
            can_merge_fun(doMergeStuff(board=board, selected_piece=selected_piece, second_piece=second_piece,
                                       merge_piece_name1="paard", merge_piece_name2="paard",
                                       rank=5))
            can_merge_fun(doMergeStuff(board=board, selected_piece=selected_piece, second_piece=second_piece,
                                       merge_piece_name1="Kasteel", merge_piece_name2="guillotine",
                                       rank=5))
            can_merge_fun(doMergeStuff(board=board, selected_piece=selected_piece, second_piece=second_piece,
                                       merge_piece_name1="loper", merge_piece_name2="bagguette",
                                       rank=5))
            can_merge_fun(doMergeStuff(board=board, selected_piece=selected_piece, second_piece=second_piece,
                                       merge_piece_name1="Tank", merge_piece_name2="pionT2",
                                       rank=5))

    if can_merge:

        move = pieces.Move(old_position=selected_piece.position, movement_class=5, old_position2=second_piece.position)

        if spawn_god:
            move = pieces.Move(movement_class=5, old_position=selected_piece.position,
                               old_position2=second_piece.position, spawn_god=spawn_god)

        return can_merge, move
    return can_merge, None


# convert to detection script
def check_merge_black(board_in, selected_piece, second_piece):
    global can_merge
    board = board_in
    spawn_god = False

    if not second_piece.is_white:
        original_pos = selected_piece.position
        if not second_piece.piece == 'none':
            can_merge_fun(doMergeStuff(board=board, selected_piece=selected_piece, second_piece=second_piece,
                                       merge_piece_name1="loper", merge_piece_name2="pion",
                                       rank=2))
            can_merge_fun(doMergeStuff(board=board, selected_piece=selected_piece, second_piece=second_piece,
                                       merge_piece_name1="loper", merge_piece_name2="loper",
                                       rank=2))

            can_merge_fun(doMergeStuff(board=board, selected_piece=selected_piece, second_piece=second_piece,
                                       merge_piece_name1="paard", merge_piece_name2="pion",
                                       rank=2))

            can_merge_fun(doMergeStuff(board=board, selected_piece=selected_piece, second_piece=second_piece,
                                       merge_piece_name1="koning", merge_piece_name2="dame",
                                       rank=2))

            can_merge_fun(doMergeStuff(board=board, selected_piece=selected_piece, second_piece=second_piece,
                                       merge_piece_name1="toren", merge_piece_name2="toren",
                                       rank=2))
            can_merge_fun(doMergeStuff(board=board, selected_piece=selected_piece, second_piece=second_piece,
                                       merge_piece_name1="toren", merge_piece_name2="pion",
                                       rank=2))

            can_merge_fun(doMergeStuff(board=board, selected_piece=selected_piece, second_piece=second_piece,
                                       merge_piece_name1="paus", merge_piece_name2="pion",
                                       rank=2))

            can_merge_fun(doMergeStuff(board=board, selected_piece=selected_piece, second_piece=second_piece,
                                       merge_piece_name1="Apostel", merge_piece_name2="pion",
                                       rank=2))

            can_merge_fun(doMergeStuff(board=board, selected_piece=selected_piece, second_piece=second_piece,
                                       merge_piece_name1="HIMAR", merge_piece_name2="pionT2",
                                       rank=2))
            if selected_piece.piece == "Jezus":
                if board[selected_piece.position[0]][2].piece == 'none':
                    if second_piece.piece == "dame":
                        spawn_god = True
                        has_merged = True
                        second_piece = pieces.Piece(original_pos, None)
                        board[original_pos[0]][original_pos[1]] = pieces.Piece(original_pos, None)
                        merge_text = f'merge(J{coord_to_notation((original_pos[0], original_pos[1]))},D{coord_to_notation(second_piece.position)}) -> Gi9'

            can_merge_fun(doMergeStuff(board=board, selected_piece=selected_piece, second_piece=second_piece,
                                       merge_piece_name1="pion", merge_piece_name2="pion",
                                       rank=2))

            can_merge_fun(doMergeStuff(board=board, selected_piece=selected_piece, second_piece=second_piece,
                                       merge_piece_name1="pionT2", merge_piece_name2="pionT2",
                                       rank=3))

            can_merge_fun(doMergeStuff(board=board, selected_piece=selected_piece, second_piece=second_piece,
                                       merge_piece_name1="pionT3", merge_piece_name2="pionT3",
                                       rank=2))
            can_merge_fun(doMergeStuff(board=board, selected_piece=selected_piece, second_piece=second_piece,
                                       merge_piece_name1="pionT4", merge_piece_name2="pionT4",
                                       rank=2))

            can_merge_fun(doMergeStuff(board=board, selected_piece=selected_piece, second_piece=second_piece,
                                       merge_piece_name1="Kasteel", merge_piece_name2="koning",
                                       rank=2))
            can_merge_fun(doMergeStuff(board=board, selected_piece=selected_piece, second_piece=second_piece,
                                       merge_piece_name1="Kasteel", merge_piece_name2="dame",
                                       rank=2))
            can_merge_fun(doMergeStuff(board=board, selected_piece=selected_piece, second_piece=second_piece,
                                       merge_piece_name1="Kasteel", merge_piece_name2="NBRF",
                                       rank=2))

            can_merge_fun(doMergeStuff(board=board, selected_piece=selected_piece, second_piece=second_piece,
                                       merge_piece_name1="bewoond kasteel", merge_piece_name2="dame",
                                       rank=2))

            can_merge_fun(doMergeStuff(board=board, selected_piece=selected_piece, second_piece=second_piece,
                                       merge_piece_name1="dameskasteel", merge_piece_name2="koning",
                                       rank=2))
            can_merge_fun(doMergeStuff(board=board, selected_piece=selected_piece, second_piece=second_piece,
                                       merge_piece_name1="dame", merge_piece_name2="pion",
                                       rank=2))
            can_merge_fun(doMergeStuff(board=board, selected_piece=selected_piece, second_piece=second_piece,
                                       merge_piece_name1="ruiter", merge_piece_name2="ruiter",
                                       rank=2))
            can_merge_fun(doMergeStuff(board=board, selected_piece=selected_piece, second_piece=second_piece,
                                       merge_piece_name1="paard", merge_piece_name2="paard",
                                       rank=2))
            can_merge_fun(doMergeStuff(board=board, selected_piece=selected_piece, second_piece=second_piece,
                                       merge_piece_name1="Kasteel", merge_piece_name2="guillotine",
                                       rank=2))
            can_merge_fun(doMergeStuff(board=board, selected_piece=selected_piece, second_piece=second_piece,
                                       merge_piece_name1="loper", merge_piece_name2="bagguette",
                                       rank=2))
            can_merge_fun(doMergeStuff(board=board, selected_piece=selected_piece, second_piece=second_piece,
                                       merge_piece_name1="Tank", merge_piece_name2="pionT2",
                                       rank=2))
    if can_merge:

        move = pieces.Move(old_position=selected_piece.position, movement_class=5, old_position2=second_piece.position)

        if spawn_god:
            move = pieces.Move(movement_class=5, old_position=selected_piece.position,
                               old_position2=second_piece.position, spawn_god=spawn_god)

        return can_merge, move
    return can_merge, None


def merge_white(board, selected_piece, second_piece):
    has_merged = False
    spawn_god = False
    merge_text = ''
    if second_piece.is_white:
        original_pos = selected_piece.position
        if not second_piece.piece == 'none' and not second_piece.position == original_pos:
            has_merged, merge_text, board = merge(board=board, merge_piece1=selected_piece
                                                  , merge_piece_name1="loper",
                                                  merge_piece_name2="pion",
                                                  new_piece=pieces.HIMAR(None, True), merge_piece2=second_piece,
                                                  original_pos=original_pos, rank=5,
                                                  has_merged=has_merged, merge_text=merge_text)
            has_merged, merge_text, board = merge(board=board, merge_piece1=selected_piece, merge_piece_name1="loper",
                                                  merge_piece2=second_piece,
                                                  merge_piece_name2="loper",
                                                  new_piece=pieces.Paus(None, True), original_pos=original_pos, rank=5,
                                                  has_merged=has_merged, merge_text=merge_text)

            has_merged, merge_text, board = merge(board=board, merge_piece1=selected_piece, merge_piece2=second_piece,
                                                  merge_piece_name1="paard",
                                                  merge_piece_name2="pion",
                                                  new_piece=pieces.Ruiter(None, True), original_pos=original_pos,
                                                  rank=5, has_merged=has_merged, merge_text=merge_text)

            has_merged, merge_text, board = merge(board=board, merge_piece1=selected_piece, merge_piece2=second_piece,
                                                  merge_piece_name1="koning",
                                                  merge_piece_name2="dame",
                                                  new_piece=pieces.NBRF(None, True), original_pos=original_pos, rank=5,
                                                  has_merged=has_merged, merge_text=merge_text)

            has_merged, merge_text, board = merge(board=board, merge_piece1=selected_piece, merge_piece2=second_piece,
                                                  merge_piece_name1="toren",
                                                  merge_piece_name2="toren",
                                                  new_piece=pieces.Kasteel(None, True), original_pos=original_pos,
                                                  rank=5, has_merged=has_merged, merge_text=merge_text)
            has_merged, merge_text, board = merge(board=board, merge_piece1=selected_piece, merge_piece2=second_piece,
                                                  merge_piece_name1="toren",
                                                  merge_piece_name2="pion",
                                                  new_piece=pieces.Tank(None, True), original_pos=original_pos, rank=5,
                                                  has_merged=has_merged, merge_text=merge_text)

            has_merged, merge_text, board = merge(board=board, merge_piece1=selected_piece, merge_piece2=second_piece,
                                                  merge_piece_name1="paus",
                                                  merge_piece_name2="pion",
                                                  new_piece=pieces.Apostel(None, True), original_pos=original_pos,
                                                  rank=5, has_merged=has_merged, merge_text=merge_text)

            has_merged, merge_text, board = merge(board=board, merge_piece1=selected_piece, merge_piece_name1="HIMAR",
                                                  merge_piece2=second_piece,
                                                  merge_piece_name2="pionT2",
                                                  new_piece=pieces.Railgun(None, True), original_pos=original_pos,
                                                  rank=5, has_merged=has_merged, merge_text=merge_text)

            has_merged, merge_text, board = merge(board=board, merge_piece1=selected_piece, merge_piece_name1="Apostel",
                                                  merge_piece2=second_piece,
                                                  merge_piece_name2="pion",
                                                  new_piece=pieces.Jezus(None, True), original_pos=original_pos, rank=5,
                                                  has_merged=has_merged, merge_text=merge_text)

            if selected_piece.piece == "Jezus":
                if board[selected_piece.position[0]][5].piece == 'none':
                    if second_piece.piece == "dame":
                        spawn_god = True
                        has_merged = True
                        board[second_piece.position[0]][second_piece.position[1]] = pieces.Piece(second_piece.position,
                                                                                                 None)
                        board[original_pos[0]][original_pos[1]] = pieces.Piece(original_pos, None)
                        merge_text = f'merge(J{coord_to_notation((original_pos[0], original_pos[1]))},D{coord_to_notation(second_piece.position)}) -> Gi9'

            has_merged, merge_text, board = merge(board=board, merge_piece1=selected_piece, merge_piece2=second_piece,
                                                  merge_piece_name1="pion", merge_piece_name2="pion",
                                                  new_piece=pieces.PionT2(None, True), original_pos=original_pos,
                                                  rank=5, has_merged=has_merged, merge_text=merge_text)
            has_merged, merge_text, board = merge(board=board, merge_piece1=selected_piece, merge_piece2=second_piece,
                                                  merge_piece_name1="pionT2", merge_piece_name2="pionT2",
                                                  new_piece=pieces.PionT3(None, True), original_pos=original_pos,
                                                  rank=4, has_merged=has_merged, merge_text=merge_text)
            has_merged, merge_text, board = merge(board=board, merge_piece1=selected_piece, merge_piece2=second_piece,
                                                  merge_piece_name1="pionT3", merge_piece_name2="pionT3",
                                                  new_piece=pieces.PionT4(None, True), original_pos=original_pos,
                                                  rank=5, has_merged=has_merged, merge_text=merge_text)
            has_merged, merge_text, board = merge(board=board, merge_piece1=selected_piece, merge_piece2=second_piece,
                                                  merge_piece_name1="pionT4", merge_piece_name2="pionT4",
                                                  new_piece=pieces.PionT5(None, True), original_pos=original_pos,
                                                  rank=5, has_merged=has_merged, merge_text=merge_text)
            has_merged, merge_text, board = merge(board=board, merge_piece1=selected_piece, merge_piece2=second_piece,
                                                  merge_piece_name1="Kasteel", merge_piece_name2="koning",
                                                  new_piece=pieces.BewoondKasteel(None, True),
                                                  original_pos=original_pos, rank=5, has_merged=has_merged,
                                                  merge_text=merge_text)
            has_merged, merge_text, board = merge(board=board, merge_piece1=selected_piece, merge_piece2=second_piece,
                                                  merge_piece_name1="Kasteel", merge_piece_name2="dame",
                                                  new_piece=pieces.Dameskasteel(None, True), original_pos=original_pos,
                                                  rank=5, has_merged=has_merged, merge_text=merge_text)
            has_merged, merge_text, board = merge(board=board, merge_piece1=selected_piece, merge_piece2=second_piece,
                                                  merge_piece_name1="Kasteel", merge_piece_name2="NBRF",
                                                  new_piece=pieces.LGBTQIA2SplusKasteel(None, True),
                                                  original_pos=original_pos, rank=5, has_merged=has_merged,
                                                  merge_text=merge_text)

            has_merged, merge_text, board = merge(board=board, merge_piece1=selected_piece, merge_piece2=second_piece,
                                                  merge_piece_name1="bewoond kasteel", merge_piece_name2="dame",
                                                  new_piece=pieces.LGBTQIA2SplusKasteel(None, True),
                                                  original_pos=original_pos, rank=5, has_merged=has_merged,
                                                  merge_text=merge_text)

            has_merged, merge_text, board = merge(board=board, merge_piece1=selected_piece, merge_piece2=second_piece,
                                                  merge_piece_name1="dameskasteel", merge_piece_name2="koning",
                                                  new_piece=pieces.LGBTQIA2SplusKasteel(None, True),
                                                  original_pos=original_pos, rank=5, has_merged=has_merged,
                                                  merge_text=merge_text)
            has_merged, merge_text, board = merge(board=board, merge_piece1=selected_piece, merge_piece2=second_piece,
                                                  merge_piece_name1="dame", merge_piece_name2="pion",
                                                  new_piece=pieces.Guillotine(None, True), original_pos=original_pos,
                                                  rank=5, has_merged=has_merged, merge_text=merge_text)
            has_merged, merge_text, board = merge(board=board, merge_piece1=selected_piece, merge_piece2=second_piece,
                                                  merge_piece_name1="ruiter", merge_piece_name2="ruiter",
                                                  new_piece=pieces.Paardatron(None, True), original_pos=original_pos,
                                                  rank=5, has_merged=has_merged, merge_text=merge_text)
            has_merged, merge_text, board = merge(board=board, merge_piece1=selected_piece, merge_piece2=second_piece,
                                                  merge_piece_name1="paard", merge_piece_name2="paard",
                                                  new_piece=pieces.Furry(None, True), original_pos=original_pos, rank=5,
                                                  has_merged=has_merged, merge_text=merge_text)
            has_merged, merge_text, board = merge(board=board, merge_piece1=selected_piece, merge_piece2=second_piece,
                                                  merge_piece_name1="Kasteel", merge_piece_name2="guillotine",
                                                  new_piece=pieces.Bastille(None, True), original_pos=original_pos,
                                                  rank=5, has_merged=has_merged, merge_text=merge_text)
            has_merged, merge_text, board = merge(board=board, merge_piece1=selected_piece, merge_piece2=second_piece,
                                                  merge_piece_name1="loper", merge_piece_name2="bagguette",
                                                  new_piece=pieces.Mimespeler(None, True), original_pos=original_pos,
                                                  rank=5, has_merged=has_merged, merge_text=merge_text)
            has_merged, merge_text, board = merge(board=board, merge_piece1=selected_piece, merge_piece2=second_piece,
                                                  merge_piece_name1="Tank", merge_piece_name2="pionT2",
                                                  new_piece=pieces.AttackHelikopter(None, True),
                                                  original_pos=original_pos, rank=5, has_merged=has_merged, merge_text=merge_text)

    return spawn_god, board, merge_text


def merge_black(board, selected_piece, second_piece):
    has_merged = False
    spawn_god = False
    merge_text = ''
    if not second_piece.is_white:
        original_pos = selected_piece.position
        if not second_piece.piece == 'none' and not second_piece.position == original_pos:
            has_merged, merge_text, board = merge(board=board, merge_piece1=selected_piece, merge_piece_name1="loper",
                                                  merge_piece2=second_piece,
                                                  merge_piece_name2="pion",
                                                  new_piece=pieces.HIMAR(None, False), original_pos=original_pos,
                                                  rank=2, has_merged=has_merged, merge_text=merge_text)
            has_merged, merge_text, board = merge(board=board, merge_piece1=selected_piece, merge_piece_name1="loper",
                                                  merge_piece2=second_piece,
                                                  merge_piece_name2="loper",
                                                  new_piece=pieces.Paus(None, False), original_pos=original_pos, rank=2,
                                                  has_merged=has_merged, merge_text=merge_text)

            has_merged, merge_text, board = merge(board=board, merge_piece1=selected_piece, merge_piece_name1="paard",
                                                  merge_piece2=second_piece,
                                                  merge_piece_name2="pion",
                                                  new_piece=pieces.Ruiter(None, False), original_pos=original_pos,
                                                  rank=2, has_merged=has_merged, merge_text=merge_text)

            has_merged, merge_text, board = merge(board=board, merge_piece1=selected_piece, merge_piece2=second_piece,
                                                  merge_piece_name1="koning", merge_piece_name2="dame",
                                                  new_piece=pieces.NBRF(None, False), original_pos=original_pos, rank=2,
                                                  has_merged=has_merged, merge_text=merge_text)

            has_merged, merge_text, board = merge(board=board, merge_piece1=selected_piece, merge_piece_name1="toren",
                                                  merge_piece2=second_piece,
                                                  merge_piece_name2="toren",
                                                  new_piece=pieces.Kasteel(None, False), original_pos=original_pos,
                                                  rank=2, has_merged=has_merged, merge_text=merge_text)
            has_merged, merge_text, board = merge(board=board, merge_piece1=selected_piece, merge_piece_name1="toren",
                                                  merge_piece2=second_piece,
                                                  merge_piece_name2="pion",
                                                  new_piece=pieces.Tank(None, False), original_pos=original_pos, rank=2,
                                                  has_merged=has_merged, merge_text=merge_text)

            has_merged, merge_text, board = merge(board=board, merge_piece1=selected_piece, merge_piece_name1="paus",
                                                  merge_piece2=second_piece,
                                                  merge_piece_name2="pion",
                                                  new_piece=pieces.Apostel(None, False), original_pos=original_pos,
                                                  rank=2, has_merged=has_merged, merge_text=merge_text)

            has_merged, merge_text, board = merge(board=board, merge_piece1=selected_piece, merge_piece2=second_piece,
                                                  merge_piece_name1="Apostel", merge_piece_name2="pion",
                                                  new_piece=pieces.Jezus(None, False), original_pos=original_pos,
                                                  rank=2, has_merged=has_merged, merge_text=merge_text)

            has_merged, merge_text, board = merge(board=board, merge_piece1=selected_piece, merge_piece_name1="HIMAR",
                                                  merge_piece2=second_piece,
                                                  merge_piece_name2="pionT2",
                                                  new_piece=pieces.Railgun(None, False), original_pos=original_pos,
                                                  rank=2, has_merged=has_merged, merge_text=merge_text)
            if selected_piece.piece == "Jezus":
                if board[selected_piece.position[0]][2].piece == 'none':
                    if second_piece.piece == "dame":
                        spawn_god = True
                        has_merged = True
                        board[second_piece.position[0]][second_piece.position[1]] = pieces.Piece(second_piece.position,
                                                                                                 None)
                        board[original_pos[0]][original_pos[1]] = pieces.Piece(original_pos, None)
                        merge_text = f'merge(J{coord_to_notation((original_pos[0], original_pos[1]))},D{coord_to_notation(second_piece.position)}) -> Gi9'

            has_merged, merge_text, board = merge(board=board, merge_piece1=selected_piece, merge_piece2=second_piece,
                                                  merge_piece_name1="pion", merge_piece_name2="pion",
                                                  new_piece=pieces.PionT2(None, False), original_pos=original_pos,
                                                  rank=2, has_merged=has_merged, merge_text=merge_text)

            has_merged, merge_text, board = merge(board=board, merge_piece1=selected_piece, merge_piece2=second_piece,
                                                  merge_piece_name1="pionT2", merge_piece_name2="pionT2",
                                                  new_piece=pieces.PionT3(None, False), original_pos=original_pos,
                                                  rank=3, has_merged=has_merged, merge_text=merge_text)

            has_merged, merge_text, board = merge(board=board, merge_piece1=selected_piece, merge_piece2=second_piece,
                                                  merge_piece_name1="pionT3", merge_piece_name2="pionT3",
                                                  new_piece=pieces.PionT4(None, False), original_pos=original_pos,
                                                  rank=2, has_merged=has_merged, merge_text=merge_text)
            has_merged, merge_text, board = merge(board=board, merge_piece1=selected_piece, merge_piece2=second_piece,
                                                  merge_piece_name1="pionT4", merge_piece_name2="pionT4",
                                                  new_piece=pieces.PionT5(None, False), original_pos=original_pos,
                                                  rank=2, has_merged=has_merged, merge_text=merge_text)

            has_merged, merge_text, board = merge(board=board, merge_piece1=selected_piece, merge_piece2=second_piece,
                                                  merge_piece_name1="Kasteel", merge_piece_name2="koning",
                                                  new_piece=pieces.BewoondKasteel(None, False),
                                                  original_pos=original_pos, rank=2, has_merged=has_merged,
                                                  merge_text=merge_text)
            has_merged, merge_text, board = merge(board=board, merge_piece1=selected_piece, merge_piece2=second_piece,
                                                  merge_piece_name1="Kasteel", merge_piece_name2="dame",
                                                  new_piece=pieces.Dameskasteel(None, False), original_pos=original_pos,
                                                  rank=2, has_merged=has_merged, merge_text=merge_text)
            has_merged, merge_text, board = merge(board=board, merge_piece1=selected_piece, merge_piece2=second_piece,
                                                  merge_piece_name1="Kasteel", merge_piece_name2="NBRF",
                                                  new_piece=pieces.LGBTQIA2SplusKasteel(None, False),
                                                  original_pos=original_pos, rank=2, has_merged=has_merged,
                                                  merge_text=merge_text)

            has_merged, merge_text, board = merge(board=board, merge_piece1=selected_piece, merge_piece2=second_piece,
                                                  merge_piece_name1="bewoond kasteel", merge_piece_name2="dame",
                                                  new_piece=pieces.LGBTQIA2SplusKasteel(None, False),
                                                  original_pos=original_pos, rank=2, has_merged=has_merged,
                                                  merge_text=merge_text)

            has_merged, merge_text, board = merge(board=board, merge_piece1=selected_piece, merge_piece2=second_piece,
                                                  merge_piece_name1="dameskasteel", merge_piece_name2="koning",
                                                  new_piece=pieces.LGBTQIA2SplusKasteel(None, False),
                                                  original_pos=original_pos, rank=2, has_merged=has_merged,
                                                  merge_text=merge_text)
            has_merged, merge_text, board = merge(board=board, merge_piece1=selected_piece, merge_piece2=second_piece,
                                                  merge_piece_name1="dame", merge_piece_name2="pion",
                                                  new_piece=pieces.Guillotine(None, False), original_pos=original_pos,
                                                  rank=2, has_merged=has_merged, merge_text=merge_text)
            has_merged, merge_text, board = merge(board=board, merge_piece1=selected_piece, merge_piece2=second_piece,
                                                  merge_piece_name1="ruiter", merge_piece_name2="ruiter",
                                                  new_piece=pieces.Paardatron(None, False), original_pos=original_pos,
                                                  rank=2, has_merged=has_merged, merge_text=merge_text)
            has_merged, merge_text, board = merge(board=board, merge_piece1=selected_piece, merge_piece2=second_piece,
                                                  merge_piece_name1="paard", merge_piece_name2="paard",
                                                  new_piece=pieces.Furry(None, False), original_pos=original_pos,
                                                  rank=2, has_merged=has_merged, merge_text=merge_text)
            has_merged, merge_text, board = merge(board=board, merge_piece1=selected_piece, merge_piece2=second_piece,
                                                  merge_piece_name1="Kasteel", merge_piece_name2="guillotine",
                                                  new_piece=pieces.Bastille(None, False), original_pos=original_pos,
                                                  rank=2, has_merged=has_merged, merge_text=merge_text)
            has_merged, merge_text, board = merge(board=board, merge_piece1=selected_piece, merge_piece2=second_piece,
                                                  merge_piece_name1="loper", merge_piece_name2="bagguette",
                                                  new_piece=pieces.Mimespeler(None, False), original_pos=original_pos,
                                                  rank=2, has_merged=has_merged, merge_text=merge_text)
            has_merged, merge_text, board = merge(board=board, merge_piece1=selected_piece, merge_piece2=second_piece,
                                                  merge_piece_name1="Tank", merge_piece_name2="pionT2",
                                                  new_piece=pieces.AttackHelikopter(None, False),
                                                  original_pos=original_pos, rank=2, has_merged=has_merged,
                                                  merge_text=merge_text)
    return spawn_god, board, merge_text


def merge(board, merge_piece1, merge_piece2, merge_piece_name1, merge_piece_name2, new_piece: pieces.Piece,
          original_pos, rank, has_merged, merge_text):
    if merge_piece1.piece == merge_piece_name1:
        if board[merge_piece1.position[0]][rank].piece == 'none':
            if merge_piece2.piece == merge_piece_name2:
                has_merged = True

                new_pos = (merge_piece1.position[0], rank)

                notatie1 = board[original_pos[0]][original_pos[1]].notatie
                notatie2 = merge_piece2.notatie
                notatie3 = new_piece.notatie

                merge_text = f'merge({notatie1}{coord_to_notation((original_pos[0], original_pos[1]))},{notatie2}{coord_to_notation(merge_piece2.position)}) -> {notatie3}{coord_to_notation((new_pos[0], new_pos[1]))}'

                board[new_pos[0]][new_pos[1]] = new_piece
                board[new_pos[0]][new_pos[1]].position = new_pos
                board[new_pos[0]][new_pos[1]].hp = calculate_merge_hp(board[original_pos[0]][original_pos[1]],
                                                                      merge_piece2, board[new_pos[0]][new_pos[1]])
                board[merge_piece2.position[0]][merge_piece2.position[1]] = pieces.Piece(original_pos, None)
                board[original_pos[0]][original_pos[1]] = pieces.Piece(original_pos, None)

    return has_merged, merge_text, board


def calculate_merge_hp(piece1, piece2, piece3):
    return round((piece1.hp + piece2.hp) / (piece1.max_hp + piece2.max_hp) * piece3.max_hp, 1)


def doMergeStuff(board, selected_piece, second_piece, merge_piece_name1, merge_piece_name2, rank):
    if selected_piece.piece == merge_piece_name1:
        if board[selected_piece.position[0]][rank].piece == 'none':
            if second_piece.piece == merge_piece_name2:
                return True

    return False
