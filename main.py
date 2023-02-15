import pygame
import os
from random import randint
pygame.init()

def file_path(file_name):
    folder_path = os.path.abspath(__file__ + "/..")
    path = os.path.join(folder_path, file_name)
    return path

FPS = 40 
WIN_WIDTH = 700
WIN_HEIGHT = 500
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARK_RED = (255, 150, 150)

window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
clock = pygame.time.Clock()

background = pygame.image.load(file_path("завантаження.jpg"))
background = pygame.transform.scale(background, (WIN_WIDTH, WIN_HEIGHT))

pygame.mixer.music.load(file_path("fonovaya-muzyika-quotzvezda-gitaryiquot-24714.wav"))
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

music_win = pygame.mixer.Sound(file_path("muzyika-iz-igryi-zelda-23480.wav"))

music_lose = pygame.mixer.Sound(file_path("fonovaya-muzyika-quotproyasneniequot-24769.wav"))
music_lose.set_volume(1)


class GameSprite(pygame.sprite.Sprite):
    def __init__(self, image, x, y, width, height, speed):
        super().__init__()
        self.image = pygame.image.load(file_path(image))
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, image, x, y, width, height, speed):
        super().__init__(image, x, y, width, height, speed)
    
    def update(self):
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.rect.left > 0:
            self.rect.x -= self.speed
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.rect.right < WIN_WIDTH:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet(file_path("ammo_for_game_IT-removebg-preview.png"), self.rect.centerx, self.rect  .top, 30, 30, 4)
        bullets.add(bullet)

class Bullet(GameSprite):
    def __init__(self, images, x, y, width, height, speed):
        super().__init__(images, x, y, width, height, speed)

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom <= 0:
            self.kill()
class Enemy(GameSprite):
    def __init__(self, image, x, y, width, height, speed):
        super().__init__(image, x, y, width, height, speed)
    
    def update(self):
        global missed_enemies
        self.rect.y += self.speed
        if self.rect.y >= WIN_HEIGHT:
            self.rect.bottom = 0
            self. rect.x = randint(0, WIN_WIDTH - self.rect.width)
            self.speed = randint(1, 7)
            missed_enemies += 1 

player = Player("images-removebg-preview.png", 300, 400, 70, 70, 5)
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

for i in range(5):
    enemy = Enemy(file_path("images-removebg-preview_.png"), randint (0, WIN_WIDTH - 70), 0, 70, 70, randint(1, 5))
    enemies.add(enemy)

missed_enemies = 0
killed_enemies = 0
font = pygame.font.SysFont("arial", 30, 0, 1)
txt_missed = font.render("пропущено: " + str(missed_enemies), True, RED)
txt_killed = font.render("збито: " + str(killed_enemies), True, GREEN)

play = True
game = True


while game == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.fire()

    if play == True:
        window.blit(background, (0, 0))

        txt_missed = font.render("пропущено: " + str(missed_enemies), True, RED)
        txt_killed = font.render("збито: " + str(killed_enemies), True, GREEN)

        window.blit(txt_missed, (10, 10))
        window.blit(txt_killed, (10, 35))

        player.reset()
        player.update()
        
        enemies.draw(window)
        enemies.update()

        bullets.draw(window)
        bullets.update()

        collide_bullets = pygame.sprite.groupcollide(enemies, bullets, False, True)
        if collide_bullets:
            for enemy in collide_bullets:
                killed_enemies += 1
                enemy.rect.bottom = 0
                enemy. rect.x = randint(0, WIN_WIDTH - enemy.rect.width)
                enemy.speed = randint(1, 7)

        if missed_enemies >= 10 or pygame.sprite.spritecollide(player, enemies, False):
            play = False
            font2 = pygame.font.SysFont("arial", 60, 1)
            txt_lose = font2.render("YOU LOSE", True, DARK_RED)
            window.blit(txt_lose, (250, 200))
            pygame.mixer.music.stop()
            music_lose.play()

        if killed_enemies >= 20:
            play = False
            font2 = pygame.font.SysFont("arial", 60, 1)
            txt_win = font2.render("YOU WIN", True, GREEN)
            window.blit(txt_win, (240, 200))
            pygame.mixer.music.stop()
            music_win.play()


    clock.tick(FPS)
    pygame.display.update()