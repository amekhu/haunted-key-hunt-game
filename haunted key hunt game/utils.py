import pygame
import math

def check_wall_collision(x, y, room, entity_size=(25, 27)):
    #collision detection function for both player and ghosts
    for wall_x, wall_y in room.wall_tiles:
        if pygame.Rect(wall_x, wall_y, 256, 256).colliderect(pygame.Rect(x, y, *entity_size)):
            return True
    return False

def draw_entity(screen, image, x, y, camerax, cameray):
    #drawing function for entities with camera offset
    screen.blit(image, (x - camerax, y - cameray))

def move_entity(current_x, current_y, dx, dy, room, check_collision_func):
    #movement function that handles collision checking
    new_x = current_x + dx
    new_y = current_y + dy
    if not check_collision_func(new_x, new_y):
        return new_x, new_y, True
    return current_x, current_y, False

def calculate_distance(x1, y1, x2, y2):
    #calculates distance between any two points
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def check_entity_collision(entity, player, action_function):
    #collision detection between an entity and the player
    if entity.active and entity.rect.colliderect(player.rect):
        return action_function(player)
    return False