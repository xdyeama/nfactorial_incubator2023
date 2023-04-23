import pygame, sys, random, math, numpy
from pygame.math import Vector2
from pygame import mixer



SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
RUNNING = True
ALL_SAME = False
IS_PAUSED = False
IS_MUSIC_ON = True

images = {
    "rock": "./assets/rock.png",
    "paper": "./assets/paper.png",
    "scissors": "./assets/scissors.png"
}

total_num = 100


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

def generate_elements(num_elements, element_class, all_elements_group):
    element_group = pygame.sprite.Group()
    for i in range(num_elements):
        element = element_class()
        element_group.add(element)
        all_elements_group.add(element)
    return element_group, all_elements_group
    


class GameObject(pygame.sprite.Sprite):
    def __init__(self, prey, enemy, image, type):
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

    def draw(self):
        screen.blit(self.image, self.rect)


    def update(self ):
        pass

    def move(self):
        self.detect_collision_with_walls()
        self.spin_direction = Vector2(random.uniform(-1.00, 1.00), random.uniform(-1.00, 1.00))
        self.rect.center = self.rect.center + self.direction + self.spin_direction

    
    def change_direction(self, other_sprite):
        if self.rect.x < other_sprite.rect.x:
            self.direction.x = - random.uniform(1, 3)
        else:
            self.direction.x = random.uniform(1, 3)
        if self.rect.y < other_sprite.rect.y:
            self.direction.y = -random.uniform(1, 3)
        else:
            self.direction.y = random.uniform(1, 3)

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





class Rock(GameObject):
    def __init__(self, direction = None, pos = None):
        super().__init__(prey = Scissor, enemy = Paper, type = 'Rock',
        image = pygame.image.load(images["rock"]))

    def change_icon(self):
        self.image = pygame.transform.scale(pygame.image.load(images["paper"]), (self.width, self.width))
 


class Paper(GameObject):
    def __init__(self, direction = None, pos = None):
        super().__init__(prey = Rock, enemy = Scissor, type='Paper',
        image = pygame.image.load(images["paper"]))

    def change_icon(self):
        self.image = self.prey.image



class Scissor(GameObject):
    def __init__(self, direction = None, pos = None):
        super().__init__(prey = Paper, enemy = Rock, type='Scissor',
        image = pygame.image.load(images["scissors"]))

    def change_icon(self):
        self.image = self.prey.image

    
class GameLogic():
    def __init__(self):
        self.all_sprites_group = pygame.sprite.Group()
        self.num_rocks = random.randint(1, total_num - 3)
        self.num_papers = random.randint(1, total_num - self.num_rocks - 1)
        self.num_scissors = random.randint(1, total_num - self.num_rocks - self.num_papers)
        self.rocks_group, self.all_sprites_group = generate_elements(self.num_rocks, Rock, self.all_sprites_group)
        self.papers_group, self.all_sprites_group = generate_elements(self.num_papers, Paper, self.all_sprites_group)
        self.scissors_group, self.all_sprites_group = generate_elements(self.num_scissors, Scissor, self.all_sprites_group)

    def detect_sprites_collisions(self, sprite):
        for other_sprite in self.all_sprites_group:
            if other_sprite != sprite and pygame.sprite.collide_rect(sprite, other_sprite):
                sprite.change_direction(other_sprite)
                sprite.change_type(other_sprite.type)
                other_sprite.change_direction(sprite)
                other_sprite.change_type(sprite.type)



    def update(self):
        for sprite in self.all_sprites_group:
            sprite.draw()
            sprite.move()
            self.detect_sprites_collisions(sprite)


    def pause(self):
        global IS_PAUSED, IS_MUSIC_ON
        font = pygame.font.SysFont('comicsansms', 100)
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


    def check_type(self):
        for sprite in self.all_sprites_group:
            curr_type = sprite.type
            is_type_same = all(sprite.type == curr_type for sprite in self.all_sprites_group)
            return is_type_same
        
    def draw_win_screen(self):
                

                    
            



def main():
    global RUNNING, ALL_SAME, IS_PAUSED, IS_MUSIC_ON
    game_logic = GameLogic()

    mixer.music.load('./assets/epic_music.mp3')
    mixer.music.play()


    while RUNNING:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    IS_PAUSED = not IS_PAUSED
                    if IS_MUSIC_ON:
                        mixer.music.pause()
                    else:
                        mixer.music.unpause()
                    IS_MUSIC_ON = not IS_MUSIC_ON
                    game_logic.pause()
        screen.fill((255, 255, 255))

        if game_logic.check_type():
            ALL_SAME = True
            RUNNING = False

        game_logic.update()

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
