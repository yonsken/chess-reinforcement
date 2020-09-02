import sys, pygame, os
from scipy import ndimage
import pygame.surfarray as surfarray
import numpy as np

def load_image(image_name, has_transparency=True, is_board_element=True):
    full_name = os.path.join(board_path, image_name)
    try:
        image = pygame.image.load(full_name)
    except pygame.error as message:
        print('Cannot load image: ', image_name)
        raise SystemExit(message)
    if has_transparency:
        image = image.convert_alpha()
    else:
        image = image.convert()
    if is_board_element:
        image = pygame.transform.scale(
            image, (tile_side_px, tile_side_px))
    return image, image.get_rect()

def get_updated_chess_board_surface():
    board = board_backround.copy()

    if chess_board.active_piece is not None:
        x, y = chess_board.active_piece_coordinates
        board.blit(move_tile_scaled,
                   (x * tile_side_px, y * tile_side_px), special_flags=pygame.BLEND_ADD)

        available_moves = chess_board.active_piece_moves
        for move_coordinates in available_moves:
            x, y = move_coordinates
            board.blit(move_tile_scaled,
                       (x * tile_side_px, y * tile_side_px), special_flags=pygame.BLEND_ADD)
    for y in range(8):
        for x in range(8):
            piece = chess_board.board_grid[x][y]
            if piece is not None:
                board.blit(piece.get_image(),
                            (x * tile_side_px, y * tile_side_px))

    return board

def draw_chess_board(screen_coordinates):
    board = get_updated_chess_board_surface()
    x_screen, y_screen = screen_coordinates
    screen.blit(board, (x_screen, y_screen))

def draw_blurred_chess_board(screen_coordinates):
    x_screen, y_screen = screen_coordinates
    screen.blit(board_blurred, (x_screen, y_screen))

class Piece(pygame.sprite.Sprite):
    def __init__(self, image_name, board_pos, is_white, is_up):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image(image_name)
        self.board_pos = board_pos
        self.is_white = is_white
        self.is_up = is_up

    def get_image(self):
        return self.image

class Pawn(Piece):
    def __init__(self, board_pos, is_white, is_up):
        if is_white:
            image_name = "white_pawn.png"
        else:
            image_name = "black_pawn.png"
        super().__init__(image_name, board_pos, is_white, is_up)

        self.has_moved = False

class Knight(Piece):
    def __init__(self, board_pos, is_white, is_up):
        if is_white:
            image_name = "white_knight.png"
        else:
            image_name = "black_knight.png"
        super().__init__(image_name, board_pos, is_white, is_up)

class Bishop(Piece):
    def __init__(self, board_pos, is_white, is_up):
        if is_white:
            image_name = "white_bishop.png"
        else:
            image_name = "black_bishop.png"
        super().__init__(image_name, board_pos, is_white, is_up)

class Rook(Piece):
    def __init__(self, board_pos, is_white, is_up):
        if is_white:
            image_name = "white_rook.png"
        else:
            image_name = "black_rook.png"
        super().__init__(image_name, board_pos, is_white, is_up)

class Queen(Piece):
    def __init__(self, board_pos, is_white, is_up):
        if is_white:
            image_name = "white_queen.png"
        else:
            image_name = "black_queen.png"
        super().__init__(image_name, board_pos, is_white, is_up)

class King(Piece):
    def __init__(self, board_pos, is_white, is_up):
        if is_white:
            image_name = "white_king.png"
        else:
            image_name = "black_king.png"
        super().__init__(image_name, board_pos, is_white, is_up)

