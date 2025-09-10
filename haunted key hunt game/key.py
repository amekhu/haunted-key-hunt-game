import pygame
from utils import draw_entity, check_entity_collision
import random

class Key(pygame.sprite.Sprite):
    #list of all active keys
    active_keys = []
    
    def __init__(self, x, y, room):
        super().__init__()
        #loads key image
        self.image = pygame.image.load("haunted key hunt game/assets/key/key.png")
        self.points = 10  #each key is worth 10 points
        #hitbox
        self.rect = self.image.get_rect(topleft=(x, y))
        #positions
        self.x = x
        self.y = y
        self.room = room
        #key state
        self.active = True
        #adds key to list of active keys
        Key.active_keys.append(self)

    def draw(self, screen, camerax, cameray):
        #draws the key on the screen
        if self.active:
            draw_entity(screen, self.image, self.x, self.y, camerax, cameray)

    def check_player_collision(self, player):
        #checks if player has collided with the key
        return check_entity_collision(self, player, self.collect) 

    def collect(self, player):
        #collects the key and adds points to player score
        if self.active:
            self.active = False
            player.add_score(self.points)
            if self in Key.active_keys:
                Key.active_keys.remove(self)
            return True
        return False

    @classmethod
    def spawn_keys(cls, tilemap, room, max_keys=12):
        #finds valid floor tiles for key spawning
        valid_tiles = [(x, y) for y, row in enumerate(tilemap) for x, tile in enumerate(row) if tile == 'floor']
        #spawns the specified number of keys
        for _ in range(max_keys):
            if valid_tiles:
                key_pos = random.choice(valid_tiles)
                valid_tiles.remove(key_pos)
                cls(key_pos[0] * 256 + room.room_x_offset, 
                    key_pos[1] * 256 + room.room_y_offset, 
                    room)
