import pygame
from pytmx.util_pygame import load_pygame
from SpriteHandler import Player, Tile

pygame.init()
screen = pygame.display.set_mode((1920, 1080))
pygame.display.toggle_fullscreen()

playerObj = Player(960,540,4)
player = pygame.sprite.Group()
player.add(playerObj)
tileGroup = pygame.sprite.Group()
clock = pygame.time.Clock()
f=0
time=0
orientation=0
isMoving=False

tmx = load_pygame('data/tiled/tmx/test.tmx')
for layer in tmx.visible_layers:
    if hasattr(layer,'data'):
        for x, y, surf in layer.tiles():
            pos = (x*16*5, y*16*5)
            t = Tile(pos, surf, tileGroup)


run=True
while run:
    time+=1
    clock.tick(60)
    screen.fill((0,0,0))
    tileGroup.draw(screen)
    tileGroup.update(isMoving)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] or keys[pygame.K_a] or keys[pygame.K_s] or keys[pygame.K_d]:
        isMoving=True
        time+=1
    else:
        isMoving=False
        time=0

    if keys[pygame.K_a] and keys[pygame.K_d]:
        isMoving=False
        time=0
    if keys[pygame.K_w] and keys[pygame.K_s]:
        isMoving=False
        time=0
    elif keys[pygame.K_a]:
        orientation=1
    elif keys[pygame.K_d]:
        orientation=2

    player.update(f, screen, orientation)
    if time==12:
        if f==3:
            f=0
        else:
            f+=1
        time=0
    elif time==0:
       f=0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run=False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run=False
        
    
    pygame.display.update()

pygame.quit()