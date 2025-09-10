import pygame

tile_size = 256 #each tile is 256x256 pixels

class Room:
    def __init__(self,tilemap):
        self.tilemap = tilemap
        self.floor_tiles = [] #will store position of all floor tiles
        self.wall_tiles = [] #will store position of all wall tiles
        #calculates offsets to center map
        self.room_x_offset = (512 - len(tilemap[0])*tile_size)//2
        self.room_y_offset = (512 - len(tilemap)*tile_size)//2
        #load images for tiles
        self.floor = pygame.image.load("haunted key hunt game/assets/roomTiles/floor.png")
        self.wall = pygame.image.load("haunted key hunt game/assets/roomTiles/wall.png")

        #processing tilemap
        for row_index, row in enumerate(tilemap): #loops through rows
            for column_index, tile in enumerate(row): 
                x = column_index * tile_size + self.room_x_offset #gives x pixel pos
                y = row_index * tile_size + self.room_y_offset # gives y pixel pos
                if tile == 'floor':
                    self.floor_tiles.append((x,y)) #store in floor list if its a floor
                elif tile == 'wall':
                    self.wall_tiles.append((x,y)) # store in wall list if its a wall
        
        #drawing the room onto the screen
    def draw(self,screen,camerax,cameray):
        for x, y in self.floor_tiles:
            screen.blit(self.floor, (x-camerax, y-cameray))
        for x, y in self.wall_tiles:
            screen.blit(self.wall, (x-camerax, y-cameray))