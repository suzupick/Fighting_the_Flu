import pygame
from pygame import mixer
import random
import math
import time
import sys

SCORE_LIMIT = 14

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('□ックマソ2')

# Player
playerImg = pygame.image.load('./graphic/sawaguchi_49_64.png')
playerX, playerY = 370, 480
playerX_change = 0 

# Enemy
enemyImg = pygame.image.load('./graphic/enemy_バイキンマン68x80.png')
enemyX = random.randint(0,736)
enemyY = random.randint(50,150)
enemyX_speed, enemyY_speed = 5, 80
enemyX_change, enemyY_change = enemyX_speed, enemyY_speed


# Bullet  
bulletImg = pygame.image.load('./graphic/bullet.png')
bulletX, bulletY = 0, 480
bulletX_change, bulletY_change = 0, 35
bullet_state = 'ready'

# Score
score_value = 0

# FPS
fps_value = 0
fps_value_prev = 0
delta_t = 1
fps_display_update_count = 0
timer = time.time()

# BGM
random_number = random.randrange(3)
if random_number == 0:
    bgm = mixer.Sound("./music/MEGALOVANIA.mp3")
    bgm.set_volume(0.8)
elif random_number == 1:
    bgm = mixer.Sound("./music/戦艦ハルバード：甲板.mp3")
    bgm.set_volume(0.8)
elif random_number == 2:
    bgm = mixer.Sound("./music/決戦.mp3")
    bgm.set_volume(0.8)

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y):
    screen.blit(enemyImg, (x, y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg, (x + 16, y + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if distance < 40:
        return True
    else:
        return False

# スタート画面
bgm_title = mixer.Sound("./music/とげとげタルめいろ.mp3")
bgm_title.set_volume(0.8)
bgm_title.play()
screen.fill((20, 20, 20))
title_font = pygame.font.Font("./font/HGRSKP.TTF", 80)
title_message = title_font.render("インフルとの死闘", True, (180, 70, 30))
screen.blit(title_message, (80, 240))
title_info_font = pygame.font.SysFont("Arial", 20)
title_info_message = title_info_font.render("PUSH SPACE KEY TO START", True, (190, 190, 190))
screen.blit(title_info_message, (270, 350))


pygame.display.update()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                running = False
                bgm_title.fadeout(3000)

start_sound = mixer.Sound('./music/round1_fight.wav')
start_sound.play()
time.sleep(2.2)
start_sound.stop()

# BGMプレイ開始
bgm.play(loops=-1)

running = True
while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -15
            if event.key == pygame.K_RIGHT:
                playerX_change = +15
            if event.key == pygame.K_SPACE:
                if bullet_state is 'ready':
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
                    laser_sound = mixer.Sound('./music/laser.wav')
                    laser_sound.set_volume(0.5)
                    laser_sound.play()
          
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Player
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy
    if enemyY > 440:
        # ゲームオーバー処理
        bgm.stop()
        mixer.Sound('./music/shout.wav').play()
        gameover_sound = mixer.Sound('./music/gameover.mp3')
        gameover_sound.play()
        screen.fill((20, 20, 20))

        # YOU DIED表示
        font = pygame.font.SysFont(None, 80)
        message = font.render('YOU DIED', False, (120, 10, 10))
        screen.blit(message, (260, 270))

        # スコア表示
        font = pygame.font.SysFont(None, 32) # フォントの作成　Noneはデフォルトのfreesansbold.ttf
        score = font.render(f"SCORE : {str(score_value)}/15", True, (200, 200, 200)) # テキストを描画したSurfaceの作成
        screen.blit(score, (320, 400))

        pygame.display.update()

        # ゲームオーバー画面ループ処理
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            

    enemyX += enemyX_change
    if enemyX <= 0:
        enemyX_change = enemyX_speed
        enemyY_change = enemyY_speed
        enemyY += enemyY_change
    elif enemyX >= 736:
        enemyX_change = - enemyX_speed
        enemyY_change = enemyY_speed
        enemyY += enemyY_change
    
    collision = isCollision(enemyX, enemyY, bulletX, bulletY)
    if collision:
        bulletY = 480
        bullet_state = 'ready'
        score_value += 1
        enemyX_speed += 1
        enemyY_speed -= 2
        if enemyY_speed < 25: enemyY_speed = 25
        enemyX = random.randint(0, 736)
        enemyY = random.randint(50, 150)
        enemyX_change *= random.randint(0, 1) * 2 - 1

        # 撃破時サウンド
        explosion_sound = mixer.Sound('./music/game_explosion9.mp3')
        explosion_sound.set_volume(0.25)
        explosion_sound.play()

        random_number = random.randrange(9)
        if score_value > SCORE_LIMIT:
            death_voice = mixer.Sound('./music/やるじゃない.mp3')
            death_voice.set_volume(1)
            death_voice.play()
        elif random_number in [0, 1, 2]:
            death_voice = mixer.Sound("./music/ブロリー_ヘェア！.mp3")
            death_voice.set_volume(1)
            death_voice.play()
        elif random_number == 3:
            death_voice = mixer.Sound("./music/お前ら人間じゃねぇ!.mp3")
            death_voice.set_volume(0.75)
            death_voice.play()
        elif random_number in [4, 5, 6]:
            death_voice = mixer.Sound('./music/アｯー♂.mp3')
            death_voice.set_volume(1)
            death_voice.play()
        elif random_number in [7, 8]:
            death_voice = mixer.Sound('./music/でたぁ.mp3')
            death_voice.set_volume(0.8)
            death_voice.play()
 
    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = 'ready'
    
    if bullet_state is 'fire':
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
    
    # Score
    font = pygame.font.SysFont(None, 32) # フォントの作成　Noneはデフォルトのfreesansbold.ttf
    score = font.render(f"SCORE : {str(score_value)} / 15", True, (255, 255, 255)) # テキストを描画したSurfaceの作成
    screen.blit(score, (20, 50))

    # ゲームクリア処理
    if score_value > SCORE_LIMIT:
        bgm.fadeout(1000)
        time.sleep(1)
        gameover_sound = mixer.Sound('./music/FFVI_勝利のファンファーレ.mp3')
        gameover_sound.play()
        screen.fill((20, 20, 20))

        # クリア画像
        game_clear_img = pygame.image.load("./graphic/game_clear_happyend.png")
        screen.blit(game_clear_img, (0, 0))

        # 治癒表示
        font = pygame.font.Font("./font/HGRSKP.TTF", 70)
        message = font.render('治癒', False, (120, 10, 10))
        screen.blit(message, (330, 220))

        pygame.display.update()

        # ゲームクリア画面ループ処理
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()


    # フレームレート制御
    current_time = time.time()
    delta_t = current_time - timer
    time.sleep(max(1/60 - delta_t, 0))

    current_time = time.time()
    delta_t = current_time - timer
    if delta_t == 0: delta_t = 1
    fps_value_tmp = 1 / delta_t
    timer = time.time()

    if fps_display_update_count > 3:
        fps_display_update_count = 0
        fps_value = fps_value_tmp
        fps_value_prev = fps_value_tmp
    else:
        fps_display_update_count += 1
        fps_value = fps_value_prev

    font = pygame.font.SysFont(None, 32) # フォントの作成　Noneはデフォルトのfreesansbold.ttf
    fps = font.render(f"FPS : {str(round(fps_value,1))}", True, (255, 255, 255)) # テキストを描画したSurfaceの作成
    screen.blit(fps, (20, 80))

    # 描画・更新
    player(playerX, playerY)
    enemy(enemyX, enemyY)
    pygame.display.update()