import pieces

sacraficial_pawns_maximum = 5


def sacrafice(board: list[list[pieces.Piece]], sacrifice_piece: pieces.Piece, sacraficial_pawns: int):
    position = sacrifice_piece.position

    if sacrifice_piece.piece != "none":

        sacraficial_pawns += sacrifice_piece.value

        if sacraficial_pawns > sacraficial_pawns_maximum:
            sacraficial_pawns = sacraficial_pawns_maximum

        board[position[0]][position[1]] = pieces.Piece(position, None)

        return board, sacraficial_pawns
    return board, sacraficial_pawns


def channel(board, selected_piece: pieces.Piece, sacraficial_pawns: int):
    board, has_channeled, sacraficial_pawns = selected_piece.on_channel(sacraficial_pawns, board)

    return board, sacraficial_pawns
