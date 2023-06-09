# general imports of all necessary packagees
import pygame, sys, random
from pygame.math import Vector2
from pygame import mixer


# general configuration of the game

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
RUNNING = True
ALL_SAME = False
IS_PAUSED = False
IS_MUSIC_ON = True
WELCOME_STATE = True
SELECTION_STATE = False
MAIN_STATE = False
END_STATE = False
WINNER_SELECTION = ""

images = {
    "rock": "./assets/rock.png",
    "paper": "./assets/paper.png",
    "scissors": "./assets/scissors.png"
}

# number of objects
total_num = 100


# default pygame initialization
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Rock, Paper, Scissor War")
clock = pygame.time.Clock()
font = pygame.font.SysFont('comicsansms', 100)

# function to generate random amount of sprites and insert them into specfic type sprite group and general group for all sprites

def generate_elements(num_elements, element_class, all_elements_group):
    element_group = pygame.sprite.Group()
    for i in range(num_elements):
        element = element_class()
        element_group.add(element)
        all_elements_group.add(element)
    return element_group, all_elements_group
    


# General class for all game objects, which inherits from pygame Sprite class
class GameObject(pygame.sprite.Sprite):
    # initialization method for a class
    def __init__(self, prey, enemy, image, type):
        #  parameters of a class
        super().__init__()
        self.width = 30
        self.prey = prey
        self.enemy = enemy
        self.image = pygame.transform.scale(image, (self.width, self.width))
        self.rect = self.image.get_rect()
        self.rect.center = Vector2(random.randint(0, SCREEN_WIDTH - self.width), random.randint(0, SCREEN_HEIGHT - self.width))
        self.speed = 2
        self.direction = Vector2(random.randint(-self.speed, self.speed), random.randint(-self.speed, self.speed)) 
        self.spin_direction = Vector2(random.uniform(-1.00, 1.00), random.uniform(-1.00, 1.00))
        self.type = type

    # function to draw class on a screen
    def draw(self):
        screen.blit(self.image, self.rect)


    # function to move an object
    def move(self):
        self.detect_collision_with_walls()
        self.spin_direction = Vector2(random.uniform(-1.00, 1.00), random.uniform(-1.00, 1.00))
        self.rect.center = self.rect.center + self.direction + self.spin_direction

    # function to change a direction on a collision with another sprite
    def change_direction(self, other_sprite):
        if self.rect.x < other_sprite.rect.x:
            self.direction.x = - random.uniform(1, 3)
        else:
            self.direction.x = random.uniform(1, 3)
        if self.rect.y < other_sprite.rect.y:
            self.direction.y = -random.uniform(1, 3)
        else:
            self.direction.y = random.uniform(1, 3)

    # function to change the direction on a collision with walls
    def detect_collision_with_walls(self):
        if self.rect.left < 0:
            self.rect.left = 0
            self.direction.x = random.uniform(1, 3)
        elif self.rect.right >= SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH 
            self.direction.x = -random.uniform(1, 3)
        if self.rect.top < 0:
            self.direction.y = random.uniform(1, 3)
            self.rect.top = 0
        elif self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT 
            self.direction.y = -random.uniform(1, 3)

    # function to change the type of an object wherether it collides with prey or enemy
    def change_type(self, other_object_type):
        match self.type:
            case 'Rock':
                if other_object_type == 'Paper':
                    self.type = 'Paper'
                    self.image = pygame.transform.scale(pygame.image.load(images['paper']), (self.width, self.width))
            case 'Paper':
                if other_object_type == "Scissor":
                    self.type = 'Scissor'
                    self.image = pygame.transform.scale(pygame.image.load(images['scissors']), (self.width, self.width))
            case 'Scissor':
                if other_object_type == "Rock":
                    self.type = 'Rock'
                    self.image = pygame.transform.scale(pygame.image.load(images['rock']), (self.width, self.width))
            case _:
                return




# Specific class for Rock objects which inherits from GameObject class
class Rock(GameObject):
    def __init__(self):
        # sending parameters to parent superclass of GameObject
        super().__init__(prey = Scissor, enemy = Paper, type = 'Rock',
        image = pygame.image.load(images["rock"]))

 

