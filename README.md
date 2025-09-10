# haunted-key-hunt-game
computer science a level nea project (1 mark off of an A*)

a 2D top down game built with python and pygame.  
the player explores a haunted mansion, collecting keys while avoiding (or defeating) ghosts.  

---

# gameplay
- control the player with the arrow keys
- collect keys scattered around the map to increase your score
- ghosts patrol the mansion but will chase you if you get too close
- you can click to shoot in the direction of the mouse to fight back
- the player has 3 hearts and ghosts have 1  
- scores are saved to a text file (key score + ghost score)

---

# features
- animated player sprites (idle, walking in 4 directions) 
- ghost AI with patrol and chase behaviour using pathfinding algorithm
- random ghost spawning on floor tiles
- separate scoring for keys and ghosts  
- simple save system for high scores 

---

# tech stack
- language: python 3  
- library: pygame  
- paradigm: object oriented programming (OOP)  

---

# how to run
clone this repo:  
  ```bash
   git clone https://github.com/amekhu/haunted-key-hunt-game.git
   cd haunted-key-hunt-game
