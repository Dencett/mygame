import pygame, sys, random
from pygame.locals import *

pygame.init()

WINDOWWIDTH = 1000
WINDOWHEIGHT = 1000

FPS = 400
clock = pygame.time.Clock()


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 150, 255)
NAVYBLUE = (0, 0, 200)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)

CENTER_BLOCK_COLOR = (153, 51, 51)
CENTER_BLOCKS_WHEN_PRESSED_COLOR = (204, 0, 0)
SURFACE_COLOR = (204, 255, 255)

SPEED = 2
ENEMY_SPEED = 1


center_blocks = []
for x in range(200, 800, 76):
    for y in range(200, 800, 76):
        block = {'rect': pygame.Rect(x, y, 68, 68), 'color': CENTER_BLOCK_COLOR}
        center_blocks.append(block)


windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Моя первая игра')

pygame.mouse.set_visible(False)


def font(size):
    return pygame.font.SysFont(None, size)


def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                return
            if event.type == MOUSEBUTTONUP:
                return


def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, BLUE)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


up_rocket_image = pygame.image.load('sprites/up_rocket.png')
right_rocket_image = pygame.image.load('sprites/right_rocket.png')
down_rocket_image = pygame.image.load('sprites/down_rocket.png')
left_rocket_image = pygame.image.load('sprites/left_rocket.png')


def rocket_block(x, y, dir):
    if dir == 'up':
        return {'rect': pygame.Rect(x, y, 20, 20), 'color': BLACK, 'dir': dir,
                'surfase': pygame.transform.scale(up_rocket_image, (20, 20))}
    if dir == 'right':
        return {'rect': pygame.Rect(x, y, 20, 20), 'color': BLACK, 'dir': dir,
                'surfase': pygame.transform.scale(right_rocket_image, (20, 20))}
    if dir == 'down':
        return {'rect': pygame.Rect(x, y, 20, 20), 'color': BLACK, 'dir': dir,
                'surfase': pygame.transform.scale(down_rocket_image, (20, 20))}
    if dir == 'left':
        return {'rect': pygame.Rect(x, y, 20, 20), 'color': BLACK, 'dir': dir,
                'surfase': pygame.transform.scale(left_rocket_image, (20, 20))}


corner_block_image = pygame.image.load('sprites/corner.png')

position_corner_blocks = [2, 802]
corner_blocks = []
for x in position_corner_blocks:
    for y in position_corner_blocks:
        corner_blocks.append({'rect': pygame.Rect(x, y, 196, 196), 'color': GREEN,
                              'surfase': pygame.transform.scale(corner_block_image, (196, 196))})

stopping = [160, 219, 295, 371, 447, 523, 599, 675, 751, 804]

enemy_image = pygame.image.load('sprites/bomb.png')

enemy_positions = {
    '1': {'position': [160, 16], 'dir': 'up'},
    '2': {'position': [160, 62], 'dir': 'up'},
    '3': {'position': [160, 108], 'dir': 'up'},
    '4': {'position': [160, 154], 'dir': 'up'},
    '5': {'position': [816, 160], 'dir': 'right'},
    '6': {'position': [862, 160], 'dir': 'right'},
    '7': {'position': [908, 160], 'dir': 'right'},
    '8': {'position': [954, 160], 'dir': 'right'},
    '9': {'position': [810, 816], 'dir': 'down'},
    '10': {'position': [810, 862], 'dir': 'down'},
    '11': {'position': [810, 908], 'dir': 'down'},
    '12': {'position': [810, 954], 'dir': 'down'},
    '13': {'position': [16, 810], 'dir': 'left'},
    '14': {'position': [62, 810], 'dir': 'left'},
    '15': {'position': [108, 810], 'dir': 'left'},
    '16': {'position': [154, 810], 'dir': 'left'}
}