class Board():
    def __init__(self):
        self.board_grid = [[None] * 8 for i in range(8)]
        self.pieces = pygame.sprite.Group()
        self.reset_board()

    def reset_board(self):
        self.board_grid[0][0] = Rook((0, 0), is_white=False, is_up=True)
        self.pieces.add(self.board_grid[0][0])
        self.board_grid[1][0] = Knight((1, 0), is_white=False, is_up=True)
        self.pieces.add(self.board_grid[1][0])
        self.board_grid[2][0] = Bishop((2, 0), is_white=False, is_up=True)
        self.pieces.add(self.board_grid[2][0])
        self.board_grid[3][0] = Queen((3, 0), is_white=False, is_up=True)
        self.pieces.add(self.board_grid[3][0])
        self.board_grid[4][0] = King((4, 0), is_white=False, is_up=True)
        self.pieces.add(self.board_grid[4][0])
        self.king_black = self.board_grid[4][0]
        self.board_grid[5][0] = Bishop((5, 0), is_white=False, is_up=True)
        self.pieces.add(self.board_grid[5][0])
        self.board_grid[6][0] = Knight((6, 0), is_white=False, is_up=True)
        self.pieces.add(self.board_grid[6][0])
        self.board_grid[7][0] = Rook((7, 0), is_white=False, is_up=True)
        self.pieces.add(self.board_grid[7][0])
    
        for column in range(8):
            self.board_grid[column][1] = Pawn(
                (column, 1), is_white=False, is_up=True)
            self.pieces.add(self.board_grid[column][1])
            self.board_grid[column][6] = Pawn(
                (column, 6), is_white=True, is_up=False)
            self.pieces.add(self.board_grid[column][6])

        self.board_grid[0][7] = Rook((0, 7), is_white=True, is_up=False)
        self.pieces.add(self.board_grid[0][7])
        self.board_grid[1][7] = Knight((1, 7), is_white=True, is_up=False)
        self.pieces.add(self.board_grid[1][7])
        self.board_grid[2][7] = Bishop((2, 7), is_white=True, is_up=False)
        self.pieces.add(self.board_grid[2][7])
        self.board_grid[3][7] = Queen((3, 7), is_white=True, is_up=False)
        self.pieces.add(self.board_grid[3][7])
        self.board_grid[4][7] = King((4, 7), is_white=True, is_up=False)
        self.pieces.add(self.board_grid[4][7])
        self.king_white = self.board_grid[4][7]
        self.board_grid[5][7] = Bishop((5, 7), is_white=True, is_up=False)
        self.pieces.add(self.board_grid[5][7])
        self.board_grid[6][7] = Knight((6, 7), is_white=True, is_up=False)
        self.pieces.add(self.board_grid[6][7])
        self.board_grid[7][7] = Rook((7, 7), is_white=True, is_up=False)
        self.pieces.add(self.board_grid[7][7])

        self.active_piece = None
        self.active_piece_coordinates = None

    def has_piece_on_position(self, coordinates):
        x, y = coordinates
        return self.board_grid[x][y] is not None

    def set_active_piece(self, coordinates):
        x, y = coordinates
        self.active_piece = self.board_grid[x][y]
        self.active_piece_coordinates = coordinates
        self.active_piece_moves = self.get_active_piece_available_moves()

    def get_piece_available_moves(self, piece):
        x_pos, y_pos = piece.board_pos
        available_moves = []

        if isinstance(piece, Pawn):
            if piece.is_up:
                dir_sign = 1
            else:
                dir_sign = -1

            move_position = (x_pos, y_pos + dir_sign)
            if not self.has_piece_on_position(move_position):
                self.check_and_add_position(
                    available_moves, move_position, piece)

                double_move_pos = (x_pos, y_pos + dir_sign * 2)
                if not piece.has_moved and not self.has_piece_on_position(double_move_pos):
                    self.check_and_add_position(
                        available_moves, double_move_pos, piece)

            possible_attack_positions = [
                (x_pos + 1, y_pos + dir_sign), (x_pos - 1, y_pos + dir_sign)]

            for position in possible_attack_positions:
                if self.is_valid_position(position) and self.has_piece_on_position(position):
                    other_piece = self.get_piece_at_position(position)
                    if self.are_pieces_enemies(piece, other_piece):
                        self.add_position(available_moves, position, piece)

        elif isinstance(piece, Knight):
            for offset_1 in [-2, 2]:
                for offset_2 in [-1, 1]:
                    self.check_and_add_position(
                        available_moves, (x_pos + offset_1, y_pos + offset_2), piece)
                    self.check_and_add_position(
                        available_moves, (x_pos + offset_2, y_pos + offset_1), piece)

        elif isinstance(piece, Bishop):
            for x_offset in [-1, 1]:
                for y_offset in [-1, 1]:
                    x, y = x_pos + x_offset, y_pos + y_offset
                    position = (x, y)

                    has_reached_obstacle = False
                    while self.is_valid_position(position) and not has_reached_obstacle:
                        self.add_position(available_moves, position, piece)

                        if self.has_piece_on_position(position):
                            has_reached_obstacle = True

                        x, y = x + x_offset, y + y_offset
                        position = (x, y)

        elif isinstance(piece, Rook):
            offsets = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            for offset in offsets:
                x_offset, y_offset = offset
                x, y = x_pos + x_offset, y_pos + y_offset
                position = (x, y)

                has_reached_obstacle = False
                while self.is_valid_position(position) and not has_reached_obstacle:
                    self.add_position(available_moves, position, piece)

                    if self.has_piece_on_position(position):
                        has_reached_obstacle = True

                    x, y = x + x_offset, y + y_offset
                    position = (x, y)

        elif isinstance(piece, Queen):
            for x_offset in [-1, 0, 1]:
                for y_offset in [-1, 0, 1]:
                    if x_offset == 0 and y_offset == 0:
                        pass

                    x, y = x_pos + x_offset, y_pos + y_offset
                    position = (x, y)

                    has_reached_obstacle = False
                    while self.is_valid_position(position) and not has_reached_obstacle:
                        self.add_position(available_moves, position, piece)

                        if self.has_piece_on_position(position):
                            has_reached_obstacle = True

                        x, y = x + x_offset, y + y_offset
                        position = (x, y)

        elif isinstance(piece, King):
            for x_offset in [-1, 0, 1]:
                for y_offset in [-1, 0, 1]:
                    if x_offset == 0 and y_offset == 0:
                        pass

                    x, y = x_pos + x_offset, y_pos + y_offset
                    position = (x, y)

                    self.check_and_add_position(available_moves, position, piece)

        print(available_moves)
        return available_moves

    def get_active_piece_available_moves(self):
        return self.get_piece_available_moves(self.active_piece)

    def add_position(self, pos_list, coordinates, moving_piece):
        if not self.has_piece_on_position(coordinates):
                pos_list.append(coordinates)
        else:
            other_piece = self.get_piece_at_position(coordinates)
            if self.are_pieces_enemies(moving_piece, other_piece):
                pos_list.append(coordinates)

    def check_and_add_position(self, pos_list, coordinates, moving_piece):
        if self.is_valid_position(coordinates):
            self.add_position(pos_list, coordinates, moving_piece)

    def get_piece_at_position(self, coordinates):
        x_pos, y_pos = coordinates
        return self.board_grid[x_pos][y_pos]

    def are_pieces_enemies(self, piece_1, piece_2):
        return piece_1.is_white != piece_2.is_white

    def is_valid_position(self, coordinates):
        x_pos, y_pos = coordinates
        return x_pos > -1 and x_pos < 8 and y_pos > -1 and y_pos < 8

    def move_active_piece(self, target_coordinates):
        x_target, y_target = target_coordinates
        x_start, y_start = self.active_piece_coordinates

        piece_at_target = self.get_piece_at_position(target_coordinates)
        if piece_at_target is not None:
            self.pieces.remove(piece_at_target)

        self.board_grid[x_target][y_target] = self.active_piece
        self.active_piece.board_pos = target_coordinates
        self.board_grid[x_start][y_start] = None

        if isinstance(self.active_piece, Pawn):
            if self.active_piece.has_moved == False:
                self.active_piece.has_moved = True

    def reset_active_piece(self):
        self.active_piece = None
        self.active_piece_coordinates = None
        self.active_piece_moves = None

    def is_king_in_check(self, is_king_white):
        if is_king_white:
            king_pos = self.king_white.board_pos
        else:
            king_pos = self.king_black.board_pos

        king_in_check = False
        for piece in self.pieces:
            if piece.is_white != is_king_white:
                print(piece)
                enemy_piece_moves = self.get_piece_available_moves(piece)
                if king_pos in enemy_piece_moves:
                    king_in_check = True
                    break

        return king_in_check


        

