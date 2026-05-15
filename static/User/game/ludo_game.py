import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 700, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ludo Game")

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,200,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)

clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

path = []

for x in range(100, 600, 40):
    path.append((x, 100))

for y in range(100, 600, 40):
    path.append((600, y))

for x in range(600, 100, -40):
    path.append((x, 600))

for y in range(600, 100, -40):
    path.append((100, y))


class Player:
    def __init__(self, color, start_index):
        self.color = color
        self.position = -1
        self.start_index = start_index

    def move(self, dice):
        if self.position == -1:
            if dice == 6:
                self.position = self.start_index
        else:
            self.position = (self.position + dice) % len(path)

    def draw(self):
        if self.position != -1:
            x, y = path[self.position]
            pygame.draw.circle(screen, self.color, (x, y), 12)


players = [
    Player(RED, 0),
    Player(GREEN, len(path)//4),
    Player(YELLOW, len(path)//2),
    Player(BLUE, 3*len(path)//4)
]

current_player = 0
dice_value = 1

def draw_board():
    screen.fill(WHITE)

    pygame.draw.rect(screen, RED, (0, 0, 300, 300))
    pygame.draw.rect(screen, GREEN, (400, 0, 300, 300))
    pygame.draw.rect(screen, BLUE, (0, 400, 300, 300))
    pygame.draw.rect(screen, YELLOW, (400, 400, 300, 300))

    pygame.draw.rect(screen, BLACK, (300, 300, 100, 100), 3)

    for p in path:
        pygame.draw.circle(screen, BLACK, p, 5)


def draw_ui():
    text = font.render(f"Dice: {dice_value}", True, BLACK)
    screen.blit(text, (300, 10))

    turn = font.render(f"Player: {current_player+1}", True, BLACK)
    screen.blit(turn, (300, 50))


running = True

while running:
    draw_board()

    for player in players:
        player.draw()

    draw_ui()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                dice_value = random.randint(1, 6)
                players[current_player].move(dice_value)

                if dice_value != 6:
                    current_player = (current_player + 1) % 4

    pygame.display.update()
    clock.tick(30)