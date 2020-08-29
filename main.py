import pygame
import pyglet
from gui import *
import modules as F
# for some reason this font wont work
pyglet.font.add_file(r'C:\Users\Michael\Documents\Summer2020\fonts\monotype-corsiva\MonotypeCorsiva.ttf')

# This file handles the main loops: start and game
main = True
while main:
    # sets the standard features for the start window
    display_width = 400
    display_height = 300
    gameDisplay = pygame.display.set_mode((display_width, display_height))

    # the start loop handles the start screen
    start = True
    while start:
        # checks for any events in pygame
        for event in pygame.event.get():
            # including the user clicking the red X
            if event.type == pygame.QUIT:
                # quits the window and the python script
                pygame.quit()
                quit()

            # or clicking their mouse (left click)
            if event.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()

                # if the mouse is clicked within the start button rectangle
                if 91 < position[0] < 208 and 161 < position[1] < 204:
                    # then stop the start screen
                    start = False

        # display title, start button, updates screen
        gameDisplay.fill(grey)
        gameDisplay.blit(title_text, (40, 60))
        gameDisplay.blit(start_surf, (90, 160))
        gameDisplay.blit(start_text, (90, 160))
        pygame.display.update()
        # controls the frames per second
        clock.tick(60)

    # re-sizes the window for the game screen
    display_width = 800
    display_height = 600
    game_screen = pygame.display.set_mode((display_width, display_height))

    # turn = 'white' if the remainder of turn_index + 1 / 2 is 0
    turn_index = 1
    turns = ('white', 'black')
    turn = turns[(turn_index+1) % 2]

    # this list will have [initial_tile, final_tile]
    current_move = []
    # sets the current board
    for i in range(8):
        for e in range(8):
            current_board[i][e] = default_board[i][e]

    # loops the game screen
    game = True
    while game:
        # checks for any pygame events
        for event in pygame.event.get():
            # if the user exits out (red X)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            # or if the user re-sizes the window
            if event.type == pygame.VIDEORESIZE:
                vid_dimensions = pygame.VIDEORESIZE
                # currently does nothing

            # or if they click their mouse (left click)
            if event.type == pygame.MOUSEBUTTONDOWN:
                point = pygame.mouse.get_pos()
                # print(point) - in case you want to find coordinates easily

                # circle math
                center = (720, 530)
                radius = 40
                distance = math.sqrt((point[0] - center[0])**2 + (point[1] - center[1])**2)

                # these two if statements control if the user clicks the restart button
                if round(distance) <= radius:
                    # go back to the start screen
                    game = False

                if round(distance) > radius:
                    # the mouse is outside the circle
                    pass

                # controls if a piece is clicked
                if F.check_image_click(point):
                    bool_1, x_1 = F.check_image_click(point)
                    current_move.append(x_1)

            # when the user raises their (left) mouse button
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()

                # checks again if the position where you lifted the left mouse button is on a tile
                if F.check_image_click(pos):
                    bool_2, x_2 = F.check_image_click(pos)
                    current_move.append(x_2)
                    # handles changes to whose turn it is
                    turn_index = F.move_piece(current_move, turn, turn_index)
                    turn = turns[(turn_index + 1) % 2]

                    black_king = True
                    white_king = True
                    # checks if the white king piece has been taken
                    for i in current_board:
                        if wK_img not in i:
                            white_king = False
                        if wK_img in i:
                            white_king = True
                            break

                    if not white_king:
                        winner_text = "Congratulations player Black!"
                        winner_text_1 = "You won the game!"
                        # makes a pop-up saying "Congratulations " + winner + "! You won the game."
                        # then upon exiting that window, return to the start menu
                        congrats_screen = pygame.display.set_mode((100, 50))
                        congrats_font = pygame.font.SysFont('MonotypeCorsiva', 40)
                        congrats_text = congrats_font.render(winner_text, True, black)
                        congrats_text_1 = congrats_font.render(winner_text_1, True, black)
                        # closes the game window and makes a pop-up window with the congratulations text
                        congrats = True
                        while congrats:
                            for event_1 in pygame.event.get():
                                # if the user exits out (red X) then they return to the start screen
                                if event_1.type == pygame.QUIT:
                                    congrats = False

                            congrats_screen.fill(pink)
                            congrats_screen.blit(congrats_text, (round(300 * .1), round(100 * .1)))
                            congrats_screen.blit(congrats_text_1, (round(300 * .1), round(100 * .4)))
                            pygame.display.flip()
                            clock.tick(20)

                        if not congrats:
                            game = False

                    # see above for details
                    for i in current_board:
                        if bK_img not in i:
                            black_king = False
                        if bK_img in i:
                            black_king = True
                            break

                    if not black_king:
                        winner_text = "Congratulations player White!"
                        winner_text_1 = "You won the game!"
                        # make a pop-up saying "Congratulations " + winner + "! You won the game."
                        # then upon exiting that window, return to the start menu
                        congrats_screen = pygame.display.set_mode((580, 100))
                        congrats_font = pygame.font.SysFont('MonotypeCorsiva', 35)
                        congrats_text = congrats_font.render(winner_text, True, black)
                        congrats_text_1 = congrats_font.render(winner_text_1, True, black)

                        # see above for details
                        congrats = True
                        while congrats:
                            for e in pygame.event.get():
                                if e.type == pygame.QUIT:
                                    congrats = False

                            congrats_screen.fill(pink)
                            congrats_screen.blit(congrats_text, (round(300 * .1), round(100 * .1)))
                            congrats_screen.blit(congrats_text_1, (round(300 * .1), round(100 * .4)))
                            pygame.display.flip()
                            clock.tick(20)
                        if not congrats:
                            game = False
                current_move = []

        # sets all the main items on the screen
        F.set_main(game_screen, display_width, display_height, blue, turn)
        # blits each game piece onto the screen
        F.set_pieces(game_screen)

        # updates the display surface
        pygame.display.flip()
        clock.tick(60)