current_path = os.path.dirname(__file__)
assets_path = os.path.join(current_path, 'assets')
board_path = os.path.join(assets_path, 'board_elements')

# Initialize the pygame modules
pygame.init()

# Define constants and variables
tile_side_px = 64
screen_size = (1280, 720)
board_y = (720 - tile_side_px * 8) / 2
board_x = board_y
board_pos = (board_x, board_y)

screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Chess with Reinforcement learning")
clock = pygame.time.Clock()

# Load resources
dark_tile_scaled, _ = load_image("brown_tile.png", has_transparency=False)
light_tile_scaled, _ = load_image("clay_tile.png", has_transparency=False)
move_tile_scaled, _ = load_image("lgray_tile.png", has_transparency=False)

background, _ = load_image("background1.jpg", has_transparency=False, is_board_element=False)
background = pygame.transform.scale(background, screen_size)
icon, _ = load_image("icon.png", is_board_element=False)
pygame.display.set_icon(icon)

board_backround = pygame.Surface((tile_side_px * 8, tile_side_px * 8)).convert()
is_next_tile_dark = False
for y in range(8):
    for x in range(8):
        if is_next_tile_dark:
            board_backround.blit(dark_tile_scaled,
                                 (x * tile_side_px, y * tile_side_px))
        else:
            board_backround.blit(light_tile_scaled,
                                 (x * tile_side_px, y * tile_side_px))
        is_next_tile_dark = not is_next_tile_dark
    is_next_tile_dark = not is_next_tile_dark
    