# Specific class for Paper objects which inherits from GameObject class
class Paper(GameObject):
    def __init__(self):
        # sending parameters to parent superclass of GameObject
        super().__init__(prey = Rock, enemy = Scissor, type='Paper',
        image = pygame.image.load(images["paper"]))



# Specific class for Scissor objects which inherits from GameObject class
class Scissor(GameObject):
    def __init__(self):
        # sending parameters to parent superclass of GameObject
        super().__init__(prey = Paper, enemy = Rock, type='Scissor',
        image = pygame.image.load(images["scissors"]))



# Class for Start button of the Welcome screen
class StartButton:
    # initialize method of a button
    def __init__(self):
        # importing start button image and setting its dimensions and location
        self.image = pygame.transform.scale(pygame.image.load('./assets/start_button.png'), (180, 100))
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT * 2 // 3)

    # draw a button on the screen
    def draw(self):
        screen.blit(self.image, self.rect)

    
# Class for General Game logic
class GameLogic():
    # initialzation method for a general game logic
    def __init__(self):
        # all necessary attributes for game
        self.all_sprites_group = pygame.sprite.Group()
        self.num_rocks = random.randint(1, total_num - 3)
        self.num_papers = random.randint(1, total_num - self.num_rocks - 1)
        self.num_scissors = random.randint(1, total_num - self.num_rocks - self.num_papers)
        self.rocks_group, self.all_sprites_group = generate_elements(self.num_rocks, Rock, self.all_sprites_group)
        self.papers_group, self.all_sprites_group = generate_elements(self.num_papers, Paper, self.all_sprites_group)
        self.scissors_group, self.all_sprites_group = generate_elements(self.num_scissors, Scissor, self.all_sprites_group)
        self.welcome_bg_image = pygame.transform.scale(pygame.image.load('./assets/welcome_bg_1.png'), (SCREEN_WIDTH, SCREEN_HEIGHT))

    # function to detect collision of different sprites
    def detect_sprites_collisions(self, sprite):
        for other_sprite in self.all_sprites_group:
            # if two sprites collide change their direction and their type
            if other_sprite != sprite and pygame.sprite.collide_rect(sprite, other_sprite):
                sprite.change_direction(other_sprite)
                sprite.change_type(other_sprite.type)
                other_sprite.change_direction(sprite)
                other_sprite.change_type(sprite.type)


    # function update the state of the game 
    def update(self):
        # draw, move and detect colliison of every sprite on the screen
        for sprite in self.all_sprites_group:
            sprite.draw()
            sprite.move()
            self.detect_sprites_collisions(sprite)

    # function to pause the game
    def pause(self):
        global IS_PAUSED, IS_MUSIC_ON
        text_surf = font.render("""Paused""", True, (0, 0, 0))
        text_rect = text_surf.get_rect()
        text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        while IS_PAUSED:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        IS_PAUSED = not IS_PAUSED
                        if IS_MUSIC_ON:
                            mixer.music.pause()
                        else:
                            mixer.music.unpause()
                        IS_MUSIC_ON = not IS_MUSIC_ON
            screen.blit(text_surf, text_rect)
            pygame.display.flip()
            clock.tick(FPS)  

    # function to check whether all objects have the same type, which concludes the end of the game
    def check_type(self):
        for sprite in self.all_sprites_group:
            curr_type = sprite.type
            is_type_same = all(sprite.type == curr_type for sprite in self.all_sprites_group)
            return is_type_same
    # function to display the welcome screen
    def draw_welcome_screen(self):
        global WELCOME_STATE, SELECTION_STATE
        start_button = StartButton()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.rect.collidepoint(pygame.mouse.get_pos()):
                    WELCOME_STATE = False
                    SELECTION_STATE = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_KP_ENTER:
                    WELCOME_STATE = False
                    SELECTION_STATE = True
        font1 = pygame.font.SysFont('comicsansms', 50)
        text_surf = font1.render("""Rock, Paper, Scissors War""", True, (0, 0, 0))
        text_rect = text_surf.get_rect()
        text_rect.center = (SCREEN_WIDTH // 2, 20)

        screen.blit(self.welcome_bg_image, (0, 0))
        screen.blit(text_surf, text_rect)
        start_button.draw()

    # function to display the winner selection screen
    def draw_selection_screen(self):
        global SELECTION_STATE, MAIN_STATE, WINNER_SELECTION
        rock_select_button = pygame.transform.scale(pygame.image.load('./assets/rock_select.png'), (100, 100))
        rock_select_rect = rock_select_button.get_rect()
        rock_select_rect.center = (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2)

        paper_select_button = pygame.transform.scale(pygame.image.load('./assets/paper_select.png'), (100, 100))
        paper_select_rect = paper_select_button.get_rect()
        paper_select_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        scissors_select_button = pygame.transform.scale(pygame.image.load('./assets/scissors_select.png'), (100, 100))
        scissors_select_rect = scissors_select_button.get_rect()
        scissors_select_rect.center = ( 3 * SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if rock_select_rect.collidepoint(pygame.mouse.get_pos()):
                    WINNER_SELECTION = "Rock"
                    SELECTION_STATE = False
                    MAIN_STATE = True
                if paper_select_rect.collidepoint(pygame.mouse.get_pos()):
                    WINNER_SELECTION = "Paper"
                    SELECTION_STATE = False
                    MAIN_STATE = True
                if scissors_select_rect.collidepoint(pygame.mouse.get_pos()):
                    WINNER_SELECTION = "Scissors"
                    SELECTION_STATE = False
                    MAIN_STATE = True
        
        font1 = pygame.font.SysFont('comicsansms', 50)
        text_surf = font1.render("""Choose your fighter""", True, (0, 0, 0))
        text_rect = text_surf.get_rect()
        text_rect.center = (SCREEN_WIDTH // 2, 50)

        screen.blit(text_surf, text_rect)
        screen.blit(rock_select_button, rock_select_rect)
        screen.blit(paper_select_button, paper_select_rect)
        screen.blit(scissors_select_button, scissors_select_rect)

    # function to display the end screen
    def draw_end_screen(self):
        curr_type = ""
        for sprite in self.all_sprites_group:
            curr_type = sprite.type
        is_right = curr_type == WINNER_SELECTION
        
        winner_image = pygame.transform.scale(pygame.image.load(f'./assets/{curr_type.lower()}_select.png'), (200, 200))
        winner_rect = winner_image.get_rect()
        winner_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        font1 = pygame.font.SysFont('comicsansms', 50)
        text_surf1 = font1.render("""is the winner""", True, (0, 0, 0))
        text_surf2 = font1.render("You are right", True, (0, 0, 0)) if is_right else font1.render("You are wrong", True, (0, 0, 0))
        text_rect1 = text_surf1.get_rect()
        text_rect2 = text_surf2.get_rect()
        text_rect1.center = (SCREEN_WIDTH // 2, 550)
        text_rect2.center = (SCREEN_WIDTH // 2, 50)

        screen.blit(winner_image, winner_rect)
        screen.blit(text_surf1, text_rect1)
        screen.blit(text_surf2, text_rect2)


        
                    
            


# main method of the game
def main():
    # global objects to be manipulated inside the main method
    global RUNNING, ALL_SAME, IS_PAUSED, IS_MUSIC_ON, MAIN_STATE, END_STATE
    # initializing the instance of the GameLogic class
    game_logic = GameLogic()

    # loading and playing the background music
    mixer.music.load('./assets/epic_music.mp3')
    mixer.music.play()

    # while cycle that runs the game
    while RUNNING:
        # checking for every event input
        for event in pygame.event.get():
            # if the exit button tis clicked, quit the game
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
            # if the P key is clicked, pause or unpause the game
                if event.key == pygame.K_p:
                    IS_PAUSED = not IS_PAUSED
                    if IS_MUSIC_ON:
                        mixer.music.pause()
                    else:
                        mixer.music.unpause()
                    IS_MUSIC_ON = not IS_MUSIC_ON
                    game_logic.pause()

        # fill screen with white color
        screen.fill((255, 255, 255))

        # Check for the different states of the game
        # Welcome Screen
        if WELCOME_STATE:
            game_logic.draw_welcome_screen()
        # Selection screen
        elif SELECTION_STATE:
            game_logic.draw_selection_screen()
        # Main game screen
        elif MAIN_STATE:
            game_logic.update()
            if game_logic.check_type():
                ALL_SAME = True
                END_STATE = True
                MAIN_STATE = False
        # End screen
        else:
            game_logic.draw_end_screen()

        pygame.display.flip()
        clock.tick(60)


# Run the game
if __name__ == "__main__":
    main()