def reached_position(d_enemy, enemy_data, corner_blocks):
    global life
    if d_enemy['dir'] == 'up':
        if d_enemy['rect'].colliderect(corner_blocks[2]['rect']):
            life -= 1
            enemy_data.remove(d_enemy)
    if d_enemy['dir'] == 'right':
        if d_enemy['rect'].colliderect(corner_blocks[3]['rect']):
            life -= 1
            enemy_data.remove(d_enemy)
    if d_enemy['dir'] == 'down':
        if d_enemy['rect'].colliderect(corner_blocks[1]['rect']):
            life -= 1
            enemy_data.remove(d_enemy)
    if d_enemy['dir'] == 'left':
        if d_enemy['rect'].colliderect(corner_blocks[0]['rect']):
            life -= 1
            enemy_data.remove(d_enemy)


windowSurface.fill(SURFACE_COLOR)
drawText('Моя игра!', font(100), windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3) - 50)
drawText('Нажмите клавишу или мышь для начала игры', font(50), windowSurface, (WINDOWWIDTH / 5) - 90,
         (WINDOWHEIGHT / 3) + 50)
drawText('Задача: унчтожить мины, чтобы не дошли до базы.',
         font(40), windowSurface, (WINDOWWIDTH / 5) - 60, (WINDOWHEIGHT / 3) + 150)
drawText('При уничтожении 4 мин сразу мины осиаются на месте.',
         font(40), windowSurface, (WINDOWWIDTH / 5) - 60, (WINDOWHEIGHT / 3) + 180)
pygame.display.update()
waitForPlayerToPressKey()

