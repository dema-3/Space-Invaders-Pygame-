import pygame
import random
from .constants_game import ConstantGame
from .laser import Laser, collide

class Ship:
    FRAMES_BETWEEN_SHOTS = 30

    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.frames_counter = 0
        self.mask = None
        self.max_health = health

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, vel, objs):
        self.frames_counter -= 1
        for laser in self.lasers[:]:
            laser.move(vel)
            if laser.off_screen(ConstantGame.HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs[:]:
                    if laser.collision(obj):
                        obj.health -= 10
                        if laser in self.lasers:
                            self.lasers.remove(laser)
                        break

    def shoot(self):
        if self.frames_counter <= 0:
            laser = Laser(
                self.x + self.get_width()//2 - self.laser_img.get_width()//2,
                self.y,
                self.laser_img
            )
            self.lasers.append(laser)
            self.frames_counter = self.FRAMES_BETWEEN_SHOTS
        else:
            self.frames_counter -= 1

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()


class Player(Ship):
    def __init__(self, x, y, health=ConstantGame.PLAYER_MAX_HEALTH):
        super().__init__(x, y, health)
        self.ship_img = ConstantGame.make_ship_surface(ConstantGame.YELLOW, 48, 36)
        self.laser_img = ConstantGame.make_laser_surface(ConstantGame.YELLOW, 6, 16)
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    def move_lasers(self, vel, objs):
        self.frames_counter -= 1
        for laser in self.lasers[:]:
            laser.move(vel)
            if laser.off_screen(ConstantGame.HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs[:]:
                    if laser.collision(obj):
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)
                        break

    def draw_healthbar(self, window):
        pygame.draw.rect(window, ConstantGame.RED,
                         (self.x, self.y + self.get_height() + 10, self.get_width(), 8))
        green_width = int(self.get_width() * max(self.health, 0) / self.max_health)
        pygame.draw.rect(window, ConstantGame.GREEN,
                         (self.x, self.y + self.get_height() + 10, green_width, 8))

    def draw(self, window):
        super().draw(window)
        self.draw_healthbar(window)


class Enemy(Ship):
    COLOR_MAP = {
        "red":   (ConstantGame.make_ship_surface(ConstantGame.RED, 40, 30),
                  ConstantGame.make_laser_surface(ConstantGame.RED, 6, 14)),
        "green": (ConstantGame.make_ship_surface(ConstantGame.GREEN, 40, 30),
                  ConstantGame.make_laser_surface(ConstantGame.GREEN, 6, 14)),
        "blue":  (ConstantGame.make_ship_surface(ConstantGame.BLUE, 40, 30),
                  ConstantGame.make_laser_surface(ConstantGame.BLUE, 6, 14)),
    }

    def __init__(self, x, y, color, health=ConstantGame.ENEMY_HEALTH):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.frames_counter = random.randint(0, self.FRAMES_BETWEEN_SHOTS)

    def move(self, vel):
        self.y += vel

    def shoot(self):
        if self.frames_counter <= 0:
            laser = Laser(
                self.x + self.get_width()//2 - self.laser_img.get_width()//2,
                self.y + self.get_height(),
                self.laser_img
            )
            self.lasers.append(laser)
            self.frames_counter = self.FRAMES_BETWEEN_SHOTS
        else:
            self.frames_counter -= 1


class Reward:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.img = ConstantGame.make_reward_surface()
        self.mask = pygame.mask.from_surface(self.img)

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return self.y > height

    def collision(self, obj):
        return collide(self, obj)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))
