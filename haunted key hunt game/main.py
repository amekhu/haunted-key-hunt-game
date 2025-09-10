import pygame
import random
import sys
from rooms import Room #imports room class
from player import Player #imports player class
from ghost import Ghost #imports ghost class
from projectile import Projectile #imports projectile class
from key import Key #imports key class
from ui import UI #imports UI class

def run_game():

    pygame.init() #initialises pygame
    pygame.mixer.init() #initialises audio
    clock = pygame.time.Clock() #sets up clock
    pygame.display.set_caption('Haunted Key Hunt') #sets window name
    screen = pygame.display.set_mode((1024, 800))

    #loads bgm
    pygame.mixer.music.load("haunted key hunt game/assets/spooky piano.mp3")
    pygame.mixer.music.play(-1)  # -1 means loop indefinitely
    pygame.mixer.music.set_volume(0.5)  #sets volume to 50%

    #create UI instance
    ui = UI(screen)

    #camera offsets
    camerax = 0
    cameray = 0

    tilemap = [ #tilemap layout in a 2D list
        ['wall', 'wall', 'wall', 'wall', 'wall', 'wall', 'wall', 'wall','wall', 'wall', 'wall', 'wall', 'wall', 'wall', 'wall', 'wall'],
        ['wall', 'floor', 'wall', 'floor', 'floor', 'floor', 'floor', 'wall','wall', 'floor', 'floor', 'wall', 'floor', 'floor', 'floor', 'wall'],
        ['wall', 'floor', 'wall', 'floor', 'floor', 'floor', 'floor', 'wall','wall', 'floor', 'floor', 'wall', 'floor', 'floor', 'floor', 'wall'],
        ['wall', 'floor', 'wall', 'floor', 'floor', 'floor', 'floor', 'floor', 'floor', 'floor', 'floor', 'wall', 'wall', 'wall', 'floor', 'wall'],
        ['wall', 'floor', 'floor', 'floor', 'floor', 'floor', 'floor', 'floor','floor', 'floor', 'floor', 'floor', 'floor', 'floor', 'floor', 'wall'],
        ['wall', 'floor', 'floor', 'floor', 'floor', 'floor', 'floor', 'wall','wall', 'floor', 'floor', 'floor', 'floor', 'floor', 'floor', 'wall'],
        ['wall', 'wall', 'floor', 'floor', 'wall', 'wall', 'wall', 'wall','wall', 'wall', 'wall', 'wall', 'floor', 'floor', 'wall', 'wall'],
        ['wall', 'wall', 'floor', 'floor', 'wall', 'wall', 'wall', 'wall','wall', 'wall', 'wall', 'wall', 'floor', 'floor', 'wall', 'wall'],
        ['wall', 'floor', 'floor', 'floor', 'floor', 'floor', 'floor', 'wall','wall', 'floor', 'floor', 'floor', 'floor', 'floor', 'floor', 'wall'],
        ['wall', 'floor', 'wall', 'floor', 'floor', 'floor', 'floor', 'floor','floor', 'floor', 'floor', 'floor', 'floor', 'floor', 'floor', 'wall'],
        ['wall', 'floor', 'floor', 'floor', 'floor', 'floor', 'floor', 'floor', 'floor', 'floor', 'floor', 'wall', 'wall', 'wall', 'wall', 'wall'],
        ['wall', 'floor', 'wall', 'floor', 'floor', 'floor', 'floor', 'wall','wall', 'floor', 'floor', 'wall', 'floor', 'floor', 'floor', 'wall'],
        ['wall', 'floor', 'wall', 'floor', 'floor', 'floor', 'floor', 'wall','wall', 'floor', 'floor', 'floor', 'floor', 'floor', 'floor', 'wall'],
        ['wall', 'wall', 'wall', 'wall', 'wall', 'wall', 'wall', 'wall','wall', 'wall', 'wall', 'wall', 'wall', 'wall', 'wall', 'wall']
        ]

    #makes room instance
    room = Room(tilemap)

    #finds a valid start position for player
    valid_floor = [(x,y) for y, row in enumerate(tilemap) for x, tile in enumerate(row) if tile == 'floor']
    player_x, player_y = random.choice(valid_floor) #chooses random spawning pos for player
    player_x = player_x * 256 + room.room_x_offset
    player_y = player_y * 256 + room.room_y_offset
    #makes player instance
    player = Player(player_x, player_y, room)

    #spawn keys
    Key.spawn_keys(tilemap, room)

    #game loop
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False #closes game when window is shut down
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and not ui.is_game_paused():
                if event.button == 1: #left mouse click
                    #gets mouse pos and creates projectile
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    #adjusts for camera offset
                    target_x = mouse_x + camerax
                    target_y = mouse_y + cameray
                    #creates new projectile from players pos
                    Projectile(player.rect.centerx, player.rect.centery, target_x, target_y, room, player)

        #centres the player in the camera
        camerax = player.rect.x - screen.get_width()//2
        cameray = player.rect.y - screen.get_height()//2

        screen.fill((0,0,0)) #clears screen
        room.draw(screen, camerax, cameray) #draws room

        #draws all game elements
        player.draw(screen, camerax, cameray)
        
        for ghost in Ghost.active_ghosts:
            if ghost.active:
                ghost.draw(screen, camerax, cameray)
                
        for key in Key.active_keys:
            if key.active:
                key.draw(screen, camerax, cameray)
                
        for projectile in Projectile.active_projectiles:
            projectile.draw(screen, camerax, cameray)

        #only updates elements if not paused
        if not ui.is_game_paused():
            player.update()
            
            #spawns a new ghost
            Ghost.spawn_ghost(tilemap, room)

            #update all active ghosts
            for ghost in Ghost.active_ghosts[:]:
                if ghost.active:
                    ghost.update(player.rect.x, player.rect.y)
                    ghost.check_player_collision(player)
                else:
                    Ghost.active_ghosts.remove(ghost)
                    
            #check for key collection
            for key in Key.active_keys[:]:
                if key.active:
                    key.check_player_collision(player)
                else:
                    Key.active_keys.remove(key)

            #update projectiles
            for projectile in Projectile.active_projectiles[:]:
                projectile.update()
                
        #draws gui
        ui.draw_hud(player)
        
        #check for death or victory
        if player.stats.lives <= 0:
            ui.draw_game_over(player, victory=False)
        elif len(Key.active_keys) == 0:  #all keys collected
            ui.draw_game_over(player, victory=True)
                    
        pygame.display.flip()
        clock.tick(60)

    return screen
