import random

import pygame
from pygame.color import THECOLORS
from pygame.rect import Rect

pygame.init()

screen = pygame.display.set_mode((300, 300))
pygame.display.set_caption('tic tac toe')
screen_rect = screen.get_rect()
clock = pygame.time.Clock()

w = int(screen_rect.width / 3)
h = int(screen_rect.height / 3)

players = ['X', 'O']
currentPlayer = 0
ai = 0
human = 1

board = [
    ['', '', ''],
    ['', '', ''],
    ['', '', '']
]

available = []


def draw_on_screen():
    for i in range(3):
        for j in range(3):
            if board[i][j] == players[0]:
                pygame.draw.line(screen, THECOLORS['black'], (int(j * w + w / 2 - w / 4), int(i * h + h / 2 - w / 4)),
                                 (int(j * w + w / 2 + w / 4), int(i * h + h / 2 + w / 4)), 3)
                pygame.draw.line(screen, THECOLORS['black'], (int(j * w + w / 2 + w / 4), int(i * h + h / 2 - w / 4)),
                                 (int(j * w + w / 2 - w / 4), int(i * h + h / 2 + w / 4)), 3)
            elif board[i][j] == players[1]:
                pygame.draw.circle(screen, THECOLORS['black'], (int(j * w + w / 2), int(i * h + h / 2)), int(h / 4), 2)


def checkWinner():
    winner = None
    # horizontal
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] != '':
            winner = board[i][0]

    # vertical
    for i in range(3):
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] != '':
            winner = board[0][i]

    # diagonal
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != '':
        winner = board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[2][0] != '':
        winner = board[0][2]

    # tie
    count = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] == '':
                count += 1
    if count == 0 and winner is None:
        return 'tie'
    else:
        return winner


scores = {'X': 1,
          'O': -1,
          'tie': 0}


def minimax(board, depth, isMaximizing):
    global scores
    result = checkWinner()
    if result is not None:
        return scores[result]
    if isMaximizing:
        bestScore = -999
        for i in range(3):
            for j in range(3):
                if board[i][j] == '':
                    board[i][j] = players[ai]
                    score = minimax(board, depth + 1, False)
                    board[i][j] = ''
                    if score > bestScore:
                        bestScore = score

        return bestScore
    else:
        bestScore = 999
        for i in range(3):
            for j in range(3):
                if board[i][j] == '':
                    board[i][j] = players[human]
                    score = minimax(board, depth + 1, True)
                    board[i][j] = ''
                    if score < bestScore:
                        bestScore = score
        return bestScore


def nextTurn():
    global currentPlayer, players, ai

    bestScore = -999

    bestmove = [random.randint(0, 2), random.randint(0, 2)]

    for i in range(3):
        for j in range(3):
            if board[i][j] == '':
                board[i][j] = players[ai]
                score = minimax(board, 1, False)
                board[i][j] = ''
                if score > bestScore:
                    bestScore = score
                    bestmove = [i, j]

    available.remove(bestmove)
    board[bestmove[0]][bestmove[1]] = players[ai]
    currentPlayer = human


def player_spot(pos):
    clicking_areas = [[Rect((int(j * w + w / 2 - w / 4), int(i * h + h / 2 - w / 4), w / 2, h / 2)) for i in range(3)]
                      for j in range(3)]
    for i, eaches in enumerate(clicking_areas):
        for j, each in enumerate(eaches):
            if Rect.collidepoint(each, pos[1], pos[0]):
                return i, j
    else:
        return None


def main():
    global currentPlayer, players
    for i in range(3):
        for j in range(3):
            if board[i][j] == '':
                available.append([i, j])
    while True:
        clock.tick(30)

        result = checkWinner()

        if result is None and currentPlayer == 0:
            nextTurn()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and len(available) >= 1 and result is None and currentPlayer == 1:
                    pos = player_spot(pygame.mouse.get_pos())
                    if pos is not None:
                        available.remove(list(pos))
                        board[pos[0]][pos[1]] = players[currentPlayer]
                        currentPlayer = (currentPlayer + 1) % len(players)
            if event.type == pygame.KEYDOWN:
                print(event)
                if event.key == pygame.K_ESCAPE:
                    exit()

        screen.fill(THECOLORS['white'])
        pygame.draw.line(screen, THECOLORS['black'], (w, 0), (w, h * 3), 3)
        pygame.draw.line(screen, THECOLORS['black'], (w * 2, 0), (w * 2, h * 3), 3)
        pygame.draw.line(screen, THECOLORS['black'], (0, h), (w * 3, h), 3)
        pygame.draw.line(screen, THECOLORS['black'], (0, h * 2), (w * 3, h * 2), 3)

        draw_on_screen()

        pygame.display.flip()
        if result is not None:
            print(result)


if __name__ == '__main__':
    main()
