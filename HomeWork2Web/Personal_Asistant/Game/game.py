import random
import os

import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT

def main():
    pygame.init()
    
    FPS = pygame.time.Clock()
    
    HEIGHT = 800
    WIDTH = 1200
    
    FONT = pygame.font.SysFont('Verdana', 20)
    
    COLOR_BLACK = (0, 0, 0)
    
    IMAGE_PATH = "Personal_assistant\Game\moution"
    PLAYER_IMAGES = os.listdir(IMAGE_PATH)
    
    main_display = pygame.display.set_mode((WIDTH, HEIGHT))
    
    bg = pygame.transform.scale( pygame.image.load('Personal_assistant\Game\\background.png'),(WIDTH,HEIGHT))
    bg_X1 = 0
    bg_X2 = bg.get_width()
    bg_move=4
    
    player_size = (10, 10)
    player = pygame.image.load('Personal_assistant\Game\player.png').convert_alpha() 
    player_rect = player.get_rect()
    player_rect.topleft = (0, HEIGHT // 2)
    player_rect.width = player.get_width()
    player_rect.height = player.get_height()
    player_move_down  = [0 , 5]
    player_move_right = [5 , 0]
    player_move_left  = [-5 ,0]
    player_move_up    = [0 ,-5]
    
    def create_enemy():
        enemy_size = (200, 100)
        enemy = pygame.image.load('Personal_assistant\Game\enemy.png').convert_alpha() 
        enemy = pygame.transform.scale(enemy, enemy_size) 
        enemy_rect = pygame.Rect(WIDTH, random.randint(200,600) , *enemy_size)
        enemy_move = [random.randint(-9, -6), 0]
        return [enemy, enemy_rect, enemy_move]
    
    def create_bonus():
        bonus_size = (70, 70)
        bonus = pygame.image.load('Personal_assistant\Game\\bonus.png').convert_alpha()
        bonus = pygame.transform.scale(bonus, bonus_size)   
        bonus_rect = pygame.Rect( random.randint(200,1000),0 , *bonus_size)
        bonus_move = [0,random.randint(6, 9)]
        return [bonus, bonus_rect, bonus_move]
    
    def create_gameover():
        gameover_size = (800, 800) 
    
        gameover = pygame.image.load('Personal_assistant\Game\gameover.png').convert_alpha()
        gameover = pygame.transform.scale(gameover, gameover_size)
    
        gameover_rect = pygame.Rect(200, 100, *gameover_size)
    
        return [gameover, gameover_rect]
    
    def show_gameover():
        gameover, gameover_rect = create_gameover()
        main_display.blit(gameover, gameover_rect)
        pygame.display.flip()
        pygame.time.delay(10)
    
    
    
    CREATE_ENEMY = pygame.USEREVENT +1
    pygame.time.set_timer(CREATE_ENEMY, 1500)
    
    CREATE_BONUS = pygame.USEREVENT +2
    pygame.time.set_timer(CREATE_BONUS, 1000)
    
    CHANGE_IMAGES = pygame.USEREVENT +3
    pygame.time.set_timer(CHANGE_IMAGES , 200)
    
    enemies = []
    
    bonuses = []
    
    score = 0
    
    image_index = 0
    
    playing = True
    
    while playing:
        FPS.tick(120)
    
        for event in pygame.event.get():
            if event.type == QUIT:
                playing = False
            if event.type == CREATE_ENEMY:
              enemies.append(create_enemy())
            if event.type == CREATE_BONUS:
              bonuses.append(create_bonus())
            if event.type == CHANGE_IMAGES:
              player = pygame.image.load(os.path.join(IMAGE_PATH, PLAYER_IMAGES[image_index]))
              image_index += 1
              if image_index >= len(PLAYER_IMAGES):
                 image_index = 0
    
        bg_X1 -= bg_move
        bg_X2 -= bg_move
    
        if bg_X1 < -bg.get_width():
            bg_X1 = bg.get_width()
    
        if bg_X2 < -bg.get_width():
            bg_X2 = bg.get_width()
    
        main_display.blit(bg, (bg_X1, 0))
        main_display.blit(bg, (bg_X2, 0))
    
        keys = pygame.key.get_pressed()
    
        if keys [K_DOWN] and player_rect.bottom < HEIGHT:
            player_rect =  player_rect.move(player_move_down)
    
        if keys [K_RIGHT] and player_rect.right < WIDTH:
            player_rect =  player_rect.move(player_move_right)
    
        if keys [K_LEFT] and player_rect.left >= 0:
            player_rect =  player_rect.move(player_move_left)
    
        if keys [K_UP] and player_rect.top >= 0:
            player_rect =  player_rect.move(player_move_up)
    
        for enemy in enemies:
         enemy[1] = enemy[1].move(enemy[2])
         main_display.blit(enemy[0], enemy[1])
    
         if player_rect.colliderect( enemy[1]):
            show_gameover()
            playing = False
    
        for bonus in bonuses:
         bonus[1] = bonus[1].move(bonus[2])
         main_display.blit(bonus[0], bonus[1])
    
         if player_rect.colliderect( bonus[1]):
            score  += 50
            bonuses.pop(bonuses.index(bonus))
    
        main_display.blit(FONT.render(str(score),True,COLOR_BLACK),(WIDTH-50,20))
        main_display.blit(player, player_rect)
    
        pygame.display.flip()
    
        enemies = [enemy for enemy in enemies if enemy[1].left >= 0]
    
        bonuses = [bonus for bonus in bonuses if bonus[1].bottom <= HEIGHT]
    pygame.quit()
pygame.QUIT

if __name__ == "__main__":
    main()