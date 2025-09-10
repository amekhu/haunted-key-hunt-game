import pygame
import random
import time
import math
from utils import check_wall_collision, move_entity, draw_entity, calculate_distance, check_entity_collision

class Ghost(pygame.sprite.Sprite):

    active_ghosts = [] #list of all ghosts in the game
    max_ghosts = 6 #max number of ghosts that can be in the game at once
    spawn_delay = 10 #time between ghost spawns in seconds
    last_spawn_time = time.time() #when the last ghost was spawned

    def __init__(self, x, y, tilemap, room):
        super().__init__()
        #loads the ghost image
        self.image = pygame.image.load('haunted key hunt game/assets/ghostSprite/front1.png')
        self.rect = self.image.get_rect(topleft=(x, y))
        #where the ghost is
        self.x = x
        self.y = y
        #where the ghost started (for patrol)
        self.start_x = x
        self.start_y = y
        #how fast the ghost moves
        self.speed = 3
        #stuff the ghost needs to know about the map
        self.tilemap = tilemap
        self.room = room
        #whether the ghost is active in the game
        self.active = True
        #what the ghost is doing
        self.chasing = False  #chasing the player?
        self.returning = False  #going back to start?
        #patrol direction (1 = right, -1 = left)
        self.patrol_direction = 1
        #how close the player needs to be for ghost to chase
        self.chase_radius = 384
        #for timing direction changes
        self.last_direction_change = time.time()
        self.direction_change_delay = 0.5
        #add this ghost to the list of active ghosts
        Ghost.active_ghosts.append(self)

    @classmethod
    def spawn_ghost(cls, tilemap, room):
        #check if we can spawn more ghosts
        if len(cls.active_ghosts) >= cls.max_ghosts:
            return None
        #check if enough time has passed since last spawn
        current_time = time.time()
        if current_time - cls.last_spawn_time <= cls.spawn_delay:
            return None
        #find valid places where ghosts can spawn
        valid_tiles = [(x, y) for y, row in enumerate(tilemap) for x, tile in enumerate(row) if tile == 'floor']
        #spawn a ghost at one of the valid tiles
        if valid_tiles: 
            spawn_x, spawn_y = random.choice(valid_tiles)
            #convert tile coords to pixel coords
            ghost = cls(spawn_x * 256 + room.room_x_offset, 
                       spawn_y * 256 + room.room_y_offset, 
                       tilemap, room)
            cls.last_spawn_time = current_time
            return ghost
        return None
    
    def draw(self, screen, camerax, cameray):
        if self.active:
            draw_entity(screen, self.image, self.x, self.y, camerax, cameray)

    def check_collision(self, x, y):
        return check_wall_collision(x, y, self.room)
    
    def move(self, dx, dy):
        new_x, new_y, moved = move_entity(self.x, self.y, dx, dy, self.room, self.check_collision)
        if moved:
            self.x = new_x
            self.y = new_y
        return moved
    
    def patrol(self):
        #makes ghost move back and forth
        dx = self.speed * self.patrol_direction
        if not self.move(dx, 0):
            #if ghost cant move due to collision, change direction
            self.patrol_direction *= -1

    def update(self, player_x, player_y):
        #if ghost is inactive dont update
        if not self.active:
            return
        #updates hitbox position
        self.rect.x = self.x
        self.rect.y = self.y
        #works out distance to decide whether to chase or patrol
        dist_to_player = calculate_distance(self.x, self.y, player_x, player_y)
        #if player is within chase radius, initiate chase
        if dist_to_player <= self.chase_radius:
            self.chasing = True
            self.chase(player_x, player_y)
        else:
            #otherwise keep patrolling
            self.chasing = False
            self.patrol()

    def chase(self, target_x, target_y):
        #works out which way to go
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx**2 + dy**2)
        #normalises direction
        if distance > 0:
            dx = dx / distance
            dy = dy / distance
            #tries to chase diagnoally first
            if not self.move(dx * self.speed, dy * self.speed):
                #if that doesn't work, horizontal then vertical
                if abs(dx) > abs(dy):
                    if not self.move(dx * self.speed, 0):
                        self.move(0, dy * self.speed)
                else:
                    if not self.move(0, dy * self.speed):
                        self.move(dx * self.speed, 0)

    def deactivate(self):
        #removes ghost from game
        self.active = False
        if self in Ghost.active_ghosts:
            Ghost.active_ghosts.remove(self)
        
    def check_player_collision(self, player):
        if not self.active:
            return False
        #checks if ghost has hit player     
        if check_entity_collision(self, player, self.damage_player):
            return True
        return False
        
    def damage_player(self, player):
        #takes away a life and deletes ghost right after but no points added
        if player.take_damage():
            self.deactivate()
            return True
        return False
