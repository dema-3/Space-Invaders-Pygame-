import pygame

class ConstantGame:
    # Window
    WIDTH = 600
    HEIGHT = 750
    FPS = 60

    # Colors
    WHITE = (255, 255, 255)
    RED   = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE  = (0, 120, 255)
    YELLOW= (255, 255, 0)
    BLACK = (0, 0, 0)

    # Speeds
    PLAYER_VEL = 5
    ENEMY_VEL = 1
    LASER_VEL = 5
    REWARD_VEL = 1

    # Health
    PLAYER_MAX_HEALTH = 100
    ENEMY_HEALTH = 100

    # Reward
    REWARD_HEAL = 10
    REWARD_SPAWN_TICKS = 300  # like in the slides

    # Assets (student-friendly: use simple surfaces instead of image files)
    @staticmethod
    def make_ship_surface(color, w=40, h=30):
        surf = pygame.Surface((w, h), pygame.SRCALPHA)
        pygame.draw.polygon(surf, color, [(w//2, 0), (0, h), (w, h)])
        return surf

    @staticmethod
    def make_laser_surface(color, w=6, h=16):
        surf = pygame.Surface((w, h), pygame.SRCALPHA)
        pygame.draw.rect(surf, color, pygame.Rect(0, 0, w, h))
        return surf

    @staticmethod
    def make_reward_surface(color=(255, 0, 255), w=18, h=18):
        surf = pygame.Surface((w, h), pygame.SRCALPHA)
        pygame.draw.circle(surf, color, (w//2, h//2), min(w, h)//2)
        return surf

    @staticmethod
    def make_background():
        bg = pygame.Surface((ConstantGame.WIDTH, ConstantGame.HEIGHT))
        bg.fill((10, 10, 30))
        import random
        for _ in range(120):
            x = random.randint(0, ConstantGame.WIDTH-1)
            y = random.randint(0, ConstantGame.HEIGHT-1)
            bg.set_at((x, y), (200, 200, 255))
        return bg
