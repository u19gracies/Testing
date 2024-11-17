import pygame

class Player(pygame.sprite.Sprite):
  def __init__(self, x, y, scale):
    pygame.sprite.Sprite.__init__(self)
    self.scale = scale
    self.x = x
    self.y = y
    self.image = pygame.image.load('data/images/basicCharacterSSheet.png').convert_alpha()
    self.shadow = pygame.image.load('data/images/playerShadow.png').convert_alpha()
    self.image = pygame.transform.scale(self.image, (self.image.get_width()*self.scale,self.image.get_height()*self.scale))
    self.shadow = pygame.transform.scale(self.shadow, (self.shadow.get_width()*4,self.shadow.get_height()*4))
    self.f = 1
    self.playerSurf = pygame.Surface((32*self.scale,32*self.scale))
    self.rect = self.playerSurf.get_rect()
    self.shadowrect = self.shadow.get_rect()
    self.shadowrect.center = (self.x, self.y+40)
    self.rect.center = (self.x, self.y)

  def update(self, f, screen, orientation):
    self.f = f
    self.playerSurf = pygame.Surface((32*self.scale,32*self.scale), pygame.SRCALPHA)
    self.playerSurf.blit(self.image, (0,0), (32*f*self.scale, 0, 32*self.scale, 32*self.scale))

    screen.blit(self.shadow, self.shadowrect)
    if orientation == 2:
      screen.blit(pygame.transform.flip(self.playerSurf, True, False), self.rect)
    else:
      screen.blit(self.playerSurf, self.rect)


class Tile(pygame.sprite.Sprite):
  def __init__(self,pos,surf,groups):
    super().__init__(groups)
    self.image = pygame.transform.scale(surf, (surf.get_width()*5,surf.get_height()*5))
    self.rect = self.image.get_rect(topleft=pos)

  def update(self, isMoving):
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
        direction = pygame.Vector2(vectorX, vectorY) * 5
      else:
        direction = pygame.Vector2(vectorX, vectorY).normalize() * 5
      
      self.rect.center+=direction