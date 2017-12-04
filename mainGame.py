# -*- coding: utf-8 -*-
"""
游戏主要的逻辑
Created on Wed Sep 11 11:05:00 2013

@author: Leo
"""

import pygame
from sys import exit
import sys

import select
from pygame.locals import *
from gameRole import *
import random


def game_engine(seedInit, assignment, sock):
    # 初始化游戏
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # 480, 800
    pygame.display.set_caption('飞机大战')
    # 载入游戏音乐
    bullet_sound = pygame.mixer.Sound('/Users/cxl/dev/PythonShootGame/resources/sound/bullet.wav')
    enemy1_down_sound = pygame.mixer.Sound('/Users/cxl/dev/PythonShootGame/resources/sound/enemy1_down.wav')
    game_over_sound = pygame.mixer.Sound('/Users/cxl/dev/PythonShootGame/resources/sound/game_over.wav')
    bullet_sound.set_volume(0.3)
    enemy1_down_sound.set_volume(0.3)
    game_over_sound.set_volume(0.3)
    pygame.mixer.music.load('/Users/cxl/dev/PythonShootGame/resources/sound/game_music.wav')
    pygame.mixer.music.play(-1, 0.0)
    pygame.mixer.music.set_volume(0.25)
    # 载入背景图
    background = pygame.image.load('/Users/cxl/dev/PythonShootGame/resources/image/background.png').convert()
    game_over = pygame.image.load('/Users/cxl/dev/PythonShootGame/resources/image/gameover.png')
    filename = '/Users/cxl/dev/PythonShootGame/resources/image/shoot.png'
    plane_img1 = pygame.image.load(filename)
    plane_img2 = pygame.image.load(filename)
    # 设置玩家相关参数
    player_rect1 = []
    player_rect1.append(pygame.Rect(0, 99, 102, 126))  # 玩家精灵图片区域
    player_rect1.append(pygame.Rect(165, 360, 102, 126))
    player_rect1.append(pygame.Rect(165, 234, 102, 126))  # 玩家爆炸精灵图片区域
    player_rect1.append(pygame.Rect(330, 624, 102, 126))
    player_rect1.append(pygame.Rect(330, 498, 102, 126))
    player_rect1.append(pygame.Rect(432, 624, 102, 126))

    player_rect2 = []
    player_rect2.append(pygame.Rect(0, 99, 102, 126))  # 玩家精灵图片区域
    player_rect2.append(pygame.Rect(165, 360, 102, 126))
    player_rect2.append(pygame.Rect(165, 234, 102, 126))  # 玩家爆炸精灵图片区域
    player_rect2.append(pygame.Rect(330, 624, 102, 126))
    player_rect2.append(pygame.Rect(330, 498, 102, 126))
    player_rect2.append(pygame.Rect(432, 624, 102, 126))

    # 玩家初始位置 (200, 600)为中间生成, 说明飞机宽度80, 飞机高度200
    # 一个左侧,一个右侧
    if assignment == 1:
        player_pos1 = [SCREEN_WIDTH * 0.33 - 40, SCREEN_HEIGHT - 200]
        player_pos2 = [SCREEN_WIDTH * 0.67 - 40, SCREEN_HEIGHT - 200]
    else:
        player_pos2 = [SCREEN_WIDTH * 0.33 - 40, SCREEN_HEIGHT - 200]
        player_pos1 = [SCREEN_WIDTH * 0.67 - 40, SCREEN_HEIGHT - 200]
    player1 = Player(plane_img1, player_rect1, player_pos1)
    player2 = Player(plane_img2, player_rect2, player_pos2)
    # 定义子弹对象使用的surface相关参数
    bullet_rect = pygame.Rect(1004, 987, 9, 21)
    bullet_img = plane_img1.subsurface(bullet_rect)

    # 定义敌机对象使用的surface相关参数
    enemy1_rect = pygame.Rect(534, 612, 57, 43)
    enemy1_img = plane_img1.subsurface(enemy1_rect)
    enemy1_down_imgs = []
    enemy1_down_imgs.append(plane_img1.subsurface(pygame.Rect(267, 347, 57, 43)))
    enemy1_down_imgs.append(plane_img1.subsurface(pygame.Rect(873, 697, 57, 43)))
    enemy1_down_imgs.append(plane_img1.subsurface(pygame.Rect(267, 296, 57, 43)))
    enemy1_down_imgs.append(plane_img1.subsurface(pygame.Rect(930, 697, 57, 43)))
    enemies1 = pygame.sprite.Group()
    enemies_down = pygame.sprite.Group()  # 存储被击毁的飞机，用来渲染击毁精灵动画
    random.seed(seedInit)  # 随机数的种子值必须一致

    shoot_frequency = 0
    enemy_frequency = 0
    player_down_index = 16
    score = 0
    clock = pygame.time.Clock()
    running = True

    # 这是游戏的主循环
    while running:
        # 控制游戏最大帧率为60
        clock.tick(60)
        # 网络部分
        CONNECTION_LIST = [sock]
        #select作用
        read_sockets, write_sockets, error_sockets = select.select(CONNECTION_LIST, [], [], 0.2)
        # 控制发射子弹频率,并发射子弹
        if not player1.is_hit:
            if shoot_frequency % 15 == 0:  # 初始值为0
                bullet_sound.play()
                player1.shoot(bullet_img)
            shoot_frequency += 1
            if shoot_frequency >= 15:
                shoot_frequency = 0

        if not player2.is_hit:
            if shoot_frequency % 15 == 0:  # 初始值为0
                bullet_sound.play()
                player2.shoot(bullet_img)
            shoot_frequency += 1
            if shoot_frequency >= 15:
                shoot_frequency = 0

        # 生成敌机
        if enemy_frequency % 50 == 0:
            enemy1_pos = [random.randint(0, SCREEN_WIDTH - enemy1_rect.width), 0]
            enemy1 = Enemy(enemy1_img, enemy1_down_imgs, enemy1_pos)
            enemies1.add(enemy1)
        enemy_frequency += 1
        if enemy_frequency >= 100:
            enemy_frequency = 0

        # 移动子弹，若超出窗口范围则删除
        for bullet in player1.bullets:
            bullet.move()
            if bullet.rect.bottom < 0:
                player1.bullets.remove(bullet)
        for bullet in player2.bullets:
            bullet.move()
            if bullet.rect.bottom < 0:
                player2.bullets.remove(bullet)

        # 移动敌机，若超出窗口范围则删除
        for enemy in enemies1:
            enemy.move()  # 全部向上移动一点
            # 判断玩家是否被击中
            if pygame.sprite.collide_circle(enemy, player1):
                enemies_down.add(enemy)
                enemies1.remove(enemy)
                player1.is_hit = True
                game_over_sound.play()
                sock.send(bytes("game_over", encoding="utf-8"))
                break
            if pygame.sprite.collide_circle(enemy, player2):
                enemies_down.add(enemy)
                enemies1.remove(enemy)
                player2.is_hit = True
                game_over_sound.play()
                sock.send(bytes("game_over", encoding="utf-8"))
                break
            if enemy.rect.top > SCREEN_HEIGHT:
                enemies1.remove(enemy)

        # 将被击中的敌机对象添加到击毁敌机Group中，用来渲染击毁动画
        enemies1_down = pygame.sprite.groupcollide(enemies1, player1.bullets, 1, 1)
        enemies2_down = pygame.sprite.groupcollide(enemies1, player2.bullets, 1, 1)
        for enemy_down in enemies1_down:
            enemies_down.add(enemy_down)
        for enemy_down in enemies2_down:
            enemies_down.add(enemy_down)

        # 绘制背景
        screen.fill(0)
        screen.blit(background, (0, 0))

        # 绘制玩家飞机
        if not player1.is_hit:
            screen.blit(player1.image[player1.img_index], player1.rect)
            # 更换图片索引使飞机有动画效果
            player1.img_index = shoot_frequency // 8
        else:
            player1.img_index = player_down_index // 8  # TODO: 什么是player_down_index
            screen.blit(player1.image[player1.img_index], player1.rect)
            player_down_index += 1
            if player_down_index > 47:
                running = False

        # 绘制玩家飞机
        if not player2.is_hit:
            screen.blit(player2.image[player2.img_index], player2.rect)
            # 更换图片索引使飞机有动画效果
            player2.img_index = shoot_frequency // 8
        else:
            player2.img_index = player_down_index // 8
            screen.blit(player2.image[player2.img_index], player2.rect)
            player_down_index += 1
            if player_down_index > 47:
                running = False

        # 绘制击毁动画
        for enemy_down in enemies_down:
            if enemy_down.down_index == 0:
                enemy1_down_sound.play()
            if enemy_down.down_index > 7:
                enemies_down.remove(enemy_down)
                score += 1000
                continue
            screen.blit(enemy_down.down_imgs[enemy_down.down_index // 2], enemy_down.rect)
            enemy_down.down_index += 1

        # 绘制子弹和敌机
        player1.bullets.draw(screen)
        player2.bullets.draw(screen)
        enemies1.draw(screen)

        # 绘制得分
        score_font = pygame.font.Font(None, 36)
        score_text = score_font.render(str(score), True, (128, 128, 128))
        text_rect = score_text.get_rect()
        text_rect.topleft = [10, 10]
        screen.blit(score_text, text_rect)

        # 更新屏幕
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # 监听键盘事件
        key_pressed = pygame.key.get_pressed()
        if not player1.is_hit:  # 若玩家被击中，则无效
            if key_pressed[K_w]:
                player1.moveUp()
                # msg = 'w'
                # sock.send(bytes(msg, encoding="utf-8"))
            if key_pressed[K_s]:
                player1.moveDown()
                # msg = 's'
                # sock.send(bytes(msg, encoding="utf-8"))
            if key_pressed[K_a]:
                player1.moveLeft()
                # msg = 'a'
                # sock.send(bytes(msg, encoding="utf-8"))
            if key_pressed[K_d]:
                player1.moveRight()
                # msg = 'd'
                # sock.send(bytes(msg, encoding="utf-8"))
            msg = str(player1.rect.left) + ":" + str(player1.rect.top) + "\n"
            sock.send(bytes(msg, encoding="utf-8"))
        if not player2.is_hit:
            # sock.send(bytes("I have: "+str(read_sockets), encoding='utf-8'))
            for asock in read_sockets:
                try:
                    data = str(asock.recv(4096), encoding='utf-8').strip()
                    # msg = 'I got msg from select in game_client!'
                    # sock.send(bytes(msg, encoding="utf-8"))
                    # sock.send(bytes("This is what I got: " + data, encoding="utf-8"))
                    if data:
                        print("data: ", data)
                        if data == 'game_over':  # 采用坐标同步方式
                            player2.is_hit = True
                        else:
                            coor = data.split(":")
                            left = int(coor[0])
                            top = int(coor[1])
                            player2.rect.left = left
                            player2.rect.top = top

                except:
                    print("error!!!")
    font = pygame.font.Font(None, 48)
    text = font.render('Score: ' + str(score), True, (255, 0, 0))
    text_rect = text.get_rect()
    text_rect.centerx = screen.get_rect().centerx
    text_rect.centery = screen.get_rect().centery + 24
    screen.blit(game_over, (0, 0))
    screen.blit(text, text_rect)
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        pygame.display.update()


if __name__ == '__main__':
    pass
