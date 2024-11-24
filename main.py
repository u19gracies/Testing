import pygame
from pytmx.util_pygame import load_pygame
from SpriteHandler import Player, BG, Item

pygame.init()
screen = pygame.display.set_mode((1920, 1080))
pygame.display.toggle_fullscreen()

#work on a system to place items on the background as coordinates rather than onto screen as causes placement to move depending on where the player is.
#make a way to check which item is actually being picked up

start = pygame.image.load('data/images/startButton.png').convert_alpha()
titlescreenBG = pygame.image.load('data/images/titlescreen.png').convert()
swordImg = pygame.image.load('data/images/sword.png').convert_alpha()
player2Img = pygame.image.load('data/images/basicCharacter.png').convert_alpha()
titlescreenBG = pygame.transform.scale(titlescreenBG, (titlescreenBG.get_width()*1.5,titlescreenBG.get_height()*1.5))
start = pygame.transform.scale(start, (start.get_width()*4,start.get_height()*4))
startRect = start.get_rect()
startRect.center = (960,540)

bgSurf = pygame.Surface((5000,5000), pygame.SRCALPHA)
tmx = load_pygame('data/tiled/tmx/test.tmx')
for layer in tmx.visible_layers:
    if hasattr(layer,'data'):
        for x, y, surf in layer.tiles():
            pos = (x*16, y*16)
            bgSurf.blit(surf, pos)

background = BG(bgSurf)

def mainloop(bgSurf):
    playerObj = Player(960,540,4)
    player = pygame.sprite.Group()
    itemGroup = pygame.sprite.Group()
    clock = pygame.time.Clock()
    swordItem = Item(2000,500,swordImg,3,True)
    player2 = Item(1920,1080,player2Img,10,False)
    itemGroup.add(swordItem)
    itemGroup.add(player2)

    player.add(playerObj)

    walktime=0
    walkf=0
    atttime=0
    attf=0
    itemtime=0
    itemf=0
    orientation=0
    playerSpeed = 4
    isMoving=False
    run=False
    attacking=False
    canAttack=True
    swordHeld=False

    def a_walk(walkf, swordHeld):
        if swordHeld:
            if walkf==7:
                walkf=0
            else:
                walkf+=1
        else:
            if walkf==3:
                walkf=0
            else:
                walkf+=1

        return walkf
    
    def a_attack(attf):
        if attf==3:
            attf=0
        else:
            attf+=1
        return attf
    
    def a_item(itemf):
        if itemf==4:
            itemf=0
        else:
            itemf+=1
        return itemf

    titlescreen=True
    while titlescreen:
        screen.blit(titlescreenBG, (0,0))
        screen.blit(start, startRect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                titlescreen=False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    titlescreen=False

            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if pygame.Rect.collidepoint(startRect, pos):
                    titlescreen=False
                    run=True
            
        pygame.display.update()

    while run:
        clock.tick(60)
        screen.fill((127,205,255))
        bgSurf = background.update(isMoving, playerSpeed)
        screen.blit(bgSurf, (background.rect))
        #pygame.draw.rect(screen, (255,0,0), playerObj.rect)
        player.update(walkf, attf, screen, orientation, attacking, swordHeld)
        itemGroup.update(screen, itemf, background.offset)

        itemtime+=1

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and keys[pygame.K_d] or keys[pygame.K_w] and keys[pygame.K_s]:
            isMoving=False
        elif keys[pygame.K_w] or keys[pygame.K_a] or keys[pygame.K_s] or keys[pygame.K_d]:
            if walktime==0:
                walktime+=6
            else:
                walktime+=1
            if walktime==12:
                walkf = a_walk(walkf, swordHeld)
                walktime=0
            isMoving=True
        else:
            isMoving=False


        if keys[pygame.K_a]:
            orientation=1
        elif keys[pygame.K_d]:
            orientation=2


        if not isMoving:
            walkf=1
            walktime=0

        if swordHeld:
            if canAttack:
                if pygame.mouse.get_pressed()[0]:
                    attacking=True
                    canAttack=False
                elif pygame.mouse.get_pressed()[2]:
                    swordHeld = False
                    playerSpeed = 4
                    walkf=0
                    itemGroup.add(Item(2000,500,swordImg,3,True))
            elif not pygame.mouse.get_pressed()[0]:
                    canAttack=True


        if attacking:
            atttime+=1
            if atttime == 3:
                attf = a_attack(attf)
                atttime=0
                if attf==0:
                    attacking=False

        if itemtime==8:
            itemtime=0
            itemf = a_item(itemf)


        itemPickedUp = pygame.sprite.groupcollide(player, itemGroup, False, True)
        for item in itemPickedUp.values():
            if item != None:
                swordHeld = True
                playerSpeed = 3

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run=False
                mainloop(bgSurf)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run=False
                    mainloop(bgSurf)
            
        
        pygame.display.update()

mainloop(bgSurf)

pygame.quit()