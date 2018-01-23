#_*_coding:utf-8_*_
from sys import exit
import pygame
import random

class bullet:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.image = pygame.image.load('fire.jpg').convert_alpha()
        self.active = False
    def move(self):
        if self.active:
            self.y -= 3
        if self.y < 0:
            self.active = False
    def restart(self):
         mousex,mousey = pygame.mouse.get_pos()
         self.x = mousex - self.image.get_width() / 2
         self.y = mousey - self.image.get_height() / 2
         self.active = True

class enemy:
    def restart(self):
        self.x = random.randint(50, 700)
        self.y = random.randint(-200, -50)
        self.speed = random.random() + 0.1
        
    def __init__(self):
        self.restart()
        self.image = pygame.image.load('enemy.jpg').convert_alpha()

    def move(self):
        if self.y < 640:
            self.y += self.speed
        else:
            self.restart()

class m_plane:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.image = pygame.image.load('cc.jpg').convert_alpha()
    def move(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.x = mouse_x - self.image.get_width() / 2
        self.y = mouse_y - self.image.get_height() / 2
    def restart(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.x = mouse_x - self.image.get_width() / 2
        self.y = mouse_y - self.image.get_height() / 2
        
def checkhit(enemy,bullet):
    if(bullet.x > enemy.x and bullet.x < enemy.x +enemy.image.get_width())\
    and(bullet.y > enemy.y and bullet.y < enemy.y+enemy.image.get_height()):
        enemy.restart()
        bullet.active = False
        return True
    return False

def check_crash(enemy,plane):
    if(plane.x + 0.7*plane.image.get_width() > enemy.x) and \
      (plane.x + 0.3*plane.image.get_width() < enemy.x + enemy.image.get_width()) and\
      (plane.y + 0.7*plane.image.get_height() > enemy.y) and \
      (plane.y + 0.7*plane.image.get_height() < enemy.y + enemy.image.get_height()):
        return True
    return False
try:
    pygame.init()
    screen = pygame.display.set_mode((768,640), 0, 32)
    pygame.display.set_caption('lkk shooting game')

    background = pygame.image.load('bb.jpg').convert()


    enemys = []
    for i in range(5):
        enemys.append(enemy())

    bullets = []
    for i in range(5):
        bullets.append(bullet())
    count_b = len(bullets)
    index_b = 0
    interval_b = 0

    plane = m_plane()
    gameover = False

    score = 0
    font = pygame.font.SysFont('arial',32)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if gameover and event.type == pygame.MOUSEBUTTONUP:
                plane.restart()
                for e in enemys:
                    e.restart()
                for b in bullets:
                    b.active = False
                score = 0
                gameover = False
        screen.blit(background, (0,0))
        if not gameover:
            interval_b -= 1
            if interval_b < 0:
                bullets[index_b].restart()
                interval_b = 50
                index_b = (index_b + 1) % count_b
            for b in bullets:
                if b.active:
                    for e in enemys:
                        if checkhit(e,b):
                            score += 100
                    b.move()
                    screen.blit(b.image,(b.x, b.y))
            
            for e in enemys:
                if check_crash(e,plane):
                    gameover = True
                e.move()
                screen.blit(e.image,(e.x, e.y))
            
            plane.move()
            screen.blit(plane.image, (plane.x,plane.y))

            text = font.render('Socre:%d'%score,1,(0,0,0))
            screen.blit(text,(0,0))
            
        else:
            text = font.render('GAMEOVER: Socre:%d'%score,1,(0,0,0))
            screen.blit(text,(384,320))

        pygame.display.update()
except:
    print('find error!')