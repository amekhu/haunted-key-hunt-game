import pygame
import os
import sys

class UI:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        #loads heart image
        self.heart_image = pygame.image.load("haunted key hunt game/data/ui/heart.png")
        #for the game over screen
        self.button_font = pygame.font.Font(None, 30)
        self.high_score = 0
        self.load_high_score()
        self.game_paused = False
        
    def load_high_score(self):
        #loads highscore from txt file
        if os.path.exists("haunted key hunt game/data/highscore.txt"):
            with open("haunted key hunt game/data/highscore.txt", "r") as f:
                content = f.read().strip()
                    #converts the content to an integer
                self.high_score = int(content)
                
    def update_high_score(self, player_score):
        #updates highscore if players score is higher
        if player_score > self.high_score:
            self.high_score = player_score
            #saves new high score as number in txt file
            with open("haunted key hunt game/data/highscore.txt", "w") as f:
                f.write(str(self.high_score))
            
    def draw_hud(self, player):
        #draw hearts and score based off stats
        for i in range(player.stats.lives):
            self.screen.blit(self.heart_image, (10 + i * 40, 10))
        score_text = self.font.render(f"Score: {player.stats.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (self.screen.get_width() - score_text.get_width() - 10, 10))

    def draw_game_over(self, player, victory=False):
        #sets game in background to pause
        self.game_paused = True
        #updates high score when game over
        self.update_high_score(player.stats.score)
        #creates transparent overlay
        overlay = pygame.Surface(self.screen.get_size())
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)
        self.screen.blit(overlay, (0, 0))
        #draws game over or victory text
        font = pygame.font.Font(None, 74)
        if victory:
            text = font.render('You Escaped!', True, (0, 255, 0))
        else:
            text = font.render('Game Over!', True, (255, 0, 0))
        text_rect = text.get_rect(center=(self.screen.get_width()/2, self.screen.get_height()/2 - 50))
        self.screen.blit(text, text_rect)
        #draws score tecxt
        score_font = pygame.font.Font(None, 36)
        score_text = score_font.render(f'Your Score: {player.stats.score}', True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(self.screen.get_width()/2, self.screen.get_height()/2 + 20))
        self.screen.blit(score_text, score_rect)
        #draws highscore text
        high_score_text = score_font.render(f'High Score: {self.high_score}', True, (255, 255, 255))
        high_score_rect = high_score_text.get_rect(center=(self.screen.get_width()/2, self.screen.get_height()/2 + 60))
        self.screen.blit(high_score_text, high_score_rect)
        #button dimensions
        button_width = 200
        button_height = 50
        button_spacing = 20
        #quit button
        quit_button = pygame.Rect(
            self.screen.get_width()/2 - button_width - button_spacing,
            self.screen.get_height()/2 + 100,
            button_width,
            button_height
        )
        pygame.draw.rect(self.screen, (200, 0, 0), quit_button)
        quit_text = self.button_font.render('Quit Game', True, (255, 255, 255))
        quit_text_rect = quit_text.get_rect(center=quit_button.center)
        self.screen.blit(quit_text, quit_text_rect)
        #return to menu button
        menu_button = pygame.Rect(
            self.screen.get_width()/2 + button_spacing,
            self.screen.get_height()/2 + 100,
            button_width,
            button_height
        )
        pygame.draw.rect(self.screen, (0, 200, 0), menu_button)
        menu_text = self.button_font.render('Return to Menu', True, (255, 255, 255))
        menu_text_rect = menu_text.get_rect(center=menu_button.center)
        self.screen.blit(menu_text, menu_text_rect)
        #handles button clicks
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()[0]
        if mouse_clicked:
            if quit_button.collidepoint(mouse_pos):
                #quits game
                pygame.quit()
                sys.exit()
            elif menu_button.collidepoint(mouse_pos):
                #resetx game state
                self.game_paused = False
                #imports and run  start screen
                from menu.startscreen import run
                run(self.screen, self.high_score)
                #exits current instance
                pygame.quit()
                sys.exit()

    def is_game_paused(self):
        #returns game state
        return self.game_paused