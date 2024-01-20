from assets import *
import pieces
import math
import render

# Set the chess board background color
bg_color = (255, 255, 255)
width = 1000
height = 1000

last_move = ''

# Create a 2D list to represent the chess board

board = [[pieces.Piece((x,y), None) for x in range(8)] for y in range(8)]

def coord_to_notation(coord):
    hashmap = {0:'a', 1:'b', 2:'c', 3:'d', 4:'e', 5:'f', 6:'g', 7:'h'}
    return f'{hashmap[coord[0]]}{8-coord[1]}'

for i in range(0,8):
    board[i][1] = pieces.Pion((i,1), False)
for i in range(0,8):
    board[i][6] = pieces.Pion((i,6), True)
board[0][7] = pieces.Toren((0,7), True)
board[7][7] = pieces.Toren((7,7), True)
board[2][7] = pieces.Loper((2,7), True)
board[5][7] = pieces.Loper((5,7), True)
board[4][7] = pieces.Koning((4,7), True)
board[3][7] = pieces.Dame((3,7), True)
board[1][7] = pieces.Paard((1,7), True)
board[6][7] = pieces.Paard((6,7), True)

board[0][0] = pieces.Toren((0,0), False)
board[7][0] = pieces.Toren((7,0), False)
board[2][0] = pieces.Loper((2,0), False)
board[5][0] = pieces.Loper((5,0), False)
board[4][0] = pieces.Koning((4,0), False)
board[3][0] = pieces.Dame((3,0), False)
board[1][0] = pieces.Paard((1,0), False)
board[6][0] = pieces.Paard((6,0), False)
game_state.zet_nummer = 1
wit_aan_de_buurt = True

event = ""

has_rikeerd = False

stage = 1
captured_pieces = []

font = pygame.font.SysFont('Comic Sans MS', 30)
font_small = pygame.font.SysFont("Comic Sans MS", 15)

running = True
selected_piece = None

merge_mode = False

show_i9 = False
i9_piece = None

wit_sacraficial_pawns = 0
zwart_sacraficial_pawns = 0



