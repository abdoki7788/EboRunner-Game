import pygame
from sys import exit
from random import choice, randint

pygame.init()
pygame.display.set_caption('Runner')

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 400

SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('./assets/graphics/player/player_walk_1.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom=(80, 300))
        self.gravity = 0
        self.index = 0
        self.player_walk = [pygame.image.load('./assets/graphics/player/player_walk_1.png'), pygame.image.load('assets/graphics/player/player_walk_2.png')]
        self.jump_sound = pygame.mixer.Sound('./assets/audio/jump.mp3')

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom == 300:
            self.gravity = -18
            self.jump_sound.set_volume(0.3)
            self.jump_sound.play()
    def apply_gravity(self):
        self.gravity += 0.8
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.gravity = 0
            self.rect.bottom = 300
    def animate_player(self):
        if self.rect.bottom < 300:
            self.image = pygame.image.load('assets/graphics/player/jump.png').convert_alpha()
        else:
            self.index += 0.1
            if self.index >= 2: self.index = 0
            self.image = self.player_walk[int(self.index)].convert_alpha()
    
    def update(self, *args, **kwargs):
        self.player_input()
        self.apply_gravity()
        self.animate_player()
        return super().update(*args, **kwargs)

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        if type == 'fly':
            fly_1 = pygame.image.load('assets/graphics/fly/fly1.png').convert_alpha()
            fly_2 = pygame.image.load('assets/graphics/fly/fly2.png').convert_alpha()
            self.surfaces = [fly_1, fly_2]
            y_pos = 200
        elif type == 'snail':
            snail_1 = pygame.image.load('assets/graphics/snail/snail1.png').convert_alpha()
            snail_2 = pygame.image.load('assets/graphics/snail/snail2.png').convert_alpha()
            self.surfaces = [snail_1, snail_2]
            y_pos = 300
        
        self.index = 0
        self.image = self.surfaces[self.index]
        self.rect = self.image.get_rect(bottomleft=(randint(900, 1200), y_pos))
        super().__init__()
    
    def animate_obstacle(self):
        self.index += 0.15
        if self.index >= len(self.surfaces): self.index = 0
        self.image = self.surfaces[int(self.index)].convert_alpha()
    
    def move_obstacle(self):
        self.rect.x -= 5
    
    def update(self, *args, **kwargs):
        self.animate_obstacle()
        self.move_obstacle()
        if self.rect.right <= 0:
            self.kill()
        return super().update(*args, **kwargs)

clock = pygame.time.Clock()
sky_surface = pygame.image.load('assets/graphics/Sky.png').convert_alpha()
ground_surface = pygame.image.load('assets/graphics/ground.png').convert_alpha()

game_active = False

score_font = pygame.font.Font('assets/font/Pixeltype.ttf', 40)
title_text = score_font.render('Abdolrahman Runner !', False, (111, 196, 169))
title_rectangle = title_text.get_rect(center=(400, 40))

start_font = pygame.font.Font('assets/font/Pixeltype.ttf', 50)
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


player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle = pygame.sprite.Group()

player_stand = pygame.image.load('assets/graphics/player/player_stand.png').convert_alpha()
player_stand_transform = pygame.transform.scale2x(player_stand)
player_stand_rectangle = player_stand_transform.get_rect(center=(400, 150))

score = 0

lose_sound = pygame.mixer.Sound('./assets/audio/lose.wav')
bg_sound = pygame.mixer.Sound('./assets/audio/music.wav')
bg_sound.set_volume(0.5)

obstacle_rect_list = []

OBSTACLE_TIMER = pygame.USEREVENT + 1
pygame.time.set_timer(OBSTACLE_TIMER, 1400)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == OBSTACLE_TIMER:
                obstacle.add(Obstacle(choice(['snail','snail','fly',])))
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                start_time = pygame.time.get_ticks()
                game_active = True
                bg_sound.play(loops=-1)

    if game_active:
        SCREEN.blit(sky_surface, (0, 0))
        SCREEN.blit(ground_surface, (0, 300))
        score = display_score()

        obstacle.draw(SCREEN)
        obstacle.update()
        player.draw(SCREEN)
        player.update()

        if pygame.sprite.spritecollide(player.sprite, obstacle, False):
            bg_sound.stop()
            lose_sound.play()
            game_active = False
            obstacle.empty()
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