import sys, pygame, os

def load_image(image_name):
    full_name = os.path.join(board_path, image_name)
    try:
        image = pygame.image.load(full_name)
    except pygame.error as message:
        print('Cannot load image: ', image_name)
        raise SystemExit(message)
    image = image.convert_alpha()
    image_scaled = pygame.transform.scale(
        image, (tile_side_px, tile_side_px))
    return image_scaled, image_scaled.get_rect()


def draw_chess_board(screen_coordinates):
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

    x_screen, y_screen = screen_coordinates
    screen.blit(board, (x_screen, y_screen))



class Piece(pygame.sprite.Sprite):
    def __init__(self, image_name, is_white, is_up):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image(image_name)
        self.is_white = is_white
        self.is_up = is_up

    def get_image(self):
        return self.image

class Pawn(Piece):
    def __init__(self, is_white, is_up):
        if is_white:
            image_name = "white_pawn.png"
        else:
            image_name = "black_pawn.png"
        super().__init__(image_name, is_white, is_up)

        self.has_moved = False

class Knight(Piece):
    def __init__(self, is_white, is_up):
        if is_white:
            image_name = "white_knight.png"
        else:
            image_name = "black_knight.png"
        super().__init__(image_name, is_white, is_up)

class Bishop(Piece):
    def __init__(self, is_white, is_up):
        if is_white:
            image_name = "white_bishop.png"
        else:
            image_name = "black_bishop.png"
        super().__init__(image_name, is_white, is_up)

class Rook(Piece):
    def __init__(self, is_white, is_up):
        if is_white:
            image_name = "white_rook.png"
        else:
            image_name = "black_rook.png"
        super().__init__(image_name, is_white, is_up)

class Queen(Piece):
    def __init__(self, is_white, is_up):
        if is_white:
            image_name = "white_queen.png"
        else:
            image_name = "black_queen.png"
        super().__init__(image_name, is_white, is_up)

class King(Piece):
    def __init__(self, is_white, is_up):
        if is_white:
            image_name = "white_king.png"
        else:
            image_name = "black_king.png"
        super().__init__(image_name, is_white, is_up)