topScore = 0
while True:
    life = 3
    move = 0
    score = 0
    hitting = 0
    rockets = []

    player_turn = False
    enemy_turn = True
    new_enemy = True

    enemy_data = []
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                if player_turn:
                    for item in center_blocks:
                        if item['rect'].collidepoint(event.pos):
                            item['color'] = CENTER_BLOCKS_WHEN_PRESSED_COLOR
            if event.type == MOUSEMOTION:
                if player_turn:
                    for item in center_blocks:
                        if not item['rect'].collidepoint(event.pos):
                            item['color'] = CENTER_BLOCK_COLOR
                        if item['rect'].collidepoint(event.pos):
                            item['color'] = CENTER_BLOCKS_WHEN_PRESSED_COLOR
            if event.type == MOUSEBUTTONUP and event.button == 1:
                if player_turn:
                    for item in center_blocks:
                        if item['rect'].collidepoint(event.pos):
                            item['color'] = CENTER_BLOCK_COLOR
                            rockets.append(rocket_block(item['rect'][0] + 24, item['rect'][1], 'up'))
                            rockets.append(rocket_block(item['rect'][0] + 48, item['rect'][1] + 24, 'right'))
                            rockets.append(rocket_block(item['rect'][0] + 24, item['rect'][1] + 48, 'down'))
                            rockets.append(rocket_block(item['rect'][0], item['rect'][1] + 24, 'left'))
                            for d_enemy in enemy_data:
                                d_enemy['stop'] += 1
                                d_enemy['traffic'] = True
                            if new_enemy:
                                if move < 5:
                                    for pos in (random.sample(list(enemy_positions.values()), 1)):
                                        enemy_data.append(
                                            {'rect': pygame.Rect(pos['position'][0], pos['position'][1], 30, 30),
                                             'dir': pos['dir'], 'traffic': True, 'stop': 0})
                                elif move < 15:
                                    for pos in (random.sample(list(enemy_positions.values()), 2)):
                                        enemy_data.append(
                                            {'rect': pygame.Rect(pos['position'][0], pos['position'][1], 30, 30),
                                             'dir': pos['dir'], 'traffic': True, 'stop': 0})
                                else:
                                    for pos in (random.sample(list(enemy_positions.values()), 3)):
                                        enemy_data.append(
                                            {'rect': pygame.Rect(pos['position'][0], pos['position'][1], 30, 30),
                                             'dir': pos['dir'], 'traffic': True, 'stop': 0})
                                new_enemy = False
                            player_turn = False

        windowSurface.fill(SURFACE_COLOR)

        for block in center_blocks:
            pygame.draw.rect(windowSurface, block['color'], block['rect'])
        for rocket in rockets:
            windowSurface.blit(rocket['surfase'], rocket['rect'])
            if rocket['dir'] == 'up':
                rocket['rect'].top -= SPEED
            if rocket['dir'] == 'right':
                rocket['rect'].left += SPEED
            if rocket['dir'] == 'down':
                rocket['rect'].top += SPEED
            if rocket['dir'] == 'left':
                rocket['rect'].left -= SPEED
            for d_enemy in enemy_data:
                if d_enemy['rect'].colliderect(rocket['rect']):
                    hitting += 1
                    score += 1
                    rockets.remove(rocket)
                    enemy_data.remove(d_enemy)

            if rocket['rect'].top < -20 or \
                    rocket['rect'].left > WINDOWWIDTH or \
                    rocket['rect'].top > WINDOWHEIGHT or \
                    rocket['rect'].left < -20:
                rockets.remove(rocket)
            if not rockets:
                if hitting < 4:
                    move += 1
                    enemy_turn = True
                    new_enemy = True
                else:
                    for d_enemy in enemy_data:
                        d_enemy['stop'] -= 1
                        enemy_turn = False
                        player_turn = True
                hitting = 0
        if enemy_turn is True and player_turn is False:
            for d_enemy in enemy_data:
                if d_enemy['dir'] == 'up':
                    if d_enemy['rect'].left < stopping[1:][d_enemy['stop']]:
                        d_enemy['rect'].left += ENEMY_SPEED
                        reached_position(d_enemy, enemy_data, corner_blocks)
                    else:
                        d_enemy['traffic'] = False
                if d_enemy['dir'] == 'right':
                    if d_enemy['rect'].top < stopping[1:][d_enemy['stop']]:
                        d_enemy['rect'].top += ENEMY_SPEED
                        reached_position(d_enemy, enemy_data, corner_blocks)
                    else:
                        d_enemy['traffic'] = False
                if d_enemy['dir'] == 'down':
                    if d_enemy['rect'].left > stopping[-2::-1][d_enemy['stop']]:
                        d_enemy['rect'].left -= ENEMY_SPEED
                        reached_position(d_enemy, enemy_data, corner_blocks)
                    else:
                        d_enemy['traffic'] = False
                if d_enemy['dir'] == 'left':
                    if d_enemy['rect'].top > stopping[-2::-1][d_enemy['stop']]:
                        d_enemy['rect'].top -= ENEMY_SPEED
                        reached_position(d_enemy, enemy_data, corner_blocks)
                    else:
                        d_enemy['traffic'] = False
            if not any([d_enemy['traffic'] for d_enemy in enemy_data]):
                enemy_turn = False
                player_turn = True

        for enemy in enemy_data:
            windowSurface.blit(pygame.transform.scale(enemy_image, (30, 30)), enemy['rect'])

        for corner_block in corner_blocks:
            windowSurface.blit(corner_block['surfase'], corner_block['rect'])
        pos = pygame.mouse.get_pos()
        mouse_block_rect = (pos[0] - 1, pos[1] - 1, 6, 6)
        mouse_block = {'rect': mouse_block_rect, 'color': BLACK}
        if pygame.mouse.get_focused():
            pygame.draw.rect(windowSurface, mouse_block['color'], mouse_block['rect'])

        drawText(f'Счёт: {score}', font(35), windowSurface, 40, 40)
        drawText(f'Рекорд: {topScore}', font(35), windowSurface, 40, 65)
        drawText(f'Жизни: {life}', font(35), windowSurface, 40, 90)

        pygame.display.update()
        if life <= 0:
            if score > topScore:
                topScore = score
            break
        clock.tick(FPS)

    windowSurface.fill(SURFACE_COLOR)
    drawText('ИГРА ОКОНЧЕНА!', font(50), windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
    drawText('Нажмите клавишу для начала новой игры', font(50), windowSurface, (WINDOWWIDTH / 3) - 120,
             (WINDOWHEIGHT / 3) + 50)
    pygame.display.update()
    waitForPlayerToPressKey()
