import pygame
import random
import os


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * height for _ in range(width)]
        self.left = 0
        self.top = 0
        self.cell_size = 10

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self):
        screen.fill('blue')
        for i in forbidden:
            pygame.draw.rect(screen, 'white', (i[0] * (HEIGHT // size[0]), i[1] * (WIDTH // size[1]),
                                               self.cell_size, self.cell_size))
        pygame.draw.rect(screen, players[0].color, (players[0].poses[0][0] * (HEIGHT // size[0]),
                                                    players[0].poses[0][1] * (WIDTH // size[1]), self.cell_size,
                                                    self.cell_size))
        pygame.draw.rect(screen, players[1].color, (players[1].poses[0][0] * (HEIGHT // size[0]),
                                                    players[1].poses[1][1] * (WIDTH // size[1]), self.cell_size,
                                                    self.cell_size))
        pygame.display.flip()


class Bike:
    def __init__(self, coords, color):
        self.poses = [coords]
        self.rot = [0, 0]
        if coords[0] == 0:
            self.rot = [1, 0]
        elif coords[0] == size[0] - 1:
            self.rot = [-1, 0]
        if coords[1] == 0:
            self.rot = [0, 1]
        elif coords[1] == size[1] - 1:
            self.rot = [0, -1]
        self.color = color

    def __eq__(self, other):
        return self.color == other.color

    def move(self, forbidden):
        global players
        self.poses.insert(0, [self.poses[0][0] + self.rot[0], self.poses[0][1] + self.rot[1]])
        if self.poses[0] in forbidden:
            if self.color == 'red':
                won.append('green')
            if self.color == 'green':
                won.append('red')
        return self.poses


def load_image(name):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname)
    return image


def start_screen():
    fon = pygame.transform.scale(load_image('fon.png'), (HEIGHT, WIDTH))
    screen.blit(fon, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        event = pygame.key.get_pressed()
        if event[pygame.K_LSHIFT] or event[pygame.K_RSHIFT]:
            game()
        if event[pygame.K_SPACE]:
            info()
        if event[pygame.K_ESCAPE]:
            return
        screen.blit(fon, (0, 0))
        pygame.display.flip()


def info():
    fon = pygame.transform.scale(load_image('info.png'), (HEIGHT, WIDTH))
    screen.blit(fon, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        event = pygame.key.get_pressed()
        if event[pygame.K_BACKSPACE]:
            return
        screen.blit(fon, (0, 0))
        pygame.display.flip()


def game():
    global players
    global forbidden
    global won
    coords = [0, 0]
    forbidden = []
    won = []
    for i in range(size[0]):
        forbidden.append([i, 0])
        forbidden.append([i, size[1] - 1])
    for i in range(size[1]):
        forbidden.append([0, i])
        forbidden.append([size[0] - 1, i])
    while coords[0] == coords[1]:
        coords = []
        for i in range(2):
            if random.choice([True, False]):
                coords.append([random.choice([0, size[0] - 1]), random.choice(range(0, size[1] - 1))])
            else:
                coords.append([random.randint(0, size[0] - 1), random.choice([0, size[1] - 1])])
    players = [Bike(coords[0], 'red'), Bike(coords[1], 'green')]
    board = Board(HEIGHT, WIDTH)
    board.set_view(0, 0, HEIGHT // size[0])
    while len(won) == 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        btns = pygame.key.get_pressed()
        if btns[pygame.K_UP] and players[0].rot != [0, 1]:
            players[0].rot = [0, -1]
        if btns[pygame.K_DOWN] and players[0].rot != [0, -1]:
            players[0].rot = [0, 1]
        if btns[pygame.K_LEFT] and players[0].rot != [1, 0]:
            players[0].rot = [-1, 0]
        if btns[pygame.K_RIGHT] and players[0].rot != [-1, 0]:
            players[0].rot = [1, 0]
        if btns[pygame.K_w] and players[1].rot != [0, 1]:
            players[1].rot = [0, -1]
        if btns[pygame.K_s] and players[1].rot != [0, -1]:
            players[1].rot = [0, 1]
        if btns[pygame.K_a] and players[1].rot != [1, 0]:
            players[1].rot = [-1, 0]
        if btns[pygame.K_d] and players[1].rot != [-1, 0]:
            players[1].rot = [1, 0]
        if btns[pygame.K_ESCAPE]:
            return

        for i in players:
            forbidden += i.move(forbidden)
        clock.tick(FPS)
        board.render()
    winner()


def winner():
    fon = load_image(won[0] + '.png')
    screen.blit(fon, (0, 0))
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        if pygame.key.get_pressed()[pygame.K_BACKSPACE]:
            return


FPS = 30
HEIGHT = 1000
WIDTH = 700
pygame.init()
screen = pygame.display.set_mode([HEIGHT, WIDTH])
clock = pygame.time.Clock()
size = [100, 70]
players = []
forbidden = []
won = []
for i in range(size[0]):
    forbidden.append([i, 0])
    forbidden.append([i, size[1] - 1])
for i in range(size[1]):
    forbidden.append([0, i])
    forbidden.append([size[0] - 1, i])
start_screen()
