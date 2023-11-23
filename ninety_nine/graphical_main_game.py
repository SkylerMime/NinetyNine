import pygame

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

pygame.init()

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

clock = pygame.time.Clock()

while True:
    # process player inputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

    # logical updates here

    screen.fill("purple")

    # render graphics here

    pygame.display.flip()
    clock.tick(60)