class Board():
    def __init__(self):
        self.board_grid = [[None] * 8 for i in range(8)] 
        self.reset_board()

    def reset_board(self):
        self.board_grid[0][0] = Rook(is_white=False, is_up=True)
        self.board_grid[1][0] = Knight(is_white=False, is_up=True)
        self.board_grid[2][0] = Bishop(is_white=False, is_up=True)
        self.board_grid[3][0] = Queen(is_white=False, is_up=True)
        self.board_grid[4][0] = King(is_white=False, is_up=True)
        self.board_grid[5][0] = Bishop(is_white=False, is_up=True)
        self.board_grid[6][0] = Knight(is_white=False, is_up=True)
        self.board_grid[7][0] = Rook(is_white=False, is_up=True)
    
        for column in range(8):
            self.board_grid[column][1] = Pawn(is_white=False, is_up=True)
            self.board_grid[column][6] = Pawn(is_white=True, is_up=False)

        self.board_grid[0][7] = Rook(is_white=True, is_up=False)
        self.board_grid[1][7] = Knight(is_white=True, is_up=False)
        self.board_grid[2][7] = Bishop(is_white=True, is_up=False)
        self.board_grid[3][7] = Queen(is_white=True, is_up=False)
        self.board_grid[4][7] = King(is_white=True, is_up=False)
        self.board_grid[5][7] = Bishop(is_white=True, is_up=False)
        self.board_grid[6][7] = Knight(is_white=True, is_up=False)
        self.board_grid[7][7] = Rook(is_white=True, is_up=False)

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

    def get_active_piece_available_moves(self):
        if self.active_piece is not None:
            x_pos, y_pos = self.active_piece_coordinates
            available_moves = []

            if isinstance(self.active_piece, Pawn):
                if self.active_piece.is_up:
                    dir_sign = 1
                else:
                    dir_sign = -1

                move_position = (x_pos, y_pos + dir_sign)
                if not self.has_piece_on_position(move_position):
                    self.check_and_add_position(
                        available_moves, move_position)

                    double_move_pos = (x_pos, y_pos + dir_sign * 2)
                    if not self.active_piece.has_moved and not self.has_piece_on_position(double_move_pos):
                        self.check_and_add_position(
                            available_moves, double_move_pos)

                possible_attack_positions = [
                    (x_pos + 1, y_pos + dir_sign), (x_pos - 1, y_pos + dir_sign)]

                for position in possible_attack_positions:
                    if self.is_valid_position(position) and self.has_piece_on_position(position):
                        other_piece = self.get_piece_at_position(position)
                        if self.are_pieces_enemies(self.active_piece, other_piece):
                            self.add_position(available_moves, position)


            elif isinstance(self.active_piece, Knight):
                for offset_1 in [-2, 2]:
                    for offset_2 in [-1, 1]:
                        self.check_and_add_position(
                            available_moves, (x_pos + offset_1, y_pos + offset_2))
                        self.check_and_add_position(
                            available_moves, (x_pos + offset_2, y_pos + offset_1))

            elif isinstance(self.active_piece, Bishop):
                for x_offset in [-1, 1]:
                    for y_offset in [-1, 1]:
                        x_piece, y_piece = self.active_piece_coordinates
                        x, y = x_piece + x_offset, y_piece + y_offset
                        position = (x, y)

                        has_reached_obstacle = False
                        while self.is_valid_position(position) and not has_reached_obstacle:
                            self.add_position(available_moves, position)
                            
                            if self.has_piece_on_position(position):
                                has_reached_obstacle = True

                            x, y = x + x_offset, y + y_offset
                            position = (x, y)

            elif isinstance(self.active_piece, Rook):
                offsets = [(0, 1), (0, -1), (1, 0), (-1, 0)]
                for offset in offsets:
                    x_offset, y_offset = offset
                    x_piece, y_piece = self.active_piece_coordinates
                    x, y = x_piece + x_offset, y_piece + y_offset
                    position = (x, y)

                    has_reached_obstacle = False
                    while self.is_valid_position(position) and not has_reached_obstacle:
                        self.add_position(available_moves, position)

                        if self.has_piece_on_position(position):
                            has_reached_obstacle = True

                        x, y = x + x_offset, y + y_offset
                        position = (x, y)

            elif isinstance(self.active_piece, Queen):
                for x_offset in [-1, 0, 1]:
                    for y_offset in [-1, 0, 1]:
                        if x_offset == 0 and y_offset == 0:
                            pass

                        x_piece, y_piece = self.active_piece_coordinates
                        x, y = x_piece + x_offset, y_piece + y_offset
                        position = (x, y)

                        has_reached_obstacle = False
                        while self.is_valid_position(position) and not has_reached_obstacle:
                            self.add_position(available_moves, position)

                            if self.has_piece_on_position(position):
                                has_reached_obstacle = True

                            x, y = x + x_offset, y + y_offset
                            position = (x, y)

            elif isinstance(self.active_piece, King):
                for x_offset in [-1, 0, 1]:
                    for y_offset in [-1, 0, 1]:
                        if x_offset == 0 and y_offset == 0:
                            pass

                        x_piece, y_piece = self.active_piece_coordinates
                        x, y = x_piece + x_offset, y_piece + y_offset
                        position = (x, y)

                        self.check_and_add_position(available_moves, position)
            
            print(available_moves)
            return available_moves
        else:
            return None

    def add_position(self, pos_list, coordinates):
        if not self.has_piece_on_position(coordinates):
                pos_list.append(coordinates)
        else:
            other_piece = self.get_piece_at_position(coordinates)
            if self.are_pieces_enemies(self.active_piece, other_piece):
                pos_list.append(coordinates)

    def check_and_add_position(self, pos_list, coordinates):
        if self.is_valid_position(coordinates):
            self.add_position(pos_list, coordinates)

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
        self.board_grid[x_target][y_target] = self.active_piece
        self.board_grid[x_start][y_start] = None

        if isinstance(self.active_piece, Pawn):
            if self.active_piece.has_moved == False:
                self.active_piece.has_moved = True

    def reset_active_piece(self):
        self.active_piece = None
        self.active_piece_coordinates = None
        self.active_piece_moves = None
        

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
clock = pygame.time.Clock()

# Load resources
dark_tile = pygame.image.load(os.path.join(
    board_path, "brown_tile.png")).convert()
light_tile = pygame.image.load(os.path.join(
    board_path, "clay_tile.png")).convert()
move_tile = pygame.image.load(os.path.join(
    board_path, "lgray_tile.png")).convert()

dark_tile_scaled = pygame.transform.scale(
    dark_tile, (tile_side_px, tile_side_px))
light_tile_scaled = pygame.transform.scale(
    light_tile, (tile_side_px, tile_side_px))
move_tile_scaled = pygame.transform.scale(
    move_tile, (tile_side_px, tile_side_px))

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

"""
pawn_white_scaled = pygame.transform.scale(
    pawn_white, (int(tile_side_px * pawn_white.get_width()
                     / pawn_white.get_height()), tile_side_px))
"""

# Prepare the representation of the chess board and all current positions of
# the chess pieces in the game

chess_board = Board()
draw_chess_board(board_pos)

#draw_chess_board((0, 0))
pygame.display.update()

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if board_rect.collidepoint(event.pos):
                mouse_x, mouse_y = mouse_pos

                grid_x = int((mouse_x - board_x) / tile_side_px)
                grid_y = int((mouse_y - board_y) / tile_side_px)
                coordinates = (grid_x, grid_y)
                
                if chess_board.active_piece is not None:
                    if coordinates in chess_board.active_piece_moves:
                        chess_board.move_active_piece(coordinates)
                        chess_board.reset_active_piece()
                    elif chess_board.has_piece_on_position(coordinates):
                        chess_board.set_active_piece(coordinates)
                    else:
                        chess_board.reset_active_piece()

                elif chess_board.has_piece_on_position(coordinates):
                    chess_board.set_active_piece(coordinates)
                    
                draw_chess_board(board_pos)
                #draw_chess_board((0, 0))
                pygame.display.flip()

    clock.tick(60)

