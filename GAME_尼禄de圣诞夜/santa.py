import pygame
from enum import Enum
import os

img_folder = os.path.join('assets', 'img')

# 方向控制：继承enum枚举类
class Direction(Enum):
    LEFT = -1
    RIGHT = 1

class santa(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, 'Santa.png')).convert_alpha()
        self.pos = [800, 0]
        self.rect = self.image.get_rect(topleft=self.pos)
        self.speed = 1
        # 最开始向左边飞
        self.dir = Direction.LEFT

    def update(self, screen):
        if self.dir == Direction.LEFT:
            if self.pos[0] <= 0:
                self.dir = Direction.RIGHT
            else:
                self.pos[0] -= self.speed

        elif self.dir == Direction.RIGHT:
            if self.pos[0] >= screen.get_width()-150:
                self.dir = Direction.LEFT
            else:
                self.pos[0] += self.speed

        self.rect.x = self.pos[0]
        # print(self.pos)
        