board_rect = board_backround.get_rect()
board_rect.x = board_x
board_rect.y = board_y

border_width = 20
border_size = (tile_side_px * 8 + border_width, tile_side_px * 8 + border_width)
board_border = pygame.Surface(border_size).convert()
board_border.fill((32, 14, 11))
#board_border_rect = board_backround.get_rect()

# Prepare the representation of the chess board and all current positions of
# the chess pieces in the game

chess_board = Board()
board_blurred = get_updated_chess_board_surface()
board_blurred_array = surfarray.pixels3d(board_blurred)
board_blurred_array = ndimage.gaussian_filter(board_blurred_array, sigma=(4, 4, 0))
surfarray.blit_array(board_blurred, board_blurred_array)
board_blurred_rect = board_blurred.get_rect()
board_blurred_rect.x = board_x
board_blurred_rect.y = board_y

screen.blit(background, (0, 0))
screen.blit(board_border, (board_x - border_width /
                           2, board_y - border_width / 2))
draw_blurred_chess_board(board_pos)
pygame.display.flip()

is_game_in_process = False
is_white_turn = True

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if board_rect.collidepoint(event.pos):
                if not is_game_in_process:
                    is_game_in_process = True
                    draw_chess_board(board_pos)
                    pygame.display.flip()
                else:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    grid_x = int((mouse_x - board_x) / tile_side_px)
                    grid_y = int((mouse_y - board_y) / tile_side_px)
                    coordinates = (grid_x, grid_y)
                    
                    if chess_board.active_piece is not None:
                        if coordinates in chess_board.active_piece_moves:
                            chess_board.move_active_piece(coordinates)
                            chess_board.reset_active_piece()
                            is_white_turn = not is_white_turn
                            print(chess_board.is_king_in_check(is_white_turn))
                        elif chess_board.has_piece_on_position(coordinates):
                            piece = chess_board.get_piece_at_position(coordinates)
                            if piece.is_white == is_white_turn:
                                chess_board.set_active_piece(coordinates)
                        else:
                            chess_board.reset_active_piece()

                    elif chess_board.has_piece_on_position(coordinates):
                        piece = chess_board.get_piece_at_position(coordinates)
                        if piece.is_white == is_white_turn:
                            chess_board.set_active_piece(coordinates)
                        
                    draw_chess_board(board_pos)
                    pygame.display.flip()

    clock.tick(60)

