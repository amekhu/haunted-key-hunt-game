import pygame
import sys
import os
import importlib.util

def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def main():
    pygame.init()
    screen = pygame.display.set_mode((1024, 800))
    pygame.display.set_caption('Haunted Key Hunt')
    
    #gets path to the menu directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    menu_dir = os.path.join(current_dir, 'menu')
    startscreen_path = os.path.join(menu_dir, 'startscreen.py')
    
    #loads start screen module
    startscreen = load_module('startscreen', startscreen_path)
    
    #runs start screen
    screen, high_score = startscreen.run(screen, 0)
    
    #game ends
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
