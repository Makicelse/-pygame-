import os
import sys
import pygame
import random
from player import Player, Sword
from gift import Gift, Gift_extra, Rewards
from santa import santa
import others

# 基础目录/路径
image_folder = os.path.join('assets', 'img')


pygame.init()
# 游戏窗口设置
screen = pygame.display.set_mode((800, 500))
# 游戏字体设置
font = pygame.font.SysFont('SimSun', 30)
# 游戏背景图设置
background = pygame.image.load(os.path.join(image_folder, 'background.png')).convert_alpha()
# 游戏基本对象
clock = pygame.time.Clock()
You = Player()
Santa = santa()

# ✨补充：重力
gravity = 0.5
# 🎁gift池（7个）
gift = [Gift() for _ in range(7)]
gift_index = 0
gift_timer = 0
# 🎅什么时候丢礼物呢？
throwGift_time = random.randint(700, 1500)
# 🏃玩家坐标
You_x = 0

# 添加计时系统
time_all = 30
counter_zero = pygame.time.get_ticks()

# 添加连击combo系统
combo_count = -1
number_img_files = {1: '1.png',\
            2: '2.png',\
            3: '3.png',\
            4: '4.png',\
            5: '5.png',\
            6: '6.png',\
            7: '7.png',\
            8: '8.png',\
            9: '9.png',\
            0: '0.png'}
number_img = {}
for num, image in number_img_files.items():
    number_img[num] = pygame.image.load(os.path.join(image_folder, image)).convert_alpha()

# 添加背景雪花
snowflakes = [others.Snowflake([random.randint(0, 800), random.randint(0, 500)], random.randint(1, 3)) for _ in range(100)]

# ✨追加：添加武器 & 额外奖励の大礼物盒
# 添加武器劈砍
Sword = Sword()
if_attack = False
# 添加大礼物盒（3个）
gift_extra = [Gift_extra() for _ in range(3)]
gift_extra_index = 0
gift_extra_timer = pygame.time.get_ticks()  # （计时）与普通礼物分开管理
# 添加礼物盒里的奖励（5个）
rewards_inside = [Rewards() for _ in range(5)]

# ✨追加：我故意在这里放置一个游玩说明，让你知道你在玩一款若智游戏（😃👍
intro_text = font.render('移动鼠标操作角色/左键跳跃/右键可攻击礼物盒', False, 'white')


running = True
# 游戏结束标志
game_over = False
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                You.if_jump = True
            elif pygame.mouse.get_pressed()[2]:
                Sword.attack_angle = 0  # 每次点击重置图片角度
                if_attack = True


# 基础游戏设置
    # 显示计时
    counter = pygame.time.get_ticks()
    time = time_all - (counter - counter_zero) // 1000 # 毫秒转成秒
    # 倒计时结束
    if not time:
        running = False
        game_over = True
    time_text = font.render('时间：'+str(time), False, 'white')  # antialias：是否抗锯齿
    # time_text_rec = time_text.get_rect

    # 隐藏鼠标指针
    pygame.mouse.set_visible(False)
    # 🏃（用鼠标）左右控制玩家
    mouse_pos = pygame.mouse.get_pos()
    You_x = mouse_pos[0]

    # 显示玩家分数
    score_text = font.render('分数：'+str(You.score), False, 'white')


# 游戏里会动の（角色）模块  
    # ❄️雪花落下
    for snow in snowflakes[:]:
        snow.update(screen)

    # 🎅左右飞行
    Santa.update(screen)

    # 🎁（隔一段时间）丢礼物
    if pygame.time.get_ticks() - gift_timer > throwGift_time:
        gift[gift_index].throw(santa_pos=Santa.pos)
        gift_index = (gift_index + 1) % len(gift)
        # 重置丢礼物の时间间隔 & 计时器
        throwGift_time = random.randint(400, 3000)
        gift_timer = pygame.time.get_ticks()

    # ✨追加：额外奖励礼物盒
    if pygame.time.get_ticks() - gift_extra_timer > throwGift_time*random.randint(5, 10):
        gift_extra[gift_extra_index].throw(santa_pos=Santa.pos)
        gift_extra_index = (gift_extra_index + 1) % len(gift_extra)
        gift_extra_timer = pygame.time.get_ticks()

    # 🎁礼物掉下
    for item in gift[:]:
        collide = pygame.sprite.collide_rect(item, You)
        # 礼物还没丢出去呢更新什么位置——pass
        if not item.show:
            pass

        # 若礼物掉出屏幕 or 掉进口袋，重置其位置 & 变换食物图片
        elif collide or item.pos[1] >= 500:
            if collide and combo_count <= 99:
                You.score += 1
                combo_count += 1
            else:
                # 没连击上，combo归零
                combo_count = -1
            item.setback()

        else:
            item.update()

    # ✨追加：额外奖励礼物盒
    for item in gift_extra[:]:
        if not item.throw:
            pass
        item.update()

    # 🏃玩家左右跑动 & 进行跳跃、攻击
    You.update(You_x, gravity)
    
    # combo数
    combo = pygame.image.load(os.path.join(image_folder, 'combo.png')).convert_alpha()
    combo_rect = combo.get_rect(topleft=(500, 350))
    num_one = number_img[combo_count % 10]
    num_one_rect = num_one.get_rect(topleft=[730, 340])
    num_ten = number_img[abs(combo_count // 10)]    # abs()是防止-1无效索引的亡羊补牢之举
    num_ten_rect = num_ten.get_rect(topleft=[670, 340])
    
    # 🗡️用剑劈砍🎁！
    collide = False
    if if_attack:
        if Sword.attack_angle >= 90:
            if_attack = False   # 动作终止条件
        Sword.slash(You.pos)
        # 砍到🎁了吗？
        for item in gift_extra[:]:
            collide = Sword.rect.colliderect(item.rect)
            if collide and not item.if_empty:
                item.if_empty = True
                You.score += 5
                # print('cut a present!')
                item.current_image = item.images[1]
                for reward in rewards_inside[:]:
                    reward.drop(item.pos)

    # 奖励全部掉落
    for reward in rewards_inside[:]:
        if reward.if_show:
            reward.update()
    

# 屏幕显示
    screen.fill('black')
    # 添加雪花
    for snow in snowflakes[:]:
        snow.draw(screen)

    # 添加背景图
    screen.blit(background, (0, 0, 800, 500))

    screen.blit(intro_text, (100, 220))
    screen.blit(time_text, (400, 250))
    screen.blit(score_text, (400, 280))
    screen.blit(Santa.image, Santa.rect)
    screen.blit(You.image, You.rect)    
    for item in gift[:]:
        item.draw(screen)
    # 额外礼物盒
    for item in gift_extra[:]:
        item.draw(screen)
    # 额外礼物盒の奖励
    for item in rewards_inside[:]:
        item.draw(screen)
    # 添加劈砍效果
    Sword.draw(screen)
    # 添加连击分数显示
    if combo_count >= 1:
        screen.blit(combo, combo_rect)
        screen.blit(num_one, num_one_rect)
        if combo_count >= 10:
            screen.blit(num_ten, num_ten_rect)

    # 屏幕刷新
    pygame.display.flip()

if game_over:
    others.game_over_Sence(screen,clock, You, Santa, gift)

# 退出game
pygame.quit()
sys.exit()