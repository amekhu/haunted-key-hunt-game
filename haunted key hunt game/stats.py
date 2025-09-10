class GameStats:
    def __init__(self):
        self.lives = 3 #start lives
        self.score = 0 #start score
        
    def take_damage(self):
        #called to remove a life
        self.lives -= 1
        return True
        
    def add_score(self, points):
        #called to add points to score
        self.score += points