import pygame
import random
from sys import exit
from random import randint, choice

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
        player_walk2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk1, player_walk2]
        self.player_index = 0
        self.player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (100, 300))
        self.gravity = 0
        
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
    
    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300
    
    def update(self):
        self.player_input()
        self.apply_gravity()
        self.playerAnimation()
        
    def playerAnimation(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk): self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        if type == 'fly':
            fly_frame1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
            fly_frame2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
            self.frames = [fly_frame1, fly_frame2]
            y_pos = 210
            
        else: 
            snail_frame1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_frame2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_frame1, snail_frame2]
            y_pos = 300
            
        self.animationIndex = 0
        
        self.image = self.frames[self.animationIndex]
        self.rect = self.image.get_rect(midbottom = (random.randint(100, 200)*8, y_pos))
    
    def animationState(self):
         self.animationIndex += 0.1
         if self.animationIndex >= len(self.frames): self.animationIndex = 0
         self.image = self.frames[int(self.animationIndex)]
    
    def update(self):
        self.animationState()
        self.rect.x -= 8
        self.position()
        self.destroy()
        
    def position(self):
        return self.rect.right
    
    def destroy(self):
        if self.rect.x <= -100:
            self.kill()
    
            
def display_score(game_score):
    score_surface = test_font.render(f'{game_score}', False, (64, 64, 64))
    score_rect = score_surface.get_rect(center = (760, 30))
    scoreText_surface = test_font.render('Score: ', False, (64, 64, 64))
    scoreText_rect = scoreText_surface.get_rect(midright = (740, 30))
    screen.blit(score_surface, score_rect)
    screen.blit(scoreText_surface, scoreText_rect)

def endNotes():
     num1 = random.randrange(0, 9)
     notes = ["You lose! You must suck.", "You lost to a snail! How embarrassing.", "Maybe you should try another day.", "You'll get 'em next time, tiger.",
              "Good effort, sport.", "Oops! You lost!", "The objective is to avoid the obstacles!", "Good try! ... not really", "Goodness you are terrible at this.", "Ouch!"]
     return notes[num1]

def collisionSprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        return False
    else:
        return True
            
pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Gamer Mode 9000')
clock = pygame.time.Clock()

game_active = False
player_gravity = 0
gameScore = 0
gameState = 0

player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

#loads environment, fonts
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
sky_surface = pygame.image.load('graphics/Sky.png')
ground_surface = pygame.image.load('graphics/ground.png')

player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand_rect = player_stand.get_rect(center = (400, 200))

eT2 = test_font.render('Pixel Runner', False, (111, 196, 169))   
eT2_rect = eT2.get_rect(center = (400, 300))


#timers
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 900)
snail_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_timer, 500)
fly_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_timer, 200)

while True:
    #draw all our elements and update everything
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
                
        else:
          if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
              game_active = True

        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly','snail','snail', 'snail'])))   
                    
                     
    if game_active:        
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))

        endNote = endNotes()
            
        player.draw(screen)
        player.update()
        
        obstacle_group.draw(screen)
        obstacle_group.update()
        
        for obstacle in obstacle_group:
            if Obstacle.position(obstacle) == 80:
                gameScore += 1
        
        game_active = collisionSprite()
        
        display_score(gameScore)   
    else:
        screen.fill((94, 129, 162))
        if gameState == 0:
            endText = test_font.render('Press Space to Start!', False, (64, 64, 64))
            endText_rect = endText.get_rect(center = (400, 100))
            screen.blit(player_stand, player_stand_rect)
            screen.blit(eT2, eT2_rect)
            screen.blit(endText, endText_rect)
        else:
            endText = test_font.render(f'{endNote}', False, (64, 64, 64))
            endText_rect = endText.get_rect(center = (400, 100))
            screen.blit(player_stand, player_stand_rect)
            display_score(gameScore)
            screen.blit(eT2, eT2_rect)
            screen.blit(endText, endText_rect)
        
        
    pygame.display.update()
    clock.tick(60)
    