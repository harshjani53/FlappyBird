import random
import sys
import pygame
from pygame.locals import *

FPS = 32
WIDTH = 289
HEIGHT = 511
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
Y_GRAPH = HEIGHT * 0.8
IMG_RESOURCE = {}
AUD_RESOURCE = {}
BIRD = 'resources/img/bird.png'
BACKGROUND = 'resources/img/background.png'
PIPE = 'resources/img/pipe.png'


def welcomeScreen():
    x_bird = int(WIDTH / 5)
    y_bird = int((HEIGHT - IMG_RESOURCE['player'].get_height()) / 2)
    x_home = int((WIDTH - IMG_RESOURCE['message'].get_width()) / 2)
    y_home = int(HEIGHT * 0.13)
    ground_bottom = 0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            else:
                SCREEN.blit(IMG_RESOURCE['background'], (0, 0))
                SCREEN.blit(IMG_RESOURCE['player'], (x_bird, y_bird))
                SCREEN.blit(IMG_RESOURCE['message'], (x_home, y_home))
                SCREEN.blit(IMG_RESOURCE['base'], (ground_bottom, Y_GRAPH))
                pygame.display.update()
                FPSCLOCK.tick(FPS)


def mainGame():
    score = 0
    x_bird = int(WIDTH / 5)
    y_bird = int(WIDTH / 2)
    ground_bottom = 0

    pipeA = createPipe()
    pipeB = createPipe()

    invertedPipes = [
        {'x': WIDTH + 200, 'y': pipeA[0]['y']},
        {'x': WIDTH + 200 + (WIDTH / 2), 'y': pipeB[0]['y']},
    ]
    straightPipes = [
        {'x': WIDTH + 200, 'y': pipeA[1]['y']},
        {'x': WIDTH + 200 + (WIDTH / 2), 'y': pipeB[1]['y']},
    ]
    pipeVelX = -4
    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1
    playerFlapAccv = -8
    playerFlapped = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if y_bird > 0:
                    playerVelY = playerFlapAccv
                    playerFlapped = True
                    AUD_RESOURCE['wing'].play()

        crashTest = isCollide(x_bird, y_bird, invertedPipes, straightPipes)
        if crashTest:
            return

        playerMidPos = x_bird + IMG_RESOURCE['player'].get_width() / 2
        for pipe in invertedPipes:
            pipeMidPos = pipe['x'] + IMG_RESOURCE['pipe'][0].get_width() / 2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                score += 1
                print(f"Your score is {score}")
                AUD_RESOURCE['point'].play()

        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
            playerFlapped = False
        playerHeight = IMG_RESOURCE['player'].get_height()
        y_bird = y_bird + min(playerVelY, Y_GRAPH - y_bird - playerHeight)

        for upperPipe, lowerPipe in zip(invertedPipes, straightPipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

        if 0 < invertedPipes[0]['x'] < 5:
            newpipe = createPipe()
            invertedPipes.append(newpipe[0])
            straightPipes.append(newpipe[1])

        if invertedPipes[0]['x'] < -IMG_RESOURCE['pipe'][0].get_width():
            invertedPipes.pop(0)
            straightPipes.pop(0)

        SCREEN.blit(IMG_RESOURCE['background'], (0, 0))
        for upperPipe, lowerPipe in zip(invertedPipes, straightPipes):
            SCREEN.blit(IMG_RESOURCE['pipe'][0], (upperPipe['x'], upperPipe['y']))
            SCREEN.blit(IMG_RESOURCE['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

        SCREEN.blit(IMG_RESOURCE['base'], (ground_bottom, Y_GRAPH))
        SCREEN.blit(IMG_RESOURCE['player'], (x_bird, y_bird))
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += IMG_RESOURCE['numbers'][digit].get_width()
        Xoffset = (WIDTH - width) / 2

        for digit in myDigits:
            SCREEN.blit(IMG_RESOURCE['numbers'][digit], (Xoffset, HEIGHT * 0.12))
            Xoffset += IMG_RESOURCE['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def isCollide(x_bird, y_bird, invertedPipes, straightPipes):
    if y_bird > Y_GRAPH - 25 or y_bird < 0:
        AUD_RESOURCE['game-over'].play()
        return True

    for pipe in invertedPipes:
        pipeHeight = IMG_RESOURCE['pipe'][0].get_height()
        if y_bird < pipeHeight + pipe['y'] and abs(x_bird - pipe['x']) < IMG_RESOURCE['pipe'][0].get_width():
            AUD_RESOURCE['game-over'].play()
            welcomeScreen()
            return True

    for pipe in straightPipes:
        if (y_bird + IMG_RESOURCE['player'].get_height() > pipe['y']) and abs(x_bird - pipe['x']) < \
                IMG_RESOURCE['pipe'][0].get_width():
            AUD_RESOURCE['game-over'].play()
            welcomeScreen()
            return True

    return False


def createPipe():

    pipeHeight = IMG_RESOURCE['pipe'][0].get_height()
    offset = HEIGHT / 3
    y2 = offset + random.randrange(0, int(HEIGHT - IMG_RESOURCE['base'].get_height() - 1.2 * offset))
    pipeX = WIDTH + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x': pipeX, 'y': -y1},
        {'x': pipeX, 'y': y2}  
    ]
    return pipe


if __name__ == "__main__":

    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird Game')
    IMG_RESOURCE['numbers'] = (
        pygame.image.load('resources/img/0.png').convert_alpha(),
        pygame.image.load('resources/img/1.png').convert_alpha(),
        pygame.image.load('resources/img/2.png').convert_alpha(),
        pygame.image.load('resources/img/3.png').convert_alpha(),
        pygame.image.load('resources/img/4.png').convert_alpha(),
        pygame.image.load('resources/img/5.png').convert_alpha(),
        pygame.image.load('resources/img/6.png').convert_alpha(),
        pygame.image.load('resources/img/7.png').convert_alpha(),
        pygame.image.load('resources/img/8.png').convert_alpha(),
        pygame.image.load('resources/img/9.png').convert_alpha(),
    )

    IMG_RESOURCE['message'] = pygame.image.load('resources/img/message.png').convert_alpha()
    IMG_RESOURCE['base'] = pygame.image.load('resources/img/base.png').convert_alpha()
    IMG_RESOURCE['pipe'] = (pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180),
                            pygame.image.load(PIPE).convert_alpha()
                            )

    # Game sounds
    AUD_RESOURCE['die'] = pygame.mixer.Sound('resources/sound/die.wav')
    AUD_RESOURCE['game-over'] = pygame.mixer.Sound('resources/sound/game-over.wav')
    AUD_RESOURCE['point'] = pygame.mixer.Sound('resources/sound/point.wav')
    AUD_RESOURCE['swoosh'] = pygame.mixer.Sound('resources/sound/swoosh.wav')
    AUD_RESOURCE['wing'] = pygame.mixer.Sound('resources/sound/wing.wav')

    IMG_RESOURCE['background'] = pygame.image.load(BACKGROUND).convert()
    IMG_RESOURCE['player'] = pygame.image.load(BIRD).convert_alpha()

    while True:
        welcomeScreen()
        mainGame()
