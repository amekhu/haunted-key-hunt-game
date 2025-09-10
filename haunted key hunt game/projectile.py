import pygame
import math
from ghost import Ghost
from utils import check_wall_collision, draw_entity
from player import Player

class Projectile(pygame.sprite.Sprite):
    #all active projectiles
    active_projectiles = []
    def __init__(self, x, y, target_x, target_y, room, player):
        super().__init__()
        #loads image
        self.image = pygame.image.load('haunted key hunt game/assets/projectile/bullet.png')
        #hitbox
        self.rect = self.image.get_rect(topleft=(x, y))
        #position
        self.x = x
        self.y = y
        #calculate direction vector
        self.room = room
        self.speed = 10
        #calculate angle and direction
        angle = math.atan2(target_y - y, target_x - x)
        self.dx = math.cos(angle) * self.speed
        self.dy = math.sin(angle) * self.speed
        #active or no?
        self.active = True
        #store player reference
        self.player = player
        #adds projectile to list of active ones
        Projectile.active_projectiles.append(self)

    def update(self):
        if not self.active:
            return
        #moves the projectiles
        self.x += self.dx
        self.y += self.dy
        self.rect.x = self.x
        self.rect.y = self.y
        #checks for wall collision
        if check_wall_collision(self.x, self.y, self.room, (8, 8)):
            self.active = False
            Projectile.active_projectiles.remove(self)
            return
        #checks for ghost collision
        for ghost in Ghost.active_ghosts[:]: #makes copy of list so it doesn't change during iteration
            if ghost.active and self.rect.colliderect(ghost.rect):
                self.active = False
                ghost.deactivate()
                Projectile.active_projectiles.remove(self)
                #add 100 points for hitting a ghost
                self.player.add_score(100)
                return
            
    def draw(self, screen, camerax, cameray):
        if self.active:
            draw_entity(screen, self.image, self.x, self.y, camerax, cameray)
