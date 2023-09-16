import pygame
import sys
import time

import connect4 as c4

pygame.init()
size = width, height = 800, 700

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 10, 40)
yellow = (255, 238, 0)

screen = pygame.display.set_mode(size)

mediumFont = pygame.font.Font("OpenSans-Regular.ttf", 28)
largeFont = pygame.font.Font("OpenSans-Regular.ttf", 40)
moveFont = pygame.font.Font("OpenSans-Regular.ttf", 60)

user = None
board = c4.initial_state()
ai_turn = False

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(black)

    # Let user choose a player.
    if user is None:

        # Draw title
        title = largeFont.render("Play Connect 4", True, white)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 50)
        screen.blit(title, titleRect)

        # Draw buttons
        playRButton = pygame.Rect((width / 8), (height / 2), width / 4, 50)
        playR = mediumFont.render("Play as Red", True, red)
        playRRect = playR.get_rect()
        playRRect.center = playRButton.center
        pygame.draw.rect(screen, white, playRButton)
        screen.blit(playR, playRRect)

        playYButton = pygame.Rect(5 * (width / 8), (height / 2), width / 4, 50)
        playY = mediumFont.render("Play as Yellow", True, yellow)
        playYRect = playY.get_rect()
        playYRect.center = playYButton.center
        pygame.draw.rect(screen, white, playYButton)
        screen.blit(playY, playYRect)

        # Check if button is clicked
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            if playRButton.collidepoint(mouse):
                time.sleep(0.2)
                user = c4.R
            elif playYButton.collidepoint(mouse):
                time.sleep(0.2)
                user = c4.Y

    else:

        # Draw game board
        tile_size = 80
        tile_origin = (width / 3.5 - (1.5 * tile_size),
                       height / 3 - (1.5 * tile_size))
        tiles = []
        for i in range(6):
            row = []
            for j in range(7):
                rect = pygame.Rect(
                    tile_origin[0] + j * tile_size,
                    tile_origin[1] + i * tile_size,
                    tile_size, tile_size
                )
                pygame.draw.rect(screen, white, rect, 7)

                if board[i][j] != c4.EMPTY:
                    move = moveFont.render(board[i][j], True, white)
                    moveRect = move.get_rect()
                    moveRect.center = rect.center
                    screen.blit(move, moveRect)
                row.append(rect)
            tiles.append(row)

        game_over = c4.terminal(board)
        player = c4.player(board)

        # Show title
        if game_over:
            winner = c4.winner(board)
            if winner is None:
                title = f"Game Over: Tie."
            else:
                title = f"Game Over: {winner} wins."
        elif user == player:
            title = f"Play as {user}"
        else:
            title = f"Computer thinking..."
        title = largeFont.render(title, True, white)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 30)
        screen.blit(title, titleRect)

        # Check for AI move
        if user != player and not game_over:
            if ai_turn:
                time.sleep(0.5)
                move = c4.minimax(board)
                board = c4.result(board, move)
                ai_turn = False
            else:
                ai_turn = True

        # Check for a user move
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1 and user == player and not game_over:
            mouse = pygame.mouse.get_pos()
            for i in range(6):
                for j in range(7):
                    if (board[i][j] == c4.EMPTY and tiles[i][j].collidepoint(mouse)):
                        print("board before move:", board)
                        print("board after move:", c4.result(board, (i, j)))
                        board = c4.result(board, (i, j))
                        print("board before move:", board)
                        exit()

        if game_over:
            againButton = pygame.Rect(width / 3, height - 65, width / 3, 50)
            again = mediumFont.render("Play Again", True, black)
            againRect = again.get_rect()
            againRect.center = againButton.center
            pygame.draw.rect(screen, white, againButton)
            screen.blit(again, againRect)
            click, _, _ = pygame.mouse.get_pressed()
            if click == 1:
                mouse = pygame.mouse.get_pos()
                if againButton.collidepoint(mouse):
                    time.sleep(0.2)
                    user = None
                    board = c4.initial_state()
                    ai_turn = False

    pygame.display.flip()
