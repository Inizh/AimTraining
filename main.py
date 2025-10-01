import time
import random
import pygame
from os.path import join

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.init()
        self.Info = pygame.display.Info()
        self.screen = pygame.display.set_mode((self.Info.current_w , self.Info.current_h) , pygame.FULLSCREEN)
        pygame.display.set_caption("Aim Training")
        self.clock = pygame.time.Clock()
        self.running = True
        self.target = pygame.sprite.Group()


    def run(self):
        targetRecon = pygame.event.custom_type()
        pygame.time.set_timer(targetRecon,1000)
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
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



class Target(pygame.sprite.Sprite):
    def __init__(self, group , info) -> None:
        super().__init__(group)
        self.image_uv = pygame.image.load(join("img" , "target_white.png"))
        self.image = pygame.transform.scale(self.image_uv , (0 , 0))
        self.scale = pygame.Vector2(256,256)
        self.time = time.time()
        self.rect = (random.randint(0 , info.current_w - 128) , random.randint(0 , info.current_h - 128)) # type: ignore


    def update(self) -> None:
        self.image = pygame.transform.scale(self.image_uv , self.scale * (time.time() - self.time))

        if int(time.time() - self.time) == 1:
            self.kill()
        


if __name__ == "__main__":
    game = Game()
    game.run()