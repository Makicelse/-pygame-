import pygame
import os

img_folder = os.path.join('assets', 'img')

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, 'player.png')).convert_alpha()
        self.pos = [0, 500] 
        self.rect = self.image.get_rect(midbottom=self.pos) 
        self.score = 0

        # ✨追加跳跃动作
        self.if_jump = False
        self.walk_depth = 3
        self.jump_height = -10

        # ✨追加攻击动作
        # self.if_attack = False
        # self.attack_angle = 0

    def run(self, pos_x):
        # 要“站在雪地上”的最佳视觉效果，则y坐标==485最佳——但这样要更换礼物掉落判定，有点麻烦，就先不做更改
        self.pos[0] = pos_x
        self.rect = self.image.get_rect(midbottom=self.pos)

        # 🙋尝试：走路时有一顿一顿的效果（键盘控制的话）

    # ✨追加额外动作：鼠标左键跳跃，鼠标右键攻击
    def jump(self, gravity):
        if self.pos[1] <= 500:
            self.pos[1] += self.jump_height
            self.jump_height += gravity
        else:
            self.pos[1] = 500  # 确保人物不超过地面
            self.if_jump = False
            self.jump_height = -10 # 重置跳跃高度


    def update(self, pos_x, gravity):
        self.run(pos_x)
        if self.if_jump:
            self.jump(gravity)
            # print(self.pos[1])



class Sword(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, 'sword.png')).convert_alpha()
        self.rotated_image = self.image
        self.rect = self.image.get_rect(topleft=[0, -200])
        self.attack_angle = 0

    def slash(self, player_pos): 
        if self.attack_angle <= 90:
            self.attack_angle += 7
            self.rotated_image = pygame.transform.rotate(self.image, self.attack_angle)
            self.rect = self.rotated_image.get_rect(bottomright=player_pos) # 剑柄绑定玩家
        else:
            self.attack_angle = 0
            self.rect.topleft = [0, -200]  # rect区域放回礼物够不到的地方，防止影响碰撞检测
        
    

    def draw(self, screen):
        screen.blit(self.rotated_image, self.rect)