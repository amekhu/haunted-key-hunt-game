import pygame
from utils import check_wall_collision, draw_entity, move_entity
from stats import GameStats

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, room):
        super().__init__()

        #loads the different img movements for the different directions
        self.images = {
            #while moving imgs
            'right': [pygame.image.load("haunted key hunt game/assets/playerSprite/right2.png"), pygame.image.load("haunted key hunt game/assets/playerSprite/right3.png")],
            'left': [pygame.image.load("haunted key hunt game/assets/playerSprite/left2.png"), pygame.image.load("haunted key hunt game/assets/playerSprite/left3.png")],
            'up': [pygame.image.load("haunted key hunt game/assets/playerSprite/back2.png"), pygame.image.load("haunted key hunt game/assets/playerSprite/back3.png")],
            'down': [pygame.image.load("haunted key hunt game/assets/playerSprite/front2.png"), pygame.image.load("haunted key hunt game/assets/playerSprite/front3.png")],
            #while idle imgs
            'idle_right': [pygame.image.load("haunted key hunt game/assets/playerSprite/right1.png")],
            'idle_left':[pygame.image.load("haunted key hunt game/assets/playerSprite/left1.png")],
            'idle_up':[pygame.image.load("haunted key hunt game/assets/playerSprite/back1.png")],
            'idle_down':[pygame.image.load("haunted key hunt game/assets/playerSprite/front1.png")],
        }

        self.image = self.images['idle_down'][0] #sets the default movement img to this
        self.rect = self.image.get_rect(topleft=(x,y)) #sets player position
        self.speed = 6 #movement speed
        self.frame_index = 0 #for animating frames
        self.animation_speed = 0.1 #for animation speed
        self.moving = False #checks if player is moving
        self.direction = 'idle_down'
        self.room = room
        #passes stats through to player
        self.stats = GameStats()

    #moves player and checks for wall collisions
    def move(self, dx, dy, direction):
        new_x, new_y, moved = move_entity(self.rect.x, self.rect.y, dx, dy, self.room, self.check_collision)
        if moved:
            self.rect.x = new_x
            self.rect.y = new_y
            self.moving = True
            self.direction = direction
        else:
            self.moving = False

    def check_collision(self, x, y):
        return check_wall_collision(x, y, self.room)
    
    def update(self):
        keys = pygame.key.get_pressed()
        self.moving = False

        if keys[pygame.K_RIGHT]:
            self.move(self.speed, 0, 'right')
        elif keys[pygame.K_LEFT]:
            self.move(-self.speed, 0, 'left')
        elif keys[pygame.K_UP]:
            self.move(0, -self.speed, 'up')
        elif keys[pygame.K_DOWN]:
            self.move(0, self.speed, 'down')

        #handles animation
        if self.moving:
            self.frame_index += self.animation_speed
            if self.frame_index >= len(self.images[self.direction]):
                self.frame_index = 0
            self.image = self.images[self.direction][int(self.frame_index)]
        else:
            self.image = self.images[f'{self.direction}'][0]
    
    #draws player onto screen
    def draw(self, screen, camerax, cameray):
        draw_entity(screen, self.image, self.rect.x, self.rect.y, camerax, cameray)

    #update stats
    def take_damage(self):
        return self.stats.take_damage()
    
    def add_score(self, points):
        self.stats.add_score(points)