def tick(screen):
    global last_move, selected_piece, board, wit_aan_de_buurt, running,merge_mode, has_rikeerd, show_i9, i9_piece, wit_sacraficial_pawns, zwart_sacraficial_pawns
    
    

    # aan zet
    if wit_aan_de_buurt:
        screen.blit(font.render("Wit aan zet!", True, (0,0,0)),(820, 20))
    else:
        screen.blit(font.render("Zwart aan zet!", True, (0,0,0)), (820, 20))

    # sacraficial text
    screen.blit(font_small.render("zwart: sacraficial pawns", True, (0,0,0)), (810, 160))

    # draw sacraficial pawns
    screen.blit(sacraficial_pawn_empty, (810, 180))
    screen.blit(sacraficial_pawn_empty, (840, 180))
    screen.blit(sacraficial_pawn_empty, (870, 180))
    screen.blit(sacraficial_pawn_empty, (900, 180))
    screen.blit(sacraficial_pawn_empty, (930, 180))

    for i in range(zwart_sacraficial_pawns):

        screen.blit(sacraficial_pawn_full, (810 + (i * 30), 180))
   
 # sacraficial text
    screen.blit(font_small.render("wit: sacraficial pawns", True, (0,0,0)), (810, 580))

    # draw sacraficial pawns
    screen.blit(sacraficial_pawn_empty, (810, 600))
    screen.blit(sacraficial_pawn_empty, (840, 600))
    screen.blit(sacraficial_pawn_empty, (870, 600))
    screen.blit(sacraficial_pawn_empty, (900, 600))
    screen.blit(sacraficial_pawn_empty, (930, 600))

    for i in range(wit_sacraficial_pawns):

        screen.blit(sacraficial_pawn_full, (810 + (i * 30), 600))

    x, y = pygame.mouse.get_pos()
    x, y = math.floor(x/100), math.floor(y/100)
    if 0 <= x <= 7 and 0 <= y <= 7:
        if selected_piece == None and not merge_mode:
            if board[x][y] != "none":
                if board[x][y].is_white == wit_aan_de_buurt:
                    pygame.draw.rect(screen, (0, 255, 0), (board[x][y].position[0] * 100, board[x][y].position[1] * 100, 100,100))
                    moves = board[x][y].get_available_positions(board)
                    for move in moves:
                        match move.movement_type:
                            case 1:
                                pygame.draw.rect(screen, (255, 255, 0), (move.position[0] * 100, move.position[1] * 100, 100,100))
                            case 2:
                                pygame.draw.rect(screen, (255, 0, 0), (move.position[0] * 100, move.position[1] * 100, 100,100))
                                
                            case 3:
                                pygame.draw.rect(screen, (255, 255, 0), (move.position[0] * 100, move.position[1] * 100, 100,100))
                            case 5:
                                pygame.draw.rect(screen, (255, 255, 0), (move.position[0] * 100, move.position[1] * 100, 100,100))

        elif merge_mode:
            if selected_piece.is_white == wit_aan_de_buurt:
                pygame.draw.rect(screen, (0, 255, 0), (selected_piece.position[0] * 100, selected_piece.position[1] * 100, 100,100))
                for x in range(0,8):
                    for y in range(0,8):
                        if not board[x][y].is_white == wit_aan_de_buurt:
                            continue
                        match selected_piece.piece:
                            case 'loper':
                                if not board[x][y].position == selected_piece.position:
                                    match board[x][y].piece:
                                        case 'pion':
                                            pygame.draw.rect(screen, (255, 94, 5), (x * 100, y * 100, 100,100))
                                        case 'loper':
                                            pygame.draw.rect(screen, (255, 94, 5), (x * 100, y * 100, 100,100))
                                        case 'bagguette':
                                            pygame.draw.rect(screen, (255, 94, 5), (x * 100, y * 100, 100,100))
                            case 'paard':
                                if not board[x][y].position == selected_piece.position:
                                    match board[x][y].piece:
                                        case 'pion':
                                            pygame.draw.rect(screen, (255, 94, 5), (x * 100, y * 100, 100,100))
                                        case 'paard':
                                            pygame.draw.rect(screen, (255, 94, 5), (x * 100, y * 100, 100,100))
                            case 'koning':
                                match board[x][y].piece:
                                    case 'dame':
                                        pygame.draw.rect(screen, (255, 94, 5), (x * 100, y * 100, 100,100))
                            case 'toren':
                                if not board[x][y].position == selected_piece.position:
                                    match board[x][y].piece:
                                        case 'toren':
                                            pygame.draw.rect(screen, (255, 94, 5), (x * 100, y * 100, 100,100))
                                        case 'pion':
                                            pygame.draw.rect(screen, (255, 94, 5), (x * 100, y * 100, 100,100))
                            case 'paus':
                                match board[x][y].piece:
                                    case "pion":
                                        pygame.draw.rect(screen, (255, 94, 5), (x * 100, y * 100, 100,100))
                            case 'Apostel':
                                match board[x][y].piece:
                                    case "pion":
                                        pygame.draw.rect(screen, (255, 94, 5), (x * 100, y * 100, 100,100))
                            case 'Jezus':
                                match board[x][y].piece:
                                    case "dame":
                                        pygame.draw.rect(screen, (255, 94, 5), (x * 100, y * 100, 100,100))
                            case 'pion':
                                if not board[x][y].position == selected_piece.position:
                                    match board[x][y].piece:
                                        case 'pion':
                                            pygame.draw.rect(screen, (255, 94, 5), (x * 100, y * 100, 100,100))
                            case 'pionT2':
                                if not board[x][y] == selected_piece.position:
                                    match board[x][y].piece:
                                        case 'pionT2':
                                            pygame.draw.rect(screen, (255, 94, 5), (x * 100, y * 100, 100,100))
                            case 'pionT3':
                                if not board[x][y].position == selected_piece.position:
                                    match board[x][y].piece:
                                        case 'pionT3':
                                            pygame.draw.rect(screen, (255, 94, 5), (x * 100, y * 100, 100,100))
                            case 'kasteel':
                                match board[x][y].piece:
                                    case 'NBRF':
                                        pygame.draw.rect(screen, (255, 94, 5), (x * 100, y * 100, 100,100))
                                    case 'koning':
                                        pygame.draw.rect(screen, (255, 94, 5), (x * 100, y * 100, 100,100))
                                    case 'dame':
                                        pygame.draw.rect(screen, (255, 94, 5), (x * 100, y * 100, 100, 100))
                                    case 'guillotine':
                                        pygame.draw.rect(screen, (255, 94, 5), (x * 100, y * 100, 100,100))
                            case 'dameskasteel':
                                match board[x][y].piece:
                                    case 'koning':
                                        pygame.draw.rect(screen, (255, 94, 5), (x * 100, y * 100, 100,100))
                            case 'HIMAR':
                                match board[x][y].piece:
                                    case 'pionT2':
                                        pygame.draw.rect(screen, (255,94, 5), (x * 100, y * 100, 100, 100))

                            case 'dame':
                                match board[x][y].piece:
                                    case 'pion':
                                        pygame.draw.rect(screen, (255, 94, 5), (x * 100, y * 100, 100, 100))
                            case 'ruiter':
                                if not board[x][y].position == selected_piece.position:
                                    match board[x][y].piece:
                                        case 'ruiter':
                                            pygame.draw.rect(screen, (255, 94, 5), (x * 100, y * 100, 100,100))
                            case 'Tank':
                                match board[x][y].piece:
                                    case 'pionT2':
                                        pygame.draw.rect(screen, (255, 94, 5), (x * 100, y * 100, 100, 100))


        else:
            if selected_piece.is_white == wit_aan_de_buurt:
                pygame.draw.rect(screen, (0, 255, 0), (selected_piece.position[0] * 100, selected_piece.position[1] * 100, 100,100))
                moves = selected_piece.get_available_positions(board)
                for move in moves:
                    match move.movement_type:
                        case 1:
                            pygame.draw.rect(screen, (255, 255, 0), (move.position[0] * 100, move.position[1] * 100, 100,100))
                        case 2:
                            pygame.draw.rect(screen, (255, 0, 0), (move.position[0] * 100, move.position[1] * 100, 100,100))
                            
                        case 3:
                            pygame.draw.rect(screen, (255, 255, 0), (move.position[0] * 100, move.position[1] * 100, 100,100))
                        case 5:
                            pygame.draw.rect(screen, (255, 255, 0), (move.position[0] * 100, move.position[1] * 100, 100,100))

    if game_state.zet_nummer == 3:

        king_exist = False
        for x in range(8):
            for y in range(8):
                if (board[x][y].piece == 'koning' or board[x][y].piece == 'NBRF' or board[x][y].piece == 'bewoond kasteel' or board[x][y].piece == 'LGBTQIA2S+Kasteel' or board[x][y].piece == 'Lenin' or board[x][y].piece == 'Stalin' or board[x][y].piece == 'Obama' or board[x][y].piece == 'Joe Biden' or board[x][y].piece == 'Stalin' or board[x][y].piece == "napoleon") and board[x][y].is_white == wit_aan_de_buurt :
                    king_exist = True

        if not king_exist:
            if wit_aan_de_buurt:
                last_move = "zwart > wit"
            else:
                last_move = "wit > zwart"
            print(last_move)

        game_state.zet_nummer = 1
        selected_piece = None
        wit_aan_de_buurt = not wit_aan_de_buurt
        game_state.zet_aantal += 1
        if game_state.zet_aantal == 10:
            event = "terminator"
        if game_state.zet_aantal == 14:
            event = ""
        if game_state.zet_aantal == 20:
            event = "kerst"
        if game_state.zet_aantal == 24:
            event == ""

    render.render_board(screen, board, i9_piece)

    font_render = font.render(last_move, False, (0,0,0))
    screen.blit(font_render, (0,800))
    # Update the display
    pygame.display.flip()

    
    return running
