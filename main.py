import time
import random
import pygame
import sys
from os.path import join

class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.init()
        self.Info = pygame.display.Info()
        self.screen = pygame.display.set_mode((self.Info.current_w , self.Info.current_h) , pygame.FULLSCREEN)
        pygame.display.set_caption("Aim Training")
        self.clock = pygame.time.Clock()
        self.running = True
        

class Play:
    def __init__(self , main) -> None:
        self.screen = main.screen
        self.clock = main.clock
        self.running = True
        self.target = pygame.sprite.Group()
        self.Info = main.Info

    def run(self) -> int | None :
        targetRecon = pygame.event.custom_type()
        pygame.time.set_timer(targetRecon,1000)
        global stateMachine
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                
                if event.type == pygame.K_ESCAPE:
                    stateMachine = 0
                    self.running = False

                if event.type == targetRecon:
                    Target(self.target , self.Info)

            self.screen.fill((0, 0, 0))
            self.target.draw(self.screen)
            self.target.update()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

    def overlay(self):
        pass


class Menu:
    def __init__(self, main: Game) -> None:
        self.screen = main.screen
        self.running = main.running
        self.Font = pygame.font.Font(join("fonts" , "Jersey M54.ttf") , 70)
        self.Title = self.Font.render("|&| AIM TRAINING |&|" , True , "white" , None)

    def run(self) -> int | None:
        global stateMachine
        while self.running:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    sys.exit()
                if e.type == pygame.K_RETURN:
                    stateMachine =  1
                    self.running = False
            
            
            self.screen.fill("black")
            self.screen.blit(self.Title , (400 , 80)) 
            button_rect = pygame.draw.rect(self.screen , "white" , pygame.rect.Rect())

            pygame.display.flip()
            
            if button_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[pygame.MOUSEBUTTONDOWN]:
                return 1           

class Target(pygame.sprite.Sprite):
    def __init__(self, group , info) -> None:
        super().__init__(group)
        self.image_uv = pygame.image.load(join("img" , "target_white.png"))
        self.image = pygame.transform.scale(self.image_uv , (0 , 0))
        self.scale = pygame.Vector2(256,256)
        self.time = time.time()
        self.rect = (random.randint(0 , info.current_w - 128) , random.randint(0 , info.current_h - 128)) # type: ignore


    def update(self) -> None:
        self.image = pygame.transform.scale(self.image_uv , self.scale * abs(1 - (time.time() - self.time)))

        if int(time.time() - self.time) == 1:
            self.kill()
        


if __name__ == "__main__":
    game = Game()
    
    play = Play(game)
    menu = Menu(game)
    stateMachine : int  = 0
    states = (menu , play)
    
    while(True):

        states[stateMachine].run()
