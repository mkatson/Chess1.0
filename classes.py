from gui import *
from modules import *


# Classes based on each piece type
class Pawn:

    def __init__(self, image, coordinates=(x, y)):
        self.image = image
        self.coords = coordinates
        # using the image as the key, the value is the color
        self.color = {bp_img: 'black', wp_img: 'white'}
        self.moves = []

    def move_rules(self):
        # a pawn can only move up one space
        # but can take a piece diagonally
        # it can also move up one space if it is it's first move
        if self.image == bp_img:
            # checks if the space in front of the pawn is open
            one_below = (self.coords[0] + 1, self.coords[1])
            if current_board[one_below[0]][one_below[1]] == 0:
                self.moves.append(one_below)

            # makes local variables for the pieces to the upper right and upper left of the pawn
            # for easy access
            up_right = (self.coords[0] + 1, self.coords[1] + 1)
            right_piece = current_board[up_right[0]][up_right[1]]
            up_left = (self.coords[0] + 1, self.coords[1] - 1)
            left_piece = current_board[up_left[0]][up_left[1]]

            # adds the diagonal move if there is a white piece there
            if right_piece != 0 and piece_colors[right_piece] == 'white':
                self.moves.append(up_right)
            if left_piece != 0 and piece_colors[left_piece] == 'white':
                self.moves.append(up_left)

            # it is the pawn's first move it can move up 2
            if self.coords[0] == 1:
                self.moves.append((self.coords[0] + 2, self.coords[1]))
            return self.moves

        # could condense this with the one above?
        if self.image == wp_img:
            # checks if the space in front of the pawn is open
            one_above = (self.coords[0] - 1, self.coords[1])
            if current_board[one_above[0]][one_above[1]] == 0:
                self.moves.append(one_above)

            # makes the pieces to the pawns upper right and upper left easy to access
            up_right = (self.coords[0] - 1, self.coords[1] + 1)
            right_piece = current_board[up_right[0]][up_right[1]]
            up_left = (self.coords[0] - 1, self.coords[1] - 1)
            left_piece = current_board[up_left[0]][up_left[1]]

            # checks if those pieces are not an open space but an enemy piece
            if right_piece != 0 and piece_colors[right_piece] == 'black':
                self.moves.append(up_right)
            if left_piece != 0 and piece_colors[left_piece] == 'black':
                self.moves.append(up_left)

            # if it is the pawn's first move it can move up 2
            if self.coords[0] == 6:
                self.moves.append((self.coords[0] - 2, self.coords[1]))
            return self.moves


class Rook:

    def __init__(self, image, coordinates=(x, y)):
        self.image = image
        # coordinates must be the board_coords or initial_piece coordinates!!!
        self.coords = coordinates
        self.color = {br_img: 'black', wr_img: 'white'}
        self.moves = []

    def move_rules(self):
        # can move forward, back, left, and right but NOT diagonally
        # for any number of spaces on the board in that direction

        # checks in each direction, appends until you hit another piece
        check_list = ('forward', 'backward', 'right', 'left')
        a = 0
        b = 0
        for direction in check_list:
            if direction == 'forward':
                a = 1
                b = 0
            if direction == 'backward':
                a = -1
                b = 0
            if direction == 'right':
                a = 0
                b = 1
            if direction == 'left':
                a = 0
                b = -1

            check = self.coords
            for i in range(len(current_board)):
                check = (check[0] + a, check[1] + b)
                # filters out-of-board coordinates
                if check[0] < 0 or check[0] > 7:
                    continue
                if check[1] < 0 or check[1] > 7:
                    continue
                # if the next space is open, append then check the next space
                if current_board[check[0]][check[1]] == 0:
                    self.moves.append(check)
                    continue
                # if the next check is a friendly piece, stop checking in that direction
                if piece_colors[current_board[check[0]][check[1]]] == self.color[self.image]:
                    break
                # if the next check is an enemy piece, append it and stop checking in that direction
                if piece_colors[current_board[check[0]][check[1]]] != self.color[self.image]:
                    self.moves.append(check)
                    break
        return self.moves


