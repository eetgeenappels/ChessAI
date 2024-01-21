import pygame
import pieces
from assets import *
import game
import math

pygame.init()
pygame.font.init()

font = pygame.font.SysFont('Comic Sans MS', 30)
font_small = pygame.font.SysFont("Comic Sans MS", 15)

# Set the chess board square colors
light_square_color = (245, 222, 179)
dark_square_color = (181, 136, 99)

board_checker_pattern = [[light_square_color for _ in range(8)] for _ in range(8)]

for i in range(8):
    for j in range(8):
        if (i + j) % 2 == 1:
            board_checker_pattern[i][j] = dark_square_color


class Button:
    def __init__(self, x, y, width, height, subtext_offset=0, text="", color_base=pygame.Color('lightskyblue3'),
                 color_clicked=pygame.Color("dodgerblue2"), text_color=(0, 0, 0),
                 subtext="",
                 text_font=pygame.font.SysFont('arial', 20), color_hovered=(100, 100, 100)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color_base
        self.color_base = color_base
        self.color_hovered = color_hovered
        self.color_clicked = color_clicked
        self.text_color = text_color
        self.text = text
        self.subtext = subtext
        self.text_font = text_font

        self.subtext_offset = subtext_offset

        self.clicked = False
        self.hovered = False

        self.on_click = None

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            button = pygame.mouse.get_pressed()
            if button[0]:
                if self.hovered:
                    self.clicked = True
                    if self.on_click is not None:
                        self.on_click(self)

    def render(self, screen):

        mouseX = pygame.mouse.get_pos()[0]
        mouseY = pygame.mouse.get_pos()[1]

        self.hovered = self.x < mouseX < self.x + self.width and self.y < mouseY < self.y + self.height

        if self.clicked:
            pygame.draw.rect(screen, self.color_clicked, (self.x, self.y, self.width, self.height))
        elif self.hovered:
            pygame.draw.rect(screen, self.color_hovered, (self.x, self.y, self.width, self.height))
        else:
            pygame.draw.rect(screen, self.color_base, (self.x, self.y, self.width, self.height))

        text_surface = font.render(self.text, True, self.text_color)
        screen.blit(text_surface, (self.x, self.y))

        subtext_surface = font.render(self.subtext, True, self.text_color)
        screen.blit(subtext_surface, (self.x, self.y + self.subtext_offset))


class ImageButton:
    def __init__(self, x, y, width, height, image):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = image

        self.clicked = False
        self.hovered = False

        self.on_click = None

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            button = pygame.mouse.get_pressed()
            print(button)
            if button[0]:
                if self.hovered:
                    self.clicked = True
                    if self.on_click is not None:
                        self.on_click(self)

    def render(self, screen):

        screen.blit(self.image, (self.x, self.y))

        mouseX = pygame.mouse.get_pos()[0]
        mouseY = pygame.mouse.get_pos()[1]

        if pygame.Rect(self.x, self.y, self.width, self.height).collidepoint((mouseX, mouseY)):
            self.hovered = True


class InputBox:

    def __init__(self, x, y, w, h, text='', color_inactive=pygame.Color('dodgerblue2'),
                 color_active=pygame.Color('lightskyblue3'), reset_on_return=True):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color_inactive
        self.color_inactive = color_inactive
        self.color_active = color_active
        self.text = text
        self.txt_surface = font.render(text, True, self.color)
        self.active = False
        self.return_event = None
        self.reset_on_return = reset_on_return

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            self.active = self.rect.collidepoint(event.pos)
            # Change the current color of the input box.
            self.color = self.color if self.active else self.color_inactive
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    if self.return_event is not None:
                        self.return_event(self.text)
                    if self.reset_on_return:
                        self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = font.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)

        # Blit the text
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))


