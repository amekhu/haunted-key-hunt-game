import pygame
import sys
from main import run_game

def run(screen, high_score):
    #colours
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    #loads fonts
    title_font = pygame.font.Font(None, 74)
    font = pygame.font.Font(None, 36)
    #makes texts
    title_text = title_font.render("Haunted Key Hunt", True, WHITE)
    start_text = font.render("Press SPACE to Start", True, WHITE)
    quit_text = font.render("Press Q to Quit", True, WHITE)
    #text rectangles
    title_rect = title_text.get_rect(center=(screen.get_width()//2, 200))
    start_rect = start_text.get_rect(center=(screen.get_width()//2, 300))
    quit_rect = quit_text.get_rect(center=(screen.get_width()//2, 350))    
    #bgm
    pygame.mixer.music.load("haunted key hunt game/assets/spooky piano.mp3")
    pygame.mixer.music.play(-1)  # -1 means loop indefinitely
    pygame.mixer.music.set_volume(0.5)  #sets volume to 50%

    #game loop
    clock = pygame.time.Clock()
    running = True
    
    while running:
        #handles events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = False
                    #runs main loop
                    run_game()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        #draws everything
        screen.fill(BLACK)
        screen.blit(title_text, title_rect)
        screen.blit(start_text, start_rect)
        screen.blit(quit_text, quit_rect)
        
        #updates display
        pygame.display.flip()
        
        #frame rate
        clock.tick(60)

    return screen, high_score
