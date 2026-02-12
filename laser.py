import pygame
from .constants_game import ConstantGame

def collide(obj1, obj2):
    offset_x = int(obj2.x - obj1.x)
    offset_y = int(obj2.y - obj1.y)
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) is not None


class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return self.y <= -self.img.get_height() or self.y >= height

    def collision(self, obj):
        return collide(self, obj)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))
