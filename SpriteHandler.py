import pygame
import keyboard


class Player(pygame.sprite.Sprite):
  def __init__(self, x, y):
    pygame.sprite.Sprite.__init__(self)
    self.image = pygame.image.load('data/images/player.png').convert_alpha()
    self.image = pygame.transform.scale(self.image, (self.image.get_width()*5,self.image.get_height()*5))
    self.rect = self.image.get_rect()
    self.rect.center = (x, y)


class Tile(pygame.sprite.Sprite):
  def __init__(self,pos,surf,groups):
    super().__init__(groups)
    self.image = pygame.transform.scale(surf, (surf.get_width()*5,surf.get_height()*5))
    self.rect = self.image.get_rect(topleft=pos)

  def update(self):
    vectorX = 0
    vectorY = 0
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