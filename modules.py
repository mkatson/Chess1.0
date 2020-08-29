import pygame
import math
from gui import *
from classes import *

# -----------------------------------------------
# FUNCTIONS HERE:


def set_main(game_screen, display_width, display_height, background, turn):
    # sets coordinates for images to be displayed
    x_bd = display_width * .1
    y_bd = display_height * .1
    x_r = display_width * .85
    y_r = display_height * .81
    x_h = display_width * .9
    y_h = display_height * .05
    x_t = display_width * .15
    y_t = display_height * .8

    # fills the background surface color and then loads the images
    turn_text = update_turn(turn)
    game_screen.fill(background)
    game_screen.blit(board_img, (round(x_bd), round(y_bd)))
    game_screen.blit(turn_text, (round(x_t), round(y_t)))
    game_screen.blit(restart_img, (round(x_r), round(y_r)))
    game_screen.blit(help_img, (round(x_h), round(y_h)))


def set_pieces(game_screen):
    # prints every piece image from the current_board on the screen

    rank = 0
    for row in current_board:
        count = 0
        for tile in row:
            x = (count * 50) + 83
            y = (rank * 50) + 68
            # tile_x = ([x - 1, y - 6, 50, 50], (count, rank))
            # tile_list.append(tile_x)
            if tile == 0:
                count += 1
                continue

            game_screen.blit(tile, (x, y))
            count += 1
        rank += 1


def check_image_click(mouse_coors):
    # this function should return True/False if an image is clicked/not clicked
    # also returns the tile tuple (x) for later use

    # temporarily creates a rectangle for each image piece
    for x in tile_list:
        x_rect = pygame.Rect(x[0])
        # checks if the mouse click coordinates were within the tile Rect
        if x_rect.collidepoint(mouse_coors[0], mouse_coors[1]):
            return True, x

    # if the click did not click any tile then it is not handled later
    return False


def move_piece(current_move, turn, turn_index):
    # this changes the current_board to reflect any moved pieces
    # it also returns without changing the turn if the move is invalid
    # it does not visually move the pieces - this is handled with set_pieces()

    # in case someone clicks outside the board and raises the click on the board
    # or vice versa
    # when the 'start' button is clicked only the MOUSEBUTTONUP event will be counted
    # so this prevents that move from being processed
    if len(current_move) == 1:
        return turn_index

    # initial_tile's current_board list coordinates are re-formatted for easier use
    board_coords = current_move[0][1]
    coord_1 = board_coords[0]
    coord_2 = board_coords[1]
    # stores the initial_tile's piece in a local variable
    initial_piece = current_board[coord_1][coord_2]

    # final_tile's current_board list coordinates are re-formatted for easier use
    board_coors = current_move[1][1]
    coor_1 = board_coors[0]
    coor_2 = board_coors[1]
    final_piece = current_board[coor_1][coor_2]

    # just in case someone tries to move a blank space = invalid move
    if initial_piece == 0:
        return turn_index

    # if the pieces are the same color = invalid move
    if final_piece != 0:
        if piece_colors[initial_piece] == piece_colors[final_piece]:
            return turn_index

    # if it is not your turn, you cannot move (i.e. if turn = 'white', black pieces cannot move)
    if turn == 'white':
        if piece_colors[initial_piece] == 'black':
            return turn_index
    if turn == 'black':
        if piece_colors[initial_piece] == 'white':
            return turn_index

    # is the move valid according to its move_rules module?
    # there may be a more concise way of coding this:
    if initial_piece == bp_img or initial_piece == wp_img:
        p = Pawn(initial_piece, board_coords)
        valid_moves = p.move_rules()
        if board_coors in valid_moves:
            pass
        else:
            return turn_index

    if initial_piece == br_img or initial_piece == wr_img:
        r = Rook(initial_piece, board_coords)
        valid_moves = r.move_rules()
        if board_coors in valid_moves:
            pass
        else:
            return turn_index

    if initial_piece == bB_img or initial_piece == wB_img:
        b = Bishop(initial_piece, board_coords)
        valid_moves = b.move_rules()
        if board_coors in valid_moves:
            pass
        else:
            return turn_index

    if initial_piece == bkn_img or initial_piece == wkn_img:
        kn = Knight(initial_piece, board_coords)
        valid_moves = kn.move_rules()
        if board_coors in valid_moves:
            pass
        else:
            return turn_index

    if initial_piece == bq_img or initial_piece == wq_img:
        q = Queen(initial_piece, board_coords)
        valid_moves = q.move_rules()
        if board_coors in valid_moves:
            pass
        else:
            return turn_index

    if initial_piece == bK_img or initial_piece == wK_img:
        K = King(initial_piece, board_coords)
        valid_moves = K.move_rules()
        if board_coors in valid_moves:
            pass
        else:
            return turn_index

    # clears the initial_tile value
    current_board[coord_1][coord_2] = 0
    # replaces the final_piece with the initial_piece
    current_board[coor_1][coor_2] = initial_piece
    # increments the turn to allow the other player to move
    turn_index += 1
    return turn_index