def render_board(screen, nathan_chess_game: game.Game, selected_piece: pieces.Piece, merge_mode: bool,
                 render_move_highlights: bool = True):
    pygame.draw.rect(screen, (255, 255, 255), (0, 0, 1000, 1000))

    # Draw the chess board
    for i in range(8):
        for j in range(8):
            pygame.draw.rect(screen, board_checker_pattern[i][j], (i * 100, j * 100, 100, 100))

    # draw i9
    if nathan_chess_game.i9_piece is not None:
        pygame.draw.rect(screen, board_checker_pattern[0][0], (810, 250, 175, 175))
        if nathan_chess_game.i9_piece.is_white:
            screen.blit(wit_god, (822, 264))
        else:
            screen.blit(zwart_god, (822, 264))

    x, y = pygame.mouse.get_pos()
    x, y = math.floor(x / 100), math.floor(y / 100)
    if 0 <= x <= 7 and 0 <= y <= 7 and render_move_highlights:
        if selected_piece is None and not merge_mode:
            if nathan_chess_game.board[x][y] != "none":
                if nathan_chess_game.board[x][y].is_white == nathan_chess_game.white_turn():
                    pygame.draw.rect(screen, (0, 255, 0), (
                        nathan_chess_game.board[x][y].position[0] * 100,
                        nathan_chess_game.board[x][y].position[1] * 100,
                        100, 100))
                    moves = nathan_chess_game.board[x][y].get_available_positions(nathan_chess_game.board)
                    for move in moves:
                        match move.movement_type:
                            case 1:
                                pygame.draw.rect(screen, (255, 255, 0),
                                                 (move.position[0] * 100, move.position[1] * 100, 100, 100))
                            case 2:
                                pygame.draw.rect(screen, (255, 0, 0),
                                                 (move.position[0] * 100, move.position[1] * 100, 100, 100))

                            case 3:
                                pygame.draw.rect(screen, (255, 255, 0),
                                                 (move.position[0] * 100, move.position[1] * 100, 100, 100))
                            case 5:
                                pygame.draw.rect(screen, (255, 255, 0),
                                                 (move.position[0] * 100, move.position[1] * 100, 100, 100))

        elif merge_mode:
            if selected_piece.is_white == nathan_chess_game.white_turn():
                pygame.draw.rect(screen, (0, 255, 0),
                                 (selected_piece.position[0] * 100, selected_piece.position[1] * 100, 100, 100))
                for x in range(0, 8):
                    for y in range(0, 8):
                        if not nathan_chess_game.board[x][y].is_white == nathan_chess_game.white_turn():
                            continue
                        match selected_piece.piece:
                            case 'loper':
                                if not nathan_chess_game.board[x][y].position == selected_piece.position:
                                    match nathan_chess_game.board[x][y].piece:
                                        case 'pion':
                                            pygame.draw.rect(screen, (255, 94, 5), (x * 100, y * 100, 100, 100))
                                        case 'loper':
                                            pygame.draw.rect(screen, (255, 94, 5), (x * 100, y * 100, 100, 100))
                                        case 'bagguette':
                                            pygame.draw.rect(screen, (255, 94, 5), (x * 100, y * 100, 100, 100))
                            case 'paard':
                                if not nathan_chess_game.board[x][y].position == selected_piece.position:
                                    match nathan_chess_game.board[x][y].piece:
                                        case 'pion':
                                            pygame.draw.rect(screen, (255, 94, 5), (x * 100, y * 100, 100, 100))
                                        case 'paard':
                                            pygame.draw.rect(screen, (255, 94, 5), (x * 100, y * 100, 100, 100))
                            case 'koning':
                                match nathan_chess_game.board[x][y].piece:
                                    case 'dame':
                                        pygame.draw.rect(screen, (255, 94, 5), (x * 100, y * 100, 100, 100))
                            case 'toren':
                                if not nathan_chess_game.board[x][y].position == selected_piece.position:
                                    match nathan_chess_game.board[x][y].piece:
                                        case 'toren':
                                            pygame.draw.rect(screen, (255, 94, 5), (x * 100, y * 100, 100, 100))
                                        case 'pion':
                                            pygame.draw.rect(screen, (255, 94, 5), (x * 100, y * 100, 100, 100))
                            case 'paus':
                                match nathan_chess_game.board[x][y].piece:
                                    case "pion":
                                        pygame.draw.rect(screen, (255, 94, 5), (x * 100, y * 100, 100, 100))
                            case 'Apostel':
                                match nathan_chess_game.board[x][y].piece:
                                    case "pion":
                                        pygame.draw.rect(screen, (255, 94, 5), (x * 100, y * 100, 100, 100))
                            case 'Jezus':
                                match nathan_chess_game.board[x][y].piece:
                                    case "dame":
                                        pygame.draw.rect(screen, (255, 94, 5), (x * 100, y * 100, 100, 100))
                            case 'pion':
                                if not nathan_chess_game.board[x][y].position == selected_piece.position:
                                    match nathan_chess_game.board[x][y].piece:
                                        case 'pion':
                                            pygame.draw.rect(screen, (255, 94, 5), (x * 100, y * 100, 100, 100))
                            case 'pionT2':
                                if not nathan_chess_game.board[x][y] == selected_piece.position:
                                    match nathan_chess_game.board[x][y].piece:
                                        case 'pionT2':
                                            pygame.draw.rect(screen, (255, 94, 5), (x * 100, y * 100, 100, 100))
                            case 'pionT3':
                                if not nathan_chess_game.board[x][y].position == selected_piece.position:
                                    match nathan_chess_game.board[x][y].piece:
                                        case 'pionT3':
                                            pygame.draw.rect(screen, (255, 94, 5), (x * 100, y * 100, 100, 100))
                            case 'kasteel':
                                match nathan_chess_game.board[x][y].piece:
                                    case 'NBRF':
                                        pygame.draw.rect(screen, (255, 94, 5), (x * 100, y * 100, 100, 100))
                                    case 'koning':
                                        pygame.draw.rect(screen, (255, 94, 5), (x * 100, y * 100, 100, 100))
                                    case 'dame':
                                        pygame.draw.rect(screen, (255, 94, 5), (x * 100, y * 100, 100, 100))
                                    case 'guillotine':
                                        pygame.draw.rect(screen, (255, 94, 5), (x * 100, y * 100, 100, 100))
                            case 'dameskasteel':
                                match nathan_chess_game.board[x][y].piece:
                                    case 'koning':
                                        pygame.draw.rect(screen, (255, 94, 5), (x * 100, y * 100, 100, 100))
                            case 'HIMAR':
                                match nathan_chess_game.board[x][y].piece:
                                    case 'pionT2':
                                        pygame.draw.rect(screen, (255, 94, 5), (x * 100, y * 100, 100, 100))

                            case 'dame':
                                match nathan_chess_game.board[x][y].piece:
                                    case 'pion':
                                        pygame.draw.rect(screen, (255, 94, 5), (x * 100, y * 100, 100, 100))
                            case 'ruiter':
                                if not nathan_chess_game.board[x][y].position == selected_piece.position:
                                    match nathan_chess_game.board[x][y].piece:
                                        case 'ruiter':
                                            pygame.draw.rect(screen, (255, 94, 5), (x * 100, y * 100, 100, 100))
                            case 'Tank':
                                match nathan_chess_game.board[x][y].piece:
                                    case 'pionT2':
                                        pygame.draw.rect(screen, (255, 94, 5), (x * 100, y * 100, 100, 100))


        else:
            if selected_piece.is_white == nathan_chess_game.wit_aan_de_buurt:
                pygame.draw.rect(screen, (0, 255, 0),
                                 (selected_piece.position[0] * 100, selected_piece.position[1] * 100, 100, 100))
                moves = selected_piece.get_available_positions(nathan_chess_game.board)
                for move in moves:
                    match move.movement_type:
                        case 1:
                            pygame.draw.rect(screen, (255, 255, 0),
                                             (move.position[0] * 100, move.position[1] * 100, 100, 100))
                        case 2:
                            pygame.draw.rect(screen, (255, 0, 0),
                                             (move.position[0] * 100, move.position[1] * 100, 100, 100))

                        case 3:
                            pygame.draw.rect(screen, (255, 255, 0),
                                             (move.position[0] * 100, move.position[1] * 100, 100, 100))
                        case 5:
                            pygame.draw.rect(screen, (255, 255, 0),
                                             (move.position[0] * 100, move.position[1] * 100, 100, 100))

    # render pieces
    for i in range(8):
        for j in range(8):
            piece: pieces.Piece = nathan_chess_game.board[i][j]
            if piece.is_white:
                match piece.piece:
                    case "pion":
                        piece_surface = wit_pion
                    case "koning":
                        piece_surface = wit_koning
                    case "loper":
                        piece_surface = wit_loper
                    case "toren":
                        piece_surface = wit_toren
                    case "dame":
                        piece_surface = wit_dame
                    case "paard":
                        if piece.snor:
                            piece_surface = wit_paard_snor
                        else:
                            piece_surface = wit_paard
                    case "HIMAR":
                        piece_surface = wit_HIMAR
                    case "ruiter":
                        piece_surface = wit_ruiter
                    case "paus":
                        piece_surface = wit_paus
                    case "NBRF":
                        piece_surface = wit_NBRF
                    case "Kasteel":
                        piece_surface = wit_kasteel
                    case "Tank":
                        piece_surface = wit_tank
                    case "Apostel":
                        piece_surface = wit_missionaris
                    case "Jezus":
                        piece_surface = wit_jezus
                    case "God":
                        piece_surface = wit_god
                    case 'pionT2':
                        piece_surface = wit_pion2
                    case 'pionT3':
                        piece_surface = wit_pion3
                    case 'pionT4':
                        piece_surface = wit_pion4
                    case 'pionT5':
                        piece_surface = wit_pion5
                    case 'bewoond kasteel':
                        piece_surface = wit_bewoond_kasteel
                    case 'dameskasteel':
                        piece_surface = wit_dameskasteel
                    case 'LGBTQIA2S+Kasteel':
                        piece_surface = wit_LGBTQIA2SplusKasteel
                    case 'Lenin':
                        piece_surface = wit_Lenin
                    case 'peasant':
                        piece_surface = wit_peasant
                    case 'ICBM missle launcher':
                        piece_surface = wit_ICBM_missle_launcer
                    case 'Stalin':
                        piece_surface = wit_stalin
                    case 'Railgun':
                        piece_surface = wit_railgun
                    case 'guillotine':
                        piece_surface = wit_Guillotine
                    case 'bagguette':
                        piece_surface = wit_bagguette
                    case 'napoleon':
                        piece_surface = wit_napoleon
                    case 'furry':
                        piece_surface = wit_furry
                    case 'paardatron':
                        piece_surface = wit_paardatron
                    case 'paardatron2000':
                        piece_surface = wit_paardatron2000
                    case "bass":
                        piece_surface = wit_bass
                    case "bastille":
                        piece_surface = wit_bastille
                    case "mimespeler":
                        piece_surface = wit_mimespeler
                    case "soldier":
                        piece_surface = wit_soldier
                    case "secret agent":
                        piece_surface = wit_secret_agent
                    case "helicopter":
                        piece_surface = wit_helicopter
                    case "Stalin Prime":
                        piece_surface = wit_stalin_prime
                    case "Lenin Prime":
                        piece_surface = wit_lenin_prime
                    case "renner":
                        piece_surface = wit_renner
            else:
                match piece.piece:
                    case "none":
                        draw_hp = False
                    case "pion":
                        piece_surface = zwart_pion
                    case "koning":
                        piece_surface = zwart_koning
                    case "loper":
                        piece_surface = zwart_loper
                    case "toren":
                        piece_surface = zwart_toren
                    case "dame":
                        piece_surface = zwart_dame
                    case "paard":
                        if piece.snor:
                            piece_surface = zwart_paard_snor
                        else:
                            piece_surface = zwart_paard
                    case "HIMAR":
                        piece_surface = zwart_HIMAR
                    case "ruiter":
                        piece_surface = zwart_ruiter
                    case "paus":
                        piece_surface = zwart_paus
                    case "NBRF":
                        piece_surface = zwart_NBRF
                    case "Kasteel":
                        piece_surface = zwart_kasteel
                    case "Tank":
                        piece_surface = zwart_tank
                    case "Apostel":
                        piece_surface = zwart_missionaris
                    case "Jezus":
                        piece_surface = zwart_jezus
                    case "God":
                        piece_surface = zwart_god
                    case 'pionT2':
                        piece_surface = zwart_pion2
                    case 'pionT3':
                        piece_surface = zwart_pion3
                    case 'pionT4':
                        piece_surface = zwart_pion4
                    case 'pionT5':
                        piece_surface = zwart_pion5
                    case 'bewoond kasteel':
                        piece_surface = zwart_bewoond_kasteel
                    case 'dameskasteel':
                        piece_surface = zwart_dameskasteel
                    case 'LGBTQIA2S+Kasteel':
                        piece_surface = zwart_LGBTQIA2SplusKasteel
                    case 'Lenin':
                        piece_surface = zwart_Lenin
                    case 'peasant':
                        piece_surface = zwart_peasant
                    case 'ICBM missle launcher':
                        piece_surface = zwart_ICBM_missle_launcer
                    case 'Joe Biden':
                        piece_surface = zwart_joe_biden
                    case 'Obama':
                        piece_surface = zwart_Obama
                    case 'Railgun':
                        piece_surface = zwart_railgun
                    case 'guillotine':
                        piece_surface = zwart_Guillotine
                    case 'bagguette':
                        piece_surface = zwart_bagguette
                    case 'napoleon':
                        piece_surface = zwart_napoleon
                    case 'furry':
                        piece_surface = zwart_furry
                    case 'paardatron':
                        piece_surface = zwart_paardatron
                    case 'paardatron2000':
                        piece_surface = zwart_paardatron2000
                    case 'bass':
                        piece_surface = zwart_bass
                    case 'bastille':
                        piece_surface = zwart_bastille
                    case 'mimespeler':
                        piece_surface = zwart_mimespeler
                    case 'helicopter':
                        piece_surface = zwart_helicopter
                    case 'Stalin':
                        piece_surface = zwart_stalin
                    case 'Stalin Prime':
                        piece_surface = zwart_stalin_prime
                    case "Lenin Prime":
                        piece_surface = zwart_lenin_prime
                    case 'renner':
                        piece_surface = zwart_renner

            if not piece.piece == "none" and not piece_surface == None:
                if not piece.boss_piece and not piece.smoll_guy:
                    screen.blit(piece_surface, (i * 100, j * 100, 100, 100))
                    pygame.draw.rect(screen, (255, 0, 0), (i * 100 + 20, j * 100 + 75, 60, 20))
                    pygame.draw.rect(screen, (0, 255, 0),
                                     (i * 100 + 20, j * 100 + 75, 60 * (piece.hp / piece.max_hp), 20))
                    screen.blit(font.render(str(piece.hp), True, (0, 0, 255)), (i * 100 + 20, j * 100 + 65, 60, 20))
                elif piece.smoll_guy:
                    screen.blit(piece_surface, (i * 100 + 10, j * 100 + 10, 100, 100))
                    pygame.draw.rect(screen, (255, 0, 0), (i * 100 + 20, j * 100 + 75, 60, 20))
                    pygame.draw.rect(screen, (0, 255, 0),
                                     (i * 100 + 20, j * 100 + 75, 60 * (piece.hp / piece.max_hp), 20))
                    screen.blit(font.render(str(piece.hp), True, (0, 0, 255)), (i * 100 + 20, j * 100 + 65, 60, 20))

                else:
                    screen.blit(piece_surface, (i * 100 - 25, j * 100 - 25, 100, 100))
                    pygame.draw.rect(screen, (255, 0, 0), (i * 100 + 20, j * 100 + 75, 60, 20))
                    pygame.draw.rect(screen, (0, 255, 0),
                                     (i * 100 + 20, j * 100 + 75, 60 * (piece.hp / piece.max_hp), 20))
                    screen.blit(font.render(str(piece.hp), True, (0, 0, 255)), (i * 100 + 20, j * 100 + 65, 60, 20))
                # aan zet
    if nathan_chess_game.wit_aan_de_buurt:
        screen.blit(font.render("Wit aan zet!", True, (0, 0, 0)), (820, 20))
    else:
        screen.blit(font.render("Zwart aan zet!", True, (0, 0, 0)), (820, 20))

    # sacraficial text
    screen.blit(font_small.render("zwart: sacraficial pawns", True, (0, 0, 0)), (810, 160))

    # draw sacraficial pawns
    screen.blit(sacraficial_pawn_empty, (810, 180))
    screen.blit(sacraficial_pawn_empty, (840, 180))
    screen.blit(sacraficial_pawn_empty, (870, 180))
    screen.blit(sacraficial_pawn_empty, (900, 180))
    screen.blit(sacraficial_pawn_empty, (930, 180))

    for i in range(nathan_chess_game.zwart_sacraficial_pawns):
        screen.blit(sacraficial_pawn_full, (810 + (i * 30), 180))

    # sacraficial text
    screen.blit(font_small.render("wit: sacraficial pawns", True, (0, 0, 0)), (810, 580))

    # draw sacraficial pawns
    screen.blit(sacraficial_pawn_empty, (810, 600))
    screen.blit(sacraficial_pawn_empty, (840, 600))
    screen.blit(sacraficial_pawn_empty, (870, 600))
    screen.blit(sacraficial_pawn_empty, (900, 600))
    screen.blit(sacraficial_pawn_empty, (930, 600))

    for i in range(nathan_chess_game.wit_sacraficial_pawns):
        screen.blit(sacraficial_pawn_full, (810 + (i * 30), 600))
