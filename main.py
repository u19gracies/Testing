import pygame
from pytmx.util_pygame import load_pygame
from SpriteHandler import Player, Tile

pygame.init()
screen = pygame.display.set_mode((1920, 1080))
pygame.display.toggle_fullscreen()

playerObj = Player(960,540)
player = pygame.sprite.Group()
player.add(playerObj)
tileGroup = pygame.sprite.Group()
clock = pygame.time.Clock()

tmx = load_pygame('data/tiled/tmx/test.tmx')
for layer in tmx.visible_layers:
    if hasattr(layer,'data'):
        for x, y, surf in layer.tiles():
            pos = (x*16*5, y*16*5)
            t = Tile(pos, surf, tileGroup)
            print(t)

run=True
while run:
    clock.tick(60)
    screen.fill((0,0,0))
    tileGroup.draw(screen)

    tileGroup.update()
    player.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run=False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run=False
        
    
    pygame.display.update()

pygame.quit()