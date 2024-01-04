import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Gamer Mode 9000')
clock = pygame.time.Clock()

test_font = pygame.font.Font('font/Pixeltype.ttf', 50)

sky_surface = pygame.image.load('graphics/Sky.png')
ground_surface = pygame.image.load('graphics/ground.png')


text_surface = test_font.render('Score:', False, (64, 64, 64))
text_rect = text_surface.get_rect(center = (400, 50))

snail_surface = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_rect = snail_surface.get_rect(midbottom = (600, 300))


player_surface = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_rect = player_surface.get_rect(midbottom = (80, 300))
player_gravity = 0


while True:
    #draw all our elements and update everything
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE: 
                player_gravity = -20
            
        if event.type == pygame.KEYUP: 
            print("keyup")
            
    screen.blit(sky_surface, (0, 0))
    screen.blit(ground_surface, (0, 300))
    pygame.draw.rect(screen, '#c0e8ec', text_rect,16,5)
    screen.blit(text_surface, text_rect)
    
    snail_rect.x -= 4
    if snail_rect.right <= 0: snail_rect.left = 800

    screen.blit(snail_surface, snail_rect)
    
    #player
    player_gravity += 1
    screen.blit(player_surface, player_rect)
    player_rect.y += player_gravity
    if player_rect.bottom >= 300:
        player_rect.bottom = 300
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        print("jump")
        
    if player_rect.colliderect(snail_rect):
        print('collide')
        
    pygame.display.update()
    clock.tick(60)
    