class Bishop:

    def __init__(self, image, coordinates=(x, y)):
        self.image = image
        self.coords = coordinates
        self.color = {bB_img: 'black', wB_img: 'white'}
        self.moves = []

    def move_rules(self):
        # a bishop should be able to move diagonally in all four directions
        # this is the same code as the rook's but with diagonal directions
        check = self.coords
        check_list = ('top right', 'top left', 'bottom right', 'bottom left')
        a = 0
        b = 0
        for e in check_list:
            if e == 'top right':
                a = -1
                b = 1
            if e == 'top left':
                a = -1
                b = -1
            if e == 'bottom right':
                a = 1
                b = 1
            if e == 'bottom left':
                a = 1
                b = -1
            check = self.coords
            for i in range(len(current_board)):
                check = (check[0] + a, check[1] + b)
                if check[0] < 0 or check[0] > 7:
                    continue
                if check[1] < 0 or check[1] > 7:
                    continue
                if current_board[check[0]][check[1]] == 0:
                    self.moves.append(check)
                    continue
                if piece_colors[current_board[check[0]][check[1]]] == self.color[self.image]:
                    break
                    pass
                if piece_colors[current_board[check[0]][check[1]]] != self.color[self.image]:
                    self.moves.append(check)
                    break
        return self.moves


class Knight:

    def __init__(self, image, coordinates=(x, y)):
        self.image = image
        self.coords = coordinates
        self.color = {bkn_img: 'black', wkn_img: 'white'}
        self.moves = []

    def move_rules(self):
        # a knight should move away 2 and over 1
        move_list = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for a, b in move_list:
            new_move = (self.coords[0] + a, self.coords[1] + b)
            # makes sure the check is not out-of-bounds
            if new_move[0] < 0 or new_move[0] > 7:
                continue
            if new_move[1] < 0 or new_move[1] > 7:
                continue
            self.moves.append(new_move)
        return self.moves


class Queen:

    def __init__(self, image, coordinates=(x, y)):
        self.image = image
        self.coords = coordinates
        self.color = {bq_img: 'black', wq_img: 'white'}
        self.moves = []

    def move_rules(self):
        # a queen should move like a rook and a bishop combined
        check = self.coords
        check_list = ('top right', 'top left', 'bottom right', 'bottom left', 'forward', 'backward', 'right', 'left')
        a = 0
        b = 0
        for e in check_list:
            if e == 'top right':
                a = -1
                b = 1
            if e == 'top left':
                a = -1
                b = -1
            if e == 'bottom right':
                a = 1
                b = 1
            if e == 'bottom left':
                a = 1
                b = -1
            if e == 'forward':
                a = 1
                b = 0
            if e == 'backward':
                a = -1
                b = 0
            if e == 'right':
                a = 0
                b = 1
            if e == 'left':
                a = 0
                b = -1
            check = self.coords
            for i in range(len(current_board)):
                check = (check[0] + a, check[1] + b)
                if check[0] < 0 or check[0] > 7:
                    continue
                if check[1] < 0 or check[1] > 7:
                    continue
                if current_board[check[0]][check[1]] == 0:
                    self.moves.append(check)
                    continue
                if piece_colors[current_board[check[0]][check[1]]] == self.color[self.image]:
                    break
                    pass
                if piece_colors[current_board[check[0]][check[1]]] != self.color[self.image]:
                    self.moves.append(check)
                    break
        return self.moves


class King:

    def __init__(self, image, coordinates=(x, y)):
        self.image = image
        self.coords = coordinates
        self.color = {bp_img: 'black', wp_img: 'white'}
        self.moves = []

    def move_rules(self):
        # a king should move one space in all directions but no more
        move_list = ((1, 0), (-1, 0), (0, -1), (0, 1))
        for a, b in move_list:
            new_move = (self.coords[0] + a, self.coords[1] + b)
            if new_move[0] < 0 or new_move[0] > 7:
                continue
            if new_move[1] < 0 or new_move[1] > 7:
                continue
            self.moves.append(new_move)
        return self.moves

# -----------------------------------------------
