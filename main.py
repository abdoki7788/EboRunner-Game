import pygame
from sys import exit
from random import randint

pygame.init()
pygame.display.set_caption('Runner')

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 400

SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

clock = pygame.time.Clock()
sky_surface = pygame.image.load('graphics/Sky.png').convert_alpha()
ground_surface = pygame.image.load('graphics/ground.png').convert_alpha()

game_active = False

score_font = pygame.font.Font('font/Pixeltype.ttf', 40)

title_text = score_font.render('Ebo Runner !', False, (111, 196, 169))
title_rectangle = title_text.get_rect(center=(400, 40))

start_font = pygame.font.Font('font/Pixeltype.ttf', 50)
start_text = start_font.render('Press Space to Start !', False, (60, 60, 60))
start_rectangle = start_text.get_rect(center=(400, 350))


start_time = 0

def display_score():
    score = (pygame.time.get_ticks() - start_time) // 1000
    score_surface =  score_font.render(f'Score: {score}', False, (64,64,64))
    score_rectangle = score_surface.get_rect(center=(400, 50))
    pygame.draw.rect(SCREEN, '#a9ddfc', score_rectangle, border_radius=3)
    SCREEN.blit(score_surface, score_rectangle)
    return score

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5
            if obstacle_rect.bottom == 300:
                SCREEN.blit(snail_surface, obstacle_rect)
            elif obstacle_rect.bottom == 210:
                SCREEN.blit(fly_surface, obstacle_rect)
        obstacle_list = [obstacle for obstacle in obstacle_list if not obstacle.right <= 0]
        return obstacle_list
    else:
        return []

def player_animation():
    global player_surface, player_index

    if player_rectangle.bottom < 300:
        player_surface = player_jump
    else:
        player_index += 0.2
        if player_index >= len(player_walk): player_index = 0
        player_surface = player_walk[int(player_index)]

snail_surface = pygame.image.load('graphics/snail/snail1.png').convert_alpha()

fly_surface = pygame.image.load('graphics/fly/fly1.png').convert_alpha()

player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0
player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()
player_surface = player_walk[player_index]
player_rectangle = player_surface.get_rect(midbottom=(60, 300))
player_gravity = 0

player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand_transform = pygame.transform.scale2x(player_stand)
player_stand_rectangle = player_stand_transform.get_rect(center=(400, 150))

score = 0

obstacle_rect_list = []

OBSTACLE_TIMER = pygame.USEREVENT + 1
pygame.time.set_timer(OBSTACLE_TIMER, 1600)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if (
                (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) or 
                event.type == pygame.MOUSEBUTTONDOWN) and player_rectangle.bottom == 300:
                player_gravity = -18
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                obstacle_rect_list = []
                start_time = pygame.time.get_ticks()
                game_active = True
        if event.type == OBSTACLE_TIMER and game_active:
            if randint(0,2):
                obstacle_rect_list.append(snail_surface.get_rect(bottomleft=(randint(900, 1100), 300)))
            else:
                obstacle_rect_list.append(fly_surface.get_rect(bottomleft=(randint(900, 1100), 210)))
    if game_active:
        SCREEN.blit(sky_surface, (0, 0))
        SCREEN.blit(ground_surface, (0, 300))
        score = display_score()

        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        player_gravity += 0.8
        SCREEN.blit(player_surface, player_rectangle)
        player_rectangle.y += player_gravity
        if player_rectangle.bottom >= 300: player_rectangle.bottom = 300
        player_animation()
        for rect in obstacle_rect_list:
            if rect.colliderect(player_rectangle):
                game_active = False
    else:
        SCREEN.fill((94, 129, 162))
        SCREEN.blit(title_text, title_rectangle)
        SCREEN.blit(player_stand_transform, player_stand_rectangle)
        SCREEN.blit(start_text, start_rectangle)
        if score > 0:
            score_message = score_font.render(f'Your score: {score}', False, (64,64,64))
            score_message_rectangle = score_message.get_rect(center=(400, 280))
            pygame.draw.rect(SCREEN, (111, 196, 169), score_message_rectangle, border_radius=3)
            SCREEN.blit(score_message, score_message_rectangle)
    pygame.display.update()
    clock.tick(60)