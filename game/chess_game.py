import sys, pygame, os
from scipy import ndimage
import pygame.surfarray as surfarray
import numpy as np
import copy

# ISSUE WITH EXPOSING THE KING TO ATTACKS IF THE KING CAPTURES AN ENEMY PIECE

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
        available_moves = chess_board.active_piece_moves

        if available_moves != set():
            board.blit(move_tile_scaled,
                    (x * tile_side_px, y * tile_side_px), special_flags=pygame.BLEND_ADD)

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
        self.can_be_attacked_enpassant = False

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

        self.has_moved = False

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

        self.has_moved = False

class Board():
    def __init__(self):
        self.board_grid = [[None] * 8 for i in range(8)]
        self.pieces = pygame.sprite.Group()
        self.is_white_turn = True
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

        self.is_king_in_check = False
        self.is_king_in_checkmate = False
        self.stalemate = False

        self.enemy_potential_attack_positions = set()
        self.ally_potential_position = set()

        self.check_save_piece_position_dict = dict()

        self.last_move = None
        self.last_move_removed_piece = None
        self.last_move_was_pieces_first_move = False

    def has_piece_on_position(self, coordinates):
        x, y = coordinates
        return self.board_grid[x][y] is not None

    def set_active_piece(self, coordinates):
        x, y = coordinates
        self.active_piece = self.board_grid[x][y]
        self.active_piece_coordinates = coordinates
        self.active_piece_moves = self.get_active_piece_available_moves()

    def get_piece_available_moves(self, piece, check_king_exposure = True):
        x_pos, y_pos = piece.board_pos
        available_moves = set()

        if isinstance(piece, Pawn):
            if piece.is_up:
                dir_sign = 1
            else:
                dir_sign = -1

            move_position = (x_pos, y_pos + dir_sign)
            self.check_and_add_position(
                available_moves, move_position, piece, check_king_exposure, False)

            double_move_pos = (x_pos, y_pos + dir_sign * 2)
            if not piece.has_moved and self.is_valid_position(move_position) and not self.has_piece_on_position(move_position):
                self.check_and_add_position(
                    available_moves, double_move_pos, piece, check_king_exposure, False)

            possible_attack_positions = [
                (x_pos + 1, y_pos + dir_sign), (x_pos - 1, y_pos + dir_sign)]

            for position in possible_attack_positions:
                if self.is_valid_position(position):
                    if self.has_piece_on_position(position):
                        other_piece = self.get_piece_at_position(position)
                        self.add_position(available_moves, position, piece, check_king_exposure, True)
                    else:  # En passant
                        x_attack, _ = position
                        check_pos = (x_attack, y_pos)
                        if self.is_valid_position(check_pos) and self.has_piece_on_position(check_pos):
                            other_piece = self.get_piece_at_position(
                                check_pos)
                            if isinstance(other_piece, Pawn) and other_piece.can_be_attacked_enpassant:
                                self.add_position(
                                    available_moves, position, piece, check_king_exposure, True)

        elif isinstance(piece, Knight):
            for offset_1 in [-2, 2]:
                for offset_2 in [-1, 1]:
                    self.check_and_add_position(
                        available_moves, (x_pos + offset_1, y_pos + offset_2), piece, check_king_exposure)
                    self.check_and_add_position(
                        available_moves, (x_pos + offset_2, y_pos + offset_1), piece, check_king_exposure)

        elif isinstance(piece, Bishop):
            for x_offset in [-1, 1]:
                for y_offset in [-1, 1]:
                    x, y = x_pos + x_offset, y_pos + y_offset
                    position = (x, y)

                    has_reached_obstacle = False
                    while not has_reached_obstacle:
                        self.check_and_add_position(
                            available_moves, position, piece, check_king_exposure)

                        if not self.is_valid_position(position) or self.has_piece_on_position(position):
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
                while not has_reached_obstacle:
                    self.check_and_add_position(
                        available_moves, position, piece, check_king_exposure)

                    if not self.is_valid_position(position) or self.has_piece_on_position(position):
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
                    while not has_reached_obstacle:
                        self.check_and_add_position(
                            available_moves, position, piece, check_king_exposure)

                        if not self.is_valid_position(position) or self.has_piece_on_position(position):
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
                    self.check_and_add_position(
                        available_moves, position, piece, check_king_exposure)

            # We don't have to check for the king being in check since a
            # different procedure is used for finding available piece moves,
            # when king is in check (not get_piece_available_moves())
            if not piece.has_moved:
                piece_right = self.get_piece_at_position((x_pos + 3, y_pos))
                piece_left = self.get_piece_at_position((x_pos - 4, y_pos))
                pieces = [piece_right, piece_left]

                for castle_piece in pieces:
                    if isinstance(castle_piece, Rook) and not self.are_pieces_enemies(piece, castle_piece) and not castle_piece.has_moved:
                        x_castle, _ = castle_piece.board_pos
                        no_pieces_inbetween = True
                        for x in range(min(x_castle, x_pos) + 1, max(x_castle, x_pos)):
                            if self.get_piece_at_position((x, y_pos)) is not None:
                                no_pieces_inbetween = False
                                break
                        
                        if no_pieces_inbetween:
                            if min(x_castle, x_pos) == x_pos:
                                x = x_pos + 2
                                x_rook = x_pos + 1
                            else:
                                x = x_pos - 2
                                x_rook = x_pos - 1
                        
                            position = (x, y_pos)
                            # We need to check that we do not pass a square that
                            # is under attack, and that we do not move into check
                            # as per the required conditions for castling
                            if (x_rook, y_pos) not in self.enemy_potential_attack_positions:
                                self.check_and_add_position(
                                    available_moves, position, piece, check_king_exposure)

        return available_moves

    def get_active_piece_available_moves(self):
        if not self.is_king_in_check:
            return self.get_piece_available_moves(self.active_piece)
        else:
            if self.active_piece in self.check_save_piece_position_dict:
                return self.check_save_piece_position_dict[self.active_piece]
            else:
                return set()

    def add_position(self, pos_list, coordinates, moving_piece, check_king_exposure, can_attack):
        if not self.has_piece_on_position(coordinates):

            if check_king_exposure:
                if not self.does_move_expose_king(moving_piece, coordinates): ### !!!
                    pos_list.add(coordinates)
            else:
                pos_list.add(coordinates)


            #pos_list.add(coordinates)
        elif can_attack:
            other_piece = self.get_piece_at_position(coordinates)
            if self.are_pieces_enemies(moving_piece, other_piece):

                if check_king_exposure:
                    if not self.does_move_expose_king(moving_piece, coordinates): 
                        pos_list.add(coordinates)
                else:
                    pos_list.add(coordinates)


                #pos_list.add(coordinates)

    def check_and_add_position(self, pos_list, coordinates, moving_piece, check_king_exposure, can_attack = True):
        if self.is_valid_position(coordinates):
            # For kings we need to check that a move does not result in a king 
            # being in check
            if isinstance(moving_piece, King):
                if coordinates not in self.enemy_potential_attack_positions: ### ISSUE WITH KING AND A PAWN
                    self.add_position(pos_list, coordinates,
                                      moving_piece, check_king_exposure, can_attack)
            else:
                self.add_position(pos_list, coordinates,
                                  moving_piece, check_king_exposure, can_attack)

            
    def get_piece_at_position(self, coordinates):
        x_pos, y_pos = coordinates
        return self.board_grid[x_pos][y_pos]

    def are_pieces_enemies(self, piece_1, piece_2):
        return piece_1.is_white != piece_2.is_white

    def is_valid_position(self, coordinates):
        x_pos, y_pos = coordinates
        return x_pos > -1 and x_pos < 8 and y_pos > -1 and y_pos < 8

    def move_piece(self, piece, target_coordinates):
        print("MOVE", piece, piece.board_pos, "=>", target_coordinates)
        x_target, y_target = target_coordinates
        x_start, y_start = piece.board_pos
        # Update the last move
        self.last_move = (piece.board_pos, target_coordinates)

        # Determine if an enemy piece gets removed as a result of this move.
        # In case it does, we need to remove it from both the board and the
        # pieces Group, but also save it as last_move_removed_piece in case
        # we want to revert this move
        piece_at_target = self.get_piece_at_position(target_coordinates)
        # Case 1: a piece on the target position
        if piece_at_target is not None:
            self.last_move_removed_piece = piece_at_target
            self.pieces.remove(piece_at_target)
        # Case 2: en passant special case where a piece gets removed from the
        # board, but not from the target position of the move
        elif isinstance(piece, Pawn) and x_start != x_target:
            removed_pawn = self.get_piece_at_position((x_target, y_start))
            self.last_move_removed_piece = removed_pawn
            self.pieces.remove(removed_pawn)
            self.board_grid[x_target][y_start] = None
        # Case 3: no piece on the target position and not en passant
        else:
            self.last_move_removed_piece = None

        # Move the piece on the board and update its position variable
        self.board_grid[x_target][y_target] = piece
        piece.board_pos = target_coordinates
        self.board_grid[x_start][y_start] = None

        # If this move is a pawn moving two positions then we need to make it
        # vulnerable to en passant
        # This status variable will be updated on the next move of the same
        # colour player for all their pawns
        if isinstance(piece, Pawn) and abs(y_start - y_target) == 2:
            piece.can_be_attacked_enpassant = True

        # Update if a piece moved if it matters for this moving piece
        # Keeping track of the move being first for a special piece is
        # necessary for move reversion
        if (isinstance(piece, Pawn) or isinstance(piece, Rook) or isinstance(piece, King)) and not piece.has_moved:
            self.last_move_was_pieces_first_move = True
            piece.has_moved = True
        else:
            self.last_move_was_pieces_first_move = False

        # Castle move
        # The validity of the move is checked in get_piece_available_moves(),
        # so we don't have to check it again
        if isinstance(piece, King) and (x_target == x_start + 2 or x_target == x_start - 2):
            if x_target == x_start + 2:
                x_rook_start = x_start + 3
                x_rook_finish = x_start + 1
            else:
                x_rook_start = x_start - 4
                x_rook_finish = x_start - 1

            rook = self.get_piece_at_position((x_rook_start, y_target))
            self.board_grid[x_rook_finish][y_target] = rook
            rook.board_pos = (x_rook_finish, y_target)
            self.board_grid[x_rook_start][y_start] = None

            rook.has_moved = True
            

    def revert_last_move(self):
        (x_start, y_start), (x_target, y_target) = self.last_move
        moved_piece = self.board_grid[x_target][y_target]
        self.board_grid[x_start][y_start] = moved_piece

        print("REVERT", moved_piece, (x_target, y_target), "=>", (x_start, y_start))

        moved_piece.board_pos = (x_start, y_start)

        removed_piece = self.last_move_removed_piece
        if removed_piece is not None:
            self.pieces.add(removed_piece)
            # Check if the move was en passant
            x_removed, y_removed = removed_piece.board_pos
            if isinstance(moved_piece, Pawn) and y_removed != y_target:
                self.board_grid[x_target][y_start] = removed_piece
                self.board_grid[x_target][y_target] = None
            else:
                self.board_grid[x_target][y_target] = removed_piece
        else:
            self.board_grid[x_target][y_target] = None

        # En passant
        if isinstance(moved_piece, Pawn) and abs(y_start - y_target) == 2:
            moved_piece.can_be_attacked_enpassant = False

        if (isinstance(moved_piece, Pawn) or isinstance(moved_piece, Rook) or isinstance(moved_piece, King)) and self.last_move_was_pieces_first_move:
            moved_piece.has_moved = False

        if isinstance(moved_piece, King) and (x_start == x_target + 2 or x_start == x_target - 2):
            if x_start == x_target - 2:
                x_rook_start = x_start - 3
                x_rook_finish = x_start - 1
            else:
                x_rook_start = x_start + 4
                x_rook_finish = x_start + 1

            rook = self.get_piece_at_position((x_rook_finish, y_start))
            self.board_grid[x_rook_start][y_start] = rook
            rook.board_pos = (x_rook_start, y_start)
            self.board_grid[x_rook_finish][y_target] = None

            rook.has_moved = False

    def reset_active_piece(self):
        self.active_piece = None
        self.active_piece_coordinates = None
        self.active_piece_moves = None

    def update_enpassant_pawns(self):
        for piece in self.pieces:
            if isinstance(piece, Pawn) and piece.is_white == self.is_white_turn and piece.can_be_attacked_enpassant:
                #print("A pawn can no longer be attacked en passant!")
                piece.can_be_attacked_enpassant = False

    def update_enemy_potential_attack_positions(self, check_king_exposure = True):
        enemy_possible_moves = set()
        for piece in self.pieces:
            if piece.is_white != self.is_white_turn:
                if isinstance(piece, Pawn):
                    x_pos, y_pos = piece.board_pos
                    if piece.is_up:
                        dir_sign = 1
                    else:
                        dir_sign = -1

                    possible_attack_positions = [
                        (x_pos + 1, y_pos + dir_sign), (x_pos - 1, y_pos + dir_sign)]
                    enemy_piece_moves = set()
                    for position in possible_attack_positions:
                        self.check_and_add_position(
                            enemy_piece_moves, position, piece, check_king_exposure)
                else:
                    enemy_piece_moves = self.get_piece_available_moves(
                        piece, check_king_exposure)
                enemy_possible_moves.update(enemy_piece_moves)
        self.enemy_potential_attack_positions = enemy_possible_moves

    def update_is_king_in_check(self):
        if self.is_white_turn:
            king = self.king_white
        else:
            king = self.king_black
        king_pos = king.board_pos

        if king_pos in self.enemy_potential_attack_positions:
            self.is_king_in_check = True
        else:
            self.is_king_in_check = False

    def update_board_status(self):
        if self.is_white_turn:
            king = self.king_white
        else:
            king = self.king_black
        king_pos = king.board_pos

        # Update all pawns of the same colour as the current player's king
        # that could have been attacked on the previous enemy's turn en passant,
        # but had not, so they no longer are attackable this way
        self.update_enpassant_pawns()

        # Find all positions that enemy pieces can attack on the next
        # opponent's turn, and all positions to which at least one allied piece 
        # can move to check for the stalemate condition (except for the king
        # piece, we need to update self.enemy_potential_attack_positions first)
        self.update_enemy_potential_attack_positions()

        # Update the board statuses in respect to the current player's king's
        # position and threats
        self.update_is_king_in_check()

        # Since we updated enemy_potential_attack_positions, which is a set of all positions 
        # that enemy pieces can attack on the next opponent's turn, we can 
        # find if the king is checkmated or if a stalemate occured
        if self.is_king_in_check:
            self.update_is_king_in_checkmate()
        else:
            self.is_king_in_checkmate = False

        print("King in check:", self.is_king_in_check)
        print("King in checkmate:", self.is_king_in_checkmate)

    def does_move_expose_king(self, piece, move_pos):
        last_move_saved = self.last_move
        last_move_removed_piece_saved = self.last_move_removed_piece
        last_move_was_pieces_first_move_saved = self.last_move_was_pieces_first_move
        enemy_potential_positions_saved = self.enemy_potential_attack_positions
        is_king_in_check_saved = self.is_king_in_check

        self.move_piece(piece, move_pos)
        self.update_enemy_potential_attack_positions(check_king_exposure = False)
        self.update_is_king_in_check()
        check_result = self.is_king_in_check
            
        self.revert_last_move()

        self.last_move = last_move_saved
        self.last_move_removed_piece = last_move_removed_piece_saved
        self.last_move_was_pieces_first_move = last_move_was_pieces_first_move_saved
        self.enemy_potential_attack_positions = enemy_potential_positions_saved
        self.is_king_in_check = is_king_in_check_saved

        return check_result

    def update_is_king_in_checkmate(self):
        enemy_potential_positions_saved = self.enemy_potential_attack_positions
        check_save_piece_position_dict = dict()
        self.is_king_in_checkmate = True
        for piece in self.pieces:
            if piece.is_white == self.is_white_turn:
                piece_possible_moves = self.get_piece_available_moves(piece)
                #print(piece.board_pos, "==>", piece_possible_moves)
                for position in piece_possible_moves:
                    self.move_piece(piece, position)
                    print("IN")
                    self.update_enemy_potential_attack_positions()
                    print("OUT")
                    self.update_is_king_in_check()
                    if not self.is_king_in_check:
                        self.is_king_in_checkmate = False
                        if piece not in check_save_piece_position_dict:
                            check_save_piece_position_dict[piece] = set()
                        check_save_piece_position_dict[piece].add(position)
                        #return
                    self.revert_last_move()

        self.enemy_potential_attack_positions = enemy_potential_positions_saved
        self.is_king_in_check = True
        #print(check_save_piece_position_dict)
        self.check_save_piece_position_dict = check_save_piece_position_dict


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

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if board_rect.collidepoint(event.pos):
                if not is_game_in_process:
                    is_game_in_process = True
                else:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    grid_x = int((mouse_x - board_x) / tile_side_px)
                    grid_y = int((mouse_y - board_y) / tile_side_px)
                    coordinates = (grid_x, grid_y)
                    
                    if chess_board.active_piece is not None:
                        if coordinates in chess_board.active_piece_moves:
                            chess_board.move_piece(chess_board.active_piece, coordinates)
                            chess_board.reset_active_piece()
                            chess_board.is_white_turn = not chess_board.is_white_turn
                            chess_board.update_board_status()
                        elif chess_board.has_piece_on_position(coordinates):
                            piece = chess_board.get_piece_at_position(coordinates)
                            if piece.is_white == chess_board.is_white_turn:
                                chess_board.set_active_piece(coordinates)
                        else:
                            chess_board.reset_active_piece()

                    elif chess_board.has_piece_on_position(coordinates):
                        piece = chess_board.get_piece_at_position(coordinates)
                        if piece.is_white == chess_board.is_white_turn:
                            chess_board.set_active_piece(coordinates)
                        
                draw_chess_board(board_pos)
                pygame.display.flip()

    clock.tick(60)

