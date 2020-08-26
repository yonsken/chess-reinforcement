import sys, pygame, os

def draw_background():
    is_next_tile_dark = False
    for x in range(8):
        for y in range(8):
            if (is_next_tile_dark):
                screen.blit(dark_tile_scaled,
                            (x * tile_side_length, y * tile_side_length))
            else:
                screen.blit(light_tile_scaled,
                            (x * tile_side_length, y * tile_side_length))
            is_next_tile_dark = not is_next_tile_dark
        is_next_tile_dark = not is_next_tile_dark


def draw_pieces():
    for x in range(8):
        for y in range(8):
            piece = chess_board.board_grid[x][y]
            if (piece is not None):
                screen.blit(piece.get_image(),
                            (y * tile_side_length, x * tile_side_length))

class Piece:
    def __init__(self, is_white):
        self.is_white = is_white
        self.image = None

    def move(self):
        pass

    def get_image(self):
        return self.image

class Pawn(Piece):
    def __init__(self, is_white):
        super().__init__(is_white)
        if is_white:
            self.image = pawn_white_scaled
        else:
            self.image = pawn_black_scaled

        self.hasMoved = False

    #def move(self):
        #if not hasMoved:

class Knight(Piece):
    def __init__(self, is_white):
        super().__init__(is_white)
        if is_white:
            self.image = knight_white_scaled
        else:
            self.image = knight_black_scaled

class Bishop(Piece):
    def __init__(self, is_white):
        super().__init__(is_white)
        if is_white:
            self.image = bishop_white_scaled
        else:
            self.image = bishop_black_scaled

class Rook(Piece):
    def __init__(self, is_white):
        super().__init__(is_white)
        if is_white:
            self.image = rook_white_scaled
        else:
            self.image = rook_black_scaled

class Queen(Piece):
    def __init__(self, is_white):
        super().__init__(is_white)
        if is_white:
            self.image = queen_white_scaled
        else:
            self.image = queen_black_scaled

class King(Piece):
    def __init__(self, is_white):
        super().__init__(is_white)
        if is_white:
            self.image = king_white_scaled
        else:
            self.image = king_black_scaled

class Board():
    def __init__(self):
        self.board_grid = [[None] * 8 for i in range(8)] 

        is_white_side = False
        for row in [0, 7]:
            self.board_grid[row][0] = Rook(is_white=is_white_side)
            self.board_grid[row][1] = Knight(is_white=is_white_side)
            self.board_grid[row][2] = Bishop(is_white=is_white_side)
            self.board_grid[row][3] = Queen(is_white=is_white_side)
            self.board_grid[row][4] = King(is_white=is_white_side)
            self.board_grid[row][5] = Bishop(is_white=is_white_side)
            self.board_grid[row][6] = Knight(is_white=is_white_side)
            self.board_grid[row][7] = Rook(is_white=is_white_side)
            is_white_side = True
    
        for column in range(8):
            self.board_grid[1][column] = Pawn(is_white=False)
            self.board_grid[6][column] = Pawn(is_white=True)

        #print(self.board_grid)
        self.active_piece = None


        
current_path = os.path.dirname(__file__)
assets_path = os.path.join(current_path, 'assets')
board_path = os.path.join(assets_path, 'board_elements')

# Initialize the pygame modules
pygame.init()

# Define constants and variables
tile_side_length = 64
screen_size = (tile_side_length * 8, tile_side_length * 8)

screen = pygame.display.set_mode(screen_size)

# Load resources
dark_tile = pygame.image.load(os.path.join(
    board_path, "brown_tile.png")).convert()
light_tile = pygame.image.load(os.path.join(
    board_path, "clay_tile.png")).convert()

dark_tile_scaled = pygame.transform.scale(
    dark_tile, (tile_side_length, tile_side_length))
light_tile_scaled = pygame.transform.scale(
    light_tile, (tile_side_length, tile_side_length))


pawn_white = pygame.image.load(os.path.join(
    board_path, "white_pawn.png")).convert_alpha()
pawn_black = pygame.image.load(os.path.join(
    board_path, "black_pawn.png")).convert_alpha()
knight_white = pygame.image.load(os.path.join(
    board_path, "white_knight.png")).convert_alpha()
knight_black = pygame.image.load(os.path.join(
    board_path, "black_knight.png")).convert_alpha()
bishop_white = pygame.image.load(os.path.join(
    board_path, "white_bishop.png")).convert_alpha()
bishop_black = pygame.image.load(os.path.join(
    board_path, "black_bishop.png")).convert_alpha()
rook_white = pygame.image.load(os.path.join(
    board_path, "white_rook.png")).convert_alpha()
rook_black = pygame.image.load(os.path.join(
    board_path, "black_rook.png")).convert_alpha()
queen_white = pygame.image.load(os.path.join(
    board_path, "white_queen.png")).convert_alpha()
queen_black = pygame.image.load(os.path.join(
    board_path, "black_queen.png")).convert_alpha()
king_white = pygame.image.load(os.path.join(
    board_path, "white_king.png")).convert_alpha()
king_black = pygame.image.load(os.path.join(
    board_path, "black_king.png")).convert_alpha()

"""
pawn_white_scaled = pygame.transform.scale(
    pawn_white, (int(tile_side_length * pawn_white.get_width()
                     / pawn_white.get_height()), tile_side_length))
"""
pawn_white_scaled = pygame.transform.scale(
    pawn_white, (tile_side_length, tile_side_length))
pawn_black_scaled = pygame.transform.scale(
    pawn_black, (tile_side_length, tile_side_length))
knight_white_scaled = pygame.transform.scale(
    knight_white, (tile_side_length, tile_side_length))
knight_black_scaled = pygame.transform.scale(
    knight_black, (tile_side_length, tile_side_length))
bishop_white_scaled = pygame.transform.scale(
    bishop_white, (tile_side_length, tile_side_length))
bishop_black_scaled = pygame.transform.scale(
    bishop_black, (tile_side_length, tile_side_length))
rook_white_scaled = pygame.transform.scale(
    rook_white, (tile_side_length, tile_side_length))
rook_black_scaled = pygame.transform.scale(
    rook_black, (tile_side_length, tile_side_length))
queen_white_scaled = pygame.transform.scale(
    queen_white, (tile_side_length, tile_side_length))
queen_black_scaled = pygame.transform.scale(
    queen_black, (tile_side_length, tile_side_length))
king_white_scaled = pygame.transform.scale(
    king_white, (tile_side_length, tile_side_length))
king_black_scaled = pygame.transform.scale(
    king_black, (tile_side_length, tile_side_length))



# Prepare the representation of the chess board and all current positions of
# the chess pieces in the game

chess_board = Board()
draw_background()
draw_pieces()
pygame.display.update()

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            #print(mouse_x, mouse_y)
            grid_x = int(mouse_x / tile_side_length)
            grid_y = int(mouse_y / tile_side_length)
            print(grid_x, grid_y)

