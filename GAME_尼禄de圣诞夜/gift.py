import pygame 
import os
import random

img_folder = os.path.join('assets', 'img')

# 食物/礼物🎁图片名
food_images = ['05_apple_pie.png', '09_baguette.png', '15_burger.png', '20_bagel.png', '36_dumplings.png']

class Gift(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # 不能统一加载一个图片——到时候要随机下不同的菜
        self.image = pygame.image.load(os.path.join(img_folder, food_images[random.randint(0, 4)])).convert_alpha()
        self.pos = [0, -70]
        self.rect = self.image.get_rect(topleft=self.pos)
        self.speed = 2
        # 是否绘制（从屏幕上消失则设为false，且draw时忽略）
        self.show = False

    def throw(self, santa_pos):
        self.show = True
        self.pos = [santa_pos[0]+50, santa_pos[1]+50]
        # 🐞bug：这里换成别的方式操作rect对象都容易出错
        self.rect = self.image.get_rect(topleft=self.pos)

    def setback(self):
        self.show = False
        self.pos = [0, -70]
        self.image = pygame.image.load(os.path.join(img_folder, food_images[random.randint(0, 4)])).convert_alpha()
        self.rect = self.image.get_rect(topleft=self.pos)

    def draw(self, screen):
        if self.show:
            screen.blit(self.image, (self.pos[0], self.pos[1], 70, 70))

    def update(self):
        self.pos[1] += self.speed
        self.rect.move_ip(0, self.speed)

# ✨追加：下落更快、且受击后掉落额外奖励的大礼物盒（代码写💩了，继承麻烦）
class Gift_extra(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images = [pygame.image.load(os.path.join(img_folder, 'present.png')).convert_alpha(),\
                      pygame.image.load(os.path.join(img_folder, 'present_box.png')).convert_alpha()]
        self.current_image = self.images[0]
        self.pos = [0, -70]
        self.rect = self.current_image.get_rect(topleft=self.pos)
        self.speed = 4
        self.show = False
        self.if_empty = False

    def setback(self):
        self.show = False
        self.if_empty = False
        self.pos = [0, -70]
        self.current_image = self.images[0]
        self.rect = self.current_image.get_rect(topleft=self.pos)

    def throw(self, santa_pos):
        self.show = True
        self.pos = [santa_pos[0]+30, santa_pos[1]+80]
        self.rect = self.current_image.get_rect(topleft=self.pos)

    

    def draw(self, screen):
        if self.show:
            screen.blit(self.current_image, self.rect)


    def update(self):
        if self.if_empty:
            self.current_image = self.images[1]
        if self.show:
            self.pos[1] += self.speed
            self.rect.move_ip(0, self.speed)
        if self.pos[1] >= 500:
            self.setback()

class Rewards(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, food_images[random.randint(0, 4)])).convert_alpha()
        self.pos = [0, -70]  
        self.rect = self.image.get_rect(topleft=self.pos)
        self.if_show = False
        self.x_speed = random.randint(-5, 3)
        self.y_speed = random.randint(-5, -1)
        self.gravity = random.uniform(0.01, 0.1)

    def drop(self, box_pos):
        self.pos = box_pos
        self.if_show = True

    def setback(self):
        self.pos = [0, -70]
        self.x_speed = random.randint(-5, 3)
        self.y_speed = random.randint(-5, -1)
        self.gravity = random.uniform(0.01, 0.1)
        self.if_show = False
        # print(self.x_speed, self.y_speed, self.gravity)

    def draw(self, screen):
        if self.if_show:
            screen.blit(self.image, self.rect)

    def update(self):
        if self.pos[1] <= 600:
            self.pos[0] += self.x_speed
            self.pos[1] += self.y_speed
            self.y_speed += self.gravity
            self.rect = self.image.get_rect(topleft=self.pos)
        else:
            self.setback()
        
    