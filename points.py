import pygame

points = pygame.sprite.Group()

class Point(pygame.sprite.Sprite):
    def __init__(self, x, y, image) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect(center=(x,y))
        points.add(self)
  
    def update(self) -> None:
        if self.rect.x <= -50 or self.rect.x >= 1250 or self.rect.y <= -50 or self.rect.y >= 850:
            self.kill()
<<<<<<< Updated upstream
        self.rect.y +=1.5
=======
        self.rect.y+=1
>>>>>>> Stashed changes


