"""
AJVYRA — Final Game Version
Final standalone game-side file for the current AJVYRA build.
After this file, development moves to the anime section.

Requires: Python 3.x + pygame
Install: pip install pygame
Run: python ajvyra_final_game_version.py
Controls: WASD / Arrow keys = move, Mouse = shoot, R = restart, ESC = exit
"""
import random
import sys
import pygame

pygame.init()
WIDTH, HEIGHT, FPS = 1000, 650, 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AJVYRA — Final Game")
clock = pygame.time.Clock()

FONT = pygame.font.Font(None, 28)
SMALL = pygame.font.Font(None, 21)
TITLE = pygame.font.Font(None, 62)
BIG = pygame.font.Font(None, 40)
WHITE=(238,240,245); MUTED=(150,155,170); BG=(10,12,18); PANEL=(22,25,35)
ACCENT=(105,165,255); DANGER=(225,75,90); GOOD=(90,205,140); GOLD=(245,195,75)

player = pygame.Rect(90, 440, 38, 38)
player_hp, score, level = 100, 0, 1
enemies, bullets, particles = [], [], []
spawn_timer = shoot_cooldown = 0.0
game_over = victory = False


def reset():
    global player_hp, score, level, enemies, bullets, particles
    global spawn_timer, shoot_cooldown, game_over, victory
    player.topleft=(90,440); player_hp=100; score=0; level=1
    enemies=[]; bullets=[]; particles=[]; spawn_timer=0; shoot_cooldown=0
    game_over=False; victory=False


def label(value, pos, font=FONT, color=WHITE, center=False):
    img=font.render(str(value), True, color); rect=img.get_rect()
    rect.center=pos if center else rect.center
    if not center: rect.topleft=pos
    screen.blit(img, rect)


def particles_at(pos, count=8):
    for _ in range(count):
        v=pygame.Vector2(random.uniform(-1,1),random.uniform(-1,1))
        if v.length()==0: v=pygame.Vector2(1,0)
        particles.append([pygame.Vector2(pos),v.normalize()*random.uniform(1,4),random.randint(12,28)])


def spawn_enemy():
    side=random.randrange(3)
    if side==0: x,y=random.randrange(WIDTH),-35
    elif side==1: x,y=WIDTH+35,random.randrange(90,HEIGHT)
    else: x,y=random.randrange(WIDTH),HEIGHT+35
    size=random.randrange(25,40)
    enemies.append({"rect":pygame.Rect(x,y,size,size),"hp":1+level//3,
                    "speed":random.uniform(1.0,1.8)+level*.08})


def shoot():
    global shoot_cooldown
    if shoot_cooldown>0 or game_over or victory: return
    direction=pygame.Vector2(pygame.mouse.get_pos())-pygame.Vector2(player.center)
    if direction.length()==0: return
    bullets.append([pygame.Vector2(player.center),direction.normalize()*11,80])
    shoot_cooldown=.13

reset()
running=True
while running:
    dt=clock.tick(FPS)/1000.0
    for event in pygame.event.get():
        if event.type==pygame.QUIT: running=False
        elif event.type==pygame.KEYDOWN:
            if event.key==pygame.K_ESCAPE: running=False
            elif event.key==pygame.K_r and (game_over or victory): reset()
        elif event.type==pygame.MOUSEBUTTONDOWN and event.button==1: shoot()

    if not game_over and not victory:
        keys=pygame.key.get_pressed()
        move=pygame.Vector2(
            int(keys[pygame.K_d] or keys[pygame.K_RIGHT])-int(keys[pygame.K_a] or keys[pygame.K_LEFT]),
            int(keys[pygame.K_s] or keys[pygame.K_DOWN])-int(keys[pygame.K_w] or keys[pygame.K_UP]))
        if move.length(): player.x+=round(move.normalize().x*5); player.y+=round(move.normalize().y*5)
        player.clamp_ip(pygame.Rect(0,75,WIDTH,HEIGHT-75))
        shoot_cooldown=max(0,shoot_cooldown-dt)
        spawn_timer+=dt
        interval=max(.28, .9-level*.055)
        if spawn_timer>=interval:
            spawn_timer=0; spawn_enemy()
            if level>=5 and random.random()<.2: spawn_enemy()

        for shot in bullets[:]:
            shot[0]+=shot[1]; shot[2]-=1
            if shot[2]<=0 or not screen.get_rect().inflate(120,120).collidepoint(shot[0]):
                bullets.remove(shot); continue
            for enemy in enemies[:]:
                if enemy["rect"].collidepoint(shot[0]):
                    enemy["hp"]-=1; particles_at(shot[0],3); bullets.remove(shot)
                    if enemy["hp"]<=0:
                        score+=100; particles_at(enemy["rect"].center,10); enemies.remove(enemy)
                    break

        for enemy in enemies[:]:
            direction=pygame.Vector2(player.center)-pygame.Vector2(enemy["rect"].center)
            if direction.length(): enemy["rect"].x+=round(direction.normalize().x*enemy["speed"]); enemy["rect"].y+=round(direction.normalize().y*enemy["speed"])
            if enemy["rect"].colliderect(player):
                player_hp-=max(1,round(25*dt)); particles_at(player.center,1)
                if player_hp<=0: player_hp=0; game_over=True

        level=min(10,1+score//1000)
        if score>=10000: victory=True
        for p in particles[:]:
            p[0]+=p[1]; p[1]*=.94; p[2]-=1
            if p[2]<=0: particles.remove(p)

    screen.fill(BG)
    for x in range(0,WIDTH,50): pygame.draw.line(screen,(27,30,42),(x,75),(x,HEIGHT))
    for y in range(75,HEIGHT,50): pygame.draw.line(screen,(27,30,42),(0,y),(WIDTH,y))
    pygame.draw.rect(screen,PANEL,(0,0,WIDTH,70))
    label("AJVYRA",TITLE,(22,7)); label(f"SCORE {score}",(245,22)); label(f"LEVEL {level}/10",(420,22)); label(f"HP {player_hp}",(600,22))
    label("WASD/ARROWS • MOUSE SHOOT",(760,25),SMALL,MUTED)
    pygame.draw.rect(screen,ACCENT,player,border_radius=8); pygame.draw.circle(screen,WHITE,player.center,5)
    for e in enemies: pygame.draw.rect(screen,DANGER,e["rect"],border_radius=6)
    for b in bullets: pygame.draw.circle(screen,GOLD,(round(b[0].x),round(b[0].y)),4)
    for p in particles: pygame.draw.circle(screen,GOOD,(round(p[0].x),round(p[0].y)),max(1,min(4,p[2]//5)))

    if game_over or victory:
        overlay=pygame.Surface((WIDTH,HEIGHT),pygame.SRCALPHA); overlay.fill((0,0,0,175)); screen.blit(overlay,(0,0))
        label("AJVYRA COMPLETE" if victory else "GAME OVER",TITLE,(WIDTH//2,265),GOOD if victory else DANGER,True)
        label(f"Final score: {score}",BIG,(WIDTH//2,335),WHITE,True)
        label("R = restart    ESC = exit",FONT,(WIDTH//2,390),MUTED,True)
    pygame.display.flip()

pygame.quit(); sys.exit()
