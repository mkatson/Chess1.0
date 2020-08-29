import pygame
import math

# this file (gui.py) handles most of the visuals using pygame
# the main.py file handles the main loops (which use these variables below)
# the modules.py file contains all the modules used in main.py (also use the variables below)

# initializes the pygame, font init modules
pygame.init()
pygame.font.init()

# referencable dimensions of the window (in case the game would be re-sized)
# although there is not currently a resize option to any of the windows
display_width = 400
display_height = 600

# referencable colors in RGB
black = (0, 0, 0)
white = (255, 255, 255)
grey = (228, 228, 220)
green = (92, 219, 104)
pink = (255, 150, 202)
blue = (146, 189, 223)

# sets title font
title_font = pygame.font.SysFont("couriernew", size=100)
title_text = title_font.render("Chess", True, black)
start_font = pygame.font.SysFont("couriernew", size=40)
start_text = start_font.render("Start", True, black)
start_size = start_font.size("Start")
start_surf = pygame.Surface(start_size)
start_surf.fill(green)


# renders the turn_text (Ex: 'Turn: Black')
def update_turn(turn):
    turn_font = pygame.font.SysFont("arial", size=20)
    turn_text = turn_font.render("Turn: " + turn, True, black)
    return turn_text


# sets up the window
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Chess 1.0')
clock = pygame.time.Clock()

# loads and rescales all the main images
board_img = pygame.image.load(r'C:\Users\Michael\Documents\Summer2020\Chess\images\chessboard.jpg')
restart_img = pygame.image.load(r'C:\Users\Michael\Documents\Summer2020\Chess\images\restart_button.png')
help_img = pygame.image.load(r'C:\Users\Michael\Documents\Summer2020\Chess\images\help_button.png')
board_img = pygame.transform.scale(board_img, (400, 400))
restart_img = pygame.transform.scale(restart_img, (80, 80))
help_img = pygame.transform.scale(help_img, (50, 50))

# loads and rescales all the game pieces
# img_list = ('bB', 'bK', 'bkn', 'bp', 'bq', 'br', 'wB', 'wK', 'wkn', 'wp', 'wq', 'wr')
# obj_list = [bB_img, bK_img, bkn_img, bp_img, bq_img, br_img,
# wB_img, wK_img, wkn_img, wp_img, wq_img, wr_img]
# Consider condensing this somehow ...

bB_img = pygame.image.load(r'C:\Users\Michael\Documents\Summer2020\Chess\images\bB.png')
bB_img = pygame.transform.scale(bB_img, (40, 40))
bK_img = pygame.image.load(r'C:\Users\Michael\Documents\Summer2020\Chess\images\bK.png')
bK_img = pygame.transform.scale(bK_img, (40, 40))
bkn_img = pygame.image.load(r'C:\Users\Michael\Documents\Summer2020\Chess\images\bkn.png')
bkn_img = pygame.transform.scale(bkn_img, (40, 40))
bp_img = pygame.image.load(r'C:\Users\Michael\Documents\Summer2020\Chess\images\bp.png')
bp_img = pygame.transform.scale(bp_img, (40, 40))
bq_img = pygame.image.load(r'C:\Users\Michael\Documents\Summer2020\Chess\images\bq.png')
bq_img = pygame.transform.scale(bq_img, (40, 40))
br_img = pygame.image.load(r'C:\Users\Michael\Documents\Summer2020\Chess\images\br.png')
br_img = pygame.transform.scale(br_img, (40, 40))

wB_img = pygame.image.load(r'C:\Users\Michael\Documents\Summer2020\Chess\images\wB.png')
wB_img = pygame.transform.scale(wB_img, (40, 40))
wK_img = pygame.image.load(r'C:\Users\Michael\Documents\Summer2020\Chess\images\wK.png')
wK_img = pygame.transform.scale(wK_img, (40, 40))
wkn_img = pygame.image.load(r'C:\Users\Michael\Documents\Summer2020\Chess\images\wkn.png')
wkn_img = pygame.transform.scale(wkn_img, (40, 40))
wp_img = pygame.image.load(r'C:\Users\Michael\Documents\Summer2020\Chess\images\wp.png')
wp_img = pygame.transform.scale(wp_img, (40, 40))
wq_img = pygame.image.load(r'C:\Users\Michael\Documents\Summer2020\Chess\images\wq.png')
wq_img = pygame.transform.scale(wq_img, (40, 40))
wr_img = pygame.image.load(r'C:\Users\Michael\Documents\Summer2020\Chess\images\wr.png')
wr_img = pygame.transform.scale(wr_img, (40, 40))

# this is a template for a chessboard which will be used to reset the game
default_board = [
            [br_img, bkn_img, bB_img, bq_img, bK_img, bB_img, bkn_img, br_img],
            [bp_img, bp_img, bp_img, bp_img, bp_img, bp_img, bp_img, bp_img],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [wp_img, wp_img, wp_img, wp_img, wp_img, wp_img, wp_img, wp_img],
            [wr_img, wkn_img, wB_img, wq_img, wK_img, wB_img, wkn_img, wr_img]
            ]
current_board = [
    [0]*8,
    [0]*8,
    [0]*8,
    [0]*8,
    [0]*8,
    [0]*8,
    [0]*8,
    [0]*8
]

# tile objects mapping screen coordinates tile_x[0] to current_board coordinates tile_x[1]
# Ex: tile_1 = ([82, 62, 50, 50], (0, 0))
# adds each tile to tile_list
tile_list = []
rank = 0
for row in default_board:
    count = 0
    for tile in row:
        x = (count * 50) + 83
        y = (rank * 50) + 68
        tile_x = ([x - 1, y - 6, 50, 50], (rank, count))
        tile_list.append(tile_x)
        count += 1
    rank += 1

# used to check what color each piece object is (see modules.move_rules)
piece_colors = {br_img: 'black', bkn_img: 'black', bB_img: 'black', bq_img: 'black',
                bK_img: 'black', bp_img: 'black', wr_img: 'white', wkn_img: 'white', wB_img: 'white', wq_img: 'white',
                wK_img: 'white', wp_img: 'white'}
