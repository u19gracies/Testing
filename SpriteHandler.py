import pygame

class Player(pygame.sprite.Sprite):
  def __init__(self, x, y, scale):
    pygame.sprite.Sprite.__init__(self)
    self.scale = scale
    self.x = x
    self.y = y
    self.walkImage = pygame.image.load('data/images/basicCharacterSSheet.png')
    self.swordWalkImage = pygame.image.load('data/images/swordDrag.png')
    self.shadow = pygame.image.load('data/images/playerShadow.png').convert_alpha()
    self.attImage = pygame.image.load('data/images/swordAttack.png').convert_alpha()
    self.walkImage = pygame.transform.scale(self.walkImage, (self.walkImage.get_width()*self.scale,self.walkImage.get_height()*self.scale))
    self.swordWalkImage = pygame.transform.scale(self.swordWalkImage, (self.swordWalkImage.get_width()*self.scale,self.swordWalkImage.get_height()*self.scale))
    self.shadow = pygame.transform.scale(self.shadow, (self.shadow.get_width()*4,self.shadow.get_height()*4))
    self.attImage = pygame.transform.scale(self.attImage, (self.attImage.get_width()*4,self.attImage.get_height()*4))
    self.shadowrect = self.shadow.get_rect()
    self.shadowrect.center = (self.x, self.y+40)

    self.playerSurf = pygame.Surface((32*self.scale,32*self.scale), pygame.SRCALPHA)
    self.rect = self.playerSurf.get_rect()
    self.rect.center = (self.x, self.y)


  def update(self, walkf, attf, screen, orientation, attacking, swordHeld):
    ##update player
    f = walkf
    if swordHeld:
      self.playerSurf = pygame.Surface((48*self.scale,48*self.scale), pygame.SRCALPHA)
      if attacking:
        f = attf
        self.playerSurf.blit(self.attImage, (0,0), (48*f*self.scale, 0, 48*self.scale, 48*self.scale))
      else:
        self.playerSurf.blit(self.swordWalkImage, (0,0), (48*f*self.scale, 0, 48*self.scale, 48*self.scale))

    else:
      self.playerSurf = pygame.Surface((32*self.scale,32*self.scale), pygame.SRCALPHA)
      self.playerSurf.blit(self.walkImage, (0,0), (32*f*self.scale, 0, 32*self.scale, 32*self.scale))

    self.rect = self.playerSurf.get_rect()
    self.rect.center = (self.x, self.y)


    screen.blit(self.shadow, self.shadowrect)
    if orientation == 2:
      screen.blit(pygame.transform.flip(self.playerSurf, True, False), self.rect)
    else:
      screen.blit(self.playerSurf, self.rect)



class BG():
  def __init__(self, surf):
    self.image = pygame.transform.scale(surf, (surf.get_width()*5,surf.get_height()*5))
    self.rect = self.image.get_rect(topleft=(0,0))
    self.offset = pygame.Vector2(0,0)
    
  def update(self, isMoving, walkSpeed):
    vectorX = 0
    vectorY = 0
    if isMoving:
      key = pygame.key.get_pressed()
      
      if key[pygame.K_w]:
        vectorY = +1
      if key[pygame.K_s]:
        vectorY = -1
      if key[pygame.K_a]:
        vectorX = +1
      if key[pygame.K_d]:
        vectorX = -1

      if vectorX==0 and vectorY==0:
        direction = pygame.Vector2(vectorX, vectorY) * walkSpeed
      else:
        direction = pygame.Vector2(vectorX, vectorY).normalize() * walkSpeed

      self.offset = direction
      
      self.rect.center+=direction
    else:
      self.offset = pygame.Vector2(0,0)

    return self.image


class Item(pygame.sprite.Sprite):
  def __init__(self, x, y, image, scale, isAnimated):
    pygame.sprite.Sprite.__init__(self)
    self.image = image
    self.scale = scale
    self.image = pygame.transform.scale(self.image, (self.image.get_width()*self.scale,self.image.get_height()*self.scale))
    self.rect = self.image.get_rect()
    self.rect.width = 32*self.scale
    self.rect.center = (x,y)
    self.isAnimated = isAnimated
  
  def update(self, screen, f, offset):
    self.surf = pygame.Surface((self.image.get_width()*self.scale,self.image.get_height()*self.scale), pygame.SRCALPHA)
    if self.isAnimated:
      self.surf.blit(self.image, (0,0), (32*f*self.scale, 0, 32*self.scale, 32*self.scale))
    else:
      self.surf.blit(self.image, (0,0), (32*0*self.scale, 0, 32*self.scale, 32*self.scale))
    self.rect.center += offset
    screen.blit(self.surf, self.rect)
    