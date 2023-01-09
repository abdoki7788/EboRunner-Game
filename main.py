import pygame
from sys import exit

pygame.init()
pygame.display.set_caption('Runner')

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 400

SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

clock = pygame.time.Clock()
sky_surface = pygame.image.load('graphics/Sky.png').convert_alpha()
ground_surface = pygame.image.load('graphics/ground.png').convert_alpha()

test_font = pygame.font.Font('font/Pixeltype.ttf', 40)
score = 0
score_surface =  test_font.render(f'score: {score}', False, (64,64,64))
score_rectangle = score_surface.get_rect(center=(WINDOW_HEIGHT, 20))

snail_surface = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_rectangle = snail_surface.get_rect(bottomright=(800, 300))
player_surface = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_rectangle = player_surface.get_rect(midbottom=(60, 300))

player_gravity = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if (
            (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) or 
            event.type == pygame.MOUSEBUTTONDOWN) and player_rectangle.bottom == 300:
            player_gravity = -20
    
    SCREEN.blit(sky_surface, (0, 0))
    SCREEN.blit(ground_surface, (0, 300))

    pygame.draw.rect(SCREEN, '#a9ddfc', score_rectangle, border_radius=3)
    
    SCREEN.blit(score_surface, score_rectangle)

    SCREEN.blit(snail_surface, snail_rectangle)
    snail_rectangle.right -= 5
    if snail_rectangle.right <= 0 : snail_rectangle.left = 800

    player_gravity += 1
    SCREEN.blit(player_surface, player_rectangle)
    player_rectangle.y += player_gravity
    if player_rectangle.bottom >= 300:
        player_rectangle.bottom = 300

    pygame.display.update()
    clock.tick(60)