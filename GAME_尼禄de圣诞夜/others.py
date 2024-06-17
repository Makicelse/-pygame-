import pygame
import os
import random

img_folder = os.path.join('assets', 'img')

# 雪花类
class Snowflake:
    def __init__(self, pos, speed):
        self.pos = pos
        self.speed = speed
        self.size = random.randint(2, 5)

    def draw(self, screen):
        pygame.draw.circle(screen, 'white', self.pos, self.size)

    def update(self, screen):
        self.pos[1] += self.speed
        if self.pos[1] >= screen.get_height():
            self.pos = [random.randint(0, screen.get_width()), random.randint(-100, -50)]


def game_over_Sence(screen, clock, You, Santa, gift):
    timeUp_image = pygame.image.load(os.path.join(img_folder, 'timeUp.png')).convert_alpha()
    # size = [timeUp_image.get_width(), timeUp_image.get_height()]
    pos = [screen.get_width(), screen.get_height()/2]
    rect = timeUp_image.get_rect(midleft=pos)
    speed = -3

    timer = pygame.time.get_ticks()
    mid = False
    running = True
    # 显示“时间到！”
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 🛠️速率修正：要控制fps，否则速度无法控制
        clock.tick(60)
        # 当文字移出屏幕时，结束函数调用
        if rect.midright[0] <= 0:
            running = False

        # 🐞bug：rect的横坐标恒为一个数（第一次800，第二次524），导致画面不更新
        # 🛠️修正：边界条件有误（忘了除以2）
        if rect.midtop[0] >= screen.get_width()/2:
            rect.move_ip(speed, 0)
            timer = pygame.time.get_ticks()
        else:
            mid = True

        # 停留3秒后再移动
        # 🛠️停留后不动 bug 修正：timer放在前面固定
        if mid and pygame.time.get_ticks() - timer >= 3000:
            rect.move_ip(speed, 0)
    
        # print(timer)
    # 屏幕显示
        screen.fill('black')
        # ✨改进：update()只会影响传入的rect对象，其余的不会变。
        # screen.blit(Santa.image, Santa.rect)
        # screen.blit(You.image, You.rect)# 记得添加口袋（鼠标）位置
        # for i in range(0, len(gift)):
        #     gift[i].draw(screen=screen)
        screen.blit(timeUp_image, rect)
        # 🐞bug：感叹号有拖尾
        pygame.display.update(rect)
        